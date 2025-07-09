"""
Adaptive Code length test for dry runs
Output: The number of lines in the source file of each module.
"""

import inspect
import sys
import os
import importlib.util


def count_lines_in_module_file(file_path: str) -> int:
    """
    Counts the number of lines in a source file.

    Args:
        file_path: Path to the Python file to count lines in.

    Returns:
        int: The number of lines in the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def count_lines_in_module_dynamic(module_name: str) -> int:
    """
    Dynamically imports a module and counts lines in its source file.

    Args:
        module_name: Name of the module to import and count lines for.

    Returns:
        int: The number of lines in the module's source file.
    """
    module_file = f"{module_name}.py"
    current_dir = os.path.dirname(__file__)
    module_path = os.path.join(current_dir, module_file)
    
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Module file not found: {module_file}")
    
    # Try to import the module dynamically
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module spec for {module_name}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Count lines directly from file (more reliable than inspect for generated code)
    return count_lines_in_module_file(module_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 2_code_length.py <module_name>")
        sys.exit(1)
    
    module_name = sys.argv[1]
    
    print(f"Testing module: {module_name}")
    try:
        lines = count_lines_in_module_dynamic(module_name)
        print(f"Number of lines: {lines}")
    except Exception as e:
        print(f"Module {module_name} failed with error: {e}")
        sys.exit(1)
