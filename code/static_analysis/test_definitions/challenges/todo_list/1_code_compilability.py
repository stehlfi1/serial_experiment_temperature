"""
Code compilability test
Output: Yes/No
"""

import py_compile
import os
import sys


def test_code_compilability(path) -> None:
    """
    Tests if the given file's code is compilable.

    Args:
        path: Path to the Python file to be tested.

    Returns:
        None
    """
    py_compile.compile(path, doraise=True)


if __name__ == "__main__":
    modules = {"chatgpt": "chatgpt.py", "claude": "claude.py", "gemini": "gemini.py"}
    module = modules[sys.argv[1]]

    if sys.argv[1] not in modules:
        raise ValueError(f"Invalid module name: {sys.argv[1]}")
    
    module_path = os.path.join(os.path.dirname(__file__), module)
    if not os.path.exists(module_path):
        print(f"File not found: {module}")
        sys.exit(1)

    print(f"Testing module: {sys.argv[1]}")
    try:
        test_code_compilability(module_path)
        print("Yes, the code is compilable.")
    except Exception as _:
        print("No, the code contains errors.")
