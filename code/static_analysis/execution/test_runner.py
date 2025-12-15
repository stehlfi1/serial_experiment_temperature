import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from ..results.data_models import TestGroupType, TEST_GROUPS, AdvancedMetrics
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
        """Parse pytest output from functional correctness tests using regex for robust parsing."""
        import re
        
        result = {"status": "unknown", "tests_run": 0, "tests_passed": 0, "tests_failed": 0, "pass_rate": 0.0}
        
        # Use regex to find pytest summary line - much more robust
        # Matches patterns like: "12 failed, 35 passed in 0.06s" or "88 passed in 0.15s"
        # Also handles warnings/skips/errors: "33 failed, 55 passed, 2 warnings in 0.19s"
        summary_pattern = r'(\d+)\s+failed.*?(\d+)\s+passed.*?in\s+[\d.]+s|(\d+)\s+passed.*?in\s+[\d.]+s|(\d+)\s+failed.*?in\s+[\d.]+s'
        
        for line in output.split('\n'):
            match = re.search(summary_pattern, line.strip())
            if match:
                groups = match.groups()
                if groups[0] and groups[1]:  # Both failed and passed
                    result["tests_failed"] = int(groups[0])
                    result["tests_passed"] = int(groups[1])
                elif groups[2]:  # Only passed
                    result["tests_passed"] = int(groups[2])
                    result["tests_failed"] = 0
                elif groups[3]:  # Only failed
                    result["tests_failed"] = int(groups[3])
                    result["tests_passed"] = 0
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
        
        # Extract clean summary - keep test progress and final summary
        lines = output.strip().split('\n')
        summary_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('/') and not line.startswith('='):
                # Keep test progress (dots/F's) and summary lines
                if re.search(r'[.F]+.*\[\s*\d+%\]|^\d+.*in\s+[\d.]+s', line):
                    summary_lines.append(line)
        
        result["summary"] = '\n'.join(summary_lines[-3:])  # Keep last 3 relevant lines
        
        return result


class TestRunner:
    def __init__(self, tests_dir: Path):
        self.tests_dir = tests_dir
        self.advanced_runner = AdvancedTestRunner()
        self.test_mapping = {
            "1_code_compilability": TestResultParser.parse_compilability_output,
            "4_functional_completeness_adaptive": TestResultParser.parse_functional_completeness_output,
            "5_functional_correctness": TestResultParser.parse_functional_correctness_output
        }
    
    def run_test(self, test_name: str, model: str, code_dir: Path, 
                 challenge: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # Map legacy test names to actual file names
        test_name_mappings = {
            "1_code_compilability": "1_code_compilability",
            "4_functional_completeness_adaptive": "4_functional_completeness",
            "5_functional_correctness": "5_functional_correctness"
        }
        
        actual_test_name = test_name_mappings.get(test_name, test_name)
        
        # Try multiple search paths
        test_file = None
        search_paths = []
        
        if test_name == "5_functional_correctness":
            # For functional correctness, try model-specific test file first
            search_paths = [
                self.tests_dir / "challenges" / challenge / f"{actual_test_name}-{model}.py",
                self.tests_dir / "challenges" / challenge / f"{actual_test_name}.py",
                self.tests_dir / challenge / f"{actual_test_name}-{model}.py",
                self.tests_dir / challenge / f"{actual_test_name}.py",
                self.tests_dir / f"{actual_test_name}.py"
            ]
        elif test_name in ["4_functional_completeness_adaptive"]:
            # For legacy adaptive tests, try legacy location first, then challenge-specific
            search_paths = [
                self.tests_dir / "metrics" / "legacy" / f"{test_name}.py",
                self.tests_dir / "challenges" / challenge / f"{actual_test_name}.py",
                self.tests_dir / challenge / f"{actual_test_name}.py",
                self.tests_dir / f"{actual_test_name}.py"
            ]
        else:
            # For other tests, try challenge-specific first
            search_paths = [
                self.tests_dir / "challenges" / challenge / f"{actual_test_name}.py",
                self.tests_dir / challenge / f"{actual_test_name}.py",
                self.tests_dir / f"{actual_test_name}.py"
            ]
        
        # Find the first existing test file
        for path in search_paths:
            if path.exists():
                test_file = path
                break
        
        if not test_file:
            result = {
                "status": "error",
                "error": f"Test file not found: {test_name}",
                "execution_time": 0
            }
            # Remove execution_time from all results except functional_correctness
            if test_name != "5_functional_correctness":
                result.pop("execution_time", None)
            return result
        
        model_file = code_dir / f"{model}.py"
        if not model_file.exists():
            result = {
                "status": "error", 
                "error": f"Model file not found: {model}.py",
                "execution_time": 0
            }
            # Remove execution_time from all results except functional_correctness
            if test_name != "5_functional_correctness":
                result.pop("execution_time", None)
            return result
        
        test_copy = code_dir / f"{test_name}.py"
        
        try:
            test_content = test_file.read_text()
            test_copy.write_text(test_content)
            
            # Handle pytest-based tests differently
            if test_name == "5_functional_correctness":
                # Run with pytest using UV with more reliable output format
                cmd = ["uv", "run", "python", "-m", "pytest", str(test_copy), "--tb=no", "-v", "--no-header"]
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
                    # Remove execution_time from all results except functional_correctness
                    if test_name != "5_functional_correctness":
                        result.pop("execution_time", None)
                    return result
                else:
                    result = {
                        "status": "success",
                        "output": process.stdout.strip(),
                        "execution_time": execution_time
                    }
                    # Remove execution_time from all results except functional_correctness
                    if test_name != "5_functional_correctness":
                        result.pop("execution_time", None)
                    return result
            else:
                result = {
                    "status": "failed",
                    "output": process.stdout.strip(),
                    "error": process.stderr.strip(),
                    "execution_time": execution_time
                }
                # Remove execution_time from all results except functional_correctness
                if test_name != "5_functional_correctness":
                    result.pop("execution_time", None)
                return result
        
        except subprocess.TimeoutExpired:
            result = {
                "status": "timeout",
                "error": "Test timed out after 30 seconds",
                "execution_time": 30.0
            }
            # Remove execution_time from all results except functional_correctness
            if test_name != "5_functional_correctness":
                result.pop("execution_time", None)
            return result
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "execution_time": time.time() - start_time
            }
            # Remove execution_time from all results except functional_correctness
            if test_name != "5_functional_correctness":
                result.pop("execution_time", None)
            return result
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
                "cognitive_complexity": advanced_metrics.cognitive_complexity,
                "max_nesting_depth": advanced_metrics.max_nesting_depth,
                "avg_nesting_depth": advanced_metrics.avg_nesting_depth
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
            "size_analysis": {
                "lines": advanced_metrics.physical_lines_of_code,  # Map legacy code_length 
                "logical_lines_of_code": advanced_metrics.logical_lines_of_code,
                "physical_lines_of_code": advanced_metrics.physical_lines_of_code,
                "comment_lines": advanced_metrics.comment_lines,
                "blank_lines": advanced_metrics.blank_lines,
                "code_to_comment_ratio": advanced_metrics.code_to_comment_ratio,
                "function_count": advanced_metrics.function_count,
                "class_count": advanced_metrics.class_count,
                "method_count": advanced_metrics.method_count,
                "avg_parameters_per_function": advanced_metrics.avg_parameters_per_function,
                "avg_wmc": advanced_metrics.avg_wmc
            },
            "modularity_oop": {
                "functions": advanced_metrics.function_count,  # Map from legacy modularity
                "classes": advanced_metrics.class_count,       # Map from legacy modularity
                "methods": advanced_metrics.method_count,      # Map from legacy modularity
                "score": 2.0,  # Placeholder - will need calculation logic
                "max_dit": advanced_metrics.max_dit,
                "avg_dit": advanced_metrics.avg_dit
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
