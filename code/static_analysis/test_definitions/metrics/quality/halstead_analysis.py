#!/usr/bin/env python3
"""
Halstead Analysis Test

Analyzes Halstead metrics (operators, operands, volume, difficulty, effort, etc.)
for temperature research on LLM-generated code.
"""

import ast
import sys
import json
import math
from pathlib import Path
from collections import Counter


class HalsteadAnalyzer(ast.NodeVisitor):
    """Analyzes Halstead metrics in Python code."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all counters."""
        self.operators = Counter()
        self.operands = Counter()
        self.operator_instances = []
        self.operand_instances = []
    
    def visit_BinOp(self, node):
        """Binary operators (+, -, *, /, etc.)."""
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.operator_instances.append(op_name)
        self.generic_visit(node)
    
    def visit_UnaryOp(self, node):
        """Unary operators (-, +, ~, not)."""
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.operator_instances.append(op_name)
        self.generic_visit(node)
    
    def visit_Compare(self, node):
        """Comparison operators (==, !=, <, >, etc.)."""
        for op in node.ops:
            op_name = type(op).__name__
            self.operators[op_name] += 1
            self.operator_instances.append(op_name)
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        """Boolean operators (and, or)."""
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.operator_instances.append(op_name)
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        """Augmented assignment operators (+=, -=, etc.)."""
        op_name = type(node.op).__name__ + "Assign"
        self.operators[op_name] += 1
        self.operator_instances.append(op_name)
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Assignment operator."""
        self.operators["Assign"] += 1
        self.operator_instances.append("Assign")
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Function definition operator."""
        self.operators["FunctionDef"] += 1
        self.operator_instances.append("FunctionDef")
        # Function name is an operand
        self.operands[node.name] += 1
        self.operand_instances.append(node.name)
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Async function definition."""
        self.operators["AsyncFunctionDef"] += 1
        self.operator_instances.append("AsyncFunctionDef")
        self.operands[node.name] += 1
        self.operand_instances.append(node.name)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Class definition operator."""
        self.operators["ClassDef"] += 1
        self.operator_instances.append("ClassDef")
        # Class name is an operand
        self.operands[node.name] += 1
        self.operand_instances.append(node.name)
        self.generic_visit(node)
    
    def visit_If(self, node):
        """If statement operator."""
        self.operators["If"] += 1
        self.operator_instances.append("If")
        self.generic_visit(node)
    
    def visit_While(self, node):
        """While loop operator."""
        self.operators["While"] += 1
        self.operator_instances.append("While")
        self.generic_visit(node)
    
    def visit_For(self, node):
        """For loop operator."""
        self.operators["For"] += 1
        self.operator_instances.append("For")
        self.generic_visit(node)
    
    def visit_Try(self, node):
        """Try statement operator."""
        self.operators["Try"] += 1
        self.operator_instances.append("Try")
        self.generic_visit(node)
    
    def visit_With(self, node):
        """With statement operator."""
        self.operators["With"] += 1
        self.operator_instances.append("With")
        self.generic_visit(node)
    
    def visit_Return(self, node):
        """Return statement operator."""
        self.operators["Return"] += 1
        self.operator_instances.append("Return")
        self.generic_visit(node)
    
    def visit_Raise(self, node):
        """Raise statement operator."""
        self.operators["Raise"] += 1
        self.operator_instances.append("Raise")
        self.generic_visit(node)
    
    def visit_Assert(self, node):
        """Assert statement operator."""
        self.operators["Assert"] += 1
        self.operator_instances.append("Assert")
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Import statement operator."""
        self.operators["Import"] += 1
        self.operator_instances.append("Import")
        for alias in node.names:
            self.operands[alias.name] += 1
            self.operand_instances.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """ImportFrom statement operator."""
        self.operators["ImportFrom"] += 1
        self.operator_instances.append("ImportFrom")
        if node.module:
            self.operands[node.module] += 1
            self.operand_instances.append(node.module)
        for alias in node.names:
            self.operands[alias.name] += 1
            self.operand_instances.append(alias.name)
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Function call operator."""
        self.operators["Call"] += 1
        self.operator_instances.append("Call")
        self.generic_visit(node)
    
    def visit_Subscript(self, node):
        """Subscript operator (indexing)."""
        self.operators["Subscript"] += 1
        self.operator_instances.append("Subscript")
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """Attribute access operator."""
        self.operators["Attribute"] += 1
        self.operator_instances.append("Attribute")
        # Attribute name is an operand
        self.operands[node.attr] += 1
        self.operand_instances.append(node.attr)
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Variable names (operands)."""
        # Skip built-in names and keywords
        if node.id not in ['True', 'False', 'None']:
            self.operands[node.id] += 1
            self.operand_instances.append(node.id)
        self.generic_visit(node)
    
    def visit_Constant(self, node):
        """Constants (operands) - Python 3.8+."""
        if isinstance(node.value, (int, float)):
            operand = f"NUM_{node.value}"
        elif isinstance(node.value, str):
            operand = f"STR_{len(node.value)}"  # Use length to avoid huge strings
        elif isinstance(node.value, bool):
            operand = f"BOOL_{node.value}"
        else:
            operand = f"CONST_{type(node.value).__name__}"
        
        self.operands[operand] += 1
        self.operand_instances.append(operand)
        self.generic_visit(node)
    
    def visit_Str(self, node):
        """String literals (Python < 3.8)."""
        operand = f"STR_{len(node.s)}"
        self.operands[operand] += 1
        self.operand_instances.append(operand)
        self.generic_visit(node)
    
    def visit_Num(self, node):
        """Numeric literals (Python < 3.8)."""
        operand = f"NUM_{node.n}"
        self.operands[operand] += 1
        self.operand_instances.append(operand)
        self.generic_visit(node)


def calculate_halstead_metrics(operators: Counter, operands: Counter) -> dict:
    """Calculate all Halstead metrics from operator and operand counts."""
    if not operators and not operands:
        return {
            "status": "no_code",
            "error": "No operators or operands found"
        }
    
    # Basic counts
    n1 = len(operators)  # Unique operators
    n2 = len(operands)   # Unique operands
    N1 = sum(operators.values())  # Total operators
    N2 = sum(operands.values())   # Total operands
    
    # Derived metrics
    n = n1 + n2  # Vocabulary
    N = N1 + N2  # Length
    
    result = {
        "operators": {
            "unique": n1,
            "total": N1,
            "details": dict(operators.most_common())
        },
        "operands": {
            "unique": n2,
            "total": N2,
            "details": dict(operands.most_common())
        },
        "vocabulary": n,
        "length": N
    }
    
    if n > 1 and N > 0:
        # Volume
        V = N * math.log2(n)
        result["volume"] = V
        
        # Difficulty
        if n2 > 0:
            D = (n1 / 2) * (N2 / n2)
            result["difficulty"] = D
            
            # Effort
            E = D * V
            result["effort"] = E
            
            # Time (in seconds, Halstead's estimation)
            T = E / 18
            result["time"] = T
            
            # Bugs (Halstead's estimation)
            B = V / 3000
            result["bugs"] = B
            
            # Additional derived metrics
            result["level"] = 1 / D if D > 0 else 0
            result["mental_discriminations"] = V / (2 * n2) if n2 > 0 else 0
            result["intelligence_content"] = V * (2 * n2) / (n1 * N2) if n1 > 0 and N2 > 0 else 0
        else:
            result["difficulty"] = 0
            result["effort"] = 0
            result["time"] = 0
            result["bugs"] = 0
    else:
        result["volume"] = 0
        result["difficulty"] = 0
        result["effort"] = 0
        result["time"] = 0
        result["bugs"] = 0
    
    result["status"] = "success"
    return result


def analyze_halstead(file_path: str) -> dict:
    """Analyze Halstead metrics for a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        tree = ast.parse(source_code)
        
        # Analyze Halstead metrics
        analyzer = HalsteadAnalyzer()
        analyzer.visit(tree)
        
        return calculate_halstead_metrics(analyzer.operators, analyzer.operands)
        
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
        print("Usage: python halstead_analysis.py <model_name>")
        sys.exit(1)
    
    model_name = sys.argv[1]
    file_path = f"{model_name}.py"
    
    if not Path(file_path).exists():
        result = {
            "status": "file_not_found",
            "error": f"File {file_path} not found"
        }
    else:
        result = analyze_halstead(file_path)
    
    # Output results as JSON for easy parsing
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
