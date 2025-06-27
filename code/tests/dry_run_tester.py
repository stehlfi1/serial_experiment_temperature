#!/usr/bin/env python3
"""
Simple Dry Run Tester

This script runs quality tests on dry run generated code using the existing test infrastructure.
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime


class DryRunTester:
    """Simple dry run tester using existing test files."""
    
    def __init__(self):
        """Initialize the tester."""
        self.project_root = Path(__file__).parent.parent.parent
        self.tests_dir = self.project_root / "code" / "tests"
        self.dry_run_dir = self.project_root / "dry_run_output"
        self.results_dir = self.dry_run_dir / "test_results"
        
        # Available tests (using adaptive versions for dry runs)
        self.tests = ["1_code_compilability", "2_code_length_adaptive", "3_modularity_adaptive", "4_functional_completeness_adaptive"]
        self.models = ["chatgpt", "claude", "gemini"]
        
        # Create results directory
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def find_test_directories(self, challenge: Optional[str] = None) -> List[Path]:
        """Find all directories with generated code to test."""
        test_dirs = []
        
        if not (self.dry_run_dir / "code").exists():
            return test_dirs
        
        code_dir = self.dry_run_dir / "code"
        
        for challenge_dir in code_dir.iterdir():
            if not challenge_dir.is_dir():
                continue
                
            challenge_name = challenge_dir.name
            
            # Skip if specific challenge requested and this isn't it
            if challenge and challenge_name != challenge:
                continue
            
            # Find all iteration directories
            for prompt_dir in challenge_dir.iterdir():
                if not prompt_dir.is_dir():
                    continue
                    
                for iter_dir in prompt_dir.iterdir():
                    if iter_dir.is_dir():
                        test_dirs.append(iter_dir)
        
        return test_dirs
    
    def run_single_test(self, test_dir: Path, test_name: str, model: str) -> Dict:
        """Run a single test on a model file."""
        result = {
            "test": test_name,
            "model": model,
            "directory": str(test_dir.relative_to(self.project_root)),
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "output": "",
            "error": ""
        }
        
        # Get challenge name from path
        # Path structure: dry_run_output/code/CHALLENGE/prompt/iteration_X
        path_parts = test_dir.relative_to(self.dry_run_dir).parts
        if len(path_parts) >= 2 and path_parts[0] == "code":
            challenge_name = path_parts[1]  # Extract challenge from path
        else:
            result["status"] = "error"
            result["error"] = f"Cannot extract challenge name from path: {test_dir}"
            return result
        
        # Check if test file exists (try adaptive version first, then challenge-specific)
        test_file = self.tests_dir / f"{test_name}.py"
        if not test_file.exists():
            # Try challenge-specific version
            test_file = self.tests_dir / challenge_name / f"{test_name}.py"
            if not test_file.exists():
                result["status"] = "error"
                result["error"] = f"Test file not found: {test_file}"
                return result
        
        # Check if model file exists
        model_file = test_dir / f"{model}.py"
        if not model_file.exists():
            result["status"] = "error" 
            result["error"] = f"Model file not found: {model_file}"
            return result
        
        # Copy test file to test directory
        test_copy = test_dir / f"{test_name}.py"
        try:
            shutil.copy2(test_file, test_copy)
            
            # Run the test
            cmd = [sys.executable, str(test_copy), model]
            process = subprocess.run(
                cmd,
                cwd=str(test_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            result["status"] = "success" if process.returncode == 0 else "failed"
            result["output"] = process.stdout.strip()
            result["error"] = process.stderr.strip()
            
        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            result["error"] = "Test timed out after 30 seconds"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        finally:
            # Clean up test file
            if test_copy.exists():
                test_copy.unlink()
        
        return result
    
    def run_all_tests(self, challenge: Optional[str] = None) -> List[Dict]:
        """Run all tests on found directories."""
        print("🚀 Starting Dry Run Quality Tests")
        print(f"📁 Dry run directory: {self.dry_run_dir}")
        
        test_dirs = self.find_test_directories(challenge)
        
        if not test_dirs:
            print("❌ No test directories found")
            return []
        
        print(f"📊 Found {len(test_dirs)} test directories")
        
        all_results = []
        
        for test_dir in test_dirs:
            dir_name = test_dir.name
            print(f"\n🔍 Testing: {dir_name}")
            
            # Check which model files exist
            for model in self.models:
                model_file = test_dir / f"{model}.py"
                if model_file.exists():
                    print(f"  📝 Testing {model}.py")
                    
                    # Run each test
                    for test in self.tests:
                        print(f"    🧪 {test}... ", end="", flush=True)
                        
                        result = self.run_single_test(test_dir, test, model)
                        all_results.append(result)
                        
                        if result["status"] == "success":
                            print("✅ PASS")
                        elif result["status"] == "failed":
                            print("❌ FAIL")
                        else:
                            print(f"⚠️  {result['status'].upper()}")
                            
                else:
                    print(f"  ⚠️  Missing: {model}.py")
        
        return all_results
    
    def save_results(self, results: List[Dict]) -> Path:
        """Save results to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.results_dir / f"dry_run_test_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def print_summary(self, results: List[Dict]):
        """Print test summary."""
        if not results:
            print("\n❌ No results to summarize")
            return
        
        total = len(results)
        success = len([r for r in results if r["status"] == "success"])
        failed = len([r for r in results if r["status"] == "failed"])
        errors = len([r for r in results if r["status"] == "error"])
        
        print("\n" + "="*50)
        print("📋 TEST SUMMARY")
        print("="*50)
        print(f"Total tests: {total}")
        print(f"✅ Passed: {success}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        
        # Group by test type
        by_test = {}
        for result in results:
            test_name = result["test"]
            if test_name not in by_test:
                by_test[test_name] = {"success": 0, "failed": 0, "error": 0}
            by_test[test_name][result["status"]] = by_test[test_name].get(result["status"], 0) + 1
        
        print(f"\n📊 By Test Type:")
        for test_name, counts in by_test.items():
            total_test = sum(counts.values())
            success_rate = (counts.get("success", 0) / total_test * 100) if total_test > 0 else 0
            print(f"  {test_name}: {success_rate:.1f}% pass rate ({counts.get('success', 0)}/{total_test})")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run quality tests on dry run generated code")
    parser.add_argument("--challenge", choices=["calculator", "ascii_art", "todo_list"], 
                       help="Test only specific challenge")
    parser.add_argument("--no-summary", action="store_true", help="Don't print summary")
    
    args = parser.parse_args()
    
    tester = DryRunTester()
    
    # Check if dry run output exists
    if not tester.dry_run_dir.exists():
        print(f"❌ Dry run directory not found: {tester.dry_run_dir}")
        print("💡 Run a dry run first: uv run python code/scraper/main.py --dry-run")
        return 1
    
    # Run tests
    results = tester.run_all_tests(args.challenge)
    
    if not results:
        return 1
    
    # Save results
    output_file = tester.save_results(results)
    print(f"\n💾 Results saved to: {output_file}")
    
    # Print summary
    if not args.no_summary:
        tester.print_summary(results)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
