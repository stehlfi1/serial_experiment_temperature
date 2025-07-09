"""
This module contains helper functions used by the scraper.
"""

import re
from pathlib import Path


def extract_python_code(text: str) -> str:
    """
    Extracts Python code blocks from a given text.

    This function searches for Python code blocks enclosed within triple backticks
    (```python ... ```) in the provided text and returns them as a single string.
    If no Python code blocks are found, it returns an empty string.

    Args:
        text (str): The input text containing potential Python code blocks.

    Returns:
        str: A string containing all extracted Python code blocks concatenated together,
             or an empty string if no code blocks are found.
    """
    code_blocks = re.findall(r"```python(.*?)```", text, re.DOTALL)
    return "\n".join(code_blocks) if code_blocks else ""


def load_string_from_file(file_path: str) -> str:
    """
    Reads the entire content of a file and returns it as a string.
    Handles both absolute and relative paths, resolving relative paths from project root.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    # Convert to Path object
    path = Path(file_path)
    
    # If path is not absolute, resolve it relative to project root
    if not path.is_absolute():
        # Get project root (3 levels up from this file: helpers.py -> scraper -> code -> project_root)
        project_root = Path(__file__).parent.parent.parent
        path = project_root / path
    
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
