
"""
ASCII Art Generator - Console Application

This module provides a class `AsciiArt` for generating 2D ASCII art shapes,
including squares, rectangles, parallelograms, right-angled triangles, and pyramids.
It is designed for high code quality, maintainability, and follows ISO/IEC 25010 requirements.

Author: [Your Name]
Date: 2024-06-xx
"""

from typing import Optional


class AsciiArt:
    """
    AsciiArt provides methods for drawing various ASCII art shapes.

    Interface:
        - draw_square(width: int, symbol: str) -> str
        - draw_rectangle(width: int, height: int, symbol: str) -> str
        - draw_parallelogram(width: int, height: int, symbol: str) -> str
        - draw_triangle(width: int, height: int, symbol: str) -> str
        - draw_pyramid(height: int, symbol: str) -> str
    """

    @staticmethod
    def _validate_positive_int(value: int, name: str) -> None:
        """Ensure the given value is a positive integer."""
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single, printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square.

        Args:
            width (int): Width and height of the square (must be > 0)
            symbol (str): The symbol to use (must be a single, printable, non-whitespace character)

        Returns:
            str: Multi-line ASCII art of the square.
        """
        self._validate_positive_int(width, 'width')
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(width)]
        return '\n'.join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle.

        Args:
            width (int): Width of the rectangle (must be > 0)
            height (int): Height of the rectangle (must be > 0)
            symbol (str): The symbol to use (must be a single, printable, non-whitespace character)

        Returns:
            str: Multi-line ASCII art of the rectangle.
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return '\n'.join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram (each row is shifted to the right).

        Args:
            width (int): Width of the parallelogram (must be > 0)
            height (int): Height of the parallelogram (must be > 0)
            symbol (str): The symbol to use (must be a single, printable, non-whitespace character)

        Returns:
            str: Multi-line ASCII art of the parallelogram.
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            line = (' ' * row) + (symbol * width)
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a left-aligned, filled, right-angled triangle.
        The base is at the bottom, the right angle is at the top-left.

        Args:
            width (int): Width of the triangle's base (must be > 0)
            height (int): Height of the triangle (must be > 0)
            symbol (str): The symbol to use (must be a single, printable, non-whitespace character)

        Returns:
            str: Multi-line ASCII art of the triangle.
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)
        # Each row's length increases proportional to height and width
        # The last row must be of "width" length
        lines = []
        for row in range(1, height + 1):
            # Calculate current row's length, ensure the last row is exactly 'width'
            line_length = max(1, round(row * width / height))
            if row == height:
                line_length = width
            lines.append(symbol * line_length)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a centered, symmetrical pyramid.

        Args:
            height (int): Height of the pyramid (must be > 0)
            symbol (str): The symbol to use (must be a single, printable, non-whitespace character)

        Returns:
            str: Multi-line ASCII art of the pyramid.
        """
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)
        lines = []
        for row in range(1, height + 1):
            symbols_in_row = 2 * row - 1
            total_width = 2 * height - 1
            spaces = (total_width - symbols_in_row) // 2
            line = (' ' * spaces) + (symbol * symbols_in_row) + (' ' * spaces)
            lines.append(line)
        return '\n'.join(lines)


# === Example usage and demonstration (for testability) ===

if __name__ == "__main__":
    art = AsciiArt()

    print("Square:")
    print(art.draw_square(5, '*'))
    print()

    print("Rectangle:")
    print(art.draw_rectangle(7, 3, '#'))
    print()

    print("Parallelogram:")
    print(art.draw_parallelogram(6, 4, '@'))
    print()

    print("Triangle:")
    print(art.draw_triangle(7, 4, '+'))
    print()

    print("Pyramid:")
    print(art.draw_pyramid(5, '^'))
