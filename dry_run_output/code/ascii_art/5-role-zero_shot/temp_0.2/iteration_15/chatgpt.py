
"""
ascii_art.py

A console-based ASCII Art generator adhering to ISO/IEC 25010 quality model.
Provides OOP-based, testable, and maintainable code to draw various ASCII art shapes.
"""

from typing import Any


class AsciiArt:
    """
    AsciiArt provides methods to generate filled ASCII shapes (square, rectangle, parallelogram,
    right-angled triangle, and pyramid) using a single printable symbol.
    All methods validate parameters and return the shape as a multi-line string.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square of the specified width using the given symbol.

        Parameters:
            width (int): The width and height of the square (must be >= 1).
            symbol (str): A single printable, non-whitespace character symbol.

        Returns:
            str: The ASCII square as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)
        return self._draw_rectangle_internal(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle of specified width and height using the given symbol.

        Parameters:
            width (int): Width of the rectangle (must be >= 1).
            height (int): Height of the rectangle (must be >= 1).
            symbol (str): A single printable, non-whitespace character symbol.

        Returns:
            str: The ASCII rectangle as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        return self._draw_rectangle_internal(width, height, symbol)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram, growing diagonally to the right.

        Parameters:
            width (int): Width of the parallelogram (must be >= 1).
            height (int): Height of the parallelogram (must be >= 1).
            symbol (str): A single printable, non-whitespace character symbol.

        Returns:
            str: The ASCII parallelogram as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle, growing diagonally right from the top-left corner.

        Parameters:
            width (int): Maximum width of the triangle's base (must be >= 1).
            height (int): Height of the triangle (must be >= 1).
            symbol (str): A single printable, non-whitespace character symbol.

        Returns:
            str: The ASCII triangle as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the symbols to print on current line, up to the width limit
            line_symbols = min(width, i + 1)
            line = symbol * line_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled, symmetrical pyramid.

        Parameters:
            height (int): The number of pyramid rows (must be >= 1).
            symbol (str): A single printable, non-whitespace character symbol.

        Returns:
            str: The ASCII pyramid as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        lines = []
        width = height * 2 - 1  # Pyramid base width
        for i in range(height):
            symbols_count = 2 * i + 1
            spaces = (width - symbols_count) // 2
            line = " " * spaces + symbol * symbols_count + " " * spaces
            lines.append(line)
        return "\n".join(lines)

    # ------------------------------
    # Internal/private methods below
    # ------------------------------
    def _draw_rectangle_internal(self, width: int, height: int, symbol: str) -> str:
        """Private helper for rectangles and squares."""
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    @staticmethod
    def _validate_positive_integer(value: Any, name: str):
        """Ensure value is an integer >= 1."""
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 1:
            raise ValueError(f"{name} must be >= 1.")

    @staticmethod
    def _validate_symbol(symbol: Any):
        """Ensure symbol is a single printable, non-whitespace character."""
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("symbol must be a printable character.")


# Example usage and basic tests
if __name__ == "__main__":
    art = AsciiArt()

    print("Square:\n", art.draw_square(4, "#"))
    print("\nRectangle:\n", art.draw_rectangle(6, 3, "*"))
    print("\nParallelogram:\n", art.draw_parallelogram(5, 4, "@"))
    print("\nTriangle:\n", art.draw_triangle(6, 4, "+"))
    print("\nPyramid:\n", art.draw_pyramid(5, "$"))
