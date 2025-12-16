
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods for drawing
various geometric shapes using ASCII characters. The implementation aligns with
the ISO/IEC 25010 standard, emphasizing quality characteristics such as
reliability, efficiency, and maintainability.
"""

import math
from typing import Dict, Any

class AsciiArt:
    """
    A class for generating console-based 2D ASCII art.

    This class provides a collection of methods to draw various geometric shapes
    like squares, rectangles, and pyramids as multi-line strings. It includes
    robust input validation to ensure reliability and produces clean,
    maintainable code.
    """

    def _validate_inputs(self, symbol: str, **dimensions: Dict[str, Any]) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper method ensures that the symbol and dimensions
        meet the required criteria, promoting code reusability and safety.

        Args:
            symbol: The character to use for drawing.
            **dimensions: A keyword dictionary of dimensions (e.g., width, height)
                          to validate.

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if a dimension is not a positive integer.
        """
        # Validate symbol type
        if not isinstance(symbol, str):
            raise TypeError("The 'symbol' must be a string.")

        # Validate symbol properties
        if len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        # Validate dimensions
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The '{name}' dimension must be an integer.")
            if value <= 0:
                raise ValueError(f"The '{name}' dimension must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the ASCII square.
        """
        self._validate_inputs(symbol, width=width)
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.
        """
        self._validate_inputs(symbol, width=width, height=height)
        row = symbol * width
        lines = [row for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that skews to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the ASCII parallelogram.
        """
        self._validate_inputs(symbol, width=width, height=height)
        row_content = symbol * width
        lines = [" " * i + row_content for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner, and its hypotenuse is
        approximated to fit the specified width and height.

        Args:
            width: The maximum width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the ASCII triangle.
        """
        self._validate_inputs(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            # Calculate the number of symbols for the current row using a
            # linear growth factor and ceiling to create a stepped hypotenuse.
            # (i + 1) is used for 1-based row counting in the calculation.
            num_symbols = math.ceil((i + 1) * width / height)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.
        """
        self._validate_inputs(symbol, height=height)
        lines = []
        for i in range(height):
            # Number of spaces to center the row's content
            leading_spaces = " " * (height - 1 - i)
            # Number of symbols increases by 2 for each row (1, 3, 5, ...)
            symbols_in_row = symbol * (2 * i + 1)
            lines.append(leading_spaces + symbols_in_row)
        return "\n".join(lines)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class and serves as
    # a basic functional test.

    artist = AsciiArt()
    print("--- ASCII Art Generator Demonstration ---")

    print("\n--- Square (5x5, '#') ---")
    print(artist.draw_square(width=5, symbol='#'))

    print("\n--- Rectangle (8x4, '*') ---")
    print(artist.draw_rectangle(width=8, height=4, symbol='*'))

    print("\n--- Parallelogram (10x5, '=') ---")
    print(artist.draw_parallelogram(width=10, height=5, symbol='='))

    print("\n--- Right-Angled Triangle (width=7, height=4, '+') ---")
    print(artist.draw_triangle(width=7, height=4, symbol='+'))

    print("\n--- Pyramid (height=6, '^') ---")
    print(artist.draw_pyramid(height=6, symbol='^'))

    print("\n--- Demonstrating Input Validation ---")

    def test_error(description: str, func, *args, **kwargs):
        """Helper to test for expected exceptions."""
        print(f"\n--- Testing: {description} ---")
        try:
            func(*args, **kwargs)
        except (ValueError, TypeError) as e:
            print(f"OK. Caught expected error: {e}")

    test_error("Negative width", artist.draw_square, width=-3, symbol='X')
    test_error("Multi-character symbol", artist.draw_rectangle, 5, 5, '@@')
    test_error("Whitespace symbol", artist.draw_pyramid, 5, ' ')
    test_error("Non-integer height", artist.draw_triangle, 5, "a", '%')

