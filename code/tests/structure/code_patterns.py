#!/usr/bin/env python3
"""
Code Patterns Analysis Test

This script analyzes various code patterns in Python code including lambdas,
generators, decorators, docstrings, and other Python-specific constructs.
Part of the structure test group for temperature research.
"""

import ast
import sys
import re
from pathlib import Path
from typing import Dict, Any, List
import json


class CodePatternsAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing code patterns."""
    
    def __init__(self):
        self.lambda_count = 0
        self.generator_count = 0
        self.decorator_count = 0
        self.docstring_count = 0
        self.comprehensions = {"list": 0, "dict": 0, "set": 0}
        self.context_managers = 0
        self.async_functions = 0
        self.property_methods = 0
        self.static_methods = 0
        self.class_methods = 0
        self.magic_methods = 0
        self.nested_functions = 0
        self.closures = 0
        self.scope_depth = 0
        self.max_scope_depth = 0
        
    def visit_Lambda(self, node):
        self.lambda_count += 1
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node):
        self.generator_count += 1
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        self.comprehensions["list"] += 1
        self.generic_visit(node)
    
    def visit_DictComp(self, node):
        self.comprehensions["dict"] += 1
        self.generic_visit(node)
    
    def visit_SetComp(self, node):
        self.comprehensions["set"] += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        self.context_managers += 1
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        self.async_functions += 1
        self._analyze_function(node)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        self._analyze_function(node)
        
        # Track scope depth for nested functions
        self.scope_depth += 1
        self.max_scope_depth = max(self.max_scope_depth, self.scope_depth)
        
        if self.scope_depth > 1:
            self.nested_functions += 1
        
        self.generic_visit(node)
        self.scope_depth -= 1
    
    def visit_ClassDef(self, node):
        # Count decorators on class
        self.decorator_count += len(node.decorator_list)
        
        # Check for docstring
        if (node.body and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and 
            isinstance(node.body[0].value.value, str)):
            self.docstring_count += 1
        
        self.generic_visit(node)
    
    def _analyze_function(self, node):
        """Analyze function-specific patterns."""
        # Count decorators
        self.decorator_count += len(node.decorator_list)
        
        # Check for docstring
        if (node.body and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and 
            isinstance(node.body[0].value.value, str)):
            self.docstring_count += 1
        
        # Analyze decorator types
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id == 'property':
                    self.property_methods += 1
                elif decorator.id == 'staticmethod':
                    self.static_methods += 1
                elif decorator.id == 'classmethod':
                    self.class_methods += 1
        
        # Check for magic methods
        if node.name.startswith('__') and node.name.endswith('__'):
            self.magic_methods += 1
        
        # Check for closures (functions that reference non-local variables)
        # This is a simplified heuristic
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                # This is a very basic check - a more sophisticated analysis
                # would track variable scopes properly
                pass


class DocstringAnalyzer:
    """Analyze docstring patterns and quality."""
    
    @staticmethod
    def analyze_docstrings(code_content: str) -> Dict[str, Any]:
        """Extract and analyze docstring patterns."""
        try:
            tree = ast.parse(code_content)
            
            docstrings = []
            functions_with_docstrings = 0
            classes_with_docstrings = 0
            total_functions = 0
            total_classes = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    total_functions += 1
                    if (node.body and isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Constant) and 
                        isinstance(node.body[0].value.value, str)):
                        functions_with_docstrings += 1
                        docstrings.append(node.body[0].value.value)
                
                elif isinstance(node, ast.ClassDef):
                    total_classes += 1
                    if (node.body and isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Constant) and 
                        isinstance(node.body[0].value.value, str)):
                        classes_with_docstrings += 1
                        docstrings.append(node.body[0].value.value)
            
            # Analyze docstring characteristics
            docstring_lengths = [len(ds) for ds in docstrings]
            multiline_docstrings = len([ds for ds in docstrings if '\n' in ds])
            
            return {
                "total_docstrings": len(docstrings),
                "functions_with_docstrings": functions_with_docstrings,
                "classes_with_docstrings": classes_with_docstrings,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "docstring_coverage_functions": functions_with_docstrings / total_functions if total_functions > 0 else 0,
                "docstring_coverage_classes": classes_with_docstrings / total_classes if total_classes > 0 else 0,
                "avg_docstring_length": sum(docstring_lengths) / len(docstring_lengths) if docstring_lengths else 0,
                "multiline_docstrings": multiline_docstrings
            }
            
        except Exception:
            return {
                "total_docstrings": 0,
                "functions_with_docstrings": 0,
                "classes_with_docstrings": 0,
                "total_functions": 0,
                "total_classes": 0,
                "docstring_coverage_functions": 0,
                "docstring_coverage_classes": 0,
                "avg_docstring_length": 0,
                "multiline_docstrings": 0
            }


def analyze_code_patterns(code_content: str) -> Dict[str, Any]:
    """
    Analyze code patterns in Python code.
    
    Args:
        code_content: String containing Python source code
        
    Returns:
        Dictionary containing code pattern metrics
    """
    try:
        tree = ast.parse(code_content)
        analyzer = CodePatternsAnalyzer()
        analyzer.visit(tree)
        
        # Get docstring analysis
        docstring_info = DocstringAnalyzer.analyze_docstrings(code_content)
        
        return {
            "lambda_count": analyzer.lambda_count,
            "generator_count": analyzer.generator_count,
            "decorator_count": analyzer.decorator_count,
            "docstring_count": analyzer.docstring_count,
            "comprehension_count": analyzer.comprehensions,
            "context_manager_count": analyzer.context_managers,
            "async_function_count": analyzer.async_functions,
            "property_method_count": analyzer.property_methods,
            "static_method_count": analyzer.static_methods,
            "class_method_count": analyzer.class_methods,
            "magic_method_count": analyzer.magic_methods,
            "nested_function_count": analyzer.nested_functions,
            "max_nesting_depth": analyzer.max_scope_depth,
            "total_comprehensions": sum(analyzer.comprehensions.values()),
            "advanced_patterns_score": (
                analyzer.lambda_count + analyzer.generator_count +
                sum(analyzer.comprehensions.values()) + analyzer.decorator_count +
                analyzer.context_managers + analyzer.async_functions
            ),
            **docstring_info,
            "error": None
        }
        
    except SyntaxError as e:
        return {
            "lambda_count": 0,
            "generator_count": 0,
            "decorator_count": 0,
            "docstring_count": 0,
            "comprehension_count": {"list": 0, "dict": 0, "set": 0},
            "context_manager_count": 0,
            "async_function_count": 0,
            "property_method_count": 0,
            "static_method_count": 0,
            "class_method_count": 0,
            "magic_method_count": 0,
            "nested_function_count": 0,
            "max_nesting_depth": 0,
            "total_comprehensions": 0,
            "advanced_patterns_score": 0,
            "total_docstrings": 0,
            "functions_with_docstrings": 0,
            "classes_with_docstrings": 0,
            "total_functions": 0,
            "total_classes": 0,
            "docstring_coverage_functions": 0,
            "docstring_coverage_classes": 0,
            "avg_docstring_length": 0,
            "multiline_docstrings": 0,
            "error": f"Syntax error: {str(e)}"
        }
        
    except Exception as e:
        return {
            "lambda_count": 0,
            "generator_count": 0,
            "decorator_count": 0,
            "docstring_count": 0,
            "comprehension_count": {"list": 0, "dict": 0, "set": 0},
            "context_manager_count": 0,
            "async_function_count": 0,
            "property_method_count": 0,
            "static_method_count": 0,
            "class_method_count": 0,
            "magic_method_count": 0,
            "nested_function_count": 0,
            "max_nesting_depth": 0,
            "total_comprehensions": 0,
            "advanced_patterns_score": 0,
            "total_docstrings": 0,
            "functions_with_docstrings": 0,
            "classes_with_docstrings": 0,
            "total_functions": 0,
            "total_classes": 0,
            "docstring_coverage_functions": 0,
            "docstring_coverage_classes": 0,
            "avg_docstring_length": 0,
            "multiline_docstrings": 0,
            "error": f"Analysis error: {str(e)}"
        }


def main():
    """Main entry point for code patterns analysis test."""
    if len(sys.argv) != 2:
        print("Usage: python code_patterns.py <code_file_path>")
        sys.exit(1)
    
    code_file = Path(sys.argv[1])
    
    if not code_file.exists():
        result = {
            "file_exists": False,
            "error": f"File not found: {code_file}",
            "lambda_count": 0,
            "generator_count": 0,
            "decorator_count": 0,
            "docstring_count": 0,
            "comprehension_count": {"list": 0, "dict": 0, "set": 0},
            "context_manager_count": 0,
            "async_function_count": 0,
            "property_method_count": 0,
            "static_method_count": 0,
            "class_method_count": 0,
            "magic_method_count": 0,
            "nested_function_count": 0,
            "max_nesting_depth": 0,
            "total_comprehensions": 0,
            "advanced_patterns_score": 0,
            "total_docstrings": 0,
            "functions_with_docstrings": 0,
            "classes_with_docstrings": 0,
            "total_functions": 0,
            "total_classes": 0,
            "docstring_coverage_functions": 0,
            "docstring_coverage_classes": 0,
            "avg_docstring_length": 0,
            "multiline_docstrings": 0
        }
    else:
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            result = analyze_code_patterns(code_content)
            result["file_exists"] = True
            
        except Exception as e:
            result = {
                "file_exists": True,
                "error": f"Failed to read file: {str(e)}",
                "lambda_count": 0,
                "generator_count": 0,
                "decorator_count": 0,
                "docstring_count": 0,
                "comprehension_count": {"list": 0, "dict": 0, "set": 0},
                "context_manager_count": 0,
                "async_function_count": 0,
                "property_method_count": 0,
                "static_method_count": 0,
                "class_method_count": 0,
                "magic_method_count": 0,
                "nested_function_count": 0,
                "max_nesting_depth": 0,
                "total_comprehensions": 0,
                "advanced_patterns_score": 0,
                "total_docstrings": 0,
                "functions_with_docstrings": 0,
                "classes_with_docstrings": 0,
                "total_functions": 0,
                "total_classes": 0,
                "docstring_coverage_functions": 0,
                "docstring_coverage_classes": 0,
                "avg_docstring_length": 0,
                "multiline_docstrings": 0
            }
    
    # Output results as JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
