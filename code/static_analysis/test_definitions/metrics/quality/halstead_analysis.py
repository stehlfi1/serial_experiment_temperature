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
from typing import Optional

# Handle imports for both CLI and integrated usage
try:
    from .constants import HALSTEAD_DIFFICULTY_DIVISOR, HALSTEAD_EFFORT_THRESHOLD
    from ...execution.ast_analyzer import ASTAnalyzer
except ImportError:
    # Fallback for direct CLI usage
    HALSTEAD_DIFFICULTY_DIVISOR = 3000
    HALSTEAD_EFFORT_THRESHOLD = 18
    ASTAnalyzer = None




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


def analyze_halstead_from_analyzer(analyzer) -> dict:
    """Extract Halstead metrics from a pre-populated ASTAnalyzer."""
    return calculate_halstead_metrics(analyzer.operators, analyzer.operands)


def analyze_halstead(file_path: str = None, analyzer: Optional['ASTAnalyzer'] = None) -> dict:
    """Analyze Halstead metrics for a Python file or from pre-populated analyzer."""
    if analyzer is not None:
        # Use provided analyzer
        result = analyze_halstead_from_analyzer(analyzer)
        return {
            "status": "success",
            "data": result
        }
    
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
        
        # Analyze Halstead metrics using shared analyzer
        local_analyzer = ASTAnalyzer()
        local_analyzer.reset()
        local_analyzer.visit(tree)
        
        # Use the shared analyzer data directly via the integration function
        result = analyze_halstead_from_analyzer(local_analyzer)
        return {
            "status": "success", 
            "data": result
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
        result = analyze_halstead(file_path=file_path)
    
    # Output results as JSON for easy parsing
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
