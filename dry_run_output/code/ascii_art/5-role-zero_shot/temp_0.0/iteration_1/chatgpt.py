
"""
ascii_art.py

A console-based 2D ASCII Art application.

Implements the AsciiArt class for drawing various ASCII shapes, adhering to
ISO/IEC 25010 quality standards: correctness, performance, modularity, safety,
testability, readability, and documentation.

Author: [Your Name]
Date: [Date]
"""

from typing import Any


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Draws a filled square of given width using the specified symbol.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draws a filled rectangle of given width and height using the specified symbol.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draws a filled parallelogram (right-leaning) of given width and height.

    draw_triangle(width: int, height: int, symbol: str) -> str
        Draws a filled right-angled triangle (top-left right angle).

    draw_pyramid(height: int, symbol: str) -> str
        Draws a filled symmetrical pyramid of given height.
    """

    def __init__(self) -> None:
        """Initialize the AsciiArt class."""
        pass

    @staticmethod
    def _validate_positive_int(value: Any, name: str) -> int:
        """
        Validates that the value is a positive integer.

        Parameters
        ----------
        value : Any
            The value to validate.
        name : str
            The name of the parameter (for error messages).

        Returns
        -------
        int
            The validated positive integer.

        Raises
        ------
        TypeError
            If value is not an integer.
        ValueError
            If value is not positive.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")
        return value

    @staticmethod
    def _validate_symbol(symbol: Any) -> str:
        """
        Validates that the symbol is a single, non-whitespace printable character.

        Parameters
        ----------
        symbol : Any
            The symbol to validate.

        Returns
        -------
        str
            The validated symbol.

        Raises
        ------
        TypeError
            If symbol is not a string.
        ValueError
            If symbol is not a single, non-whitespace printable character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")
        return symbol

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Parameters
        ----------
        width : int
            The width (and height) of the square.
        symbol : str
            The symbol to use for drawing.

        Returns
        -------
        str
            The ASCII art square as a multi-line string.
        """
        width = self._validate_positive_int(width, "width")
        symbol = self._validate_symbol(symbol)
        # Each line is 'width' symbols
        line = symbol * width
        return '\n'.join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Parameters
        ----------
        width : int
            The width of the rectangle.
        height : int
            The height of the rectangle.
        symbol : str
            The symbol to use for drawing.

        Returns
        -------
        str
            The ASCII art rectangle as a multi-line string.
        """
        width = self._validate_positive_int(width, "width")
        height = self._validate_positive_int(height, "height")
        symbol = self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-leaning parallelogram.

        Each row is shifted by one space to the right.

        Parameters
        ----------
        width : int
            The width of the parallelogram.
        height : int
            The height of the parallelogram.
        symbol : str
            The symbol to use for drawing.

        Returns
        -------
        str
            The ASCII art parallelogram as a multi-line string.
        """
        width = self._validate_positive_int(width, "width")
        height = self._validate_positive_int(height, "height")
        symbol = self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = spaces + (symbol * width)
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left right angle).

        The triangle grows to the right and down.

        Parameters
        ----------
        width : int
            The base width of the triangle.
        height : int
            The height of the triangle.
        symbol : str
            The symbol to use for drawing.

        Returns
        -------
        str
            The ASCII art triangle as a multi-line string.
        """
        width = self._validate_positive_int(width, "width")
        height = self._validate_positive_int(height, "height")
        symbol = self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Calculate the number of symbols for this row
            # Linear interpolation: from 1 to width over height rows
            num_symbols = max(1, round((row + 1) * width / height))
            line = symbol * num_symbols
            lines.append(line)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid.

        Parameters
        ----------
        height : int
            The height of the pyramid.
        symbol : str
            The symbol to use for drawing.

        Returns
        -------
        str
            The ASCII art pyramid as a multi-line string.
        """
        height = self._validate_positive_int(height, "height")
        symbol = self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            lines.append(line)
        return '\n'.join(lines)


# Example usage and test cases (for demonstration and testability)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square (width=4, symbol='#'):\n")
    print(art.draw_square(4, '#'))
    print("\nRectangle (width=6, height=3, symbol='*'):\n")
    print(art.draw_rectangle(6, 3, '*'))
    print("\nParallelogram (width=5, height=4, symbol='@'):\n")
    print(art.draw_parallelogram(5, 4, '@'))
    print("\nTriangle (width=7, height=5, symbol='+'):\n")
    print(art.draw_triangle(7, 5, '+'))
    print("\nPyramid (height=5, symbol='^'):\n")
    print(art.draw_pyramid(5, '^'))
