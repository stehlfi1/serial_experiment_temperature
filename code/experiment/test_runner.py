import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List


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


class TestRunner:
    def __init__(self, tests_dir: Path):
        self.tests_dir = tests_dir
        self.test_mapping = {
            "1_code_compilability": TestResultParser.parse_compilability_output,
            "2_code_length_adaptive": TestResultParser.parse_code_length_output,
            "3_modularity_adaptive": TestResultParser.parse_modularity_output,
            "4_functional_completeness_adaptive": TestResultParser.parse_functional_completeness_output
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
            test_copy.write_text(test_file.read_text())
            
            cmd = [sys.executable, str(test_copy), model]
            process = subprocess.run(
                cmd,
                cwd=str(code_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            execution_time = time.time() - start_time
            
            if process.returncode == 0:
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
                                challenge: str) -> Dict[str, Dict[str, Any]]:
        results = {}
        
        for test_name in self.test_mapping.keys():
            results[test_name] = self.run_test(test_name, model, code_dir, challenge)
        
        return results
