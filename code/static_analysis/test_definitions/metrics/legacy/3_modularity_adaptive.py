"""
Adaptive modularity test for dry runs
Output: Modularity score based on code structure analysis.
"""

import ast
import sys
import os
import importlib.util


def analyze_code_structure(file_path: str) -> dict:
    """
    Analyzes the structure of a Python file.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        dict: Dictionary containing structure metrics.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError as e:
            return {"error": f"Syntax error: {e}", "functions": 0, "classes": 0, "score": 0}
    
    functions = 0
    classes = 0
    methods = 0
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
            # Count methods in class
            for class_node in node.body:
                if isinstance(class_node, ast.FunctionDef):
                    methods += 1
    
    # Simple modularity score calculation
    # Higher score for more functions and classes
    total_components = functions + classes
    if total_components == 0:
        score = 0
    else:
        # Score based on presence of classes (good OOP practice) and function distribution
        class_bonus = min(classes * 0.3, 1.0)  # Bonus for having classes, capped at 1.0
        function_bonus = min(functions * 0.1, 1.0)  # Bonus for having functions, capped at 1.0
        score = class_bonus + function_bonus
    
    return {
        "functions": functions,
        "classes": classes,
        "methods": methods,
        "total_components": total_components,
        "score": round(score, 2)
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 3_modularity_adaptive.py <module_name>")
        sys.exit(1)
    
    module_name = sys.argv[1]
    module_file = f"{module_name}.py"
    current_dir = os.path.dirname(__file__)
    module_path = os.path.join(current_dir, module_file)
    
    print(f"Testing module: {module_name}")
    
    if not os.path.exists(module_path):
        print(f"Module file not found: {module_file}")
        sys.exit(1)
    
    try:
        result = analyze_code_structure(module_path)
        
        if "error" in result:
            print(f"Analysis failed: {result['error']}")
            sys.exit(1)
        
        print(f"Functions: {result['functions']}")
        print(f"Classes: {result['classes']}")
        print(f"Methods: {result['methods']}")
        print(f"Modularity score: {result['score']}")
        
    except Exception as e:
        print(f"Module {module_name} failed with error: {e}")
        sys.exit(1)
