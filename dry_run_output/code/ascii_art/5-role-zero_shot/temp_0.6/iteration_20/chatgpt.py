
"""
ASCII Art Generator - Console-based 2D ASCII Art Application

This module provides the AsciiArt class that allows drawing
various 2D shapes as ASCII art using a symbol. Developed in adherence
to ISO/IEC 25010: maintainability, correctness, usability, reliability, etc.

Shapes supported:
- Square
- Rectangle
- Parallelogram
- Right-angled Triangle
- Pyramid
"""

from typing import Any


class AsciiArt:
    """
    Class for generating console-based ASCII art shapes.
    Each shape is returned as a multiline string.
    """

    def _validate_dimension(self, name: str, value: int) -> None:
        """
        Validates that the dimension value is a positive integer.
        Args:
            name: Name of the parameter (for error message).
            value: The dimension value to validate.
        Raises:
            ValueError: If value is not a positive integer.
            TypeError: If value is not integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        if value <= 0:
            raise ValueError(f"{name} must be positive")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace printable character.
        Args:
            symbol: The symbol to validate.
        Raises:
            ValueError: If symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character")
        if symbol.isspace():
            raise ValueError("symbol must not be a whitespace character")
        if not symbol.isprintable():
            raise ValueError("symbol must be printable")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: Number of characters for both width and height (>0).
            symbol: A single, printable, non-whitespace character.

        Returns:
            Multiline string representing the square.
        """
        self._validate_dimension('width', width)
        self._validate_symbol(symbol)
        row = symbol * width
        return "\n".join([row for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: Number of columns (>0).
            height: Number of rows (>0).
            symbol: A single, printable, non-whitespace character.

        Returns:
            Multiline string representing the rectangle.
        """
        self._validate_dimension('width', width)
        self._validate_dimension('height', height)
        self._validate_symbol(symbol)
        row = symbol * width
        return "\n".join([row for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram (diagonally shifts to the right).

        Args:
            width: Base width of the parallelogram (>0).
            height: Height of the parallelogram (>0).
            symbol: A single, printable, non-whitespace character.

        Returns:
            Multiline string representing the parallelogram.
        """
        self._validate_dimension('width', width)
        self._validate_dimension('height', height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            spaces = " " * i
            line = spaces + (symbol * width)
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle, aligned to top-left.

        Args:
            width: Maximum width (base) of the triangle (>0).
            height: Height of the triangle (>0).
            symbol: A single, printable, non-whitespace character.

        Returns:
            Multiline string representing the triangle.
        """
        self._validate_dimension('width', width)
        self._validate_dimension('height', height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            curr_width = min(width, i + 1)
            line = symbol * curr_width
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: Height of the pyramid (>0).
            symbol: A single, printable, non-whitespace character.

        Returns:
            Multiline string representing the pyramid.
        """
        self._validate_dimension('height', height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Number of symbols on this row: 1, 3, 5, ...
            symbols_count = 2 * i + 1
            spaces_count = height - i - 1
            line = " " * spaces_count + symbol * symbols_count + " " * spaces_count
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    # Basic test examples (for illustration/testability)
    art = AsciiArt()

    print("Square:\n", art.draw_square(4, "#"))
    print("\nRectangle:\n", art.draw_rectangle(6, 3, "*"))
    print("\nParallelogram:\n", art.draw_parallelogram(5, 4, "$"))
    print("\nRight Triangle:\n", art.draw_triangle(5, 5, "+"))
    print("\nPyramid:\n", art.draw_pyramid(4, "%"))
