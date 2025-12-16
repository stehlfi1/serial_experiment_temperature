
"""
ascii_art.py

A high-quality, maintainable Python module for generating 2D console-based ASCII art,
adhering to ISO/IEC 25010 standards for correctness, performance, safety, modularity, 
testability, and documentation.

Author: [Your Name]
"""

from typing import Any


class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    Each drawing method returns a multi-line string representation of the shape.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Draw a filled square of the given width using the symbol.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draw a filled rectangle.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draw a filled parallelogram (right-leaning).

    draw_triangle(width: int, height: int, symbol: str) -> str
        Draw a filled right-angled triangle.

    draw_pyramid(height: int, symbol: str) -> str
        Draw a filled, symmetrical pyramid.
    """

    def __init__(self) -> None:
        """Initialize the AsciiArt class. No state is stored."""
        pass

    @staticmethod
    def _validate_positive_integer(value: Any, name: str) -> None:
        """
        Validate that a value is a positive integer.

        Parameters
        ----------
        value : Any
            The value to check.
        name : str
            Name of the parameter (for error messaging).

        Raises
        ------
        TypeError
            If value is not an integer.
        ValueError
            If value is less than 1.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 1:
            raise ValueError(f"{name} must be a positive integer greater than 0.")

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Validate that symbol is a single, printable, non-whitespace character.

        Parameters
        ----------
        symbol : Any
            The character to check.

        Raises
        ------
        TypeError
            If symbol is not a string.
        ValueError
            If symbol is not a single character or is not printable or is whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square of given width using the symbol.

        Parameters
        ----------
        width : int
            The width and height of the square (>0).
        symbol : str
            A single, printable, non-whitespace character to use.

        Returns
        -------
        str
            Multiline string representing the ASCII art square.
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)

        line = symbol * width
        art = "\n".join([line for _ in range(width)])
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the symbol.

        Parameters
        ----------
        width : int
            Width of the rectangle (>0).
        height : int
            Height of the rectangle (>0).
        symbol : str
            Single, printable, non-whitespace character.

        Returns
        -------
        str
            Multiline string representing the ASCII art rectangle.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        line = symbol * width
        art = "\n".join([line for _ in range(height)])
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram (right-leaning upward to the right).

        Parameters
        ----------
        width : int
            The width of the parallelogram base (>0).
        height : int
            The height (>0).
        symbol : str
            Single, printable, non-whitespace character.

        Returns
        -------
        str
            Multiline string for the parallelogram.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            lines.append(" " * row + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle (right angle at the top-left).

        Parameters
        ----------
        width : int
            The base width of the triangle (>0).
        height : int
            The triangle's height (>0).
        symbol : str
            Single, printable, non-whitespace character.

        Returns
        -------
        str
            Multiline string of the triangle.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Calculate the length for this row (linearly interpolate between width and 1)
            current_width = max(1, round(width * (height - row) / height))
            lines.append(symbol * current_width)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled, symmetrical pyramid of the given height.

        Parameters
        ----------
        height : int
            The pyramid's height (>0).
        symbol : str
            Single, printable, non-whitespace character.

        Returns
        -------
        str
            Multiline string of the pyramid.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Each row: spaces + symbols + spaces
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            lines.append(" " * num_spaces + symbol * num_symbols + " " * num_spaces)
        return "\n".join(lines)


# ========== Simple Test Cases for Demonstration ==========

if __name__ == "__main__":
    art = AsciiArt()
    print("Square (size 4, '*'):\n")
    print(art.draw_square(4, "*"))
    print("\nRectangle (4 x 2, '#'):\n")
    print(art.draw_rectangle(4, 2, "#"))
    print("\nParallelogram (5 x 3, '+'):\n")
    print(art.draw_parallelogram(5, 3, "+"))
    print("\nTriangle (width 5, height 4, '@'):\n")
    print(art.draw_triangle(5, 4, "@"))
    print("\nPyramid (height 4, '$'):\n")
    print(art.draw_pyramid(4, "$"))
