"""
Code modularity test
Output: The number of classes, functions, and methods in each module.
"""

import ast
import inspect
import sys


import chatgpt
import claude
import gemini


def count_classes_functions_methods(module) -> tuple:
    """
    Count the number of classes, functions, and methods in a given Python module.

    Args:
        module (module): The Python module to analyze.

    Returns:
        tuple: A tuple containing three integers:
            - class_count (int): The number of classes in the module.
            - function_count (int): The number of functions in the module (excluding methods).
            - method_count (int): The number of methods in the module.
    """
    file_path = inspect.getfile(module)

    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    class_count = 0
    function_count = 0
    method_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_count += 1
            method_count += sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
        elif isinstance(node, ast.FunctionDef):
            if not any(
                isinstance(parent, ast.ClassDef) and node in parent.body
                for parent in ast.walk(tree)
            ):
                function_count += 1

    return class_count, function_count, method_count


if __name__ == "__main__":
    modules = {"chatgpt": chatgpt, "claude": claude, "gemini": gemini}

    if sys.argv[1] not in modules:
        raise ValueError(f"Invalid module name: {sys.argv[1]}")

    print(f"Testing module: {modules[sys.argv[1]].__name__}")
    try:
        classes, functions, methods = count_classes_functions_methods(
            modules[sys.argv[1]]
        )
        if classes is not None and functions is not None and methods is not None:
            print(f"Number of classes: {classes}")
            print(f"Number of methods: {methods}")
            print(f"Number of functions: {functions}")
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__name__} failed with error.")
