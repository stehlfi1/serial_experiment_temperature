import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from .data_models import TestGroupType, TEST_GROUPS, AdvancedMetrics
from .advanced_test_runner import AdvancedTestRunner


class TestResultParser:
    @staticmethod
    def parse_compilability_output(output: str) -> Dict[str, Any]:
        lines = output.strip().split('\n')
        
        if "Yes, the code is compilable." in output:
            return {
                "status": "pass",
                "compiles": True,
                "errors": []
            }
        else:
            return {
                "status": "fail", 
                "compiles": False,
                "errors": [line for line in lines if "error" in line.lower()]
            }
    
    @staticmethod
    def parse_code_length_output(output: str) -> Dict[str, Any]:
        lines = output.strip().split('\n')
        
        for line in lines:
            if "Number of lines:" in line:
                try:
                    line_count = int(line.split(":")[1].strip())
                    return {
                        "lines": line_count,
                        "status": "success"
                    }
                except (ValueError, IndexError):
                    pass
        
        return {
            "lines": 0,
            "status": "error",
            "error": "Could not parse line count"
        }
    
    @staticmethod
    def parse_modularity_output(output: str) -> Dict[str, Any]:
        lines = output.strip().split('\n')
        result = {"status": "success"}
        
        for line in lines:
            if "Functions:" in line:
                try:
                    result["functions"] = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
            elif "Classes:" in line:
                try:
                    result["classes"] = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
            elif "Methods:" in line:
                try:
                    result["methods"] = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
            elif "Modularity score:" in line:
                try:
                    result["score"] = float(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
        
        if "score" not in result:
            result["status"] = "error"
            result["error"] = "Could not parse modularity score"
        
        return result
    
    @staticmethod
    def parse_functional_completeness_output(output: str) -> Dict[str, Any]:
        lines = output.strip().split('\n')
        result = {"status": "success"}
        
        for line in lines:
            if "Expected features:" in line:
                try:
                    result["expected_features"] = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
            elif "Found features:" in line:
                try:
                    result["found_features"] = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
            elif "Completeness score:" in line:
                try:
                    result["score"] = float(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    pass
            elif "Features found:" in line:
                features_str = line.split(":", 1)[1].strip()
                result["features_found"] = [f.strip() for f in features_str.split(",") if f.strip()]
        
        if "score" not in result:
            result["status"] = "error"
            result["error"] = "Could not parse completeness score"
        
        return result

    @staticmethod
    def parse_functional_correctness_output(output: str) -> Dict[str, Any]:
        """Parse pytest output from functional correctness tests."""
        result = {"status": "unknown", "tests_run": 0, "tests_passed": 0, "tests_failed": 0, "pass_rate": 0.0}
        
        lines = output.strip().split('\n')
        
        # Find the summary line with test counts
        for line in lines:
            line = line.strip()
            # Parse pytest summary line (e.g., "12 failed, 35 passed in 0.06s")
            if " passed" in line and " failed" in line and " in " in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        try:
                            result["tests_passed"] = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass
                    elif part == "failed" and i > 0:
                        try:
                            result["tests_failed"] = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass
                break
            # Handle cases with only passed or only failed
            elif " passed in " in line and " failed" not in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        try:
                            result["tests_passed"] = int(parts[i-1])
                            result["tests_failed"] = 0
                        except (ValueError, IndexError):
                            pass
                break
            elif " failed in " in line and " passed" not in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "failed" and i > 0:
                        try:
                            result["tests_failed"] = int(parts[i-1])
                            result["tests_passed"] = 0
                        except (ValueError, IndexError):
                            pass
                break
        
        # Calculate totals and percentages
        result["tests_run"] = result["tests_passed"] + result["tests_failed"]
        
        if result["tests_run"] > 0:
            result["pass_rate"] = round(result["tests_passed"] / result["tests_run"], 3)
            result["pass_percentage"] = round((result["tests_passed"] / result["tests_run"]) * 100, 1)
            
            if result["tests_failed"] == 0:
                result["status"] = "success"
            elif result["tests_passed"] > result["tests_failed"]:
                result["status"] = "partial"
            else:
                result["status"] = "failed"
        else:
            result["status"] = "error"
            result["error"] = "No test results found in pytest output"
        
        # Include a summary of the output, but truncate verbose error details
        summary_lines = []
        for line in lines:
            if "FAILURES" in line or "short test summary" in line:
                break
            if line.strip() and not line.startswith('/'):  # Skip file path lines
                summary_lines.append(line)
        
        result["summary"] = '\n'.join(summary_lines[-5:])  # Keep only last 5 relevant lines
        
        return result


class TestRunner:
    def __init__(self, tests_dir: Path):
        self.tests_dir = tests_dir
        self.advanced_runner = AdvancedTestRunner()
        self.test_mapping = {
            "1_code_compilability": TestResultParser.parse_compilability_output,
            "2_code_length_adaptive": TestResultParser.parse_code_length_output,
            "3_modularity_adaptive": TestResultParser.parse_modularity_output,
            "4_functional_completeness_adaptive": TestResultParser.parse_functional_completeness_output,
            "5_functional_correctness": TestResultParser.parse_functional_correctness_output
        }
    
    def run_test(self, test_name: str, model: str, code_dir: Path, 
                 challenge: str) -> Dict[str, Any]:
        start_time = time.time()
        
        test_file = self.tests_dir / f"{test_name}.py"
        if not test_file.exists():
            test_file = self.tests_dir / challenge / f"{test_name}.py"
        
        if not test_file.exists():
            return {
                "status": "error",
                "error": f"Test file not found: {test_name}",
                "execution_time": 0
            }
        
        model_file = code_dir / f"{model}.py"
        if not model_file.exists():
            return {
                "status": "error", 
                "error": f"Model file not found: {model}.py",
                "execution_time": 0
            }
        
        test_copy = code_dir / f"{test_name}.py"
        
        try:
            test_content = test_file.read_text()
            
            # Handle pytest-based tests differently
            if test_name == "5_functional_correctness":
                # Modify the test content to import from the correct model file
                # Find the main class name from the challenge
                class_name = self._get_main_class_name(challenge)
                import_line = f"from {model} import {class_name}"
                
                # Replace the commented imports with the correct import
                lines = test_content.split('\n')
                modified_lines = []
                for line in lines:
                    if line.strip().startswith('# from ') and class_name in line:
                        # Skip commented imports
                        continue
                    elif line.strip() == '' and len(modified_lines) > 0 and modified_lines[-1].startswith('import'):
                        # Add our import after the import section
                        modified_lines.append(line)
                        modified_lines.append(import_line)
                        modified_lines.append('')
                    else:
                        modified_lines.append(line)
                
                # If we didn't find a good place to insert, add it after the imports
                if import_line not in '\n'.join(modified_lines):
                    # Find the last import and add after it
                    for i, line in enumerate(modified_lines):
                        if line.startswith('import ') or line.startswith('from '):
                            continue
                        else:
                            modified_lines.insert(i, import_line)
                            modified_lines.insert(i+1, '')
                            break
                
                test_content = '\n'.join(modified_lines)
            
            test_copy.write_text(test_content)
            
            # Handle pytest-based tests differently
            if test_name == "5_functional_correctness":
                # Run with pytest using UV
                cmd = ["uv", "run", "python", "-m", "pytest", str(test_copy), "--tb=line", "-q"]
            else:
                # Run regular tests
                cmd = [sys.executable, str(test_copy), model]
                
            process = subprocess.run(
                cmd,
                cwd=str(code_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            execution_time = time.time() - start_time
            
            # For pytest tests, we always want to parse the output even if some tests failed
            if test_name == "5_functional_correctness":
                parser = self.test_mapping.get(test_name)
                if parser:
                    result = parser(process.stdout)
                    result["execution_time"] = execution_time
                    return result
                else:
                    return {
                        "status": "unknown",
                        "output": process.stdout.strip(),
                        "execution_time": execution_time
                    }
            # For other tests, use return code to determine success
            elif process.returncode == 0:
                parser = self.test_mapping.get(test_name)
                if parser:
                    result = parser(process.stdout)
                    result["execution_time"] = execution_time
                    return result
                else:
                    return {
                        "status": "success",
                        "output": process.stdout.strip(),
                        "execution_time": execution_time
                    }
            else:
                return {
                    "status": "failed",
                    "output": process.stdout.strip(),
                    "error": process.stderr.strip(),
                    "execution_time": execution_time
                }
        
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": "Test timed out after 30 seconds",
                "execution_time": 30.0
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "execution_time": time.time() - start_time
            }
        finally:
            if test_copy.exists():
                test_copy.unlink()
    
    def run_all_tests_for_model(self, model: str, code_dir: Path, 
                                challenge: str, test_groups: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run all tests for a model, including both legacy and advanced test groups."""
        results = {}
        
        # Determine which test groups to run
        groups_to_run = test_groups or ["legacy"]  # Default to legacy only for backward compatibility
        
        # Legacy tests
        if "legacy" in groups_to_run:
            legacy_results = {}
            for test_name in self.test_mapping.keys():
                legacy_results[test_name] = self.run_test(test_name, model, code_dir, challenge)
            results["legacy"] = legacy_results
        
        # Advanced tests
        model_file = code_dir / f"{model}.py"
        
        if "quality" in groups_to_run or "structure" in groups_to_run:
            if model_file.exists():
                try:
                    advanced_metrics = self.advanced_runner.run_all_advanced_tests(model_file)
                    
                    if "quality" in groups_to_run:
                        results["quality"] = self._extract_quality_metrics(advanced_metrics)
                    
                    if "structure" in groups_to_run:
                        results["structure"] = self._extract_structure_metrics(advanced_metrics)
                        
                except Exception as e:
                    error_result = {"status": "error", "error": str(e)}
                    if "quality" in groups_to_run:
                        results["quality"] = error_result
                    if "structure" in groups_to_run:
                        results["structure"] = error_result
            else:
                error_result = {"status": "error", "error": f"Model file not found: {model}.py"}
                if "quality" in groups_to_run:
                    results["quality"] = error_result
                if "structure" in groups_to_run:
                    results["structure"] = error_result
        
        return results
    
    def _extract_quality_metrics(self, advanced_metrics: AdvancedMetrics) -> Dict[str, Any]:
        """Extract quality-related metrics from advanced metrics."""
        return {
            "complexity_analysis": {
                "cyclomatic_complexity": advanced_metrics.cyclomatic_complexity,
                "cyclomatic_complexity_per_function": advanced_metrics.cyclomatic_complexity_per_function,
                "cognitive_complexity": advanced_metrics.cognitive_complexity,
                "cognitive_complexity_per_function": advanced_metrics.cognitive_complexity_per_function,
                "max_nesting_depth": advanced_metrics.max_nesting_depth,
                "avg_nesting_depth": advanced_metrics.avg_nesting_depth,
                "nesting_depth_per_function": advanced_metrics.nesting_depth_per_function
            },
            "halstead_analysis": {
                "volume": advanced_metrics.halstead_volume,
                "difficulty": advanced_metrics.halstead_difficulty,
                "effort": advanced_metrics.halstead_effort,
                "time": advanced_metrics.halstead_time,
                "bugs": advanced_metrics.halstead_bugs,
                "length": advanced_metrics.halstead_length,
                "vocabulary": advanced_metrics.halstead_vocabulary,
                "operators": advanced_metrics.halstead_operators,
                "operands": advanced_metrics.halstead_operands,
                "operator_count": advanced_metrics.halstead_operator_count,
                "operand_count": advanced_metrics.halstead_operand_count
            },
            "maintainability_analysis": {
                "maintainability_index": advanced_metrics.maintainability_index,
                "maintainability_rank": advanced_metrics.maintainability_rank,
                "abc_assignment_count": advanced_metrics.abc_assignment_count,
                "abc_branch_count": advanced_metrics.abc_branch_count,
                "abc_condition_count": advanced_metrics.abc_condition_count,
                "abc_magnitude": advanced_metrics.abc_magnitude
            },
            "size_analysis": {
                "logical_lines_of_code": advanced_metrics.logical_lines_of_code,
                "physical_lines_of_code": advanced_metrics.physical_lines_of_code,
                "comment_lines": advanced_metrics.comment_lines,
                "blank_lines": advanced_metrics.blank_lines,
                "code_to_comment_ratio": advanced_metrics.code_to_comment_ratio,
                "function_count": advanced_metrics.function_count,
                "class_count": advanced_metrics.class_count,
                "method_count": advanced_metrics.method_count,
                "methods_per_class": advanced_metrics.methods_per_class,
                "parameters_per_function": advanced_metrics.parameters_per_function,
                "avg_parameters_per_function": advanced_metrics.avg_parameters_per_function,
                "wmc_per_class": advanced_metrics.wmc_per_class,
                "avg_wmc": advanced_metrics.avg_wmc
            },
            "code_style_analysis": {
                "naming_convention_score": advanced_metrics.naming_convention_score,
                "simple_function_ratio": advanced_metrics.simple_function_ratio,
                "complex_function_ratio": advanced_metrics.complex_function_ratio,
                "very_complex_function_ratio": advanced_metrics.very_complex_function_ratio
            },
            "status": "success"
        }
    
    def _extract_structure_metrics(self, advanced_metrics: AdvancedMetrics) -> Dict[str, Any]:
        """Extract structure-related metrics from advanced metrics."""
        return {
            "ast_analysis": {
                "node_count": advanced_metrics.ast_node_count,
                "depth": advanced_metrics.ast_depth,
                "node_types": advanced_metrics.ast_node_types,
                "unique_node_types": advanced_metrics.ast_unique_node_types
            },
            "control_flow_analysis": {
                "loop_count": advanced_metrics.loop_count,
                "conditional_count": advanced_metrics.conditional_count,
                "comprehension_count": advanced_metrics.comprehension_count
            },
            "oop_metrics": {
                "depth_of_inheritance": advanced_metrics.depth_of_inheritance,
                "max_dit": advanced_metrics.max_dit,
                "avg_dit": advanced_metrics.avg_dit,
                "children_per_class": advanced_metrics.children_per_class,
                "max_noc": advanced_metrics.max_noc,
                "avg_noc": advanced_metrics.avg_noc,
                "coupling_per_class": advanced_metrics.coupling_per_class,
                "max_cbo": advanced_metrics.max_cbo,
                "avg_cbo": advanced_metrics.avg_cbo
            },
            "code_patterns": {
                "lambda_count": advanced_metrics.lambda_count,
                "generator_count": advanced_metrics.generator_count,
                "decorator_count": advanced_metrics.decorator_count,
                "docstring_count": advanced_metrics.docstring_count,
                "return_statement_count": advanced_metrics.return_statement_count,
                "raise_statement_count": advanced_metrics.raise_statement_count,
                "assert_statement_count": advanced_metrics.assert_statement_count
            },
            "variable_usage": {
                "variable_count": advanced_metrics.variable_count,
                "global_variable_count": advanced_metrics.global_variable_count,
                "nonlocal_variable_count": advanced_metrics.nonlocal_variable_count
            },
            "operator_distribution": advanced_metrics.operator_distribution,
            "literal_usage": {
                "string_literal_count": advanced_metrics.string_literal_count,
                "number_literal_count": advanced_metrics.number_literal_count,
                "boolean_literal_count": advanced_metrics.boolean_literal_count
            },
            "import_analysis": {
                "import_count": advanced_metrics.import_count,
                "from_import_count": advanced_metrics.from_import_count,
                "unique_imports": advanced_metrics.unique_imports,
                "stdlib_imports": advanced_metrics.stdlib_imports,
                "third_party_imports": advanced_metrics.third_party_imports
            },
            "status": "success"
        }
    
    def _get_main_class_name(self, challenge: str) -> str:
        """Get the main class name for a given challenge."""
        class_mapping = {
            "ascii_art": "AsciiArt",
            "calculator": "Calculator", 
            "todo_list": "TaskManager"
        }
        return class_mapping.get(challenge, "UnknownClass")
