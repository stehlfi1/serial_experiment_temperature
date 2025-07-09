"""
Code length test
Output: The number of lines in the source file of each module.
"""

import inspect
import sys


import chatgpt
import claude
import gemini


def count_lines_in_module(module) -> int:
    """
    Counts the number of lines in the source file of a given module.

    Args:
        module: The module whose source file's lines are to be counted.

    Returns:
        int: The number of lines in the module's source file.
    """
    source_file = inspect.getfile(module)
    with open(source_file, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


if __name__ == "__main__":
    modules = {"chatgpt": chatgpt, "claude": claude, "gemini": gemini}

    if sys.argv[1] not in modules:
        raise ValueError(f"Invalid module name: {sys.argv[1]}")

    print(f"Testing module: {modules[sys.argv[1]].__name__}")
    try:
        lines = count_lines_in_module(modules[sys.argv[1]])
        print(f"Number of lines: {lines}")
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__name__} failed with error.")
