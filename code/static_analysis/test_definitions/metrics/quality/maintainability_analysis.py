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

# Import shared analyzer integration
try:
    from .halstead_analysis import analyze_halstead_from_analyzer
    from ...execution.ast_analyzer import ASTAnalyzer
except ImportError:
    # Fallback for CLI usage
    import sys
    import importlib.util
    from pathlib import Path
    
    halstead_path = Path(__file__).parent / "halstead_analysis.py"
    spec = importlib.util.spec_from_file_location("halstead_analysis", halstead_path)
    halstead_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(halstead_module)
    analyze_halstead_from_analyzer = halstead_module.analyze_halstead_from_analyzer
    
    ast_analyzer_path = Path(__file__).parent.parent.parent.parent / "execution" / "ast_analyzer.py"
    spec = importlib.util.spec_from_file_location("ast_analyzer", ast_analyzer_path)
    ast_analyzer_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ast_analyzer_module)
    ASTAnalyzer = ast_analyzer_module.ASTAnalyzer




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


def analyze_maintainability_from_analyzer(analyzer, source_code: str) -> dict:
    """Analyze maintainability metrics from a pre-populated ASTAnalyzer."""
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
    
    # Calculate Halstead volume using shared analyzer
    halstead_result = analyze_halstead_from_analyzer(analyzer)
    halstead_volume = halstead_result.get("volume", 0)
    
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
        "data": {
            "maintainability_index": mi_result.get("index", 0),
            "maintainability_rank": mi_result.get("rank", "F"),
            "abc_assignment_count": analyzer.assignments,
            "abc_branch_count": analyzer.branches,
            "abc_condition_count": analyzer.conditions,
            "abc_magnitude": abc_magnitude,
            "halstead_volume": halstead_volume,
            "cyclomatic_complexity": analyzer.cyclomatic_complexity,
            "logical_lines": logical_lines,
            "comment_ratio": comment_ratio
        }
    }


def analyze_maintainability(file_path: str) -> dict:
    """Analyze maintainability metrics for a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        tree = ast.parse(source_code)
        
        # Use shared analyzer instead of duplicate MaintainabilityAnalyzer
        analyzer = ASTAnalyzer()
        analyzer.reset()
        analyzer.visit(tree)
        
        # Use the shared analyzer integration function
        result = analyze_maintainability_from_analyzer(analyzer, source_code)
        
        # Convert to legacy format for compatibility
        data = result["data"]
        return {
            "status": "success",
            "abc_metrics": {
                "assignments": data["abc_assignment_count"],
                "branches": data["abc_branch_count"],
                "conditions": data["abc_condition_count"],
                "magnitude": data["abc_magnitude"]
            },
            "maintainability_index": {
                "index": data["maintainability_index"],
                "rank": data["maintainability_rank"]
            },
            "halstead_volume": data["halstead_volume"],
            "cyclomatic_complexity": data["cyclomatic_complexity"],
            "lines_of_code": {
                "logical": data["logical_lines"],
                "comments": int(data["logical_lines"] * data["comment_ratio"]),
                "blank": 0,  # Not tracked in shared analyzer version
                "total": data["logical_lines"] + int(data["logical_lines"] * data["comment_ratio"]),
                "comment_ratio": data["comment_ratio"]
            },
            "structure": {
                "functions": len(analyzer.functions),
                "classes": len(analyzer.classes),
                "imports": len(analyzer.imports) + len(analyzer.from_imports),
                "docstrings": analyzer.docstring_count,
                "docstring_ratio": analyzer.docstring_count / max(len(analyzer.functions) + len(analyzer.classes), 1)
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
