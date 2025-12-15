"""
CodeBLEU wrapper for measuring code-aware similarity between Python files.
Provides a simple interface to the codebleu library for temperature research.
"""

import ast
from pathlib import Path
from typing import Optional, Dict, Any
import tempfile
import os

try:
    from codebleu import calc_codebleu
    CODEBLEU_AVAILABLE = True
except ImportError:
    CODEBLEU_AVAILABLE = False
    print("Warning: codebleu not installed. Install with: pip install codebleu")


class CodeBLEUCalculator:
    """Calculate CodeBLEU similarity between two Python code files."""
    
    def __init__(self):
        if not CODEBLEU_AVAILABLE:
            raise ImportError("codebleu library not available. Install with: pip install codebleu")
    
    def calculate_similarity(self, code1_path: str, code2_path: str) -> Dict[str, float]:
        """
        Calculate CodeBLEU similarity between two Python files.
        
        Args:
            code1_path: Path to first Python file
            code2_path: Path to second Python file
            
        Returns:
            Dict with CodeBLEU scores and components
        """
        try:
            # Read the code files
            with open(code1_path, 'r', encoding='utf-8') as f:
                code1 = f.read()
            with open(code2_path, 'r', encoding='utf-8') as f:
                code2 = f.read()
            
            return self.calculate_similarity_from_strings(code1, code2)
            
        except Exception as e:
            return {
                "codebleu": 0.0,
                "bleu": 0.0,
                "weighted_ngram_match": 0.0,
                "syntax_match": 0.0,
                "dataflow_match": 0.0,
                "error": str(e)
            }
    
    def calculate_similarity_from_strings(self, code1: str, code2: str) -> Dict[str, float]:
        """
        Calculate CodeBLEU similarity between two code strings.
        
        Args:
            code1: First Python code string
            code2: Second Python code string
            
        Returns:
            Dict with CodeBLEU scores and components
        """
        try:
            # Validate that both are valid Python
            if not self._is_valid_python(code1) or not self._is_valid_python(code2):
                return {
                    "codebleu": 0.0,
                    "bleu": 0.0,
                    "weighted_ngram_match": 0.0,
                    "syntax_match": 0.0,
                    "dataflow_match": 0.0,
                    "error": "Invalid Python syntax"
                }
            
            # Calculate CodeBLEU - pass code strings directly
            result = calc_codebleu(
                references=[code1],  # Reference code string
                predictions=[code2], # Prediction code string
                lang="python"
            )

            return {
                "codebleu": result.get("codebleu", 0.0),
                "bleu": result.get("ngram_match_score", 0.0),
                "weighted_ngram_match": result.get("weighted_ngram_match_score", 0.0),
                "syntax_match": result.get("syntax_match_score", 0.0),
                "dataflow_match": result.get("dataflow_match_score", 0.0)
            }
                        
        except Exception as e:
            return {
                "codebleu": 0.0,
                "bleu": 0.0,
                "weighted_ngram_match": 0.0,
                "syntax_match": 0.0,
                "dataflow_match": 0.0,
                "error": str(e)
            }
    
    def _is_valid_python(self, code: str) -> bool:
        """Check if code string is valid Python syntax."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False


def calculate_codebleu_similarity(file1: str, file2: str) -> Dict[str, float]:
    """
    Convenience function to calculate CodeBLEU similarity between two files.
    
    Args:
        file1: Path to first Python file
        file2: Path to second Python file
        
    Returns:
        Dict with CodeBLEU scores
    """
    if not CODEBLEU_AVAILABLE:
        return {
            "codebleu": 0.0,
            "error": "codebleu library not available"
        }
    
    calculator = CodeBLEUCalculator()
    return calculator.calculate_similarity(file1, file2)


if __name__ == "__main__":
    # Simple test
    if CODEBLEU_AVAILABLE:
        # Test with identical code
        test_code = """
def add(a, b):
    return a + b

result = add(1, 2)
print(result)
"""
        
        calculator = CodeBLEUCalculator()
        result = calculator.calculate_similarity_from_strings(test_code, test_code)
        print("Identical code similarity:", result)
        
        # Test with slightly different code
        test_code2 = """
def add(x, y):
    return x + y

result = add(1, 2)
print(result)
"""
        
        result2 = calculator.calculate_similarity_from_strings(test_code, test_code2)
        print("Similar code similarity:", result2)
    else:
        print("CodeBLEU not available for testing")