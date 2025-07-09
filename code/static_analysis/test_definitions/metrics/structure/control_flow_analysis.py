#!/usr/bin/env python3
"""
Control Flow Analysis Test

This script analyzes control flow constructs in Python code including loops,
conditionals, comprehensions, and exception handling.
Part of the structure test group for temperature research.
"""

import ast
import sys
from pathlib import Path
from typing import Dict, Any
import json


class ControlFlowAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing control flow constructs."""
    
    def __init__(self):
        self.loop_count = {"for": 0, "while": 0}
        self.conditional_count = {"if": 0, "try": 0, "elif": 0, "except": 0, "with": 0}
        self.comprehension_count = {"list": 0, "dict": 0, "set": 0, "generator": 0}
        self.return_count = 0
        self.raise_count = 0
        self.assert_count = 0
        self.yield_count = 0
        self.await_count = 0
        
    def visit_For(self, node):
        self.loop_count["for"] += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.loop_count["while"] += 1
        self.generic_visit(node)
    
    def visit_If(self, node):
        self.conditional_count["if"] += 1
        # Count elif branches
        current = node
        while hasattr(current, 'orelse') and current.orelse:
            if len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                self.conditional_count["elif"] += 1
                current = current.orelse[0]
            else:
                break
        self.generic_visit(node)
    
    def visit_Try(self, node):
        self.conditional_count["try"] += 1
        self.conditional_count["except"] += len(node.handlers)
        self.generic_visit(node)
    
    def visit_With(self, node):
        self.conditional_count["with"] += 1
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        self.comprehension_count["list"] += 1
        self.generic_visit(node)
    
    def visit_DictComp(self, node):
        self.comprehension_count["dict"] += 1
        self.generic_visit(node)
    
    def visit_SetComp(self, node):
        self.comprehension_count["set"] += 1
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node):
        self.comprehension_count["generator"] += 1
        self.generic_visit(node)
    
    def visit_Return(self, node):
        self.return_count += 1
        self.generic_visit(node)
    
    def visit_Raise(self, node):
        self.raise_count += 1
        self.generic_visit(node)
    
    def visit_Assert(self, node):
        self.assert_count += 1
        self.generic_visit(node)
    
    def visit_Yield(self, node):
        self.yield_count += 1
        self.generic_visit(node)
    
    def visit_YieldFrom(self, node):
        self.yield_count += 1
        self.generic_visit(node)
    
    def visit_Await(self, node):
        self.await_count += 1
        self.generic_visit(node)


def analyze_control_flow(code_content: str) -> Dict[str, Any]:
    """
    Analyze control flow constructs in Python code.
    
    Args:
        code_content: String containing Python source code
        
    Returns:
        Dictionary containing control flow metrics
    """
    try:
        tree = ast.parse(code_content)
        analyzer = ControlFlowAnalyzer()
        analyzer.visit(tree)
        
        return {
            "loop_count": analyzer.loop_count,
            "conditional_count": analyzer.conditional_count,
            "comprehension_count": analyzer.comprehension_count,
            "return_statement_count": analyzer.return_count,
            "raise_statement_count": analyzer.raise_count,
            "assert_statement_count": analyzer.assert_count,
            "yield_statement_count": analyzer.yield_count,
            "await_statement_count": analyzer.await_count,
            "total_control_structures": (
                sum(analyzer.loop_count.values()) +
                sum(analyzer.conditional_count.values()) +
                sum(analyzer.comprehension_count.values())
            ),
            "error": None
        }
        
    except SyntaxError as e:
        return {
            "loop_count": {"for": 0, "while": 0},
            "conditional_count": {"if": 0, "try": 0, "elif": 0, "except": 0, "with": 0},
            "comprehension_count": {"list": 0, "dict": 0, "set": 0, "generator": 0},
            "return_statement_count": 0,
            "raise_statement_count": 0,
            "assert_statement_count": 0,
            "yield_statement_count": 0,
            "await_statement_count": 0,
            "total_control_structures": 0,
            "error": f"Syntax error: {str(e)}"
        }
    except Exception as e:
        return {
            "loop_count": {"for": 0, "while": 0},
            "conditional_count": {"if": 0, "try": 0, "elif": 0, "except": 0, "with": 0},
            "comprehension_count": {"list": 0, "dict": 0, "set": 0, "generator": 0},
            "return_statement_count": 0,
            "raise_statement_count": 0,
            "assert_statement_count": 0,
            "yield_statement_count": 0,
            "await_statement_count": 0,
            "total_control_structures": 0,
            "error": f"Analysis error: {str(e)}"
        }


def main():
    """Main entry point for control flow analysis test."""
    if len(sys.argv) != 2:
        print("Usage: python control_flow_analysis.py <code_file_path>")
        sys.exit(1)
    
    code_file = Path(sys.argv[1])
    
    if not code_file.exists():
        result = {
            "file_exists": False,
            "error": f"File not found: {code_file}",
            "loop_count": {"for": 0, "while": 0},
            "conditional_count": {"if": 0, "try": 0, "elif": 0, "except": 0, "with": 0},
            "comprehension_count": {"list": 0, "dict": 0, "set": 0, "generator": 0},
            "return_statement_count": 0,
            "raise_statement_count": 0,
            "assert_statement_count": 0,
            "yield_statement_count": 0,
            "await_statement_count": 0,
            "total_control_structures": 0
        }
    else:
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            result = analyze_control_flow(code_content)
            result["file_exists"] = True
            
        except Exception as e:
            result = {
                "file_exists": True,
                "error": f"Failed to read file: {str(e)}",
                "loop_count": {"for": 0, "while": 0},
                "conditional_count": {"if": 0, "try": 0, "elif": 0, "except": 0, "with": 0},
                "comprehension_count": {"list": 0, "dict": 0, "set": 0, "generator": 0},
                "return_statement_count": 0,
                "raise_statement_count": 0,
                "assert_statement_count": 0,
                "yield_statement_count": 0,
                "await_statement_count": 0,
                "total_control_structures": 0
            }
    
    # Output results as JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
