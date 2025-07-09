"""
Static code analysis
Output: Pylint report
"""

import inspect
import sys
import pylint.lint


import chatgpt
import claude
import gemini


def test_code_analysibility(module) -> None:
    """
    Tests the code quality of a given module using pylint.

    Args:
        module: The module to be analyzed. This should be a Python module object.

    Returns:
        None
    """
    file = inspect.getfile(module)
    pylint.lint.Run([file])


if __name__ == "__main__":
    modules = {"chatgpt": chatgpt, "claude": claude, "gemini": gemini}

    if sys.argv[1] not in modules:
        raise ValueError(f"Invalid module name: {sys.argv[1]}")

    print(f"Testing module: {modules[sys.argv[1]].__name__}")
    try:
        test_code_analysibility(modules[sys.argv[1]])
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__name__} failed with error.")
