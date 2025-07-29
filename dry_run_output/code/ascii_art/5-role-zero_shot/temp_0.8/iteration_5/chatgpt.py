
"""
ascii_art.py

A high-quality, maintainable ASCII Art generator adhering to ISO/IEC 25010 quality attributes.
Implements methods for drawing various ASCII shapes in a console application.
"""

from typing import Any


class AsciiArt:
    """
    AsciiArt provides methods to generate ASCII art shapes.
    Each method returns a multi-line string representing the drawn shape.

    Shapes provided:
        - draw_square
        - draw_rectangle
        - draw_parallelogram
        - draw_triangle
        - draw_pyramid
    """

    def __init__(self) -> None:
        """Initialize AsciiArt instance. No state is maintained."""
        pass

    @staticmethod
    def _validate_positive_int(value: Any, name: str) -> int:
        """
        Validate that the provided value is a positive integer.
        :param value: The value to validate.
        :param name: The variable name (for error message).
        :return: The validated positive integer.
        :raises TypeError: If value is not an int.
        :raises ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 1:
            raise ValueError(f"{name} must be a positive integer (>= 1).")
        return value

    @staticmethod
    def _validate_symbol(symbol: Any) -> str:
        """
        Validate that the symbol is a single printable non-whitespace character.
        :param symbol: The symbol to validate.
        :return: The validated symbol as a string.
        :raises TypeError: If symbol is not a string.
        :raises ValueError: If symbol is not a single, printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("symbol must be a printable character.")
        return symbol

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square of given width with the provided symbol.
        :param width: The width (and height) of the square.
        :param symbol: The symbol to use.
        :return: The ASCII art as a string.
        """
        width = self._validate_positive_int(width, "width")
        symbol = self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(width)]
        return '\n'.join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle of given width and height with the provided symbol.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :param symbol: The symbol to use.
        :return: The ASCII art as a string.
        """
        width = self._validate_positive_int(width, "width")
        height = self._validate_positive_int(height, "height")
        symbol = self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return '\n'.join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled left-aligned parallelogram (each row shifted right by one space).
        :param width: The width of the parallelogram.
        :param height: The height of the parallelogram.
        :param symbol: The symbol to use.
        :return: The ASCII art as a string.
        """
        width = self._validate_positive_int(width, "width")
        height = self._validate_positive_int(height, "height")
        symbol = self._validate_symbol(symbol)
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle (right angle at top-left, grows right and down).
        :param width: The width (base) of the triangle.
        :param height: The height of the triangle.
        :param symbol: The symbol to use.
        :return: The ASCII art as a string.
        """
        width = self._validate_positive_int(width, "width")
        height = self._validate_positive_int(height, "height")
        symbol = self._validate_symbol(symbol)
        lines = []
        # For each row, calculate the number of symbols: proportional to row/height
        for row in range(height):
            # Ensure the base is exactly 'width' wide at the bottom row
            num_symbols = max(1, round((row + 1) * width / height))
            if num_symbols > width:
                num_symbols = width
            lines.append(symbol * num_symbols)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid with given height.
        :param height: The height of the pyramid.
        :param symbol: The symbol to use.
        :return: The ASCII art as a string.
        """
        height = self._validate_positive_int(height, "height")
        symbol = self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Number of symbols in the row: 1, 3, 5, ... (2*i+1)
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            line = (' ' * num_spaces) + (symbol * num_symbols) + (' ' * num_spaces)
            lines.append(line)
        return '\n'.join(lines)


# Example usage (for testing):
if __name__ == '__main__':
    art = AsciiArt()
    print("Square:\n" + art.draw_square(5, "#"))
    print("\nRectangle:\n" + art.draw_rectangle(7, 3, "*"))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, "$"))
    print("\nTriangle:\n" + art.draw_triangle(7, 5, "@"))
    print("\nPyramid:\n" + art.draw_pyramid(5, "X"))
