
"""
ascii_art.py

A console-based 2D ASCII Art application adhering to ISO/IEC 25010 standards.
Implements shape-drawing functions within an OOP AsciiArt class, with robust input validation,
testability, readability, and maintainability.
"""

from typing import Any

class AsciiArt:
    """
    Class for generating ASCII art shapes.
    Provides methods for drawing squares, rectangles, parallelograms, triangles, and pyramids,
    using a specified single printable non-whitespace character.
    """

    def __init__(self) -> None:
        """
        Initializes an AsciiArt instance.
        """
        pass  # No state needed; methods are stateless

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace printable character.

        Raises:
            ValueError: If the symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_positive_int(value: Any, name: str) -> None:
        """
        Validates that the value is an integer >= 1.

        Raises:
            ValueError: If value is not a valid positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 1:
            raise ValueError(f"{name} must be >= 1.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of specified width with the chosen symbol.

        Args:
            width (int): The width and height of the square (>=1).
            symbol (str): The symbol to fill the square with (single, printable, non-whitespace).

        Returns:
            str: The ASCII art square as a multi-line string.
        """
        self._validate_positive_int(width, "Width")
        self._validate_symbol(symbol)

        row = symbol * width
        square = "\n".join([row for _ in range(width)])
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of specified width and height with the chosen symbol.

        Args:
            width (int): The width of the rectangle (>=1).
            height (int): The height of the rectangle (>=1).
            symbol (str): The symbol to fill the rectangle with (single, printable, non-whitespace).

        Returns:
            str: The ASCII art rectangle as a multi-line string.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)

        row = symbol * width
        rectangle = "\n".join([row for _ in range(height)])
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram of specified width and height, shifted right each row.

        Args:
            width (int): The width of the parallelogram (>=1).
            height (int): The height of the parallelogram (>=1).
            symbol (str): The symbol to fill the parallelogram with (single, printable, non-whitespace).

        Returns:
            str: The ASCII art parallelogram as a multi-line string.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)

        parallelogram_rows = []
        for row_idx in range(height):
            spaces = " " * row_idx
            symbols = symbol * width
            parallelogram_rows.append(f"{spaces}{symbols}")
        return "\n".join(parallelogram_rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left right angle), growing to the right.

        Args:
            width (int): The maximum width (base) of the triangle (>=1).
            height (int): The height of the triangle (>=1).
            symbol (str): The symbol to fill the triangle with (single, printable, non-whitespace).

        Returns:
            str: The ASCII art triangle as a multi-line string.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)

        triangle_rows = []
        for row_idx in range(height):
            # Calculate the number of symbols for this row (linear growth)
            # Ensures that the last row reaches 'width'
            row_symbols = max(1, round((row_idx + 1) * width / height))
            triangle_rows.append(symbol * row_symbols)
        return "\n".join(triangle_rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid of specified height.

        Args:
            height (int): The height of the pyramid (>=1).
            symbol (str): The symbol to fill the pyramid with (single, printable, non-whitespace).

        Returns:
            str: The ASCII art pyramid as a multi-line string.
        """
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)

        pyramid_rows = []
        for row_idx in range(height):
            num_symbols = 2 * row_idx + 1
            num_spaces = height - row_idx - 1
            row = (" " * num_spaces) + (symbol * num_symbols) + (" " * num_spaces)
            pyramid_rows.append(row)
        return "\n".join(pyramid_rows)


# --------------- Example Usage / Test Cases ----------------

if __name__ == "__main__":
    art = AsciiArt()

    print("Square (Width=4, Symbol='#'):\n")
    print(art.draw_square(4, '#'))
    print("\nRectangle (Width=6, Height=3, Symbol='*'):\n")
    print(art.draw_rectangle(6, 3, '*'))
    print("\nParallelogram (Width=5, Height=4, Symbol='$'):\n")
    print(art.draw_parallelogram(5, 4, '$'))
    print("\nRight-angled Triangle (Width=5, Height=4, Symbol='@'):\n")
    print(art.draw_triangle(5, 4, '@'))
    print("\nPyramid (Height=5, Symbol='^'):\n")
    print(art.draw_pyramid(5, '^'))
