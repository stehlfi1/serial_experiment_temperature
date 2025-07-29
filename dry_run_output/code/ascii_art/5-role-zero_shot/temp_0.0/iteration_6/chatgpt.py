
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

    Provides methods to draw square, rectangle, parallelogram, right-angled triangle,
    and pyramid using a single printable symbol.
    """

    def __init__(self) -> None:
        """Initialize the AsciiArt class."""
        pass

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single, non-whitespace printable character.

        Raises:
            ValueError: If the symbol is invalid.
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
        """
        Validate that the value is a positive integer.

        Args:
            value: The value to check.
            name: The name of the parameter (for error messages).

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square of given width using the specified symbol.

        Args:
            width: The width (and height) of the square.
            symbol: The symbol to use for drawing.

        Returns:
            A multi-line string representing the square.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        line = symbol * width
        square = [line for _ in range(width)]
        return "\n".join(square)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle of given width and height using the specified symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The symbol to use for drawing.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        line = symbol * width
        rectangle = [line for _ in range(height)]
        return "\n".join(rectangle)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram (right-leaning) of given width and height.

        Each row is shifted by one space to the right, starting from the top.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The symbol to use for drawing.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        parallelogram = []
        for row in range(height):
            spaces = " " * row
            line = spaces + (symbol * width)
            parallelogram.append(line)
        return "\n".join(parallelogram)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle (top-left right angle).

        The triangle grows diagonally to the right, starting from the top-left corner.

        Args:
            width: The base width of the triangle.
            height: The height of the triangle.
            symbol: The symbol to use for drawing.

        Returns:
            A multi-line string representing the triangle.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        triangle = []
        for row in range(height):
            # Calculate the number of symbols for this row
            # The last row should have width symbols
            # The first row should have at least 1 symbol
            # Linear interpolation between 1 and width over height rows
            if height == 1:
                num_symbols = width
            else:
                num_symbols = max(1, (width * (row + 1)) // height)
            line = symbol * num_symbols
            triangle.append(line)
        return "\n".join(triangle)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid of given height.

        Args:
            height: The height of the pyramid.
            symbol: The symbol to use for drawing.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        pyramid = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = (" " * num_spaces) + (symbol * num_symbols) + (" " * num_spaces)
            pyramid.append(line)
        return "\n".join(pyramid)


# Example usage and test cases (for demonstration and testability)
if __name__ == "__main__":
    art = AsciiArt()

    print("Square (width=4, symbol='#'):")
    print(art.draw_square(4, '#'))
    print()

    print("Rectangle (width=6, height=3, symbol='*'):")
    print(art.draw_rectangle(6, 3, '*'))
    print()

    print("Parallelogram (width=5, height=4, symbol='@'):")
    print(art.draw_parallelogram(5, 4, '@'))
    print()

    print("Right-angled Triangle (width=7, height=5, symbol='+'):")
    print(art.draw_triangle(7, 5, '+'))
    print()

    print("Pyramid (height=5, symbol='^'):")
    print(art.draw_pyramid(5, '^'))
    print()
