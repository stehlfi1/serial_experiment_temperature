
"""
ascii_art.py

An OOP-based, ISO/IEC 25010-compliant ASCII Art app for drawing basic 2D shapes.
Implements input validation, consistent error handling, and shape rendering.

Author: [Your Name]
"""

from typing import Any


class AsciiArt:
    """
    Provides methods to draw various 2D ASCII art shapes.
    All methods validate their input and return a multi-line string with the drawn shape.
    """

    @staticmethod
    def _validate_positive_integer(value: Any, name: str) -> None:
        """
        Validates that a given value is a positive integer (>=1).
        Raises:
            ValueError: if value is not an integer >=1.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 1:
            raise ValueError(f"{name} must be at least 1.")

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Validates that the provided symbol is a single, non-whitespace, printable character.
        Raises:
            ValueError: if symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of 'width' x 'width' using the specified symbol.
        Args:
            width (int): The width/height of the square; must be >=1.
            symbol (str): The filling character (single, non-whitespace).
        Returns:
            str: The multi-line ASCII art string of the square.
        """
        self._validate_positive_integer(width, "Width")
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle using the specified width, height, and symbol.
        Args:
            width (int): Rectangle width; must be >=1.
            height (int): Rectangle height; must be >=1.
            symbol (str): Filling character.
        Returns:
            str: ASCII art of the rectangle.
        """
        self._validate_positive_integer(width, "Width")
        self._validate_positive_integer(height, "Height")
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        Each row is indented by increasing spaces, forming a diagonal right slope.
        Args:
            width (int): Number of symbols per row; must be >=1.
            height (int): Number of rows; must be >=1.
            symbol (str): Filling character.
        Returns:
            str: ASCII art of the parallelogram.
        """
        self._validate_positive_integer(width, "Width")
        self._validate_positive_integer(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            indent = ' ' * row
            line = indent + (symbol * width)
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle (top-left right angle).
        Each row increases in length, up to the maximum width and height.
        Args:
            width (int): The max width of the triangle's base.
            height (int): The number of rows.
            symbol (str): Filling character.
        Returns:
            str: ASCII art of the triangle.
        """
        self._validate_positive_integer(width, "Width")
        self._validate_positive_integer(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(1, height + 1):
            count = min(width, row)  # Limit growth to max width
            line = symbol * count
            lines.append(line)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetric pyramid with the given height and symbol.
        The base width is (2 * height - 1).
        Args:
            height (int): Number of levels in the pyramid; must be >=1.
            symbol (str): Filling character.
        Returns:
            str: ASCII art of the pyramid.
        """
        self._validate_positive_integer(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            spaces = height - row - 1
            symbols = 2 * row + 1
            line = (' ' * spaces) + (symbol * symbols) + (' ' * spaces)
            lines.append(line)
        return '\n'.join(lines)


if __name__ == "__main__":
    # Example demonstration for testing
    art = AsciiArt()

    print("Square:\n")
    print(art.draw_square(5, "#"))
    print("\nRectangle:\n")
    print(art.draw_rectangle(8, 3, "*"))
    print("\nParallelogram:\n")
    print(art.draw_parallelogram(5, 4, "@"))
    print("\nTriangle:\n")
    print(art.draw_triangle(6, 4, "+"))
    print("\nPyramid:\n")
    print(art.draw_pyramid(5, "$"))
