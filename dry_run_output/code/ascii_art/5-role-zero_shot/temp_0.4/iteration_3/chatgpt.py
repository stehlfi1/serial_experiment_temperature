
"""
ascii_art.py

A console-based ASCII Art drawing application implemented in Python, adhering to ISO/IEC 25010 quality requirements.
Provides high-quality, maintainable code using OOP and proper input validation.

Author: Senior Software Developer
"""

from typing import Any


class AsciiArt:
    """
    AsciiArt
    ========
    Provides methods to generate strings representing various 2D ASCII art shapes.

    Each method returns a multi-line string representation of the shape using a single, valid, printable symbol.
    """

    def __init__(self) -> None:
        """Initialize the ASCII Art class. No state is retained."""
        pass

    @staticmethod
    def _validate_symbol(symbol: Any) -> str:
        """Validate that symbol is a single printable, non-whitespace character."""
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")
        return symbol

    @staticmethod
    def _validate_positive_integer(value: Any, name: str) -> int:
        """Validate that value is a positive integer > 0, for parameters like width and height."""
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer (greater than 0).")
        return value

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using symbol.

        :param width: The width and height of the square (must be positive integer)
        :param symbol: Single, printable, non-whitespace character
        :return: Multi-line string of the square
        """
        w = self._validate_positive_integer(width, "width")
        s = self._validate_symbol(symbol)
        line = s * w
        art = '\n'.join([line for _ in range(w)])
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height using symbol.

        :param width: The width of the rectangle (must be positive integer)
        :param height: The height of the rectangle (must be positive integer)
        :param symbol: Single, printable, non-whitespace character
        :return: Multi-line string of the rectangle
        """
        w = self._validate_positive_integer(width, "width")
        h = self._validate_positive_integer(height, "height")
        s = self._validate_symbol(symbol)
        line = s * w
        art = '\n'.join([line for _ in range(h)])
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that grows diagonally to the right,
        starting from the top left corner (each row is shifted by one space).

        :param width: The width of the parallelogram (must be positive integer)
        :param height: The height of the parallelogram (must be positive integer)
        :param symbol: Single, printable, non-whitespace character
        :return: Multi-line string of the parallelogram
        """
        w = self._validate_positive_integer(width, "width")
        h = self._validate_positive_integer(height, "height")
        s = self._validate_symbol(symbol)
        lines = []
        for row in range(h):
            lines.append(' ' * row + s * w)
        art = '\n'.join(lines)
        return art

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle, aligned to top-left and
        growing to the right, with given width and height.

        Each row's length is linearly interpolated between 1 and width
        over height rows.

        :param width: The width of the triangle's base (must be positive integer)
        :param height: The height of the triangle (must be positive integer)
        :param symbol: Single, printable, non-whitespace character
        :return: Multi-line string of the triangle
        """
        w = self._validate_positive_integer(width, "width")
        h = self._validate_positive_integer(height, "height")
        s = self._validate_symbol(symbol)
        lines = []
        for row in range(h):
            # Compute current row width proportionally (ceil of linear scale)
            if h == 1:
                current_width = w
            else:
                current_width = max(1, ((w - 1) * row // (h - 1)) + 1)
            lines.append(s * current_width)
        art = '\n'.join(lines)
        return art

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid (isosceles triangle) of given height.

        :param height: The height of the pyramid (must be positive integer)
        :param symbol: Single, printable, non-whitespace character
        :return: Multi-line string of the pyramid
        """
        h = self._validate_positive_integer(height, "height")
        s = self._validate_symbol(symbol)
        lines = []
        for row in range(h):
            num_symbols = (row * 2) + 1
            spaces = h - row - 1
            line = ' ' * spaces + s * num_symbols + ' ' * spaces
            lines.append(line)
        art = '\n'.join(lines)
        return art


if __name__ == '__main__':
    # Example usages; acts as a basic test/demo
    art = AsciiArt()
    print("--- Square ---")
    print(art.draw_square(4, '#'))
    print("\n--- Rectangle ---")
    print(art.draw_rectangle(5, 2, '*'))
    print("\n--- Parallelogram ---")
    print(art.draw_parallelogram(5, 4, '+'))
    print("\n--- Triangle ---")
    print(art.draw_triangle(5, 4, '@'))
    print("\n--- Pyramid ---")
    print(art.draw_pyramid(3, '$'))
