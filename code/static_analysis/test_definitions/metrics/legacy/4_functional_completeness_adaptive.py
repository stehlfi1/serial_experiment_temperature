"""
Adaptive functional completeness test for dry runs
Output: Functional completeness score based on expected features.
"""

import ast
import sys
import os
import re


def analyze_calculator_completeness(file_path: str) -> dict:
    """
    Analyzes functional completeness of a calculator implementation.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        dict: Dictionary containing completeness metrics.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return {"error": f"Syntax error: {e}", "score": 0, "features": []}
    
    # Expected features for a calculator
    expected_features = {
        "addition": ["+", "add", "plus"],
        "subtraction": ["-", "subtract", "minus"],
        "multiplication": ["*", "multiply", "times"],
        "division": ["/", "divide"],
        "main_function": ["main", "__main__"],
        "input_handling": ["input(", "sys.argv", "argparse"],
        "error_handling": ["try:", "except", "raise"],
        "calculation_function": ["calculate", "eval", "compute"],
        "output": ["print(", "return"]
    }
    
    found_features = []
    content_lower = content.lower()
    
    # Check for each expected feature
    for feature, keywords in expected_features.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                found_features.append(feature)
                break
    
    # Calculate completeness score
    total_features = len(expected_features)
    found_count = len(found_features)
    score = round(found_count / total_features, 2)
    
    return {
        "expected_features": total_features,
        "found_features": found_count,
        "score": score,
        "features_found": found_features,
        "missing_features": [f for f in expected_features.keys() if f not in found_features]
    }


def analyze_ascii_art_completeness(file_path: str) -> dict:
    """
    Analyzes functional completeness of an ASCII art implementation.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        dict: Dictionary containing completeness metrics.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    expected_features = {
        "text_input": ["input(", "sys.argv", "text"],
        "ascii_generation": ["ascii", "art", "font", "figlet"],
        "output": ["print(", "return"],
        "main_function": ["main", "__main__"],
        "string_manipulation": ["join", "split", "format"]
    }
    
    found_features = []
    content_lower = content.lower()
    
    for feature, keywords in expected_features.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                found_features.append(feature)
                break
    
    total_features = len(expected_features)
    found_count = len(found_features)
    score = round(found_count / total_features, 2)
    
    return {
        "expected_features": total_features,
        "found_features": found_count,
        "score": score,
        "features_found": found_features,
        "missing_features": [f for f in expected_features.keys() if f not in found_features]
    }


def analyze_todo_completeness(file_path: str) -> dict:
    """
    Analyzes functional completeness of a TODO list implementation.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        dict: Dictionary containing completeness metrics.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    expected_features = {
        "add_task": ["add", "append", "insert"],
        "remove_task": ["remove", "delete", "pop"],
        "list_tasks": ["list", "show", "display", "print"],
        "main_function": ["main", "__main__"],
        "data_storage": ["list", "dict", "[]", "{}"],
        "user_interface": ["input(", "menu", "choice"],
        "task_management": ["task", "todo", "item"]
    }
    
    found_features = []
    content_lower = content.lower()
    
    for feature, keywords in expected_features.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                found_features.append(feature)
                break
    
    total_features = len(expected_features)
    found_count = len(found_features)
    score = round(found_count / total_features, 2)
    
    return {
        "expected_features": total_features,
        "found_features": found_count,
        "score": score,
        "features_found": found_features,
        "missing_features": [f for f in expected_features.keys() if f not in found_features]
    }


def get_challenge_from_path(current_path: str) -> str:
    """Extract challenge name from the current path."""
    path_parts = current_path.split(os.sep)
    
    # Look for challenge names in path
    challenges = ["calculator", "ascii_art", "todo_list"]
    for part in reversed(path_parts):
        if part in challenges:
            return part
    
    # Default to calculator if not found
    return "calculator"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 4_functional_completeness_adaptive.py <module_name>")
        sys.exit(1)
    
    module_name = sys.argv[1]
    module_file = f"{module_name}.py"
    current_dir = os.path.dirname(__file__)
    module_path = os.path.join(current_dir, module_file)
    
    print(f"Testing module: {module_name}")
    
    if not os.path.exists(module_path):
        print(f"Module file not found: {module_file}")
        sys.exit(1)
    
    # Determine challenge type from path
    challenge = get_challenge_from_path(current_dir)
    print(f"Detected challenge: {challenge}")
    
    try:
        if challenge == "calculator":
            result = analyze_calculator_completeness(module_path)
        elif challenge == "ascii_art":
            result = analyze_ascii_art_completeness(module_path)
        elif challenge == "todo_list":
            result = analyze_todo_completeness(module_path)
        else:
            result = analyze_calculator_completeness(module_path)  # Default
        
        if "error" in result:
            print(f"Analysis failed: {result['error']}")
            sys.exit(1)
        
        print(f"Expected features: {result['expected_features']}")
        print(f"Found features: {result['found_features']}")
        print(f"Completeness score: {result['score']}")
        print(f"Features found: {', '.join(result['features_found'])}")
        if result['missing_features']:
            print(f"Missing features: {', '.join(result['missing_features'])}")
        
    except Exception as e:
        print(f"Module {module_name} failed with error: {e}")
        sys.exit(1)
