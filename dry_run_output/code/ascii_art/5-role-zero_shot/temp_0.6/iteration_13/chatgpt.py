
"""
ASCII Art Application - Console-based, OOP style

This module defines the AsciiArt class which adheres to ISO/IEC 25010 requirements, 
drawing various ASCII art shapes with robust validation and clean, maintainable code.

Each drawing function returns the result as a multi-line string.

Author: Senior Software Developer
"""

from typing import Optional

class AsciiArt:
    """
    A class to generate 2D ASCII art shapes for console applications.

    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def __init__(self):
        pass  # No state; placeholder for possible future extension

    @staticmethod
    def _validate_dimension(value: int, name: str = "Dimension") -> None:
        """
        Validates that a dimension value is a positive integer.

        :param value: The value to validate.
        :param name: The name of the dimension for error messages.
        :raises ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace character.

        :param symbol: The symbol to validate.
        :raises ValueError: If symbol is not a single, non-whitespace, printable character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square using the specified symbol.

        :param width: The width and height of the square (must be positive integer).
        :param symbol: The filling character (single non-whitespace symbol).
        :return: Multiline string representing the square.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)
        row = symbol * width
        art = '\n'.join([row for _ in range(width)])
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        :param width: Number of columns (must be positive integer).
        :param height: Number of rows (must be positive integer).
        :param symbol: Filling symbol (single non-whitespace character).
        :return: Multiline string representing the rectangle.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        row = symbol * width
        art = '\n'.join([row for _ in range(height)])
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, each row shifted right by one space from the previous.

        :param width: Width of the parallelogram (must be positive integer).
        :param height: Height (number of rows, must be positive integer).
        :param symbol: Filling symbol (single non-whitespace character).
        :return: Multiline string representing the parallelogram.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        art_rows = []
        for i in range(height):
            spaces = ' ' * i
            art_rows.append(spaces + symbol * width)
        return '\n'.join(art_rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle (top-left right angle), height rows, growing rightward.

        The number of symbols in each row grows linearly, such that the bottom row is "width" symbols wide.

        :param width: Length of base (must be positive integer).
        :param height: Height of triangle (must be positive integer).
        :param symbol: Filling symbol (single character).
        :return: Multiline string representing the triangle.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        art_rows = []
        for i in range(1, height + 1):
            # Calculate proportional width for each row
            row_width = max(1, (width * i) // height)
            art_rows.append(symbol * row_width)
        return '\n'.join(art_rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid centered horizontally.

        :param height: Number of rows (must be positive integer).
        :param symbol: Filling symbol (single character).
        :return: Multiline string representing the pyramid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        art_rows = []
        for i in range(height):
            padding = ' ' * (height - i - 1)
            row_symbols = symbol * (2 * i + 1)
            art_rows.append(f"{padding}{row_symbols}{padding}")
        return '\n'.join(art_rows)


# -------------------------------
# Example usage (Testability demo)
# -------------------------------

if __name__ == "__main__":
    art = AsciiArt()

    print("SQUARE (width=4):")
    print(art.draw_square(4, "#"))
    print()

    print("RECTANGLE (width=6, height=3):")
    print(art.draw_rectangle(6, 3, "@"))
    print()

    print("PARALLELOGRAM (width=5, height=4):")
    print(art.draw_parallelogram(5, 4, "*"))
    print()

    print("TRIANGLE (width=7, height=5):")
    print(art.draw_triangle(7, 5, "+"))
    print()

    print("PYRAMID (height=4):")
    print(art.draw_pyramid(4, "$"))
    print()
