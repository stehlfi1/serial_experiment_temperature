
"""
ASCII Art Drawing Application

Implements a console-based ASCII Art generator using OOP, adhering to ISO/IEC 25010 quality standards.
Supports drawing of squares, rectangles, parallelograms, right-angled triangles, and pyramids with
custom single-character symbols. Inputs validated with robust error handling.

Author: (Your Name)
Date: (Date)
"""

from typing import Any


class AsciiArt:
    """
    Class providing methods to generate ASCII representations
    of various geometric shapes.
    """

    def __init__(self) -> None:
        """Initialize AsciiArt class. Nothing to setup currently."""
        pass

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single, printable, non-whitespace character.
        :param symbol: Symbol to validate
        :raises ValueError: If symbol is invalid
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")

        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    @staticmethod
    def _validate_dimension(value: Any, name: str) -> None:
        """
        Validates that the provided dimension is a positive integer.
        :param value: Value to check
        :param name: Name of the parameter for error message
        :raises ValueError: If input is not a positive integer
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Generates a string representing a filled square.

        :param width: Width (also height) of the square, in characters. Must be positive integer.
        :param symbol: Single, non-whitespace printable character to fill the square.
        :return: Multi-line string representing ASCII-art square.
        """
        self._validate_dimension(width, 'width')
        self._validate_symbol(symbol)

        row = symbol * width
        square = '\n'.join([row for _ in range(width)])
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a string representing a filled rectangle.

        :param width: Width of the rectangle, in characters. Must be positive integer.
        :param height: Height of the rectangle, in characters. Must be positive integer.
        :param symbol: Single, non-whitespace printable character.
        :return: Multi-line string representing ASCII-art rectangle.
        """
        self._validate_dimension(width, 'width')
        self._validate_dimension(height, 'height')
        self._validate_symbol(symbol)

        row = symbol * width
        rectangle = '\n'.join([row for _ in range(height)])
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a string representing a filled parallelogram,
        growing diagonally to the right from the top-left.

        :param width: Width of the parallelogram, in characters. Must be positive integer.
        :param height: Height of the parallelogram, in characters. Must be positive integer.
        :param symbol: Single, non-whitespace printable character.
        :return: Multi-line string representing ASCII-art parallelogram.
        """
        self._validate_dimension(width, 'width')
        self._validate_dimension(height, 'height')
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            spaces = ' ' * i
            row = spaces + (symbol * width)
            rows.append(row)
        parallelogram = '\n'.join(rows)
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a string representing a filled right-angled triangle,
        growing to the right and down, right angle at top-left.

        :param width: Base width of the triangle, in characters. Must be positive integer.
        :param height: Height of the triangle, in characters. Must be positive integer.
        :param symbol: Single, non-whitespace printable character.
        :return: Multi-line string representing ASCII-art triangle.
        :raises ValueError: If height < 1, width < 1
        """
        self._validate_dimension(width, 'width')
        self._validate_dimension(height, 'height')
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Linear interpolation: growing line by line until full width on last line
            w = max(1, (width * (i + 1) + height - 1) // height)
            # Guarantee last row has exactly width symbols
            if i == height - 1:
                w = width
            row = symbol * w
            rows.append(row)
        triangle = '\n'.join(rows)
        return triangle

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Generates a string representing a filled, symmetric pyramid.

        :param height: Height of the pyramid. Must be positive integer.
        :param symbol: Single, non-whitespace printable character.
        :return: Multi-line string representing ASCII-art pyramid.
        """
        self._validate_dimension(height, 'height')
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            n_symbols = 2 * i + 1
            spaces = height - i - 1
            row = (' ' * spaces) + (symbol * n_symbols)
            rows.append(row)
        pyramid = '\n'.join(rows)
        return pyramid


# EXAMPLE USAGE / TESTS (can be replaced with proper unittests)

if __name__ == "__main__":
    art = AsciiArt()

    print("Square:\n", art.draw_square(5, "*"), sep='')
    print("\nRectangle:\n", art.draw_rectangle(8, 3, "#"), sep='')
    print("\nParallelogram:\n", art.draw_parallelogram(6, 4, "+"), sep='')
    print("\nTriangle:\n", art.draw_triangle(5, 4, "@"), sep='')
    print("\nPyramid:\n", art.draw_pyramid(5, "$"), sep='')
