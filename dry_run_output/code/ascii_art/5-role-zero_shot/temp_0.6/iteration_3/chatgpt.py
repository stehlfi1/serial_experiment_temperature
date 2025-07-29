
"""
ascii_art.py

A console-based 2D ASCII Art application for drawing basic shapes.

Author: Senior Software Developer
ISO/IEC 25010 Compliance: The code adheres to maintainability, reliability, usability, and functional suitability requirements.
"""

from typing import Any


class AsciiArt:
    """
    A class for generating ASCII representations of geometric shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using the specified symbol.

        :param width: Length of each side of the square (must be >= 1)
        :param symbol: Single, non-whitespace printable character
        :return: Multiline string representing the square
        :raises ValueError: If invalid arguments are provided
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)

        line = symbol * width
        art = "\n".join([line for _ in range(width)])
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height using the specified symbol.

        :param width: Width of the rectangle (must be >= 1)
        :param height: Height of the rectangle (must be >= 1)
        :param symbol: Single, non-whitespace printable character
        :return: Multiline string representing the rectangle
        :raises ValueError: If invalid arguments are provided
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        line = symbol * width
        art = "\n".join([line for _ in range(height)])
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram with the top edge left-aligned and each row shifted right by one space.

        :param width: Width of the parallelogram (must be >= 1)
        :param height: Height of the parallelogram (must be >= 1)
        :param symbol: Single, non-whitespace printable character
        :return: Multiline string representing the parallelogram
        :raises ValueError: If invalid arguments are provided
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Each subsequent line is shifted right by one space
            line = ' ' * i + symbol * width
            lines.append(line)
        art = "\n".join(lines)
        return art

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (right angle at top-left, grows to the right and down).

        :param width: Base width of the triangle (must be >= 1)
        :param height: Height of the triangle (must be >= 1)
        :param symbol: Single, non-whitespace printable character
        :return: Multiline string representing the triangle
        :raises ValueError: If invalid arguments are provided
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Determine number of symbols for this row (at least 1, at most width)
            num_symbols = min(width, max(1, (i + 1) * width // height))
            line = symbol * num_symbols
            lines.append(line)
        art = "\n".join(lines)
        return art

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, centered pyramid of a given height.

        :param height: Height of the pyramid (must be >= 1)
        :param symbol: Single, non-whitespace printable character
        :return: Multiline string representing the pyramid
        :raises ValueError: If invalid arguments are provided
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)

        lines = []
        # The base width is always (height * 2 - 1)
        base_width = height * 2 - 1
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            lines.append(line)
        art = "\n".join(lines)
        return art

    # --- Private helper methods ---

    def _validate_dimensions(self, **kwargs: Any) -> None:
        """
        Validates that all provided dimensions are positive integers.

        :param kwargs: Dimension names and their values
        :raises ValueError: If any dimension is not a positive integer
        """
        for name, value in kwargs.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value < 1:
                raise ValueError(f"{name.capitalize()} must be >= 1.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace printable character.

        :param symbol: Character to use for drawing
        :raises ValueError: If symbol is invalid
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be whitespace.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

# Example test cases (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n" + art.draw_square(4, '#'))
    print("\nRectangle:\n" + art.draw_rectangle(6, 3, '*'))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, '+'))
    print("\nTriangle:\n" + art.draw_triangle(6, 4, '@'))
    print("\nPyramid:\n" + art.draw_pyramid(5, '$'))
