
"""
ascii_art.py

A maintainable, efficient, and testable module for generating 2D ASCII art shapes in the console,
following the ISO/IEC 25010:2011 standard for software quality.

Author: [Your Name]
"""

import string

class AsciiArt:
    """
    Provides methods for drawing various ASCII shapes.

    All methods perform input validation to ensure correct usage.

    Usage:
        art = AsciiArt()
        square = art.draw_square(5, "#")
        print(square)
    """

    def __init__(self):
        # No instance-level state needed, but class is kept for OOP extensibility.
        pass

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square shape using the specified width and symbol.

        :param width: Size of the square (must be >= 1)
        :param symbol: The symbol to fill the square with (single, printable, non-whitespace char)
        :return: Multiline string representing the square
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)
        # Square: equal width and height
        line = symbol * width
        return "\n".join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle shape.

        :param width: Width of the rectangle (must be >= 1)
        :param height: Height of the rectangle (must be >= 1)
        :param symbol: The symbol to fill the rectangle with
        :return: Multiline string
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-leaning parallelogram.

        :param width: Width of the parallelogram (must be >= 1)
        :param height: Height of the parallelogram (must be >= 1)
        :param symbol: The symbol to fill the parallelogram with
        :return: Multiline string
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            spaces = " " * row
            lines.append(f"{spaces}{symbol * width}")
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle (grows towards bottom-right).

        :param width: Maximum width of the triangle base (must be >= 1)
        :param height: Height of the triangle (must be >= 1)
        :param symbol: Fill symbol
        :return: Multiline string
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        # The number of symbols per row grows proportionally, but at least 1 per row.
        lines = []
        for row in range(height):
            # Compute how many symbols on this row
            # Distribute 'width' over 'height' steps (last row has 'width')
            num_symbols = max(1, round((row + 1) * width / height))
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a centered, symmetrical pyramid.

        :param height: Number of rows, the base width will be (2*height - 1)
        :param symbol: Fill symbol
        :return: Multiline string
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        width = 2 * height - 1  # Base width
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = (width - num_symbols) // 2
            lines.append(" " * num_spaces + symbol * num_symbols + " " * num_spaces)
        return "\n".join(lines)

    # ------------------- Static Validation Methods -------------------

    @staticmethod
    def _validate_positive_int(value: int, name: str):
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer (got {type(value).__name__})")
        if value < 1:
            raise ValueError(f"{name} must be >= 1 (got {value})")

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates that the symbol is a single, printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character")
        if symbol in string.whitespace:
            raise ValueError("symbol must not be a whitespace character")
        if not symbol.isprintable():
            raise ValueError("symbol must be printable")


# ------------------- Example Console Usage -------------------

if __name__ == "__main__":
    # Demonstrate usage (Testability)
    art = AsciiArt()
    print("SQUARE (width=5, symbol='*'):\n")
    print(art.draw_square(5, '*'))
    print("\nRECTANGLE (width=7, height=3, symbol='#'):\n")
    print(art.draw_rectangle(7, 3, '#'))
    print("\nPARALLELOGRAM (width=5, height=4, symbol='@'):\n")
    print(art.draw_parallelogram(5, 4, '@'))
    print("\nRIGHT-TRIANGLE (width=6, height=4, symbol='%'):\n")
    print(art.draw_triangle(6, 4, '%'))
    print("\nPYRAMID (height=5, symbol='+'):\n")
    print(art.draw_pyramid(5, '+'))
