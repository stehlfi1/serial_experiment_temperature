
"""
ascii_art.py
============

A robust console-based ASCII art generator adhering to ISO/IEC 25010 quality standards.
Implements various shape-drawing utilities with comprehensive validation and documentation.

Author: [Your Name]
Date: [Today's Date]
"""

from typing import Any


class AsciiArt:
    """
    AsciiArt provides methods to generate filled ASCII shapes as strings.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Draws a solid square.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draws a solid rectangle.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draws a solid parallelogram (right-diagonally shifted).

    draw_triangle(width: int, height: int, symbol: str) -> str
        Draws a solid right-angled triangle (top-left right angle).

    draw_pyramid(height: int, symbol: str) -> str
        Draws a solid pyramid, centered horizontally.
    """

    def __init__(self) -> None:
        """
        Initializes the AsciiArt generator. No internal state required.
        """
        pass

    def _validate_symbol(self, symbol: Any) -> None:
        """
        Validates the symbol is a single, non-whitespace printable character.

        Raises
        ------
        TypeError
            If symbol is not str.
        ValueError
            If symbol is not a single, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")

    def _validate_positive_int(self, name: str, value: Any) -> None:
        """
        Validates that value is a positive integer.

        Raises
        ------
        TypeError
            If value is not an integer.
        ValueError
            If value is not positive.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Parameters
        ----------
        width : int
            The width and height of the square. Must be positive.
        symbol : str
            The single character to use to fill the square.

        Returns
        -------
        str
            The ASCII art of the square.

        Raises
        ------
        TypeError, ValueError
            If arguments are invalid.
        """
        self._validate_positive_int("width", width)
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Parameters
        ----------
        width : int
            Width of the rectangle. Must be positive.
        height : int
            Height of the rectangle. Must be positive.
        symbol : str
            The single character to use to fill the rectangle.

        Returns
        -------
        str
            The ASCII art of the rectangle.

        Raises
        ------
        TypeError, ValueError
            If arguments are invalid.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram.

        Each row shifts one space to the right relative to the row above.

        Parameters
        ----------
        width : int
            Width of the parallelogram. Must be positive.
        height : int
            Height of the parallelogram. Must be positive.
        symbol : str
            The single character to use to fill the parallelogram.

        Returns
        -------
        str
            The ASCII art of the parallelogram.

        Raises
        ------
        TypeError, ValueError
            If arguments are invalid.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            shift = " " * row
            line = shift + (symbol * width)
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left angle).

        The horizontal side grows to 'width', and the vertical side grows to 'height'.
        Each line's length is proportional: 
            For row y in 0..height-1, length = ceil((width * (y+1)) / height)

        Parameters
        ----------
        width : int
            The length of the triangle's base. Must be positive.
        height : int
            The height of the triangle. Must be positive.
        symbol : str
            The single character to use to fill the triangle.

        Returns
        -------
        str
            The ASCII art of the triangle.

        Raises
        ------
        TypeError, ValueError
            If arguments are invalid.
        """
        from math import ceil

        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        lines = []
        for row in range(1, height + 1):
            # Proportional row length:
            symbols_in_row = ceil(width * row / height)
            line = symbol * symbols_in_row
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled pyramid, centered horizontally.

        For row i in 0..n-1: leading spaces = (height-1)-i, then (2*i+1) symbols

        Parameters
        ----------
        height : int
            Pyramid height (number of rows). Must be positive.
        symbol : str
            The single character to use to fill the pyramid.

        Returns
        -------
        str
            The ASCII art of the pyramid.

        Raises
        ------
        TypeError, ValueError
            If arguments are invalid.
        """
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            line = spaces + symbols
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage and demonstration
    art = AsciiArt()

    # Test cases
    print("SQUARE (width=4, symbol='#')\n")
    print(art.draw_square(4, "#"))
    print("\nRECTANGLE (width=6, height=3, symbol='*')\n")
    print(art.draw_rectangle(6, 3, "*"))
    print("\nPARALLELOGRAM (width=5, height=4, symbol='@')\n")
    print(art.draw_parallelogram(5, 4, "@"))
    print("\nTRIANGLE (width=7, height=5, symbol='^')\n")
    print(art.draw_triangle(7, 5, "^"))
    print("\nPYRAMID (height=5, symbol='&')\n")
    print(art.draw_pyramid(5, "&"))
