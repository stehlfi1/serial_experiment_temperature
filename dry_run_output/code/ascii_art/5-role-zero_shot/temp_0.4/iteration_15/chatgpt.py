
"""
ascii_art.py

A console-based 2D ASCII Art application using OOP, compliant with ISO/IEC 25010 quality standards.
Implements drawing functions for basic shapes with robust input validation and high code quality.

Author: Senior Software Developer
"""

from typing import Optional

class AsciiArt:
    """
    Class providing methods to generate 2D ASCII art for various shapes.
    Methods return the shapes as multi-line strings.
    All drawing methods validate parameters for correctness and safety.
    """

    def __init__(self):
        pass

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single, non-whitespace printable character.

        Raises:
            ValueError: If validation fails.
        """
        if len(symbol) != 1:
            raise ValueError("The symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("The symbol cannot be whitespace.")
        if not symbol.isprintable():
            raise ValueError("The symbol must be printable.")

    @staticmethod
    def _validate_positive(value: int, name: str) -> None:
        """
        Validate that a value is a positive integer.

        Args:
            value: The value to check.
            name: Name of the parameter for error messages.

        Raises:
            ValueError: If validation fails.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width (and height) of the square
            symbol: The single character to use

        Returns:
            String representing the square.

        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_positive(width, "width")
        self._validate_symbol(symbol)

        row = symbol * width
        ascii_art = '\n'.join([row for _ in range(width)])
        return ascii_art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: Width of the rectangle
            height: Height of the rectangle
            symbol: The single character to use

        Returns:
            String representing the rectangle.

        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_positive(width, "width")
        self._validate_positive(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        ascii_art = '\n'.join([row for _ in range(height)])
        return ascii_art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram (each row is shifted right by 1 space from the above row).

        Args:
            width: Width of the parallelogram (number of symbols per row)
            height: Height of the parallelogram
            symbol: The single character to use

        Returns:
            String representing the parallelogram.

        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_positive(width, "width")
        self._validate_positive(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = f"{spaces}{symbol * width}"
            lines.append(line)
        ascii_art = '\n'.join(lines)
        return ascii_art

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle aligned to the top-left, growing downwards and rightwards.
        The base will be at most 'width' characters wide and 'height' tall.

        Args:
            width: Maximum width of the triangle's base
            height: Number of lines (height of the triangle)
            symbol: The single character to use

        Returns:
            String representing the triangle.

        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_positive(width, "width")
        self._validate_positive(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Calculate how many symbols per row (right-angled)
            num_syms = min(width, row + 1)
            lines.append(symbol * num_syms)
        ascii_art = '\n'.join(lines)
        return ascii_art

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the given height.

        Args:
            height: The number of rows in the pyramid
            symbol: The single character to use

        Returns:
            String representing the pyramid.

        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_positive(height, "height")
        self._validate_symbol(symbol)

        lines = []
        base_width = 2 * height - 1  # Pyramid is symmetrical
        for row in range(height):
            symbols = 2 * row + 1
            spaces = (base_width - symbols) // 2
            line = ' ' * spaces + symbol * symbols + ' ' * spaces
            lines.append(line)
        ascii_art = '\n'.join(lines)
        return ascii_art

# Example usage/testing code, can be placed under if __name__ == "__main__":
if __name__ == "__main__":
    art = AsciiArt()

    print("SQUARE:\n")
    print(art.draw_square(4, "#"), "\n")

    print("RECTANGLE:\n")
    print(art.draw_rectangle(6, 3, "*"), "\n")

    print("PARALLELOGRAM:\n")
    print(art.draw_parallelogram(5, 4, "@"), "\n")

    print("TRIANGLE:\n")
    print(art.draw_triangle(5, 4, "+"), "\n")

    print("PYRAMID:\n")
    print(art.draw_pyramid(5, "^"), "\n")
