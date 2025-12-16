
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains a suite of static methods
for creating various geometric shapes using ASCII characters. The implementation
prioritizes code quality, adhering to principles of the ISO/IEC 25010 standard,
including correctness, performance, safety, and maintainability.
"""

import math
from typing import Optional


class AsciiArt:
    """
    A utility class for generating 2D ASCII art shapes.

    This class provides a collection of static methods to draw various
    geometric shapes using ASCII characters. All methods are stateless and can be
    called directly on the class without needing to create an instance.
    """

    @staticmethod
    def _validate_input(
        symbol: str,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> None:
        """
        Validates the common inputs for drawing functions (internal use).

        Args:
            symbol: The character to use for drawing.
            width: The width of the shape (if applicable).
            height: The height of the shape (if applicable).

        Raises:
            TypeError: If width or height are not integers.
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if width or height are not positive integers.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        if width is not None:
            if not isinstance(width, int):
                raise TypeError("The 'width' must be an integer.")
            if width <= 0:
                raise ValueError("The 'width' must be a positive integer.")

        if height is not None:
            if not isinstance(height, int):
                raise TypeError("The 'height' must be an integer.")
            if height <= 0:
                raise ValueError("The 'height' must be a positive integer.")

    @staticmethod
    def draw_square(width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square. Must be a positive integer.
            symbol: The character used to draw the square. Must be a single,
                    non-whitespace character.

        Returns:
            A multi-line string representing the square.
        """
        # A square is a special case of a rectangle.
        # Delegate to draw_rectangle, which includes its own validation.
        return AsciiArt.draw_rectangle(width=width, height=width, symbol=symbol)

    @staticmethod
    def draw_rectangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width: The width of the rectangle. Must be a positive integer.
            height: The height of the rectangle. Must be a positive integer.
            symbol: The character used to draw the rectangle. Must be a single,
                    non-whitespace character.

        Returns:
            A multi-line string representing the rectangle.
        """
        AsciiArt._validate_input(symbol=symbol, width=width, height=height)
        row = symbol * width
        lines = [row] * height
        return "\n".join(lines)

    @staticmethod
    def draw_parallelogram(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that slants to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width: The width of the parallelogram's top/bottom side.
                   Must be a positive integer.
            height: The vertical height of the parallelogram. Must be a positive
                    integer.
            symbol: The character used to draw the shape. Must be a single,
                    non-whitespace character.

        Returns:
            A multi-line string representing the parallelogram.
        """
        AsciiArt._validate_input(symbol=symbol, width=width, height=height)
        base_row = symbol * width
        lines = [(" " * i) + base_row for i in range(height)]
        return "\n".join(lines)

    @staticmethod
    def draw_triangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner. The shape is scaled
        to fit the given width and height, with the base at the bottom.

        Args:
            width: The width of the triangle's base. Must be a positive integer.
            height: The height of the triangle. Must be a positive integer.
            symbol: The character used to draw the shape. Must be a single,
                    non-whitespace character.

        Returns:
            A multi-line string representing the triangle.
        """
        AsciiArt._validate_input(symbol=symbol, width=width, height=height)
        lines = []
        for i in range(height):
            # Calculate the number of symbols for the current row (i is 0-indexed).
            # This creates a linear growth from ~1 to `width` over `height` rows.
            num_symbols = math.ceil((i + 1) * width / height)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    @staticmethod
    def draw_pyramid(height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid. Must be a positive integer.
            symbol: The character used to draw the shape. Must be a single,
                    non-whitespace character.

        Returns:
            A multi-line string representing the pyramid.
        """
        AsciiArt._validate_input(symbol=symbol, height=height)
        # The full width of the pyramid's base is 2 * height - 1
        full_width = 2 * height - 1
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            # The str.center() method is perfect for centering the symbols
            row_content = (symbol * num_symbols).center(full_width)
            lines.append(row_content)
        return "\n".join(lines)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.

    print("--- 5x5 Square with '#' ---")
    print(AsciiArt.draw_square(width=5, symbol="#"))
    print("\n" + "="*30 + "\n")

    print("--- 8x4 Rectangle with '*' ---")
    print(AsciiArt.draw_rectangle(width=8, height=4, symbol="*"))
    print("\n" + "="*30 + "\n")

    print("--- 10x5 Parallelogram with '+' ---")
    print(AsciiArt.draw_parallelogram(width=10, height=5, symbol="+"))
    print("\n" + "="*30 + "\n")

    print("--- 7x7 Right-angled Triangle with 'T' ---")
    print(AsciiArt.draw_triangle(width=7, height=7, symbol="T"))
    print("\n" + "="*30 + "\n")

    print("--- Stretched 10x5 Right-angled Triangle with 'S' ---")
    print(AsciiArt.draw_triangle(width=10, height=5, symbol="S"))
    print("\n" + "="*30 + "\n")

    print("--- 6-level Pyramid with '^' ---")
    print(AsciiArt.draw_pyramid(height=6, symbol="^"))
    print("\n" + "="*30 + "\n")

    print("--- Example of Input Validation ---")
    try:
        AsciiArt.draw_square(width=-3, symbol="X")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        AsciiArt.draw_rectangle(width=5, height=3, symbol="@@")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        AsciiArt.draw_pyramid(height=4, symbol=" ")
    except ValueError as e:
        print(f"Caught expected error: {e}")
