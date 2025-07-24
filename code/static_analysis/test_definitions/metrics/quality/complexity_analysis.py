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
from typing import Optional


def analyze_complexity_from_analyzer(analyzer) -> dict:
    """Extract complexity metrics from a pre-populated ASTAnalyzer."""
    # Calculate averages
    avg_function_complexity = 0
    avg_function_nesting = 0
    avg_cognitive_complexity = 0
    
    if analyzer.function_complexities:
        avg_function_complexity = sum(analyzer.function_complexities) / len(analyzer.function_complexities)
    
    if analyzer.nesting_depths:
        avg_function_nesting = sum(analyzer.nesting_depths) / len(analyzer.nesting_depths)
        
    # Use proper cognitive complexity from shared analyzer
    if analyzer.function_cognitive_complexities:
        avg_cognitive_complexity = sum(analyzer.function_cognitive_complexities) / len(analyzer.function_cognitive_complexities)
    
    # Calculate complexity distribution
    simple_functions = sum(1 for cc in analyzer.function_complexities if cc <= 5)
    complex_functions = sum(1 for cc in analyzer.function_complexities if cc > 10)
    very_complex_functions = sum(1 for cc in analyzer.function_complexities if cc > 20)
    total_functions = len(analyzer.function_complexities)
    
    return {
        "status": "success",
        "data": {
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
                "max_overall": analyzer.max_nesting,
                "per_function": analyzer.nesting_depths,
                "average": avg_function_nesting,
                "max_function": max(analyzer.nesting_depths) if analyzer.nesting_depths else 0
            },
            "function_count": len(analyzer.function_complexities)
        }
    }


def analyze_complexity(file_path: str = None, analyzer: Optional['ASTAnalyzer'] = None) -> dict:
    """Analyze complexity metrics for a Python file or from pre-populated analyzer."""
    if analyzer is not None:
        # Use provided analyzer
        return analyze_complexity_from_analyzer(analyzer)
    
    # Parse file and create own analyzer
    try:
        # Import shared analyzer for CLI usage
        try:
            from ...execution.ast_analyzer import ASTAnalyzer
        except ImportError:
            # Fallback for CLI usage - import directly from file path
            import sys
            import importlib.util
            from pathlib import Path
            
            ast_analyzer_path = Path(__file__).parent.parent.parent.parent / "execution" / "ast_analyzer.py"
            spec = importlib.util.spec_from_file_location("ast_analyzer", ast_analyzer_path)
            ast_analyzer_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ast_analyzer_module)
            ASTAnalyzer = ast_analyzer_module.ASTAnalyzer
        
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        tree = ast.parse(source_code)
        
        # Analyze complexity using shared analyzer
        local_analyzer = ASTAnalyzer()
        local_analyzer.reset()
        local_analyzer.visit(tree)
        
        # Use the shared analyzer data directly via the integration function
        return analyze_complexity_from_analyzer(local_analyzer)
        
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
