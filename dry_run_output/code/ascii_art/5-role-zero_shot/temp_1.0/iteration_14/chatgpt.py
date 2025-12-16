
"""
ASCII Art Drawing Application

This module defines the AsciiArt class, which provides methods to draw various ASCII art shapes.
The implementation conforms to quality requirements of the ISO/IEC 25010 standard including 
correctness, performance, modularity, safety, testability, and readability.
"""

from typing import Any


class AsciiArt:
    """
    ASCII Art Generator Class

    Provides methods to generate filled ASCII shapes as multi-line strings.
    Includes input validation for safety and robustness.
    """

    def __init__(self) -> None:
        """
        Initializes the AsciiArt class.
        No state is kept—methods are pure functions.
        """
        pass

    @staticmethod
    def _validate_int(name: str, value: Any, minimum: int = 1) -> None:
        """
        Validates that an input value is an integer and >= minimum.

        Args:
            name (str): Parameter name (for error messages)
            value (Any): Value to check
            minimum (int): Minimum allowed value (inclusive)

        Raises:
            TypeError: If value is not int
            ValueError: If value < minimum
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < minimum:
            raise ValueError(f"{name} must be >= {minimum}.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates symbol input.

        Args:
            symbol (str): Symbol to check

        Raises:
            ValueError: If symbol is not single printable non-whitespace character
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a non-whitespace printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled ASCII square.

        Args:
            width (int): Side length (must be >= 1)
            symbol (str): Drawing symbol (one printable character)

        Returns:
            str: A multiline string with the square.
        """
        self._validate_int("width", width, 1)
        self._validate_symbol(symbol)

        line = symbol * width
        square = "\n".join(line for _ in range(width))
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled ASCII rectangle.

        Args:
            width (int): Rectangle width (must be >= 1)
            height (int): Rectangle height (must be >= 1)
            symbol (str): Drawing symbol

        Returns:
            str: Multiline string of rectangle
        """
        self._validate_int("width", width, 1)
        self._validate_int("height", height, 1)
        self._validate_symbol(symbol)

        line = symbol * width
        rectangle = "\n".join(line for _ in range(height))
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with symbol, each subsequent row
        indented by an additional space.

        Args:
            width (int): Parallelogram width
            height (int): Parallelogram height
            symbol (str): Symbol to fill

        Returns:
            str: Multiline string of parallelogram
        """
        self._validate_int("width", width, 1)
        self._validate_int("height", height, 1)
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            line = (" " * row) + (symbol * width)
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle, growing to the right from top-left.

        Each row increases in length from 1 up to width, but never exceeds height rows.

        Args:
            width (int): Maximum triangle base width
            height (int): Triangle height
            symbol (str): Drawing symbol

        Returns:
            str: Multiline string triangle
        """
        self._validate_int("width", width, 1)
        self._validate_int("height", height, 1)
        self._validate_symbol(symbol)

        lines = []
        # For best fill: the number of symbols per row
        for row in range(height):
            num_symbols = min(width, row + 1)
            line = symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a centered, symmetrical pyramid.

        Args:
            height (int): Pyramid height (must be >= 1)
            symbol (str): Drawing symbol

        Returns:
            str: Multiline string pyramid
        """
        self._validate_int("height", height, 1)
        self._validate_symbol(symbol)

        lines = []
        base_width = height * 2 - 1  # Pyramid base width
        for row in range(height):
            num_symbols = 1 + 2 * row
            num_spaces = (base_width - num_symbols) // 2
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


# Example usage and testing
if __name__ == "__main__":
    aa = AsciiArt()
    print("SQUARE:")
    print(aa.draw_square(5, "#"))
    print("\nRECTANGLE:")
    print(aa.draw_rectangle(7, 3, "*"))
    print("\nPARALLELOGRAM:")
    print(aa.draw_parallelogram(5, 4, "$"))
    print("\nTRIANGLE:")
    print(aa.draw_triangle(6, 4, "+"))
    print("\nPYRAMID:")
    print(aa.draw_pyramid(4, "@"))
