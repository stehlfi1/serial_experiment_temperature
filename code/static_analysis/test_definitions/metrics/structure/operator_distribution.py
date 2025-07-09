#!/usr/bin/env python3
"""
Operator Distribution Analysis Test

This script analyzes the distribution and usage of different operators in Python code
including arithmetic, comparison, logical, and other operators.
Part of the structure test group for temperature research.
"""

import ast
import sys
from pathlib import Path
from typing import Dict, Any
import json


class OperatorAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing operator usage patterns."""
    
    def __init__(self):
        # Binary operators
        self.binary_ops = {
            'Add': 0, 'Sub': 0, 'Mult': 0, 'Div': 0, 'FloorDiv': 0, 'Mod': 0, 'Pow': 0,
            'LShift': 0, 'RShift': 0, 'BitOr': 0, 'BitXor': 0, 'BitAnd': 0,
            'MatMult': 0  # @ operator for matrix multiplication
        }
        
        # Comparison operators
        self.compare_ops = {
            'Eq': 0, 'NotEq': 0, 'Lt': 0, 'LtE': 0, 'Gt': 0, 'GtE': 0,
            'Is': 0, 'IsNot': 0, 'In': 0, 'NotIn': 0
        }
        
        # Boolean operators
        self.bool_ops = {
            'And': 0, 'Or': 0
        }
        
        # Unary operators
        self.unary_ops = {
            'UAdd': 0, 'USub': 0, 'Not': 0, 'Invert': 0
        }
        
        # Augmented assignment operators
        self.aug_assign_ops = {
            'Add': 0, 'Sub': 0, 'Mult': 0, 'Div': 0, 'FloorDiv': 0, 'Mod': 0, 'Pow': 0,
            'LShift': 0, 'RShift': 0, 'BitOr': 0, 'BitXor': 0, 'BitAnd': 0, 'MatMult': 0
        }
        
        # Literal counts
        self.string_literals = 0
        self.number_literals = 0
        self.boolean_literals = 0
        self.none_literals = 0
        
        # Complex expressions
        self.nested_expressions = 0
        self.max_expression_depth = 0
        self.current_depth = 0
    
    def visit_BinOp(self, node):
        op_name = type(node.op).__name__
        if op_name in self.binary_ops:
            self.binary_ops[op_name] += 1
        
        self.current_depth += 1
        self.max_expression_depth = max(self.max_expression_depth, self.current_depth)
        
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_Compare(self, node):
        for op in node.ops:
            op_name = type(op).__name__
            if op_name in self.compare_ops:
                self.compare_ops[op_name] += 1
        
        self.current_depth += 1
        self.max_expression_depth = max(self.max_expression_depth, self.current_depth)
        
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_BoolOp(self, node):
        op_name = type(node.op).__name__
        if op_name in self.bool_ops:
            self.bool_ops[op_name] += 1
        
        self.current_depth += 1
        self.max_expression_depth = max(self.max_expression_depth, self.current_depth)
        
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_UnaryOp(self, node):
        op_name = type(node.op).__name__
        if op_name in self.unary_ops:
            self.unary_ops[op_name] += 1
        
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        op_name = type(node.op).__name__
        if op_name in self.aug_assign_ops:
            self.aug_assign_ops[op_name] += 1
        
        self.generic_visit(node)
    
    def visit_Constant(self, node):
        if isinstance(node.value, str):
            self.string_literals += 1
        elif isinstance(node.value, (int, float, complex)):
            self.number_literals += 1
        elif isinstance(node.value, bool):
            self.boolean_literals += 1
        elif node.value is None:
            self.none_literals += 1
        
        self.generic_visit(node)
    
    # Legacy support for older Python versions
    def visit_Str(self, node):
        self.string_literals += 1
        self.generic_visit(node)
    
    def visit_Num(self, node):
        self.number_literals += 1
        self.generic_visit(node)
    
    def visit_NameConstant(self, node):
        if isinstance(node.value, bool):
            self.boolean_literals += 1
        elif node.value is None:
            self.none_literals += 1
        self.generic_visit(node)


def analyze_operator_distribution(code_content: str) -> Dict[str, Any]:
    """
    Analyze operator distribution in Python code.
    
    Args:
        code_content: String containing Python source code
        
    Returns:
        Dictionary containing operator distribution metrics
    """
    try:
        tree = ast.parse(code_content)
        analyzer = OperatorAnalyzer()
        analyzer.visit(tree)
        
        # Calculate totals and percentages
        total_binary_ops = sum(analyzer.binary_ops.values())
        total_compare_ops = sum(analyzer.compare_ops.values())
        total_bool_ops = sum(analyzer.bool_ops.values())
        total_unary_ops = sum(analyzer.unary_ops.values())
        total_aug_assign_ops = sum(analyzer.aug_assign_ops.values())
        total_operators = (total_binary_ops + total_compare_ops + 
                          total_bool_ops + total_unary_ops + total_aug_assign_ops)
        
        total_literals = (analyzer.string_literals + analyzer.number_literals + 
                         analyzer.boolean_literals + analyzer.none_literals)
        
        # Calculate operator complexity score
        complexity_weights = {
            'arithmetic': 1,    # +, -, *, /, etc.
            'bitwise': 2,       # &, |, ^, <<, >>
            'comparison': 1,    # ==, !=, <, etc.
            'logical': 1,       # and, or
            'augmented': 1.5,   # +=, -=, etc.
        }
        
        arithmetic_ops = (analyzer.binary_ops['Add'] + analyzer.binary_ops['Sub'] + 
                         analyzer.binary_ops['Mult'] + analyzer.binary_ops['Div'] + 
                         analyzer.binary_ops['FloorDiv'] + analyzer.binary_ops['Mod'] + 
                         analyzer.binary_ops['Pow'])
        
        bitwise_ops = (analyzer.binary_ops['BitAnd'] + analyzer.binary_ops['BitOr'] + 
                      analyzer.binary_ops['BitXor'] + analyzer.binary_ops['LShift'] + 
                      analyzer.binary_ops['RShift'])
        
        operator_complexity_score = (
            arithmetic_ops * complexity_weights['arithmetic'] +
            bitwise_ops * complexity_weights['bitwise'] +
            total_compare_ops * complexity_weights['comparison'] +
            total_bool_ops * complexity_weights['logical'] +
            total_aug_assign_ops * complexity_weights['augmented']
        )
        
        return {
            "operator_distribution": {
                "binary_operators": analyzer.binary_ops,
                "comparison_operators": analyzer.compare_ops,
                "boolean_operators": analyzer.bool_ops,
                "unary_operators": analyzer.unary_ops,
                "augmented_assignment": analyzer.aug_assign_ops
            },
            "operator_totals": {
                "total_binary_ops": total_binary_ops,
                "total_comparison_ops": total_compare_ops,
                "total_boolean_ops": total_bool_ops,
                "total_unary_ops": total_unary_ops,
                "total_augmented_assignment": total_aug_assign_ops,
                "total_operators": total_operators
            },
            "literal_distribution": {
                "string_literal_count": analyzer.string_literals,
                "number_literal_count": analyzer.number_literals,
                "boolean_literal_count": analyzer.boolean_literals,
                "none_literal_count": analyzer.none_literals,
                "total_literals": total_literals
            },
            "expression_complexity": {
                "max_expression_depth": analyzer.max_expression_depth,
                "operator_complexity_score": operator_complexity_score,
                "operators_per_literal": total_operators / total_literals if total_literals > 0 else 0
            },
            "operator_categories": {
                "arithmetic_operators": arithmetic_ops,
                "bitwise_operators": bitwise_ops,
                "logical_operators": total_bool_ops + total_compare_ops,
                "assignment_operators": total_aug_assign_ops
            },
            "operator_diversity": {
                "unique_binary_ops": len([op for op, count in analyzer.binary_ops.items() if count > 0]),
                "unique_comparison_ops": len([op for op, count in analyzer.compare_ops.items() if count > 0]),
                "unique_boolean_ops": len([op for op, count in analyzer.bool_ops.items() if count > 0]),
                "unique_unary_ops": len([op for op, count in analyzer.unary_ops.items() if count > 0]),
                "total_unique_operators": len([
                    op for ops_dict in [analyzer.binary_ops, analyzer.compare_ops, 
                                       analyzer.bool_ops, analyzer.unary_ops, analyzer.aug_assign_ops]
                    for op, count in ops_dict.items() if count > 0
                ])
            },
            "error": None
        }
        
    except SyntaxError as e:
        return _get_empty_operator_result(f"Syntax error: {str(e)}")
    except Exception as e:
        return _get_empty_operator_result(f"Analysis error: {str(e)}")


def _get_empty_operator_result(error_msg: str) -> Dict[str, Any]:
    """Return empty result structure with error message."""
    return {
        "operator_distribution": {
            "binary_operators": {op: 0 for op in ['Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod', 'Pow', 'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd', 'MatMult']},
            "comparison_operators": {op: 0 for op in ['Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE', 'Is', 'IsNot', 'In', 'NotIn']},
            "boolean_operators": {'And': 0, 'Or': 0},
            "unary_operators": {'UAdd': 0, 'USub': 0, 'Not': 0, 'Invert': 0},
            "augmented_assignment": {op: 0 for op in ['Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod', 'Pow', 'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd', 'MatMult']}
        },
        "operator_totals": {
            "total_binary_ops": 0,
            "total_comparison_ops": 0,
            "total_boolean_ops": 0,
            "total_unary_ops": 0,
            "total_augmented_assignment": 0,
            "total_operators": 0
        },
        "literal_distribution": {
            "string_literal_count": 0,
            "number_literal_count": 0,
            "boolean_literal_count": 0,
            "none_literal_count": 0,
            "total_literals": 0
        },
        "expression_complexity": {
            "max_expression_depth": 0,
            "operator_complexity_score": 0,
            "operators_per_literal": 0
        },
        "operator_categories": {
            "arithmetic_operators": 0,
            "bitwise_operators": 0,
            "logical_operators": 0,
            "assignment_operators": 0
        },
        "operator_diversity": {
            "unique_binary_ops": 0,
            "unique_comparison_ops": 0,
            "unique_boolean_ops": 0,
            "unique_unary_ops": 0,
            "total_unique_operators": 0
        },
        "error": error_msg
    }


def main():
    """Main entry point for operator distribution analysis test."""
    if len(sys.argv) != 2:
        print("Usage: python operator_distribution.py <code_file_path>")
        sys.exit(1)
    
    code_file = Path(sys.argv[1])
    
    if not code_file.exists():
        result = _get_empty_operator_result(f"File not found: {code_file}")
        result["file_exists"] = False
    else:
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            result = analyze_operator_distribution(code_content)
            result["file_exists"] = True
            
        except Exception as e:
            result = _get_empty_operator_result(f"Failed to read file: {str(e)}")
            result["file_exists"] = True
    
    # Output results as JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
