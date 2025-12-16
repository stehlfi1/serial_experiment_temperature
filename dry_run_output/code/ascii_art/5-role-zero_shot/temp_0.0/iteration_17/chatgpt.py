
"""
ascii_art.py

A high-quality Python module for creating 2D ASCII art shapes in the console.

Author: AI Software Developer
Adheres to ISO/IEC 25010 quality standards:
- Functional Suitability, Performance Efficiency, Reliability, Usability,
  Security (robust validation), Maintainability, Portability (pure Python), Compatibility.

This module defines the AsciiArt class for drawing various ASCII shapes with robust input validation,
efficient algorithms, modular methods, and well-documented, readable code.
"""

from typing import Any


class AsciiArt:
    """
    A class to generate filled 2D ASCII art shapes.
    Supported shapes: Square, Rectangle, Parallelogram, Right-angled triangle, Symmetrical pyramid.
    """

    def __init__(self) -> None:
        """Initialize AsciiArt object."""
        pass  # No instance variables needed

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single, non-whitespace, printable character.

        Raises:
            ValueError: If symbol is not acceptable.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_positive_integer(value: Any, name: str) -> None:
        """
        Validate that the value is a positive integer.

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square of given width and symbol.

        Args:
            width (int): Width and height of the square (must be positive).
            symbol (str): The character to fill the square with.

        Returns:
            str: Multiline string representing the square.
        """
        self._validate_positive_integer(width, "Width")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle with given width, height and symbol.

        Args:
            width (int): Number of characters per row.
            height (int): Number of rows.
            symbol (str): The character to fill the rectangle with.

        Returns:
            str: Multiline string representing the rectangle.
        """
        self._validate_positive_integer(width, "Width")
        self._validate_positive_integer(height, "Height")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram (each row shifted to right) of given width and height.

        Args:
            width (int): Number of characters per row.
            height (int): Number of rows.
            symbol (str): The character to fill the parallelogram with.

        Returns:
            str: Multiline string representing the parallelogram.
        """
        self._validate_positive_integer(width, "Width")
        self._validate_positive_integer(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Each row is prefixed with increasing spaces, up to height - 1 spaces
            lines.append(" " * row + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle (top-left corner) with given width and height.

        The triangle grows horizontally rightward, each row increases by 1 until max width.

        Args:
            width (int): The maximum characters (base) at the bottom row.
            height (int): Number of lines (triangle height).
            symbol (str): The character to fill the triangle with.

        Returns:
            str: Multiline string representing the triangle.
        """
        self._validate_positive_integer(width, "Width")
        self._validate_positive_integer(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Calculate stars for each row (equally spaced between 1 ... width)
            num_symbols = max(1, min(width, (row + 1) * width // height))
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical filled pyramid.

        Args:
            height (int): Height of the pyramid (number of levels, must be positive).
            symbol (str): The character to fill the pyramid with.

        Returns:
            str: Multiline string representing the pyramid.
        """
        self._validate_positive_integer(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        width = height * 2 - 1
        for row in range(height):
            # Number of symbols increases by 2 per row
            num_symbols = 2 * row + 1
            num_spaces = (width - num_symbols) // 2
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


# --- (Optional) Example Usage/Testing (Can be deleted/commented out in production) ---
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n" + art.draw_square(4, '#'))
    print("\nRectangle:\n" + art.draw_rectangle(6, 3, '$'))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, '/'))
    print("\nTriangle:\n" + art.draw_triangle(8, 5, '*'))
    print("\nPyramid:\n" + art.draw_pyramid(5, '@'))
