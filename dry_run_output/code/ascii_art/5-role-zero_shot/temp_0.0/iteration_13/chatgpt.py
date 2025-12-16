
"""
ascii_art.py
-------------
A console-based 2D ASCII ART application.
Implements the AsciiArt class with drawing methods according to ISO/IEC 25010 standards.

Author: Senior Software Developer
"""

import string


class AsciiArt:
    """
    AsciiArt provides methods for drawing various filled ASCII shapes.
    All methods validate input and return a multi-line string.
    """

    def __init__(self):
        pass  # Reserved for future extensibility

    @staticmethod
    def _validate_positive_integer(value: int, name: str):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer, got {value}.")

    @staticmethod
    def _validate_symbol(symbol: str):
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol in string.whitespace:
            raise ValueError("Symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square of given width using the specified symbol.
        :param width: Width (and height) of the square, positive integer.
        :param symbol: Single printable, non-whitespace character.
        :return: Multi-line string representing the square.
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle of given width and height using the specified symbol.
        :param width: Width of the rectangle, positive integer.
        :param height: Height of the rectangle, positive integer.
        :param symbol: Single printable, non-whitespace character.
        :return: Multi-line string representing the rectangle.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.
        Each line is shifted right by one additional space compared to the previous.
        :param width: Width of each line, positive integer.
        :param height: Total number of lines (height), positive integer.
        :param symbol: Single printable, non-whitespace character.
        :return: Multi-line string representing the parallelogram.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for shift in range(height):
            line = " " * shift + symbol * width
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle starting from the top-left corner,
        growing diagonally to the right.
        The width parameter is a maximum width (base), and height is total lines.
        The filled area increases per line.
        :param width: Base width (length of the bottom side), positive integer.
        :param height: Height of the triangle (number of lines), positive integer.
        :param symbol: Single printable, non-whitespace character.
        :return: Multi-line string representing the right-angled triangle.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(1, height + 1):
            filled = min(width, (row * width + height - 1) // height)
            # Ensures the triangle fills to width in the last row
            line = symbol * filled
            lines.append(line)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled, symmetrical pyramid of specified height.
        Every row is centered; the pyramid's base width is (2*height - 1).
        :param height: Height of pyramid (number of lines), positive integer.
        :param symbol: Single printable, non-whitespace character.
        :return: Multi-line string representing the pyramid.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        max_width = 2 * height - 1
        lines = []
        for row in range(height):
            filled = 2 * row + 1
            spaces = (max_width - filled) // 2
            line = " " * spaces + symbol * filled + " " * spaces
            lines.append(line)
        return '\n'.join(lines)


# Example usage (for easy testing/demonstration, remove or comment this when importing as a module):
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n", art.draw_square(5, "#"))
    print("\nRectangle:\n", art.draw_rectangle(8, 3, "*"))
    print("\nParallelogram:\n", art.draw_parallelogram(6, 4, "+"))
    print("\nRight-angled Triangle:\n", art.draw_triangle(7, 5, "@"))
    print("\nPyramid:\n", art.draw_pyramid(4, "$"))
