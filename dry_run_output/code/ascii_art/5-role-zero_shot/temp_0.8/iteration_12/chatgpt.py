
"""
ascii_art.py

Console-based 2D ASCII Art Application

This module provides the AsciiArt class, offering methods to generate various ASCII art shapes
according to robustness, maintainability, and quality requirements inspired by ISO/IEC 25010.
"""

from typing import Any


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    Shapes supported:
    - Square
    - Rectangle
    - Parallelogram
    - Right-angled triangle
    - Pyramid
    """

    def __init__(self) -> None:
        """
        Initializes the AsciiArt class.
        Currently stateless; constructor provided for future extensibility.
        """
        pass

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates if the symbol is a single, non-whitespace printable character.

        Raises:
            ValueError: If symbol is not a single printable character.
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
        Validates if value is a positive integer.

        Args:
            value: The value to check.
            name: Parameter name for exception messages.

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be positive and greater than zero.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.

        Args:
            width: The width and height of the square (must be positive).
            symbol: The ASCII character for drawing the shape.

        Returns:
            A multi-line string representing the square.

        Raises:
            ValueError or TypeError: For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height.

        Args:
            width: The width of the rectangle (must be positive).
            height: The height of the rectangle (must be positive).
            symbol: The ASCII character for drawing the shape.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            ValueError or TypeError: For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram of specified width and height.

        The first row starts at the left; each subsequent row is shifted right by one space.

        Args:
            width: Base width of the parallelogram (must be positive).
            height: Height of the parallelogram (must be positive).
            symbol: The ASCII character for drawing the shape.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            ValueError or TypeError: For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle growing to the right, starting from the top-left corner.

        Each row fills proportionally depending on height and width.

        Args:
            width: The base width of the triangle (must be positive).
            height: The height of the triangle (must be positive).
            symbol: The ASCII character for drawing the shape.

        Returns:
            A multi-line string representing the triangle.

        Raises:
            ValueError or TypeError: For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        # Ensure at least one symbol on each line; proportional growth
        lines = []
        for i in range(height):
            num_symbols = max(1, round((i + 1) * width / height))
            line = symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical centered pyramid with the given height.

        Args:
            height: The number of rows in the pyramid (must be positive).
            symbol: The ASCII character for drawing the shape.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            ValueError or TypeError: For invalid arguments.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        max_width = 2 * height - 1
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = (max_width - num_symbols) // 2
            line = (" " * num_spaces) + (symbol * num_symbols) + (" " * num_spaces)
            lines.append(line)
        return "\n".join(lines)


# --- Example usage and test cases (remove or refactor for integration into a larger system) ---

if __name__ == "__main__":
    art = AsciiArt()
    print("Square (5, '#'):")
    print(art.draw_square(5, '#'))
    print("\nRectangle (7x3, '*'):")
    print(art.draw_rectangle(7, 3, '*'))
    print("\nParallelogram (6x4, '@'):")
    print(art.draw_parallelogram(6, 4, '@'))
    print("\nTriangle (8x5, '+'):")
    print(art.draw_triangle(8, 5, '+'))
    print("\nPyramid (5, '$'):")
    print(art.draw_pyramid(5, '$'))
