"""
Jaccard similarity calculator for token-based code comparison.
Provides multiple tokenization strategies for different levels of analysis.
"""

import re
import ast
import keyword
from typing import Set, List, Dict, Any
from pathlib import Path


class JaccardCalculator:
    """Calculate Jaccard similarity between Python code files using various tokenization strategies."""
    
    def __init__(self):
        self.python_keywords = set(keyword.kwlist)
        self.operators = {'+', '-', '*', '/', '//', '%', '**', '=', '==', '!=', '<', '>', '<=', '>=', 
                         'and', 'or', 'not', 'is', 'in', '&', '|', '^', '~', '<<', '>>', '+=', '-=', 
                         '*=', '/=', '//=', '%=', '**=', '&=', '|=', '^=', '<<=', '>>='}
    
    def calculate_similarity(self, file1: str, file2: str) -> Dict[str, float]:
        """
        Calculate Jaccard similarity between two Python files using multiple tokenization strategies.
        
        Args:
            file1: Path to first Python file
            file2: Path to second Python file
            
        Returns:
            Dict with Jaccard similarities for different tokenization methods
        """
        try:
            with open(file1, 'r', encoding='utf-8') as f:
                code1 = f.read()
            with open(file2, 'r', encoding='utf-8') as f:
                code2 = f.read()
            
            return self.calculate_similarity_from_strings(code1, code2)
            
        except Exception as e:
            return {
                "jaccard_tokens": 0.0,
                "jaccard_words": 0.0,
                "jaccard_identifiers": 0.0,
                "jaccard_keywords": 0.0,
                "jaccard_ast_names": 0.0,
                "error": str(e)
            }
    
    def calculate_similarity_from_strings(self, code1: str, code2: str) -> Dict[str, float]:
        """
        Calculate Jaccard similarity between two code strings using multiple methods.
        
        Args:
            code1: First Python code string
            code2: Second Python code string
            
        Returns:
            Dict with Jaccard similarities for different tokenization methods
        """
        try:
            results = {}
            
            # Token-level Jaccard (split by whitespace and punctuation)
            tokens1 = self._tokenize_basic(code1)
            tokens2 = self._tokenize_basic(code2)
            results["jaccard_tokens"] = self._jaccard_similarity(tokens1, tokens2)
            
            # Word-level Jaccard (alphanumeric words only)
            words1 = self._extract_words(code1)
            words2 = self._extract_words(code2)
            results["jaccard_words"] = self._jaccard_similarity(words1, words2)
            
            # Identifier-level Jaccard (variable/function names)
            identifiers1 = self._extract_identifiers(code1)
            identifiers2 = self._extract_identifiers(code2)
            results["jaccard_identifiers"] = self._jaccard_similarity(identifiers1, identifiers2)
            
            # Keyword-level Jaccard (Python keywords only)
            keywords1 = self._extract_keywords(code1)
            keywords2 = self._extract_keywords(code2)
            results["jaccard_keywords"] = self._jaccard_similarity(keywords1, keywords2)
            
            # AST-based name extraction
            ast_names1 = self._extract_ast_names(code1)
            ast_names2 = self._extract_ast_names(code2)
            results["jaccard_ast_names"] = self._jaccard_similarity(ast_names1, ast_names2)
            
            return results
            
        except Exception as e:
            return {
                "jaccard_tokens": 0.0,
                "jaccard_words": 0.0,
                "jaccard_identifiers": 0.0,
                "jaccard_keywords": 0.0,
                "jaccard_ast_names": 0.0,
                "error": str(e)
            }
    
    def _jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """Calculate Jaccard similarity coefficient between two sets."""
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def _tokenize_basic(self, code: str) -> Set[str]:
        """Basic tokenization: split by whitespace and punctuation."""
        # Remove comments and strings to focus on code structure
        code_no_comments = self._remove_comments_and_strings(code)
        
        # Split by whitespace and common punctuation
        tokens = re.findall(r'\w+|[^\w\s]', code_no_comments)
        
        # Filter out empty tokens and normalize
        return {token.strip().lower() for token in tokens if token.strip()}
    
    def _extract_words(self, code: str) -> Set[str]:
        """Extract alphanumeric words (identifiers, keywords, etc.)."""
        code_no_comments = self._remove_comments_and_strings(code)
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code_no_comments)
        return {word.lower() for word in words}
    
    def _extract_identifiers(self, code: str) -> Set[str]:
        """Extract user-defined identifiers (excluding keywords and builtins)."""
        words = self._extract_words(code)
        # Filter out Python keywords and common builtins
        builtins = {'int', 'str', 'list', 'dict', 'set', 'tuple', 'bool', 'float', 
                   'len', 'range', 'print', 'input', 'open', 'file', 'type', 'object'}
        return words - self.python_keywords - builtins
    
    def _extract_keywords(self, code: str) -> Set[str]:
        """Extract Python keywords from code."""
        words = self._extract_words(code)
        return words & self.python_keywords
    
    def _extract_ast_names(self, code: str) -> Set[str]:
        """Extract names using AST parsing (more accurate than regex)."""
        try:
            tree = ast.parse(code)
            names = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    names.add(node.id.lower())
                elif isinstance(node, ast.FunctionDef):
                    names.add(node.name.lower())
                elif isinstance(node, ast.ClassDef):
                    names.add(node.name.lower())
                elif isinstance(node, ast.Attribute):
                    names.add(node.attr.lower())
            
            return names
            
        except SyntaxError:
            # Fallback to word extraction if AST parsing fails
            return self._extract_words(code)
    
    def _remove_comments_and_strings(self, code: str) -> str:
        """Remove comments and string literals to focus on code structure."""
        try:
            tree = ast.parse(code)
            
            # Get all string literal positions to remove them
            string_positions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
                        string_positions.append((node.lineno, node.col_offset))
                elif isinstance(node, ast.Str):  # For older Python versions
                    if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
                        string_positions.append((node.lineno, node.col_offset))
            
            # Simple approach: remove lines starting with # and triple-quoted strings
            lines = code.split('\n')
            filtered_lines = []
            
            for line in lines:
                # Remove inline comments (simple approach)
                if '#' in line:
                    # Don't remove # inside strings (simplified)
                    comment_pos = line.find('#')
                    line = line[:comment_pos]
                
                # Remove empty lines and whitespace-only lines
                if line.strip():
                    filtered_lines.append(line)
            
            return '\n'.join(filtered_lines)
            
        except SyntaxError:
            # Fallback: simple regex-based removal
            # Remove single-line comments
            code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
            # Remove triple-quoted strings (simplified)
            code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
            code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
            return code
    
    def calculate_weighted_jaccard(self, file1: str, file2: str, weights: Dict[str, float] = None) -> float:
        """
        Calculate weighted Jaccard similarity combining multiple tokenization methods.
        
        Args:
            file1: Path to first Python file
            file2: Path to second Python file
            weights: Dict with weights for each similarity type
            
        Returns:
            Weighted Jaccard similarity score
        """
        if weights is None:
            weights = {
                "jaccard_tokens": 0.2,
                "jaccard_words": 0.2,
                "jaccard_identifiers": 0.3,
                "jaccard_keywords": 0.1,
                "jaccard_ast_names": 0.2
            }
        
        similarities = self.calculate_similarity(file1, file2)
        
        if "error" in similarities:
            return 0.0
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for sim_type, weight in weights.items():
            if sim_type in similarities:
                weighted_sum += similarities[sim_type] * weight
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0


def calculate_jaccard_similarity(file1: str, file2: str) -> Dict[str, float]:
    """
    Convenience function to calculate Jaccard similarity between two files.
    
    Args:
        file1: Path to first Python file
        file2: Path to second Python file
        
    Returns:
        Dict with Jaccard similarities for different tokenization methods
    """
    calculator = JaccardCalculator()
    return calculator.calculate_similarity(file1, file2)


if __name__ == "__main__":
    # Simple test
    test_code1 = """
def add_numbers(a, b):
    result = a + b
    return result

x = add_numbers(1, 2)
print(x)
"""
    
    test_code2 = """
def add_numbers(x, y):
    result = x + y
    return result

z = add_numbers(1, 2)
print(z)
"""
    
    test_code3 = """
def multiply(a, b):
    product = a * b
    return product

result = multiply(2, 3)
print(result)
"""
    
    calculator = JaccardCalculator()
    
    # Test similar code
    result1 = calculator.calculate_similarity_from_strings(test_code1, test_code2)
    print("Similar code Jaccard:", result1)
    
    # Test different code
    result2 = calculator.calculate_similarity_from_strings(test_code1, test_code3)
    print("Different code Jaccard:", result2)
    
    # Test weighted similarity
    weighted1 = calculator.calculate_weighted_jaccard("", "")  # Would need temp files for real test
    print("Note: Weighted similarity requires file paths for full test")