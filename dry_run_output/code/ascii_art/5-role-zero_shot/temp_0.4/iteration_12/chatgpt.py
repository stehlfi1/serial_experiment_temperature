
"""
ascii_art.py
A console-based ASCII Art generator for various 2D shapes, adhering to ISO/IEC 25010 quality standards.

Author: [Your Name]
Date: [Today's Date]

This module provides the AsciiArt class with functionality to draw:
- Square
- Rectangle
- Parallelogram
- Right-angled Triangle
- Pyramid

Each shape is drawn as a multi-line string, using a user-defined printable single character as the fill symbol.

Error handling follows Python conventions, raising built-in exceptions for invalid input.
"""

from typing import Any

class AsciiArt:
    """
    AsciiArt provides methods to generate different filled ASCII shapes as multi-line strings.

    Each method validates its inputs and raises appropriate exceptions.
    """

    def __init__(self) -> None:
        pass  # No state is held by the AsciiArt class

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the symbol for drawing.

        Args:
            symbol (str): The fill character.

        Raises:
            ValueError: If the symbol is not exactly one non-whitespace printable character.
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
    def _validate_positive_int(value: Any, name: str) -> None:
        """
        Validates that the value is a positive integer.

        Args:
            value (Any): The value to be validated.
            name (str): The name of the parameter for error messages.

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer (got {value}).")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): Width and height (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The ASCII art as a multi-line string.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        # Each line is 'width' symbols; number of lines = width
        line = symbol * width
        art = "\n".join(line for _ in range(width))
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): Width (must be positive).
            height (int): Height (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The ASCII art as a multi-line string.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        line = symbol * width
        art = "\n".join(line for _ in range(height))
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-leaning parallelogram.
        Each subsequent row is shifted one space right.

        Args:
            width (int): Number of symbols per line (must be positive).
            height (int): Number of lines (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The ASCII art as a multi-line string.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            spaces = " " * row
            art_line = f"{spaces}{symbol * width}"
            lines.append(art_line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle, growing to the right and down from the top-left.

        Args:
            width (int): The length of the triangle's base (must be positive).
            height (int): The number of lines (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The ASCII art as a multi-line string.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # For each row except last, calculate incremental width of symbol
            n_symbols = min(width, (row + 1) * width // height)
            if n_symbols == 0:
                n_symbols = 1
            lines.append(symbol * n_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        Args:
            height (int): Height of the pyramid (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The ASCII art as a multi-line string.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            n_symbols = 2 * row + 1
            n_spaces = height - row - 1
            line = " " * n_spaces + symbol * n_symbols + " " * n_spaces
            lines.append(line)
        return "\n".join(lines)

# Example usage (for testing, can be removed in production)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n", art.draw_square(4, "#"))
    print("\nRectangle:\n", art.draw_rectangle(6, 3, "*"))
    print("\nParallelogram:\n", art.draw_parallelogram(5, 4, "+"))
    print("\nTriangle:\n", art.draw_triangle(6, 4, "@"))
    print("\nPyramid:\n", art.draw_pyramid(5, "$"))
