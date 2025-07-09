#!/usr/bin/env python3
"""
Code Style Analysis Test

Analyzes code style and quality patterns for temperature research on LLM-generated code.
"""

import ast
import sys
import json
import re
from pathlib import Path
from collections import Counter, defaultdict


class StyleAnalyzer(ast.NodeVisitor):
    """Analyzes code style and quality patterns."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all counters."""
        # Naming patterns
        self.identifiers = []
        self.function_names = []
        self.class_names = []
        self.variable_names = []
        self.constant_names = []
        
        # Code patterns
        self.magic_numbers = []
        self.string_literals = []
        self.long_functions = []
        self.complex_expressions = []
        
        # Style metrics
        self.indentation_levels = []
        self.line_lengths = []
        
        # Quality indicators
        self.error_handling = {"try_blocks": 0, "except_handlers": 0, "finally_blocks": 0}
        self.documentation = {"functions_with_docstrings": 0, "classes_with_docstrings": 0}
        self.best_practices = {"list_comprehensions": 0, "dict_comprehensions": 0, "generators": 0}
        
        # Code smells
        self.code_smells = {
            "long_parameter_lists": 0,
            "deep_nesting": 0,
            "large_classes": 0,
            "duplicate_code_patterns": 0
        }
        
        # Current context
        self.current_function = None
        self.current_class = None
        self.nesting_level = 0
        self.max_nesting = 0
    
    def visit_FunctionDef(self, node):
        """Analyze function definitions."""
        old_function = self.current_function
        old_nesting = self.max_nesting
        self.current_function = node.name
        self.max_nesting = 0
        
        # Analyze function name
        self.function_names.append(node.name)
        self.identifiers.append(("function", node.name))
        
        # Check parameter count (code smell)
        param_count = len(node.args.args) + len(node.args.kwonlyargs)
        if param_count > 5:  # Arbitrary threshold
            self.code_smells["long_parameter_lists"] += 1
        
        # Check for docstring
        docstring = ast.get_docstring(node)
        if docstring:
            self.documentation["functions_with_docstrings"] += 1
        
        # Calculate function length
        if hasattr(node, 'end_lineno') and node.end_lineno:
            func_length = node.end_lineno - node.lineno
            if func_length > 50:  # Arbitrary threshold
                self.long_functions.append({
                    "name": node.name,
                    "length": func_length,
                    "start_line": node.lineno
                })
        
        self.generic_visit(node)
        
        # Check nesting in this function
        if self.max_nesting > 4:  # Arbitrary threshold
            self.code_smells["deep_nesting"] += 1
        
        self.current_function = old_function
        self.max_nesting = max(old_nesting, self.max_nesting)
    
    def visit_AsyncFunctionDef(self, node):
        """Handle async functions."""
        self.visit_FunctionDef(node)
    
    def visit_ClassDef(self, node):
        """Analyze class definitions."""
        old_class = self.current_class
        self.current_class = node.name
        
        # Analyze class name
        self.class_names.append(node.name)
        self.identifiers.append(("class", node.name))
        
        # Check for docstring
        docstring = ast.get_docstring(node)
        if docstring:
            self.documentation["classes_with_docstrings"] += 1
        
        self.generic_visit(node)
        
        # Check class size (count methods)
        method_count = sum(1 for child in ast.walk(node) if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)))
        if method_count > 20:  # Arbitrary threshold
            self.code_smells["large_classes"] += 1
        
        self.current_class = old_class
    
    def visit_Name(self, node):
        """Analyze variable names."""
        if isinstance(node.ctx, ast.Store):  # Variable assignment
            self.variable_names.append(node.id)
            self.identifiers.append(("variable", node.id))
            
            # Check if it looks like a constant (all uppercase)
            if node.id.isupper() and len(node.id) > 1:
                self.constant_names.append(node.id)
        
        self.generic_visit(node)
    
    def visit_Constant(self, node):
        """Analyze literals."""
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            # Check for magic numbers (not 0, 1, -1)
            if node.value not in [0, 1, -1] and not (0 < node.value < 100 and node.value == int(node.value)):
                self.magic_numbers.append(node.value)
        
        elif isinstance(node.value, str) and len(node.value) > 50:
            # Long string literals
            self.string_literals.append({
                "length": len(node.value),
                "preview": node.value[:50] + "..." if len(node.value) > 50 else node.value
            })
        
        self.generic_visit(node)
    
    def visit_Num(self, node):
        """Handle numeric literals in older Python versions."""
        if node.n not in [0, 1, -1] and not (0 < node.n < 100 and node.n == int(node.n)):
            self.magic_numbers.append(node.n)
        self.generic_visit(node)
    
    def visit_Str(self, node):
        """Handle string literals in older Python versions."""
        if len(node.s) > 50:
            self.string_literals.append({
                "length": len(node.s),
                "preview": node.s[:50] + "..." if len(node.s) > 50 else node.s
            })
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        """Count list comprehensions (good practice)."""
        self.best_practices["list_comprehensions"] += 1
        self.generic_visit(node)
    
    def visit_DictComp(self, node):
        """Count dictionary comprehensions (good practice)."""
        self.best_practices["dict_comprehensions"] += 1
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node):
        """Count generator expressions (good practice)."""
        self.best_practices["generators"] += 1
        self.generic_visit(node)
    
    def visit_Try(self, node):
        """Analyze error handling."""
        self.error_handling["try_blocks"] += 1
        if node.finalbody:
            self.error_handling["finally_blocks"] += 1
        
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_ExceptHandler(self, node):
        """Count exception handlers."""
        self.error_handling["except_handlers"] += 1
        self.generic_visit(node)
    
    def visit_If(self, node):
        """Track nesting in if statements."""
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_While(self, node):
        """Track nesting in while loops."""
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_For(self, node):
        """Track nesting in for loops."""
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_With(self, node):
        """Track nesting in with statements."""
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def _enter_block(self):
        """Enter a nested block."""
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
    
    def _exit_block(self):
        """Exit a nested block."""
        self.nesting_level -= 1


def analyze_naming_conventions(identifiers: list) -> dict:
    """Analyze naming convention compliance."""
    patterns = {
        "snake_case": re.compile(r'^[a-z_][a-z0-9_]*$'),
        "camelCase": re.compile(r'^[a-z][a-zA-Z0-9]*$'),
        "PascalCase": re.compile(r'^[A-Z][a-zA-Z0-9]*$'),
        "UPPER_CASE": re.compile(r'^[A-Z_][A-Z0-9_]*$'),
        "mixed_case": re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$')
    }
    
    results = {pattern: {"count": 0, "examples": []} for pattern in patterns}
    results["total"] = len(identifiers)
    results["non_conforming"] = {"count": 0, "examples": []}
    
    convention_counts = Counter()
    
    for id_type, name in identifiers:
        matched = False
        for pattern_name, pattern in patterns.items():
            if pattern.match(name):
                results[pattern_name]["count"] += 1
                if len(results[pattern_name]["examples"]) < 5:
                    results[pattern_name]["examples"].append(f"{name} ({id_type})")
                convention_counts[pattern_name] += 1
                matched = True
                break
        
        if not matched:
            results["non_conforming"]["count"] += 1
            if len(results["non_conforming"]["examples"]) < 5:
                results["non_conforming"]["examples"].append(f"{name} ({id_type})")
    
    # Determine dominant convention
    if convention_counts:
        dominant_convention = convention_counts.most_common(1)[0][0]
        consistency_score = convention_counts[dominant_convention] / len(identifiers)
    else:
        dominant_convention = "none"
        consistency_score = 0
    
    results["dominant_convention"] = dominant_convention
    results["consistency_score"] = consistency_score
    
    # Python-specific scoring
    function_vars_snake = sum(1 for id_type, name in identifiers 
                             if id_type in ["function", "variable"] and patterns["snake_case"].match(name))
    classes_pascal = sum(1 for id_type, name in identifiers 
                        if id_type == "class" and patterns["PascalCase"].match(name))
    
    total_functions_vars = sum(1 for id_type, _ in identifiers if id_type in ["function", "variable"])
    total_classes = sum(1 for id_type, _ in identifiers if id_type == "class")
    
    python_compliance = 0
    if total_functions_vars > 0:
        python_compliance += (function_vars_snake / total_functions_vars) * 0.7
    if total_classes > 0:
        python_compliance += (classes_pascal / total_classes) * 0.3
    
    results["python_compliance_score"] = python_compliance
    
    return results


def analyze_code_quality(source_code: str) -> dict:
    """Analyze overall code quality indicators."""
    lines = source_code.split('\n')
    
    quality_metrics = {
        "line_count": len(lines),
        "avg_line_length": sum(len(line) for line in lines) / max(len(lines), 1),
        "max_line_length": max(len(line) for line in lines) if lines else 0,
        "long_lines": sum(1 for line in lines if len(line) > 80),
        "very_long_lines": sum(1 for line in lines if len(line) > 120),
        "empty_lines": sum(1 for line in lines if not line.strip()),
        "comment_lines": sum(1 for line in lines if line.strip().startswith('#'))
    }
    
    # Code density
    non_empty_lines = len(lines) - quality_metrics["empty_lines"]
    if non_empty_lines > 0:
        quality_metrics["comment_ratio"] = quality_metrics["comment_lines"] / non_empty_lines
        quality_metrics["code_density"] = (non_empty_lines - quality_metrics["comment_lines"]) / non_empty_lines
    else:
        quality_metrics["comment_ratio"] = 0
        quality_metrics["code_density"] = 0
    
    return quality_metrics


def calculate_style_score(naming_result: dict, quality_metrics: dict, 
                         analyzer: StyleAnalyzer, total_functions: int, total_classes: int) -> dict:
    """Calculate overall style score."""
    score_components = {}
    
    # Naming convention score (30%)
    naming_score = naming_result["python_compliance_score"]
    score_components["naming"] = naming_score * 0.3
    
    # Documentation score (20%)
    total_documentable = total_functions + total_classes
    if total_documentable > 0:
        doc_score = (analyzer.documentation["functions_with_docstrings"] + 
                    analyzer.documentation["classes_with_docstrings"]) / total_documentable
    else:
        doc_score = 0
    score_components["documentation"] = doc_score * 0.2
    
    # Code complexity score (25%)
    complexity_penalties = (
        analyzer.code_smells["long_parameter_lists"] * 0.1 +
        analyzer.code_smells["deep_nesting"] * 0.15 +
        analyzer.code_smells["large_classes"] * 0.1 +
        len(analyzer.long_functions) * 0.05
    )
    complexity_score = max(0, 1 - complexity_penalties)
    score_components["complexity"] = complexity_score * 0.25
    
    # Best practices score (15%)
    best_practices_count = sum(analyzer.best_practices.values())
    total_opportunities = max(1, total_functions + len(analyzer.variable_names))
    practices_score = min(1, best_practices_count / total_opportunities)
    score_components["best_practices"] = practices_score * 0.15
    
    # Error handling score (10%)
    if analyzer.error_handling["try_blocks"] > 0:
        error_score = min(1, analyzer.error_handling["except_handlers"] / analyzer.error_handling["try_blocks"])
    else:
        error_score = 0.5  # Neutral score if no error handling
    score_components["error_handling"] = error_score * 0.1
    
    total_score = sum(score_components.values())
    
    return {
        "total_score": total_score,
        "grade": "A" if total_score >= 0.9 else "B" if total_score >= 0.7 else "C" if total_score >= 0.5 else "D",
        "components": score_components
    }


def analyze_style(file_path: str) -> dict:
    """Analyze code style for a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        tree = ast.parse(source_code)
        
        # Analyze code
        analyzer = StyleAnalyzer()
        analyzer.visit(tree)
        
        # Analyze naming conventions
        naming_result = analyze_naming_conventions(analyzer.identifiers)
        
        # Analyze code quality
        quality_metrics = analyze_code_quality(source_code)
        
        # Calculate style score
        style_score = calculate_style_score(
            naming_result, quality_metrics, analyzer,
            len(analyzer.function_names), len(analyzer.class_names)
        )
        
        return {
            "status": "success",
            "naming_conventions": naming_result,
            "code_quality": quality_metrics,
            "code_smells": analyzer.code_smells,
            "best_practices": analyzer.best_practices,
            "documentation": analyzer.documentation,
            "error_handling": analyzer.error_handling,
            "magic_numbers": {
                "count": len(analyzer.magic_numbers),
                "examples": list(set(analyzer.magic_numbers))[:10]
            },
            "long_functions": analyzer.long_functions,
            "style_score": style_score,
            "summary": {
                "total_identifiers": len(analyzer.identifiers),
                "functions": len(analyzer.function_names),
                "classes": len(analyzer.class_names),
                "variables": len(analyzer.variable_names),
                "constants": len(analyzer.constant_names)
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
        print("Usage: python code_style_analysis.py <model_name>")
        sys.exit(1)
    
    model_name = sys.argv[1]
    file_path = f"{model_name}.py"
    
    if not Path(file_path).exists():
        result = {
            "status": "file_not_found",
            "error": f"File {file_path} not found"
        }
    else:
        result = analyze_style(file_path)
    
    # Output results as JSON for easy parsing
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
