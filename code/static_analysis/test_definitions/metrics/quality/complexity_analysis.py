#!/usr/bin/env python3
"""
Complexity Analysis Test

Analyzes cyclomatic complexity, cognitive complexity, and nesting depth
for temperature research on LLM-generated code.
"""

import ast
import sys
import json
from pathlib import Path

from .constants import (
    SIMPLE_COMPLEXITY_THRESHOLD,
    COMPLEX_COMPLEXITY_THRESHOLD, 
    VERY_COMPLEX_COMPLEXITY_THRESHOLD
)


class ComplexityAnalyzer(ast.NodeVisitor):
    """Analyzes complexity metrics in Python code."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all counters."""
        self.cyclomatic_complexity = 1  # Start with 1
        self.function_complexities = []
        self.current_function_complexity = 1
        self.nesting_depth = 0
        self.max_nesting_depth = 0
        self.function_nesting_depths = []
        self.current_max_nesting = 0
        
        # For cognitive complexity
        self.cognitive_complexity = 0
        self.function_cognitive_complexities = []
        self.current_cognitive = 0
        self.cognitive_nesting_level = 0
    
    def visit_FunctionDef(self, node):
        """Analyze function complexity."""
        # Save current state
        old_cc = self.current_function_complexity
        old_nesting = self.current_max_nesting
        old_cognitive = self.current_cognitive
        old_cog_nesting = self.cognitive_nesting_level
        
        # Reset for this function
        self.current_function_complexity = 1
        self.current_max_nesting = 0
        self.current_cognitive = 0
        self.cognitive_nesting_level = 0
        
        # Visit function body
        self.generic_visit(node)
        
        # Store function metrics
        self.function_complexities.append(self.current_function_complexity)
        self.function_nesting_depths.append(self.current_max_nesting)
        self.function_cognitive_complexities.append(self.current_cognitive)
        
        # Restore global state
        self.current_function_complexity = old_cc
        self.current_max_nesting = old_nesting
        self.current_cognitive = old_cognitive
        self.cognitive_nesting_level = old_cog_nesting
    
    def visit_AsyncFunctionDef(self, node):
        """Handle async functions same as regular functions."""
        self.visit_FunctionDef(node)
    
    def visit_If(self, node):
        """Handle if statements."""
        self._add_complexity(1)
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_While(self, node):
        """Handle while loops."""
        self._add_complexity(1)
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_For(self, node):
        """Handle for loops."""
        self._add_complexity(1)
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_Try(self, node):
        """Handle try-except blocks."""
        # Each except handler adds complexity
        complexity_increase = len(node.handlers)
        if node.orelse:  # else clause
            complexity_increase += 1
        if node.finalbody:  # finally clause
            complexity_increase += 1
        
        self._add_complexity(complexity_increase)
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_With(self, node):
        """Handle with statements."""
        self._add_complexity(1)
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_ExceptHandler(self, node):
        """Handle except clauses."""
        self._add_complexity(1, cognitive_bonus=True)
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        """Handle boolean operators (and, or)."""
        # Each additional operand adds complexity
        complexity_increase = len(node.values) - 1
        self._add_complexity(complexity_increase)
        self.generic_visit(node)
    
    def _add_complexity(self, amount, cognitive_bonus=False):
        """Add complexity to both cyclomatic and cognitive measures."""
        self.current_function_complexity += amount
        self.cyclomatic_complexity += amount
        
        # Cognitive complexity includes nesting bonus
        cognitive_increase = amount
        if cognitive_bonus or self.cognitive_nesting_level > 0:
            cognitive_increase += self.cognitive_nesting_level
        
        self.current_cognitive += cognitive_increase
        self.cognitive_complexity += cognitive_increase
    
    def _enter_block(self):
        """Enter a nested block."""
        self.nesting_depth += 1
        self.cognitive_nesting_level += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.nesting_depth)
        self.current_max_nesting = max(self.current_max_nesting, self.nesting_depth)
    
    def _exit_block(self):
        """Exit a nested block."""
        self.nesting_depth -= 1
        self.cognitive_nesting_level -= 1


def analyze_complexity(file_path: str) -> dict:
    """Analyze complexity metrics for a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        tree = ast.parse(source_code)
        
        # Analyze complexity
        analyzer = ComplexityAnalyzer()
        analyzer.visit(tree)
        
        # Calculate averages
        avg_function_complexity = 0
        avg_function_nesting = 0
        avg_cognitive_complexity = 0
        
        if analyzer.function_complexities:
            avg_function_complexity = sum(analyzer.function_complexities) / len(analyzer.function_complexities)
        
        if analyzer.function_nesting_depths:
            avg_function_nesting = sum(analyzer.function_nesting_depths) / len(analyzer.function_nesting_depths)
        
        if analyzer.function_cognitive_complexities:
            avg_cognitive_complexity = sum(analyzer.function_cognitive_complexities) / len(analyzer.function_cognitive_complexities)
        
        # Calculate complexity distribution
        simple_functions = sum(1 for cc in analyzer.function_complexities if cc <= 5)
        complex_functions = sum(1 for cc in analyzer.function_complexities if cc > 10)
        very_complex_functions = sum(1 for cc in analyzer.function_complexities if cc > 20)
        total_functions = len(analyzer.function_complexities)
        
        return {
            "status": "success",
            "cyclomatic_complexity": {
                "total": analyzer.cyclomatic_complexity,
                "per_function": analyzer.function_complexities,
                "average": avg_function_complexity,
                "max": max(analyzer.function_complexities) if analyzer.function_complexities else 0,
                "distribution": {
                    "simple": simple_functions,
                    "complex": complex_functions,
                    "very_complex": very_complex_functions,
                    "simple_ratio": simple_functions / max(total_functions, 1),
                    "complex_ratio": complex_functions / max(total_functions, 1),
                    "very_complex_ratio": very_complex_functions / max(total_functions, 1)
                }
            },
            "cognitive_complexity": {
                "total": analyzer.cognitive_complexity,
                "per_function": analyzer.function_cognitive_complexities,
                "average": avg_cognitive_complexity,
                "max": max(analyzer.function_cognitive_complexities) if analyzer.function_cognitive_complexities else 0
            },
            "nesting_depth": {
                "max_overall": analyzer.max_nesting_depth,
                "per_function": analyzer.function_nesting_depths,
                "average": avg_function_nesting,
                "max_function": max(analyzer.function_nesting_depths) if analyzer.function_nesting_depths else 0
            },
            "function_count": len(analyzer.function_complexities)
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
        print("Usage: python complexity_analysis.py <model_name>")
        sys.exit(1)
    
    model_name = sys.argv[1]
    file_path = f"{model_name}.py"
    
    if not Path(file_path).exists():
        result = {
            "status": "file_not_found",
            "error": f"File {file_path} not found"
        }
    else:
        result = analyze_complexity(file_path)
    
    # Output results as JSON for easy parsing
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
