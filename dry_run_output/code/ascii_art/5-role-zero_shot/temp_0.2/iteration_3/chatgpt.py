
"""
ascii_art.py

A console-based ASCII Art generator adhering to ISO/IEC 25010 quality standards.
Implements high-quality and maintainable OOP using Python.

Author: [Your Name]
Date: [Date]
"""

import string


class AsciiArt:
    """
    A class to draw various 2D ASCII art shapes.

    Shapes include:
      - Square
      - Rectangle
      - Parallelogram
      - Right-angled Triangle
      - Pyramid

    All outputs are "returned" as multi-line strings.
    """

    def _validate_positive_int(self, value, name):
        """
        Validate that the given value is a positive integer (>= 1).

        :param value: Integer to validate
        :param name: Name of the parameter (for error messages)
        :raises ValueError: If value is not a positive integer
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        if value < 1:
            raise ValueError(f"{name} must be >= 1")

    def _validate_symbol(self, symbol):
        """
        Validate that the given symbol is a single printable, non-whitespace character.

        :param symbol: Symbol to validate
        :raises ValueError: If symbol is invalid
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError("symbol must be a single printable, non-whitespace character")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square.

        :param width: The width (and height) of the square (>=1)
        :param symbol: A single printable non-whitespace character
        :return: A multi-line string representing the square
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        row = symbol * width
        art = "\n".join([row for _ in range(width)])
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle.

        :param width: The width of the rectangle (>=1)
        :param height: The height of the rectangle (>=1)
        :param symbol: A single printable non-whitespace character
        :return: A multi-line string representing the rectangle
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        art = "\n".join([row for _ in range(height)])
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram.

        Each row is shifted by one space to the right, starting from zero.
        :param width: The width of the parallelogram (>=1)
        :param height: The height of the parallelogram (>=1)
        :param symbol: A single printable non-whitespace character
        :return: A multi-line string representing the parallelogram
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = [
            (' ' * i) + (symbol * width)
            for i in range(height)
        ]
        art = "\n".join(lines)
        return art

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle.

        The triangle grows both in width and height from the top-left
        corner, expanding exponentially to the right (row i has width = proportional to i).

        The base line is as long as width.
        :param width: The base width of the triangle (>=1)
        :param height: The height of the triangle (>=1)
        :param symbol: A single printable non-whitespace character
        :return: A multi-line string representing the triangle
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Linear interpolation to determine filled length for each row
            # Ensure at least 1 symbol per row
            line_len = max(1, (width * (i + 1)) // height)
            lines.append(symbol * line_len)
        art = "\n".join(lines)
        return art

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid.

        :param height: The height of the pyramid (>=1)
        :param symbol: A single printable non-whitespace character
        :return: A multi-line string representing the pyramid
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        width = 2 * height - 1
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = (width - num_symbols) // 2
            line = (' ' * num_spaces) + (symbol * num_symbols) + (' ' * num_spaces)
            lines.append(line)
        art = "\n".join(lines)
        return art


if __name__ == "__main__":
    # Basic demonstration and test cases
    art = AsciiArt()

    print("Square (width=5, symbol='#'):")
    print(art.draw_square(5, '#'))
    print()

    print("Rectangle (width=7, height=3, symbol='*'):")
    print(art.draw_rectangle(7, 3, '*'))
    print()

    print("Parallelogram (width=5, height=4, symbol='@'):")
    print(art.draw_parallelogram(5, 4, '@'))
    print()

    print("Right-angled Triangle (width=7, height=4, symbol='&'):")
    print(art.draw_triangle(7, 4, '&'))
    print()

    print("Pyramid (height=5, symbol='A'):")
    print(art.draw_pyramid(5, 'A'))
    print()

    # Validation test (should raise ValueError)
    try:
        art.draw_square(4, ' ')
    except Exception as e:
        print("Error (expected):", e)

    try:
        art.draw_rectangle(-2, 3, 'X')
    except Exception as e:
        print("Error (expected):", e)

    try:
        art.draw_triangle(5, 3, '**')
    except Exception as e:
        print("Error (expected):", e)
