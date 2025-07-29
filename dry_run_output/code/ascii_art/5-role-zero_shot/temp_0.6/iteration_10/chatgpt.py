
"""
ascii_art.py

A modular, maintainable ASCII Art generator for console-based 2D shapes,
implemented according to ISO/IEC 25010 quality requirements.

Author: [Your Name]
"""

import string


class AsciiArt:
    """
    Provides methods to generate various ASCII art shapes as multi-line strings.
    All methods validate input and raise appropriate exceptions on invalid input.
    """

    def __init__(self):
        pass

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates that the symbol is a single, non-whitespace, printable character.
        Raises ValueError or TypeError on invalid input.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if symbol not in string.printable or not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_positive_int(value: int, name: str):
        """
        Validates that the value is a positive integer (>0).
        Raises ValueError or TypeError on invalid input.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of given width using the specified symbol.

        :param width: Width (and height) of the square (must be positive).
        :param symbol: Single printable character to fill the square.
        :return: A multi-line string representing the square.
        """
        self._validate_positive_int(width, "Width")
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of given width and height using the specified symbol.

        :param width: Width of the rectangle (must be positive).
        :param height: Height of the rectangle (must be positive).
        :param symbol: Single printable character to fill the rectangle.
        :return: A multi-line string representing the rectangle.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram of given width and height using the specified symbol.
        Each row is shifted right by one space compared to the previous row.

        :param width: Width of the parallelogram (must be positive).
        :param height: Height of the parallelogram (must be positive).
        :param symbol: Single printable character to fill the parallelogram.
        :return: A multi-line string representing the parallelogram.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            line = " " * row + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle (top-left right angle) of given width and height.
        Each row starts at the left and grows in length, up to the specified width.

        :param width: Width of the triangle's base (must be positive).
        :param height: Height of the triangle (must be positive).
        :param symbol: Single printable character to fill the triangle.
        :return: A multi-line string representing the triangle.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Compute number of symbols for this row (linear growth)
            # First row: at least 1, last row: width
            line_len = max(1, round((row + 1) * width / height))
            line_len = min(line_len, width)
            line = symbol * line_len
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of given height using the specified symbol.
        The base of the pyramid will have (2*height - 1) symbols.

        :param height: Height of the pyramid (must be positive).
        :param symbol: Single printable character to fill the pyramid.
        :return: A multi-line string representing the pyramid.
        """
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


# Example usage and basic tests
if __name__ == "__main__":
    art = AsciiArt()
    print("Square (width=4, symbol='#'):\n")
    print(art.draw_square(4, "#"))
    print("\nRectangle (width=5, height=3, symbol='*'):\n")
    print(art.draw_rectangle(5, 3, "*"))
    print("\nParallelogram (width=6, height=4, symbol='@'):\n")
    print(art.draw_parallelogram(6, 4, "@"))
    print("\nTriangle (width=5, height=4, symbol='+'):\n")
    print(art.draw_triangle(5, 4, "+"))
    print("\nPyramid (height=5, symbol='^'):\n")
    print(art.draw_pyramid(5, "^"))
