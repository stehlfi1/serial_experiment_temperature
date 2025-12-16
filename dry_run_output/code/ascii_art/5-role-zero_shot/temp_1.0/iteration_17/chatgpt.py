
"""
ascii_art.py

A console-based ASCII Art application using OOP principles,
designed per ISO/IEC 25010 quality requirements.

Author: [Your Name]
Date: [Today's Date]
"""

from typing import Any


class AsciiArt:
    """
    A class to generate 2D ASCII Art shapes as multi-line strings.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str:
        Returns a filled square ASCII art of given width and symbol.
    draw_rectangle(width: int, height: int, symbol: str) -> str:
        Returns a filled rectangle ASCII art of given dimensions and symbol.
    draw_parallelogram(width: int, height: int, symbol: str) -> str:
        Returns a filled right-leaning parallelogram ASCII art.
    draw_triangle(width: int, height: int, symbol: str) -> str:
        Returns a filled right-angled triangle (top-left corner) ASCII art.
    draw_pyramid(height: int, symbol: str) -> str:
        Returns a filled symmetrical pyramid of given height and symbol.
    """

    def _validate_positive_integer(self, value: Any, arg_name: str) -> None:
        """
        Validates that a given value is a positive integer.
        Raises TypeError or ValueError as appropriate.
        """
        if not isinstance(value, int):
            raise TypeError(f"{arg_name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{arg_name} must be a positive integer.")

    def _validate_symbol(self, symbol: Any) -> None:
        """
        Validates that symbol is a single, printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square with the given width and symbol.

        Parameters
        ----------
        width : int
            The length of the square sides (must be positive).
        symbol : str
            The symbol to fill the square (single printable character).

        Returns
        -------
        str
            A multi-line string representing the square.
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)

        line = symbol * width
        return "\n".join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width, height, and symbol.

        Parameters
        ----------
        width : int
            The width of the rectangle (must be positive).
        height : int
            The height of the rectangle (must be positive).
        symbol : str
            The symbol to fill the rectangle (single printable character).

        Returns
        -------
        str
            Multi-line string representing the rectangle.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        line = symbol * width
        return "\n".join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, right-leaning, with given width and height.

        Parameters
        ----------
        width : int
            The width of the parallelogram (must be positive).
        height : int
            The height of the parallelogram (must be positive).
        symbol : str
            The symbol to fill the parallelogram (single printable character).

        Returns
        -------
        str
            Multi-line string representing the parallelogram.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left corner is the right angle).

        Parameters
        ----------
        width : int
            The width (base) of the triangle (must be positive).
        height : int
            The height of the triangle (must be positive).
        symbol : str
            The symbol to fill the triangle (single printable character).

        Returns
        -------
        str
            Multi-line string representing the triangle.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Each row is filled incrementally: base on proportion of width to height
            chars_this_row = max(1, (width * (height - row)) // height)
            line = symbol * chars_this_row
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid of given height and symbol.

        Parameters
        ----------
        height : int
            The height of the pyramid (must be positive).
        symbol : str
            The symbol to fill the pyramid (single printable character).

        Returns
        -------
        str
            Multi-line string representing the pyramid.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            spaces = height - i - 1
            symbols = 2 * i + 1
            line = " " * spaces + symbol * symbols + " " * spaces
            lines.append(line)
        return "\n".join(lines)


# Example usage or test code (for manual testing only, not part of module interface)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n", art.draw_square(5, '#'), sep='')
    print("\nRectangle:\n", art.draw_rectangle(6, 3, '*'), sep='')
    print("\nParallelogram:\n", art.draw_parallelogram(5, 4, '+'), sep='')
    print("\nTriangle:\n", art.draw_triangle(7, 5, 'X'), sep='')
    print("\nPyramid:\n", art.draw_pyramid(4, 'O'), sep='')
