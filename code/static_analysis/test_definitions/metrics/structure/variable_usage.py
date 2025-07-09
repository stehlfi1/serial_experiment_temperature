#!/usr/bin/env python3
"""
Variable Usage Analysis Test

This script analyzes variable usage patterns in Python code including variable
counts, scope analysis, and naming patterns.
Part of the structure test group for temperature research.
"""

import ast
import sys
import re
from pathlib import Path
from typing import Dict, Any, Set, List
import json


class VariableUsageAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing variable usage patterns."""
    
    def __init__(self):
        self.variables = set()
        self.global_variables = set()
        self.nonlocal_variables = set()
        self.imports = set()
        self.from_imports = set()
        self.function_parameters = []
        self.variable_assignments = 0
        self.variable_loads = 0
        self.scope_stack = []
        self.current_scope = 'global'
        self.scope_variables = {'global': set()}
        
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.variables.add(node.id)
            self.scope_variables[self.current_scope].add(node.id)
            self.variable_assignments += 1
        elif isinstance(node.ctx, ast.Load):
            self.variable_loads += 1
        
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        # Track function parameters
        for arg in node.args.args:
            self.function_parameters.append(arg.arg)
        
        # Enter new scope
        old_scope = self.current_scope
        self.current_scope = f"function_{node.name}"
        self.scope_variables[self.current_scope] = set()
        self.scope_stack.append(old_scope)
        
        self.generic_visit(node)
        
        # Exit scope
        self.current_scope = self.scope_stack.pop()
    
    def visit_ClassDef(self, node):
        # Enter new scope
        old_scope = self.current_scope
        self.current_scope = f"class_{node.name}"
        self.scope_variables[self.current_scope] = set()
        self.scope_stack.append(old_scope)
        
        self.generic_visit(node)
        
        # Exit scope
        self.current_scope = self.scope_stack.pop()
    
    def visit_Global(self, node):
        for name in node.names:
            self.global_variables.add(name)
        self.generic_visit(node)
    
    def visit_Nonlocal(self, node):
        for name in node.names:
            self.nonlocal_variables.add(name)
        self.generic_visit(node)
    
    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.add(name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.from_imports.add(name)
        self.generic_visit(node)


class NamingConventionAnalyzer:
    """Analyze naming conventions in Python code."""
    
    @staticmethod
    def analyze_naming_conventions(variables: Set[str], functions: List[str], 
                                 classes: List[str]) -> Dict[str, Any]:
        """Analyze naming convention compliance."""
        
        # Python naming convention patterns
        snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
        camel_case_pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
        pascal_case_pattern = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
        constant_pattern = re.compile(r'^[A-Z_][A-Z0-9_]*$')
        private_pattern = re.compile(r'^_[a-zA-Z0-9_]*$')
        magic_pattern = re.compile(r'^__[a-zA-Z0-9_]*__$')
        
        # Analyze variables
        snake_case_vars = len([v for v in variables if snake_case_pattern.match(v)])
        constant_vars = len([v for v in variables if constant_pattern.match(v)])
        private_vars = len([v for v in variables if private_pattern.match(v)])
        
        # Analyze functions
        snake_case_funcs = len([f for f in functions if snake_case_pattern.match(f)])
        magic_funcs = len([f for f in functions if magic_pattern.match(f)])
        
        # Analyze classes  
        pascal_case_classes = len([c for c in classes if pascal_case_pattern.match(c)])
        
        total_vars = len(variables)
        total_funcs = len(functions)
        total_classes = len(classes)
        
        return {
            "snake_case_variables": snake_case_vars,
            "constant_variables": constant_vars,
            "private_variables": private_vars,
            "snake_case_functions": snake_case_funcs,
            "magic_functions": magic_funcs,
            "pascal_case_classes": pascal_case_classes,
            "variable_naming_score": snake_case_vars / total_vars if total_vars > 0 else 1.0,
            "function_naming_score": snake_case_funcs / total_funcs if total_funcs > 0 else 1.0,
            "class_naming_score": pascal_case_classes / total_classes if total_classes > 0 else 1.0,
            "overall_naming_score": (
                (snake_case_vars + snake_case_funcs + pascal_case_classes) /
                (total_vars + total_funcs + total_classes)
                if (total_vars + total_funcs + total_classes) > 0 else 1.0
            )
        }


def get_function_and_class_names(code_content: str) -> tuple:
    """Extract function and class names from code."""
    try:
        tree = ast.parse(code_content)
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return functions, classes
    except:
        return [], []


def analyze_variable_usage(code_content: str) -> Dict[str, Any]:
    """
    Analyze variable usage patterns in Python code.
    
    Args:
        code_content: String containing Python source code
        
    Returns:
        Dictionary containing variable usage metrics
    """
    try:
        tree = ast.parse(code_content)
        analyzer = VariableUsageAnalyzer()
        analyzer.visit(tree)
        
        # Get function and class names for naming analysis
        functions, classes = get_function_and_class_names(code_content)
        
        # Analyze naming conventions
        naming_info = NamingConventionAnalyzer.analyze_naming_conventions(
            analyzer.variables, functions, classes
        )
        
        # Calculate variable statistics
        unique_parameters = set(analyzer.function_parameters)
        parameter_frequency = {}
        for param in analyzer.function_parameters:
            parameter_frequency[param] = parameter_frequency.get(param, 0) + 1
        
        return {
            "variable_count": len(analyzer.variables),
            "global_variable_count": len(analyzer.global_variables),
            "nonlocal_variable_count": len(analyzer.nonlocal_variables),
            "import_count": len(analyzer.imports),
            "from_import_count": len(analyzer.from_imports),
            "unique_imports": len(analyzer.imports) + len(analyzer.from_imports),
            "variable_assignments": analyzer.variable_assignments,
            "variable_loads": analyzer.variable_loads,
            "assignment_to_load_ratio": (
                analyzer.variable_assignments / analyzer.variable_loads 
                if analyzer.variable_loads > 0 else 0
            ),
            "function_parameter_count": len(analyzer.function_parameters),
            "unique_parameter_count": len(unique_parameters),
            "parameter_reuse_ratio": (
                (len(analyzer.function_parameters) - len(unique_parameters)) / 
                len(analyzer.function_parameters)
                if len(analyzer.function_parameters) > 0 else 0
            ),
            "most_common_parameters": sorted(
                parameter_frequency.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],
            "scope_count": len(analyzer.scope_variables),
            "variables_per_scope": {
                scope: len(vars) for scope, vars in analyzer.scope_variables.items()
            },
            **naming_info,
            "error": None
        }
        
    except SyntaxError as e:
        return {
            "variable_count": 0,
            "global_variable_count": 0,
            "nonlocal_variable_count": 0,
            "import_count": 0,
            "from_import_count": 0,
            "unique_imports": 0,
            "variable_assignments": 0,
            "variable_loads": 0,
            "assignment_to_load_ratio": 0,
            "function_parameter_count": 0,
            "unique_parameter_count": 0,
            "parameter_reuse_ratio": 0,
            "most_common_parameters": [],
            "scope_count": 0,
            "variables_per_scope": {},
            "snake_case_variables": 0,
            "constant_variables": 0,
            "private_variables": 0,
            "snake_case_functions": 0,
            "magic_functions": 0,
            "pascal_case_classes": 0,
            "variable_naming_score": 0,
            "function_naming_score": 0,
            "class_naming_score": 0,
            "overall_naming_score": 0,
            "error": f"Syntax error: {str(e)}"
        }
        
    except Exception as e:
        return {
            "variable_count": 0,
            "global_variable_count": 0,
            "nonlocal_variable_count": 0,
            "import_count": 0,
            "from_import_count": 0,
            "unique_imports": 0,
            "variable_assignments": 0,
            "variable_loads": 0,
            "assignment_to_load_ratio": 0,
            "function_parameter_count": 0,
            "unique_parameter_count": 0,
            "parameter_reuse_ratio": 0,
            "most_common_parameters": [],
            "scope_count": 0,
            "variables_per_scope": {},
            "snake_case_variables": 0,
            "constant_variables": 0,
            "private_variables": 0,
            "snake_case_functions": 0,
            "magic_functions": 0,
            "pascal_case_classes": 0,
            "variable_naming_score": 0,
            "function_naming_score": 0,
            "class_naming_score": 0,
            "overall_naming_score": 0,
            "error": f"Analysis error: {str(e)}"
        }


def main():
    """Main entry point for variable usage analysis test."""
    if len(sys.argv) != 2:
        print("Usage: python variable_usage.py <code_file_path>")
        sys.exit(1)
    
    code_file = Path(sys.argv[1])
    
    if not code_file.exists():
        result = {
            "file_exists": False,
            "error": f"File not found: {code_file}",
            "variable_count": 0,
            "global_variable_count": 0,
            "nonlocal_variable_count": 0,
            "import_count": 0,
            "from_import_count": 0,
            "unique_imports": 0,
            "variable_assignments": 0,
            "variable_loads": 0,
            "assignment_to_load_ratio": 0,
            "function_parameter_count": 0,
            "unique_parameter_count": 0,
            "parameter_reuse_ratio": 0,
            "most_common_parameters": [],
            "scope_count": 0,
            "variables_per_scope": {},
            "snake_case_variables": 0,
            "constant_variables": 0,
            "private_variables": 0,
            "snake_case_functions": 0,
            "magic_functions": 0,
            "pascal_case_classes": 0,
            "variable_naming_score": 0,
            "function_naming_score": 0,
            "class_naming_score": 0,
            "overall_naming_score": 0
        }
    else:
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            result = analyze_variable_usage(code_content)
            result["file_exists"] = True
            
        except Exception as e:
            result = {
                "file_exists": True,
                "error": f"Failed to read file: {str(e)}",
                "variable_count": 0,
                "global_variable_count": 0,
                "nonlocal_variable_count": 0,
                "import_count": 0,
                "from_import_count": 0,
                "unique_imports": 0,
                "variable_assignments": 0,
                "variable_loads": 0,
                "assignment_to_load_ratio": 0,
                "function_parameter_count": 0,
                "unique_parameter_count": 0,
                "parameter_reuse_ratio": 0,
                "most_common_parameters": [],
                "scope_count": 0,
                "variables_per_scope": {},
                "snake_case_variables": 0,
                "constant_variables": 0,
                "private_variables": 0,
                "snake_case_functions": 0,
                "magic_functions": 0,
                "pascal_case_classes": 0,
                "variable_naming_score": 0,
                "function_naming_score": 0,
                "class_naming_score": 0,
                "overall_naming_score": 0
            }
    
    # Output results as JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
