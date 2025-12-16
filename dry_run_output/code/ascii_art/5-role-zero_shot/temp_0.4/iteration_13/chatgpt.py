
"""
ascii_art.py

A console-based 2D ASCII ART application (OOP design) adhering to ISO/IEC 25010 principles
and Python best practices. All feature functions are in the AsciiArt class.
"""

import string


class AsciiArt:
    """
    Provides methods for generating various 2D ASCII shapes.

    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Returns a square of given width filled with the specified symbol.

        :param width: The width and height of the square (must be positive >0).
        :param symbol: A single visible, non-whitespace character.
        :return: Multi-line string representation of the square.
        :raises ValueError: On invalid width or symbol input.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)
        line = symbol * width
        # Each row contains 'width' symbols; there are 'width' rows
        return "\n".join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Returns a rectangle of given width and height filled with the symbol.

        :param width: Rectangle width (must be positive >0).
        :param height: Rectangle height (must be positive >0).
        :param symbol: A single visible, non-whitespace character.
        :return: Multi-line string representation of the rectangle.
        :raises ValueError: On invalid width/height or symbol.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Returns a parallelogram (rows each shifted right by one space).

        :param width: Parallelogram width (must be positive >0).
        :param height: Parallelogram height (must be positive >0).
        :param symbol: A single visible, non-whitespace character.
        :return: Multi-line string of the parallelogram.
        :raises ValueError: On invalid width/height or symbol.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        # Each row begins with i spaces then 'width' symbols
        rows = []
        for i in range(height):
            row = ' ' * i + symbol * width
            rows.append(row)
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Returns a right-angled triangle (top-left is right angle).

        :param width: Max triangle width (number of symbols in bottom row, >0).
        :param height: Number of triangle rows (must be positive >0).
        :param symbol: A single visible, non-whitespace character.
        :return: Multi-line string representation of the triangle.
        :raises ValueError: On invalid width/height or symbol.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        # Compute how much the width should grow at each step
        triangle_lines = []
        for i in range(height):
            # Progressively increase the number of symbols per row
            # Last row reaches width. Integer rounding for consistent fill
            num_symbols = max(1, (width * (i + 1)) // height)
            triangle_lines.append(symbol * num_symbols)
        return "\n".join(triangle_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Returns a symmetric pyramid with the given height.

        :param height: The number of rows in the pyramid (must be positive >0).
        :param symbol: A single visible, non-whitespace character.
        :return: Multi-line string representation of the pyramid.
        :raises ValueError: On invalid height or symbol.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        # Max width is (height * 2) - 1
        max_width = height * 2 - 1
        pyramid_rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            row = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            pyramid_rows.append(row)
        return "\n".join(pyramid_rows)

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates that symbol is a single, printable non-whitespace character.

        :param symbol: symbol to validate
        :raises ValueError: if symbol is invalid
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if symbol not in string.printable.strip():
            raise ValueError("Symbol must be a printable non-whitespace character.")

    @staticmethod
    def _validate_positive_int(value: int, arg_name: str):
        """
        Validates that a value is a positive integer (>0).
        :param value: int
        :param arg_name: argument name for error messaging
        :raises ValueError: if value is not > 0
        """
        if not isinstance(value, int):
            raise TypeError(f"{arg_name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{arg_name.capitalize()} must be a positive integer (>0).")


if __name__ == "__main__":
    # Minimal CLI for quick testing
    art = AsciiArt()
    print("Square (width=4, '*'):\n", art.draw_square(4, '*'), '\n')
    print("Rectangle (width=5, height=3, '#'):\n", art.draw_rectangle(5, 3, '#'), '\n')
    print("Parallelogram (width=5, height=4, '+'):\n", art.draw_parallelogram(5, 4, '+'), '\n')
    print("Triangle (width=6, height=4, '%'):\n", art.draw_triangle(6, 4, '%'), '\n')
    print("Pyramid (height=5, '@'):\n", art.draw_pyramid(5, '@'), '\n')
