
"""
ascii_art.py

ASCII Art Drawing Application (Console-based)
Compliant with ISO/IEC 25010 quality requirements:
- Functional suitability: Shapes rendered per specification
- Reliability: Validations for robust operation
- Maintainability: Modular, well-documented OOP design
- Security/Safety: Input validation and error handling
- Portability: Standard Python 3, no dependencies

Author: [Your Name]
"""

from typing import Any


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    Provides methods for various basic shapes.
    """

    def __init__(self) -> None:
        """Initializes the AsciiArt object."""
        pass  # No state; class is stateless, adhering to modularity and testability

    @staticmethod
    def _validate_dimensions(*args: Any) -> None:
        """
        Validates that all provided dimensions are positive integers.
        Raises ValueError if invalid.
        """
        for value in args:
            if not isinstance(value, int) or value <= 0:
                raise ValueError("Width and height values must be positive integers (> 0).")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is exactly one non-whitespace, printable character.
        Raises ValueError if invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of given width, filled with the symbol.

        Args:
            width (int): The side length of the square.
            symbol (str): The symbol to fill the square.

        Returns:
            str: A multi-line string representing the ASCII square.

        Raises:
            ValueError, TypeError: For invalid arguments.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        row = symbol * width
        return '\n'.join([row for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of given width and height, filled with the symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to fill the rectangle.

        Returns:
            str: A multi-line string representing the ASCII rectangle.

        Raises:
            ValueError, TypeError: For invalid arguments.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        row = symbol * width
        return '\n'.join([row for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a left-aligned parallelogram with rightward diagonal, filled with symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to fill the parallelogram.

        Returns:
            str: A multi-line string representing the ASCII parallelogram.

        Raises:
            ValueError, TypeError: For invalid arguments.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Each row has i leading spaces
            line = (' ' * i) + (symbol * width)
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a left-aligned right-angled triangle growing right and down.

        Args:
            width (int): The maximum base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to fill the triangle.

        Returns:
            str: A multi-line string representing the ASCII triangle.

        Raises:
            ValueError, TypeError: For invalid arguments.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        # Draw triangle such that last row reaches "width" symbols
        lines = []
        for row in range(1, height + 1):
            # Compute proportional length for each row
            line_len = max(1, (width * row) // height)
            line_len = min(line_len, width)
            lines.append(symbol * line_len)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical centered pyramid.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to fill the pyramid.

        Returns:
            str: A multi-line string representing the ASCII pyramid.

        Raises:
            ValueError, TypeError: For invalid arguments.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = (' ' * num_spaces) + (symbol * num_symbols) + (' ' * num_spaces)
            lines.append(line)
        return '\n'.join(lines)


if __name__ == "__main__":
    # Example usage & simple test cases (satisfying testability requirement)

    art = AsciiArt()

    try:
        print("SQUARE (5x5, #):")
        print(art.draw_square(5, '#'), end="\n\n")

        print("RECTANGLE (7x3, @):")
        print(art.draw_rectangle(7, 3, '@'), end="\n\n")

        print("PARALLELOGRAM (6x4, *):")
        print(art.draw_parallelogram(6, 4, '*'), end="\n\n")

        print("RIGHT-ANGLED TRIANGLE (width=7, height=4, $):")
        print(art.draw_triangle(7, 4, '$'), end="\n\n")

        print("PYRAMID (height=5, ^):")
        print(art.draw_pyramid(5, '^'), end="\n\n")
    except (ValueError, TypeError) as e:
        print("Input Error:", e)
