
"""
ascii_art.py -- Console-based 2D ASCII Art application

This module defines the AsciiArt class to generate ASCII representations
of common 2D shapes. Compliant with high code quality standards (ISO/IEC 25010).
"""

import string


class AsciiArt:
    """
    Provides methods for drawing various 2D ASCII art shapes.

    Public methods:
        - draw_square(width: int, symbol: str) -> str
        - draw_rectangle(width: int, height: int, symbol: str) -> str
        - draw_parallelogram(width: int, height: int, symbol: str) -> str
        - draw_triangle(width: int, height: int, symbol: str) -> str
        - draw_pyramid(height: int, symbol: str) -> str
    """

    def __init__(self):
        pass

    # ----------------
    # Validations
    # ----------------
    def _validate_int(self, value: int, name: str, min_value: int = 1):
        """Validate that an integer value is >= min_value."""
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < min_value:
            raise ValueError(f"{name} must be >= {min_value}.")

    def _validate_symbol(self, symbol: str):
        """
        Validate the drawing symbol.
        Requirements:
          - Must be exactly 1 character
          - Must be a printable, non-whitespace character
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if symbol not in string.printable or symbol in string.whitespace:
            raise ValueError("Symbol must be a printable, non-whitespace character.")

    # -----------------------------------
    # ASCII Art Drawing Implementations
    # -----------------------------------

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using symbol.
        Raises ValueError for invalid arguments.
        """
        self._validate_int(width, "Width")
        self._validate_symbol(symbol)

        art_lines = [symbol * width for _ in range(width)]
        return '\n'.join(art_lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given dimensions using symbol.
        Raises ValueError for invalid arguments.
        """
        self._validate_int(width, "Width")
        self._validate_int(height, "Height")
        self._validate_symbol(symbol)

        art_lines = [symbol * width for _ in range(height)]
        return '\n'.join(art_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram (rightward, top-left start) using symbol.
        Each subsequent row is shifted by one space to the right.
        Raises ValueError for invalid arguments.
        """
        self._validate_int(width, "Width")
        self._validate_int(height, "Height")
        self._validate_symbol(symbol)

        art_lines = []
        for row in range(height):
            line = ' ' * row + symbol * width
            art_lines.append(line)
        return '\n'.join(art_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle (top-left at [0,0]) using symbol.
        Grows to the right and downward.
        Each row has at most 'width' symbols; fills height rows.

        The triangle's first row is 1 symbol wide, the last is min(width, height) wide.
        """
        self._validate_int(width, "Width")
        self._validate_int(height, "Height")
        self._validate_symbol(symbol)

        art_lines = []
        max_cols = min(width, height)
        for row in range(height):
            row_width = min(row + 1, max_cols)
            art_lines.append(symbol * row_width)
        return '\n'.join(art_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a centered, symmetrical pyramid of given height using symbol.
        Base is 2*height-1 symbols wide. Each row centered with respect to base.
        """
        self._validate_int(height, "Height")
        self._validate_symbol(symbol)

        art_lines = []
        base_width = (2 * height) - 1
        for row in range(height):
            num_symbols = (2 * row) + 1
            num_spaces = height - row - 1
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            art_lines.append(line)
        return '\n'.join(art_lines)

# ----------------------------------------------
# Example usages and basic testability (optional)
# ----------------------------------------------
if __name__ == "__main__":
    art = AsciiArt()
    # Sample test cases (can easily hook to an actual test suite!)
    print("SQUARE:\n" + art.draw_square(5, '#'), end="\n\n")
    print("RECTANGLE:\n" + art.draw_rectangle(7, 3, '*'), end="\n\n")
    print("PARALLELOGRAM:\n" + art.draw_parallelogram(5, 4, '@'), end="\n\n")
    print("TRIANGLE:\n" + art.draw_triangle(6, 4, '&'), end="\n\n")
    print("PYRAMID:\n" + art.draw_pyramid(4, '$'), end="\n\n")
