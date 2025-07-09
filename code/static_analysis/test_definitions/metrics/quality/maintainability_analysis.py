#!/usr/bin/env python3
"""
Maintainability Analysis Test

Analyzes maintainability index, ABC metrics, and overall code maintainability
for temperature research on LLM-generated code.
"""

import ast
import sys
import json
import math
from pathlib import Path
from collections import Counter


class MaintainabilityAnalyzer(ast.NodeVisitor):
    """Analyzes maintainability metrics in Python code."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all counters."""
        # ABC metrics
        self.assignments = 0
        self.branches = 0
        self.conditions = 0
        
        # For Halstead volume calculation
        self.operators = Counter()
        self.operands = Counter()
        
        # For cyclomatic complexity
        self.cyclomatic_complexity = 1
        
        # Lines of code
        self.logical_lines = 0
        self.comment_lines = 0
        self.blank_lines = 0
        
        # Other quality indicators
        self.functions = []
        self.classes = []
        self.imports = 0
        self.docstrings = 0
    
    def visit_Assign(self, node):
        """Count assignments."""
        self.assignments += len(node.targets)
        self.operators["Assign"] += 1
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        """Count augmented assignments."""
        self.assignments += 1
        op_name = type(node.op).__name__ + "Assign"
        self.operators[op_name] += 1
        self.generic_visit(node)
    
    def visit_AnnAssign(self, node):
        """Count annotated assignments."""
        if node.value:  # Only count if there's a value
            self.assignments += 1
        self.operators["AnnAssign"] += 1
        self.generic_visit(node)
    
    # Branch counting
    def visit_If(self, node):
        """Count if statements as branches."""
        self.branches += 1
        self.conditions += 1
        self.cyclomatic_complexity += 1
        self.operators["If"] += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        """Count while loops as branches."""
        self.branches += 1
        self.conditions += 1
        self.cyclomatic_complexity += 1
        self.operators["While"] += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Count for loops as branches."""
        self.branches += 1
        self.cyclomatic_complexity += 1
        self.operators["For"] += 1
        self.generic_visit(node)
    
    def visit_Try(self, node):
        """Count try-except as branches."""
        self.branches += len(node.handlers)
        if node.orelse:
            self.branches += 1
        if node.finalbody:
            self.branches += 1
        self.cyclomatic_complexity += len(node.handlers) + (1 if node.orelse else 0) + (1 if node.finalbody else 0)
        self.operators["Try"] += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        """Count with statements as branches."""
        self.branches += 1
        self.cyclomatic_complexity += 1
        self.operators["With"] += 1
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        """Count except handlers."""
        self.operators["ExceptHandler"] += 1
        self.generic_visit(node)
    
    # Condition counting
    def visit_Compare(self, node):
        """Count comparison operations as conditions."""
        self.conditions += len(node.ops)
        for op in node.ops:
            op_name = type(op).__name__
            self.operators[op_name] += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        """Count boolean operations as conditions."""
        self.conditions += len(node.values) - 1  # n operands = n-1 operators
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.generic_visit(node)
    
    def visit_UnaryOp(self, node):
        """Count unary operations."""
        if isinstance(node.op, ast.Not):
            self.conditions += 1
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.generic_visit(node)
    
    # Function and class counting
    def visit_FunctionDef(self, node):
        """Count functions."""
        func_info = {
            "name": node.name,
            "args": len(node.args.args),
            "decorators": len(node.decorator_list),
            "docstring": ast.get_docstring(node) is not None,
            "lineno": node.lineno
        }
        self.functions.append(func_info)
        
        if func_info["docstring"]:
            self.docstrings += 1
        
        self.operators["FunctionDef"] += 1
        self.operands[node.name] += 1
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Count async functions."""
        func_info = {
            "name": node.name,
            "args": len(node.args.args),
            "decorators": len(node.decorator_list),
            "docstring": ast.get_docstring(node) is not None,
            "lineno": node.lineno,
            "async": True
        }
        self.functions.append(func_info)
        
        if func_info["docstring"]:
            self.docstrings += 1
        
        self.operators["AsyncFunctionDef"] += 1
        self.operands[node.name] += 1
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Count classes."""
        class_info = {
            "name": node.name,
            "bases": len(node.bases),
            "decorators": len(node.decorator_list),
            "docstring": ast.get_docstring(node) is not None,
            "lineno": node.lineno
        }
        self.classes.append(class_info)
        
        if class_info["docstring"]:
            self.docstrings += 1
        
        self.operators["ClassDef"] += 1
        self.operands[node.name] += 1
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Count imports."""
        self.imports += len(node.names)
        self.operators["Import"] += 1
        for alias in node.names:
            self.operands[alias.name] += 1
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Count from imports."""
        self.imports += len(node.names)
        self.operators["ImportFrom"] += 1
        if node.module:
            self.operands[node.module] += 1
        for alias in node.names:
            self.operands[alias.name] += 1
        self.generic_visit(node)
    
    # Other operators for Halstead
    def visit_BinOp(self, node):
        """Binary operators."""
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Function calls."""
        self.operators["Call"] += 1
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Variable names."""
        if node.id not in ['True', 'False', 'None']:
            self.operands[node.id] += 1
        self.generic_visit(node)
    
    def visit_Constant(self, node):
        """Constants."""
        if isinstance(node.value, (int, float)):
            operand = f"NUM_{node.value}"
        elif isinstance(node.value, str):
            operand = f"STR_{len(node.value)}"
        else:
            operand = f"CONST_{type(node.value).__name__}"
        self.operands[operand] += 1
        self.generic_visit(node)


def calculate_halstead_volume(operators: Counter, operands: Counter) -> float:
    """Calculate Halstead volume."""
    n1 = len(operators)
    n2 = len(operands)
    N1 = sum(operators.values())
    N2 = sum(operands.values())
    
    n = n1 + n2
    N = N1 + N2
    
    if n > 1 and N > 0:
        return N * math.log2(n)
    return 0


def calculate_maintainability_index(halstead_volume: float, cyclomatic_complexity: int, 
                                   logical_lines: int, comment_ratio: float = 0) -> dict:
    """Calculate maintainability index and related metrics."""
    if logical_lines <= 0:
        return {
            "index": 0,
            "rank": "F",
            "error": "No logical lines of code"
        }
    
    # Standard Maintainability Index formula
    # MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC) + 50 * sin(sqrt(2.4 * CM))
    # Simplified version without comment metric:
    # MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
    
    try:
        mi = 171
        
        if halstead_volume > 0:
            mi -= 5.2 * math.log(halstead_volume)
        
        mi -= 0.23 * cyclomatic_complexity
        mi -= 16.2 * math.log(logical_lines)
        
        # Add comment bonus if available
        if comment_ratio > 0:
            mi += 50 * math.sin(math.sqrt(2.4 * comment_ratio))
        
        # Ensure MI is not negative
        mi = max(0, mi)
        
        # Determine rank
        if mi > 85:
            rank = "A"
            description = "Excellent"
        elif mi > 70:
            rank = "B"
            description = "Good"
        elif mi > 50:
            rank = "C"
            description = "Moderate"
        elif mi > 25:
            rank = "D"
            description = "Poor"
        else:
            rank = "F"
            description = "Very Poor"
        
        return {
            "index": mi,
            "rank": rank,
            "description": description,
            "components": {
                "base": 171,
                "halstead_penalty": 5.2 * math.log(halstead_volume) if halstead_volume > 0 else 0,
                "complexity_penalty": 0.23 * cyclomatic_complexity,
                "size_penalty": 16.2 * math.log(logical_lines),
                "comment_bonus": 50 * math.sin(math.sqrt(2.4 * comment_ratio)) if comment_ratio > 0 else 0
            }
        }
    
    except (ValueError, ZeroDivisionError) as e:
        return {
            "index": 0,
            "rank": "F",
            "error": str(e)
        }


def analyze_maintainability(file_path: str) -> dict:
    """Analyze maintainability metrics for a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        tree = ast.parse(source_code)
        
        # Analyze code
        analyzer = MaintainabilityAnalyzer()
        analyzer.visit(tree)
        
        # Count lines
        lines = source_code.split('\n')
        logical_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#'):
                comment_lines += 1
            else:
                logical_lines += 1
        
        # Calculate Halstead volume
        halstead_volume = calculate_halstead_volume(analyzer.operators, analyzer.operands)
        
        # Calculate ABC magnitude
        abc_magnitude = math.sqrt(
            analyzer.assignments**2 + 
            analyzer.branches**2 + 
            analyzer.conditions**2
        )
        
        # Calculate comment ratio
        total_lines = logical_lines + comment_lines
        comment_ratio = comment_lines / max(total_lines, 1)
        
        # Calculate maintainability index
        mi_result = calculate_maintainability_index(
            halstead_volume, 
            analyzer.cyclomatic_complexity, 
            logical_lines, 
            comment_ratio
        )
        
        return {
            "status": "success",
            "abc_metrics": {
                "assignments": analyzer.assignments,
                "branches": analyzer.branches,
                "conditions": analyzer.conditions,
                "magnitude": abc_magnitude
            },
            "maintainability_index": mi_result,
            "halstead_volume": halstead_volume,
            "cyclomatic_complexity": analyzer.cyclomatic_complexity,
            "lines_of_code": {
                "logical": logical_lines,
                "comments": comment_lines,
                "blank": blank_lines,
                "total": len(lines),
                "comment_ratio": comment_ratio
            },
            "structure": {
                "functions": len(analyzer.functions),
                "classes": len(analyzer.classes),
                "imports": analyzer.imports,
                "docstrings": analyzer.docstrings,
                "docstring_ratio": analyzer.docstrings / max(len(analyzer.functions) + len(analyzer.classes), 1)
            },
            "quality_indicators": {
                "avg_function_args": sum(f.get("args", 0) for f in analyzer.functions) / max(len(analyzer.functions), 1),
                "decorated_functions": sum(1 for f in analyzer.functions if f.get("decorators", 0) > 0),
                "inheritance_usage": sum(1 for c in analyzer.classes if c.get("bases", 0) > 0)
            }
        }
        
    except SyntaxError as e:
        return {
            "status": "syntax_error",
            "error": f"Syntax error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    """Main function for command line usage."""
    if len(sys.argv) != 2:
        print("Usage: python maintainability_analysis.py <model_name>")
        sys.exit(1)
    
    model_name = sys.argv[1]
    file_path = f"{model_name}.py"
    
    if not Path(file_path).exists():
        result = {
            "status": "file_not_found",
            "error": f"File {file_path} not found"
        }
    else:
        result = analyze_maintainability(file_path)
    
    # Output results as JSON for easy parsing
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
