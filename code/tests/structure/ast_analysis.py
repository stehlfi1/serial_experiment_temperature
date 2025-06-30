#!/usr/bin/env python3
"""
AST Analysis Test

This script analyzes the Abstract Syntax Tree (AST) of Python code to extract
structural metrics including node counts, tree depth, and node type distribution.
Part of the structure test group for temperature research.
"""

import ast
import sys
from pathlib import Path
from typing import Dict, Any
import json


class ASTAnalyzer(ast.NodeVisitor):
    """AST visitor for collecting structural metrics."""
    
    def __init__(self):
        self.node_count = 0
        self.max_depth = 0
        self.current_depth = 0
        self.node_types = {}
        
    def visit(self, node):
        self.node_count += 1
        node_type = type(node).__name__
        self.node_types[node_type] = self.node_types.get(node_type, 0) + 1
        
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        
        self.generic_visit(node)
        self.current_depth -= 1


def analyze_ast_structure(code_content: str) -> Dict[str, Any]:
    """
    Analyze AST structure of Python code.
    
    Args:
        code_content: String containing Python source code
        
    Returns:
        Dictionary containing AST metrics
    """
    try:
        tree = ast.parse(code_content)
        analyzer = ASTAnalyzer()
        analyzer.visit(tree)
        
        return {
            "ast_node_count": analyzer.node_count,
            "ast_depth": analyzer.max_depth,
            "ast_node_types": analyzer.node_types,
            "ast_unique_node_types": len(analyzer.node_types),
            "error": None
        }
        
    except SyntaxError as e:
        return {
            "ast_node_count": 0,
            "ast_depth": 0,
            "ast_node_types": {},
            "ast_unique_node_types": 0,
            "error": f"Syntax error: {str(e)}"
        }
    except Exception as e:
        return {
            "ast_node_count": 0,
            "ast_depth": 0,
            "ast_node_types": {},
            "ast_unique_node_types": 0,
            "error": f"Analysis error: {str(e)}"
        }


def main():
    """Main entry point for AST analysis test."""
    if len(sys.argv) != 2:
        print("Usage: python ast_analysis.py <code_file_path>")
        sys.exit(1)
    
    code_file = Path(sys.argv[1])
    
    if not code_file.exists():
        result = {
            "file_exists": False,
            "error": f"File not found: {code_file}",
            "ast_node_count": 0,
            "ast_depth": 0,
            "ast_node_types": {},
            "ast_unique_node_types": 0
        }
    else:
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            result = analyze_ast_structure(code_content)
            result["file_exists"] = True
            
        except Exception as e:
            result = {
                "file_exists": True,
                "error": f"Failed to read file: {str(e)}",
                "ast_node_count": 0,
                "ast_depth": 0,
                "ast_node_types": {},
                "ast_unique_node_types": 0
            }
    
    # Output results as JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
