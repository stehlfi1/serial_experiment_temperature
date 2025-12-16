
"""
ascii_art.py

Console-based 2D ASCII ART application.

Implements drawing of square, rectangle, parallelogram, right-angled triangle, and pyramid shapes
using a user-specified printable symbol.

Adheres to ISO/IEC 25010 standards for code quality, maintainability, and reliability.
"""

from typing import Any


class AsciiArt:
    """
    Provides methods for drawing various 2D ASCII art shapes.

    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace printable character.
        Raises:
            ValueError: If symbol is not valid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    def _validate_dimension(self, name: str, value: Any) -> None:
        """
        Validates that the dimension (width/height) is an integer >= 1.
        Args:
            name: Name of the dimension for error messages.
            value: The value to be validated.
        Raises:
            ValueError: If dimension is invalid.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 1:
            raise ValueError(f"{name} must be a positive integer (>= 1).")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square shape.

        Args:
            width: The width and height of the square (>= 1).
            symbol: A single printable character.

        Returns:
            A string representing the square.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_dimension('width', width)
        self._validate_symbol(symbol)

        square = (symbol * width + '\n') * width
        return square.rstrip('\n')

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle shape.

        Args:
            width: The width of the rectangle (>= 1).
            height: The height of the rectangle (>= 1).
            symbol: A single printable character.

        Returns:
            A string representing the rectangle.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_dimension('width', width)
        self._validate_dimension('height', height)
        self._validate_symbol(symbol)

        rectangle = (symbol * width + '\n') * height
        return rectangle.rstrip('\n')

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram shape (shifted right each row).

        Args:
            width: The width of the parallelogram (>= 1).
            height: The height of the parallelogram (>= 1).
            symbol: A single printable character.

        Returns:
            A string representing the parallelogram.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_dimension('width', width)
        self._validate_dimension('height', height)
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            line = (' ' * row) + (symbol * width)
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left right angle).
        The triangle grows to the right, starting from the top-left corner,
        fitting within the specified width and height.

        Args:
            width: The maximum width of the triangle base (>= 1).
            height: The height of the triangle (>= 1).
            symbol: A single printable character.

        Returns:
            A string representing the triangle.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_dimension('width', width)
        self._validate_dimension('height', height)
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Determine number of symbols for this line
            # Last row should reach width
            symbols_in_row = max(1, round((row + 1) * width / height))
            # Ensure we do not exceed width
            symbols_in_row = min(symbols_in_row, width)
            line = symbol * symbols_in_row
            lines.append(line)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid.

        Args:
            height: The number of levels of the pyramid (>= 1).
            symbol: A single printable character.

        Returns:
            A string representing the pyramid.

        Raises:
            ValueError, TypeError: For invalid input.
        """
        self._validate_dimension('height', height)
        self._validate_symbol(symbol)

        lines = []
        base_width = (height * 2) - 1
        for level in range(1, height + 1):
            symbols_in_row = (level * 2) - 1
            spaces = (base_width - symbols_in_row) // 2
            line = (' ' * spaces) + (symbol * symbols_in_row) + (' ' * spaces)
            lines.append(line)
        return '\n'.join(lines)


# Example usage (uncomment to run in a script or interactive python session)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n" + art.draw_square(4, '*'))
    print("\nRectangle:\n" + art.draw_rectangle(6, 3, '#'))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, '&'))
    print("\nTriangle:\n" + art.draw_triangle(6, 5, '%'))
    print("\nPyramid:\n" + art.draw_pyramid(5, '+'))
