
"""
ascii_art.py

A console-based ASCII Art application with OOP design. Provides methods to draw
various 2D shapes as ASCII art, following ISO/IEC 25010 requirements.

Author: [Your Name]
"""

import string

class AsciiArt:
    """
    AsciiArt class for drawing various 2D ASCII art shapes.

    Methods:
        - draw_square(width: int, symbol: str) -> str
        - draw_rectangle(width: int, height: int, symbol: str) -> str
        - draw_parallelogram(width: int, height: int, symbol: str) -> str
        - draw_triangle(width: int, height: int, symbol: str) -> str
        - draw_pyramid(height: int, symbol: str) -> str
    """

    def __init__(self):
        """Initializes the AsciiArt class (stateless)."""
        pass

    @staticmethod
    def _validate_positive_int(name: str, value: int) -> None:
        """Validate that value is an integer and greater than zero."""
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be positive (>= 1).")

    @staticmethod
    def _validate_single_printable_symbol(symbol: str) -> None:
        """Validate that symbol is a single printable non-whitespace character."""
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character.")
        if symbol not in string.printable or symbol.isspace():
            raise ValueError("symbol must be a non-whitespace printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using the specified symbol.

        Args:
            width (int): The width and height of the square (> 0).
            symbol (str): A 1-character printable symbol (not whitespace).

        Returns:
            str: Multiline ASCII art string representing the square.
        """
        self._validate_positive_int("width", width)
        self._validate_single_printable_symbol(symbol)

        line = symbol * width
        shape = "\n".join([line for _ in range(width)])
        return shape

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height using the symbol.

        Args:
            width (int): The rectangle's width (> 0).
            height (int): The rectangle's height (> 0).
            symbol (str): A 1-character printable symbol (not whitespace).

        Returns:
            str: Multiline ASCII art string representing the rectangle.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_single_printable_symbol(symbol)

        line = symbol * width
        shape = "\n".join([line for _ in range(height)])
        return shape

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-leaning parallelogram.

        Each line is shifted one space to the right from the line above.

        Args:
            width (int): The parallelogram's width (> 0).
            height (int): The parallelogram's height (> 0).
            symbol (str): A 1-character printable symbol (not whitespace).

        Returns:
            str: Multiline ASCII art string representing the parallelogram.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_single_printable_symbol(symbol)

        lines = []
        for row in range(height):
            spaces = " " * row
            art_line = spaces + (symbol * width)
            lines.append(art_line)
        shape = "\n".join(lines)
        return shape

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left corner) of given width and height.

        Each row i has number of symbols:
            n = min(width, 1 + floor((width - 1) * i / (height - 1)))
            for row i in [0, height-1]

        Args:
            width (int): The triangle's base width (> 0).
            height (int): The triangle's height (> 0).
            symbol (str): A 1-character printable symbol (not whitespace).

        Returns:
            str: Multiline ASCII art string representing the triangle.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_single_printable_symbol(symbol)

        lines = []
        for row in range(height):
            # Ensure last row is exactly width, first row >= 1
            if height == 1:
                num_syms = width
            else:
                # Linearly interpolate from 1 to width
                num_syms = 1 + (width - 1) * row // (height - 1)
            art_line = symbol * num_syms
            lines.append(art_line)
        shape = "\n".join(lines)
        return shape

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid of specified height.

        Maximum width at base is (2 * height - 1).

        Args:
            height (int): Height of the pyramid (> 0).
            symbol (str): A 1-character printable symbol (not whitespace).

        Returns:
            str: Multiline ASCII art string representing the pyramid.
        """
        self._validate_positive_int("height", height)
        self._validate_single_printable_symbol(symbol)

        lines = []
        for row in range(height):
            num_syms = 2 * row + 1
            spaces = " " * (height - row - 1)
            art_line = spaces + (symbol * num_syms) + spaces
            lines.append(art_line)
        shape = "\n".join(lines)
        return shape


# Example usage and testing (for demonstration purposes)
if __name__ == "__main__":
    art = AsciiArt()
    print("SQUARE:\n", art.draw_square(5, "#"), end="\n\n")
    print("RECTANGLE:\n", art.draw_rectangle(7, 3, "*"), end="\n\n")
    print("PARALLELOGRAM:\n", art.draw_parallelogram(5, 4, "@"), end="\n\n")
    print("TRIANGLE:\n", art.draw_triangle(5, 4, "$"), end="\n\n")
    print("PYRAMID:\n", art.draw_pyramid(3, "+"), end="\n")
