
"""
ascii_art.py

A console-based 2D ASCII Art application following ISO/IEC 25010 quality standards.
Implements OOP with the AsciiArt class and provides methods for drawing various ASCII shapes.

Author: Senior Python Developer
Date: 2024-06-18

Usage Example:
    art = AsciiArt()
    print(art.draw_square(4, '#'))
"""

from typing import Optional


class AsciiArt:
    """
    Class for generating ASCII art shapes.
    Provides methods to draw square, rectangle, parallelogram, triangle, and pyramid.
    Ensures input validation and shape consistency.
    """

    def __init__(self):
        """Initialize AsciiArt instance."""
        pass  # Currently, no initialization is required.

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validate that symbol is a single, printable, non-whitespace character.

        :param symbol: Character to fill the shape.
        :raises ValueError: if symbol is invalid.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_positive_int(value: int, name: str):
        """
        Validate that a value is a positive integer.

        :param value: Integer value to check.
        :param name: Name of the parameter, for error messages.
        :raises ValueError: if value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square of the specified width using the given symbol.

        :param width: Width and height of the square (must be positive integer).
        :param symbol: Single, non-whitespace, printable character.
        :return: Multi-line string of the square.
        """
        self._validate_positive_int(width, 'width')
        self._validate_symbol(symbol)

        row = symbol * width
        square = [row for _ in range(width)]
        return '\n'.join(square)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle of given width and height using the specified symbol.

        :param width: Width of the rectangle (must be positive integer).
        :param height: Height of the rectangle (must be positive integer).
        :param symbol: Single, non-whitespace, printable character.
        :return: Multi-line string of the rectangle.
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)

        row = symbol * width
        rectangle = [row for _ in range(height)]
        return '\n'.join(rectangle)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram where each row shifts one space to the right.

        :param width: Width of the parallelogram sides (must be positive integer).
        :param height: Height of the parallelogram (must be positive integer).
        :param symbol: Single, non-whitespace, printable character.
        :return: Multi-line string of the parallelogram.
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Each row shifts right by i spaces
            row = ' ' * i + symbol * width
            rows.append(row)
        return '\n'.join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle growing to the right and down.

        :param width: Width of the triangle's base (must be positive integer).
        :param height: Height of the triangle (must be positive integer).
        :param symbol: Single, non-whitespace, printable character.
        :return: Multi-line string of the triangle.
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)

        rows = []
        # For proportional triangle, use the formula: n = round(width * (row + 1) / height)
        for row in range(height):
            fill = round(width * (row + 1) / height)
            fill = max(fill, 1)      # Ensure at least one symbol in first row
            fill = min(fill, width)  # Never exceed the given width
            rows.append(symbol * fill)
        return '\n'.join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical, filled pyramid with the specified height.

        :param height: Height of the pyramid (must be positive integer).
        :param symbol: Single, non-whitespace, printable character.
        :return: Multi-line string of the pyramid.
        """
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)

        width = 2 * height - 1  # Pyramid base width

        rows = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            rows.append(line)
        return '\n'.join(rows)

# Example usage for demonstration/testing (should be separated for unit test scripts)
if __name__ == "__main__":
    art = AsciiArt()
    print("SQUARE:\n" + art.draw_square(4, '*') + "\n")
    print("RECTANGLE:\n" + art.draw_rectangle(6, 3, '+') + "\n")
    print("PARALLELOGRAM:\n" + art.draw_parallelogram(5, 4, '#') + "\n")
    print("TRIANGLE:\n" + art.draw_triangle(5, 4, '@') + "\n")
    print("PYRAMID:\n" + art.draw_pyramid(5, '$'))
