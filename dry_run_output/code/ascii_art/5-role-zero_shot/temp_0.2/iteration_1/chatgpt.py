
"""
ascii_art.py

A console-based 2D ASCII ART generator implemented using OOP principles.
Adheres to ISO/IEC 25010 standards for maintainability, modularity,
and software quality.

Author: Senior Software Developer
"""

import string

class AsciiArt:
    """
    Class to generate console-based 2D ASCII art shapes.
    Provides methods to draw different shapes and ensures input validation.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using the specified symbol.

        Args:
            width (int): The width and height of the square (must be >=1).
            symbol (str): Single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the square.

        Raises:
            ValueError: If invalid arguments are provided.
        """
        self._validate_dimensions(width, 'width')
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(width)]
        return '\n'.join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width (int): The width of the rectangle (must be >=1).
            height (int): The height of the rectangle (must be >=1).
            symbol (str): Single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the rectangle.

        Raises:
            ValueError: If invalid arguments are provided.
        """
        self._validate_dimensions(width, 'width')
        self._validate_dimensions(height, 'height')
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return '\n'.join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram shape (slants right).

        Args:
            width (int): The width of the parallelogram (must be >=1).
            height (int): The height of the parallelogram (must be >=1).
            symbol (str): Single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the parallelogram.

        Raises:
            ValueError: If invalid arguments are provided.
        """
        self._validate_dimensions(width, 'width')
        self._validate_dimensions(height, 'height')
        self._validate_symbol(symbol)

        lines = [
            (' ' * i) + (symbol * width)
            for i in range(height)
        ]
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle. Each row increases by width/height.

        Args:
            width (int): The base width of the triangle (must be >=1).
            height (int): The height of the triangle (must be >=1).
            symbol (str): Single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the triangle.

        Raises:
            ValueError: If invalid arguments are provided.
        """
        self._validate_dimensions(width, 'width')
        self._validate_dimensions(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        for row in range(1, height+1):
            symbols_in_row = max(1, (width * row) // height)
            lines.append(symbol * symbols_in_row)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid of given height.

        Args:
            height (int): The height of the pyramid (must be >=1).
            symbol (str): Single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the pyramid.

        Raises:
            ValueError: If invalid arguments are provided.
        """
        self._validate_dimensions(height, 'height')
        self._validate_symbol(symbol)
        lines = []
        for row in range(1, height+1):
            num_symbols = 2 * row - 1
            num_spaces = height - row
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            lines.append(line)
        return '\n'.join(lines)

    @staticmethod
    def _validate_dimensions(value: int, name: str) -> None:
        """
        Validates that the provided dimension is a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 1:
            raise ValueError(f"{name} must be >= 1.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the input symbol is a single printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if symbol not in string.printable or symbol in string.whitespace:
            raise ValueError("Symbol must be a single printable, non-whitespace character.")


# Example usage and test cases (for demonstration, can remove or replace with unit tests)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square (3, '*'):\n", art.draw_square(3, '*'))
    print("\nRectangle (5, 2, '#'):\n", art.draw_rectangle(5, 2, '#'))
    print("\nParallelogram (4, 3, '+'):\n", art.draw_parallelogram(4, 3, '+'))
    print("\nTriangle (5, 5, '@'):\n", art.draw_triangle(5, 5, '@'))
    print("\nPyramid (4, '^'):\n", art.draw_pyramid(4, '^'))
