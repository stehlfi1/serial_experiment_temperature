
"""
ascii_art.py

A console-based 2D ASCII Art application with an OOP design, meeting ISO/IEC 25010 quality requirements.
Implements drawing of filled ASCII shapes (square, rectangle, parallelogram, triangle, pyramid) with robust validation.
"""

from typing import Any


class AsciiArt:
    """
    ASCII Art generator for various 2D shapes.
    Provides methods to create shapes as multi-line strings using a user-specified symbol.
    """

    def __init__(self) -> None:
        """Initialize the ASCII art generator."""
        pass

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """Validate the symbol for drawing (must be a single, non-whitespace printable character).

        Raises:
            ValueError: if the symbol is not valid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_positive_int(value: Any, name: str) -> None:
        """Validate that the value is a positive integer.

        Args:
            value: Value to be checked.
            name: Name of the parameter (for error messages).

        Raises:
            ValueError: if the value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be positive (greater than 0).")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square with the given width and symbol.
        Args:
            width: The width and height of the square (must be positive integer).
            symbol: The symbol used to draw the square (single, printable, non-whitespace character).
        Returns:
            str: The square as a multi-line string.
        """
        self._validate_positive_int(width, "Width")
        self._validate_symbol(symbol)
        # Square: width x width symbols
        line = symbol * width
        return '\n'.join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle with the given width, height and symbol.
        Args:
            width: Width of the rectangle (must be positive integer).
            height: Height of the rectangle (must be positive integer).
            symbol: The symbol used to draw the rectangle (single character).
        Returns:
            str: The rectangle as a multi-line string.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram (each row shifted right by one space).
        Args:
            width: Number of symbols in each row (positive integer).
            height: Number of rows (positive integer).
            symbol: The symbol used to draw the shape (single character).
        Returns:
            str: The parallelogram as a multi-line string.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            spaces = ' ' * i
            line = spaces + (symbol * width)
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle (grows to the right and down).
        Args:
            width: Width of the triangle's base (positive integer).
            height: Height of the triangle (positive integer).
            symbol: The symbol used to draw the shape (single character).
        Returns:
            str: The triangle as a multi-line string.
        Note:
            The right angle is at the top-left. Shape fills proportionally.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # The number of symbols per row increases downwards, capped at width
            row_length = max(1, (width * (i + 1)) // height)
            # Ensure that the last line is exactly 'width' long
            if i == height - 1:
                row_length = width
            lines.append(symbol * row_length)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a centered, filled, symmetrical pyramid of given height and symbol.
        Args:
            height: Number of rows, and also determines base width (positive integer).
            symbol: The symbol used to draw the shape (single character).
        Returns:
            str: The pyramid as a multi-line string.
        """
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            line = (' ' * num_spaces) + (symbol * num_symbols)
            lines.append(line)
        return '\n'.join(lines)


# Example testing code (not interactive, suitable for unit tests or direct use)
if __name__ == '__main__':
    art = AsciiArt()
    print('Square (width=4, #):')
    print(art.draw_square(4, '#'))
    print('\nRectangle (width=6, height=3, *):')
    print(art.draw_rectangle(6, 3, '*'))
    print('\nParallelogram (width=5, height=4, $):')
    print(art.draw_parallelogram(5, 4, '$'))
    print('\nRight-angled Triangle (width=5, height=4, &):')
    print(art.draw_triangle(5, 4, '&'))
    print('\nPyramid (height=5, @):')
    print(art.draw_pyramid(5, '@'))
