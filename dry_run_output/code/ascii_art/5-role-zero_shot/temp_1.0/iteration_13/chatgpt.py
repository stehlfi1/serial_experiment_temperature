
"""
ASCII Art Generator Module

This module provides an `AsciiArt` class, which supports methods to generate
various 2D ASCII art shapes (square, rectangle, parallelogram, right-angled triangle, pyramid) 
using a single printable symbol.

Adheres to ISO/IEC 25010 quality standards in correctness, modularity, safety, performance, 
testability, and maintainability.
"""

import string


class AsciiArt:
    """
    Class for generating 2D ASCII art shapes.
    Includes input validation and produces multi-line string shapes.
    """

    def __init__(self):
        pass  # No mutable state required

    @staticmethod
    def _validate_positive_integer(value, name):
        """
        Validates that a value is a positive integer (>= 1).
        Raises ValueError if invalid.
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer (>= 1). Got {value}.")

    @staticmethod
    def _validate_symbol(symbol):
        """
        Validates a symbol: must be a single, non-whitespace, printable character.
        Raises ValueError or TypeError if invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if symbol not in string.printable or symbol in string.whitespace:
            raise ValueError("Symbol must be a printable, non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using the specified symbol.
        Returns a multi-line string.
        """
        self._validate_positive_integer(width, 'width')
        self._validate_symbol(symbol)

        line = symbol * width
        return '\n'.join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of width x height using the specified symbol.
        Returns a multi-line string.
        """
        self._validate_positive_integer(width, 'width')
        self._validate_positive_integer(height, 'height')
        self._validate_symbol(symbol)

        line = symbol * width
        return '\n'.join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram of given width and height.
        Each successive row is indented one more space to the right.
        Returns a multi-line string.
        """
        self._validate_positive_integer(width, 'width')
        self._validate_positive_integer(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            indent = ' ' * row
            lines.append(f"{indent}{symbol * width}")
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle with the right angle at the top-left.
        Grows diagonally to the right and down.
        Returns a multi-line string.
        """
        self._validate_positive_integer(width, 'width')
        self._validate_positive_integer(height, 'height')
        self._validate_symbol(symbol)

        # Determine maximum "base" width per row
        lines = []
        for row in range(height):
            # Compute the desired width for this row (proportional to height)
            curr_width = max(1, int(round(width * (height - row) / height)))
            lines.append(symbol * curr_width)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid with the given height.
        Returns a multi-line string.
        """
        self._validate_positive_integer(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        base_width = 2 * height - 1  # Odd width
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = (base_width - num_symbols) // 2
            lines.append(' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces)
        return '\n'.join(lines)


# Example usage (for testing/demo - remove or comment in production code)
if __name__ == '__main__':
    art = AsciiArt()
    print("SQUARE:\n", art.draw_square(5, '#'))
    print("\nRECTANGLE:\n", art.draw_rectangle(7, 3, '*'))
    print("\nPARALLELOGRAM:\n", art.draw_parallelogram(6, 4, '&'))
    print("\nTRIANGLE:\n", art.draw_triangle(8, 5, '%'))
    print("\nPYRAMID:\n", art.draw_pyramid(5, '$'))
