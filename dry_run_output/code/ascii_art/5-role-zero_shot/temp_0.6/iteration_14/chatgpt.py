
"""
ascii_art.py

A console-based ASCII art application implementing various 2D shapes using OOP, 
adhering to ISO/IEC 25010 quality requirements and best practices.

Author: Senior Software Developer
Date: 2024
"""

from typing import Any


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    Provides functions to draw square, rectangle, parallelogram, triangle, and pyramid.
    """

    def __init__(self) -> None:
        """Initialize the AsciiArt class."""
        pass  # No state required

    def _validate_dimension(self, name: str, value: int) -> None:
        """
        Validate that a dimension (width or height) is a positive integer.

        Args:
            name: The name of the variable ('width' or 'height')
            value: The value to be validated

        Raises:
            ValueError: If `value` is not a positive integer
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer, got {type(value).__name__}.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer, got {value}.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate that the symbol is a single, printable, non-whitespace character.

        Args:
            symbol: The symbol to validate

        Raises:
            ValueError: If symbol is invalid
        """
        if not isinstance(symbol, str):
            raise TypeError(f"symbol must be a string, got {type(symbol).__name__}.")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("symbol cannot be whitespace.")
        if not symbol.isprintable():
            raise ValueError("symbol must be printable.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square with the given width and symbol.

        Args:
            width: Side-length of the square
            symbol: Symbol to use

        Returns:
            A multi-line string representing the square
        """
        self._validate_dimension("width", width)
        self._validate_symbol(symbol)

        line = symbol * width
        drawing = "\n".join([line for _ in range(width)])
        return drawing

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle with the given width, height, and symbol.

        Args:
            width: Number of columns
            height: Number of rows
            symbol: Symbol to use

        Returns:
            A multi-line string representing the rectangle
        """
        self._validate_dimension("width", width)
        self._validate_dimension("height", height)
        self._validate_symbol(symbol)

        line = symbol * width
        drawing = "\n".join([line for _ in range(height)])
        return drawing

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram starting from top-left, each row shifted right.

        Args:
            width: Number of columns in each row
            height: Number of rows
            symbol: Symbol to use

        Returns:
            A multi-line string representing the parallelogram
        """
        self._validate_dimension("width", width)
        self._validate_dimension("height", height)
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            line = " " * i + symbol * width
            rows.append(line)
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle (top-left), with given width and height.

        Args:
            width: The base width (max length of the triangle)
            height: The height of the triangle (number of rows)
            symbol: The symbol to use

        Returns:
            A multi-line string representing the triangle

        Note:
            The triangle grows both rightwards (columns) and downwards (rows).
            Each row i (0-based) has min(width, ceil((i+1)*width/height)) symbols.
        """
        self._validate_dimension("width", width)
        self._validate_dimension("height", height)
        self._validate_symbol(symbol)

        # To cover both axes equally, compute length for each row
        rows = []
        for i in range(height):
            # Compute proportional width for current row
            # Last row will always be width
            row_len = (width * (i + 1) + height - 1) // height
            row_len = min(row_len, width)
            rows.append(symbol * row_len)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a centered, filled pyramid of given height.

        Args:
            height: Height of the pyramid (number of rows)
            symbol: Symbol to use

        Returns:
            A multi-line string representing the pyramid
        """
        self._validate_dimension("height", height)
        self._validate_symbol(symbol)

        rows = []
        base_width = 2 * height - 1  # Pyramid is centered

        for i in range(height):
            symbols_in_row = 2 * i + 1
            spaces = (base_width - symbols_in_row) // 2
            row = " " * spaces + symbol * symbols_in_row + " " * spaces
            rows.append(row)
        return "\n".join(rows)


if __name__ == "__main__":
    # Example usage and basic tests
    art = AsciiArt()
    print("Square:\n" + art.draw_square(4, '#'))
    print("\nRectangle:\n" + art.draw_rectangle(6, 3, '*'))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, '$'))
    print("\nRight-angled Triangle:\n" + art.draw_triangle(6, 4, '@'))
    print("\nPyramid:\n" + art.draw_pyramid(5, '+'))
