
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains methods for drawing
various geometric shapes using ASCII characters. The implementation prioritizes
code quality, maintainability, and reliability, adhering to the principles
outlined in the ISO/IEC 25010 standard.
"""

import math
from typing import Final

# --- Constants for Error Messages ---
# Using constants for messages improves maintainability and consistency.
INVALID_DIMENSION_MSG: Final[str] = (
    "Dimensions (width, height) must be positive integers."
)
INVALID_SYMBOL_MSG: Final[str] = (
    "Symbol must be a single, non-whitespace, printable character."
)


class AsciiArt:
    """
    A class containing methods to generate 2D ASCII art shapes.

    This class provides a collection of static methods for drawing geometric
    shapes like squares, rectangles, and pyramids. All methods are designed
    to be pure functions, returning a string representation of the shape
    without any side effects. Input validation is performed to ensure
    robustness and reliability.
    """

    @staticmethod
    def _validate_dimension(*dimensions: int) -> None:
        """
        Validates that all provided dimensions are positive integers.

        Args:
            *dimensions: A variable number of integer dimensions to validate.

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive number (> 0).
        """
        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError(INVALID_DIMENSION_MSG)
            if dim <= 0:
                raise ValueError(INVALID_DIMENSION_MSG)

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single, printable, non-whitespace character.

        Args:
            symbol: The character to use for drawing.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single character, is not
                        printable, or is a whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError(INVALID_SYMBOL_MSG)
        if len(symbol) != 1 or not symbol.isprintable() or symbol.isspace():
            raise ValueError(INVALID_SYMBOL_MSG)

    @staticmethod
    def draw_square(width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        This method is a convenience wrapper around draw_rectangle.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII square.

        Raises:
            ValueError: If width is not a positive integer or the symbol is invalid.
            TypeError: If width is not an integer or symbol is not a string.
        """
        # Reuses the draw_rectangle logic for maintainability.
        return AsciiArt.draw_rectangle(width, width, symbol)

    @staticmethod
    def draw_rectangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.

        Raises:
            ValueError: If dimensions are not positive or the symbol is invalid.
            TypeError: If dimensions are not integers or symbol is not a string.
        """
        AsciiArt._validate_dimension(width, height)
        AsciiArt._validate_symbol(symbol)

        row = symbol * width
        # Using a list comprehension and str.join() is highly efficient.
        return "\n".join([row for _ in range(height)])

    @staticmethod
    def draw_parallelogram(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that slants to the right.

        Each subsequent row is indented by one additional space.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII parallelogram.

        Raises:
            ValueError: If dimensions are not positive or the symbol is invalid.
            TypeError: If dimensions are not integers or symbol is not a string.
        """
        AsciiArt._validate_dimension(width, height)
        AsciiArt._validate_symbol(symbol)

        shape_rows = [
            " " * i + symbol * width for i in range(height)
        ]
        return "\n".join(shape_rows)

    @staticmethod
    def draw_triangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle's base has the specified width, and its height is scaled
        linearly across the specified number of rows.

        Args:
            width: The width of the triangle's base (last row).
            height: The number of rows in the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII triangle.

        Raises:
            ValueError: If dimensions are not positive or the symbol is invalid.
            TypeError: If dimensions are not integers or symbol is not a string.
        """
        AsciiArt._validate_dimension(width, height)
        AsciiArt._validate_symbol(symbol)

        shape_rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            # This scales the triangle's width linearly from 1 to `width`
            # over `height` rows. `math.ceil` ensures a clean shape.
            # `i + 1` is used because row index `i` is 0-based.
            num_symbols = math.ceil((i + 1) * width / height)
            shape_rows.append(symbol * num_symbols)

        return "\n".join(shape_rows)

    @staticmethod
    def draw_pyramid(height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII pyramid.

        Raises:
            ValueError: If height is not a positive integer or the symbol is invalid.
            TypeError: If height is not an integer or symbol is not a string.
        """
        AsciiArt._validate_dimension(height)
        AsciiArt._validate_symbol(symbol)

        shape_rows = []
        for i in range(height):
            # For row `i`, calculate leading spaces and number of symbols.
            # Spaces decrease from `height - 1` to 0.
            # Symbols increase in steps of 2 (1, 3, 5, ...).
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            shape_rows.append(spaces + symbols)

        return "\n".join(shape_rows)


# --- Example Usage ---
if __name__ == "__main__":
    # This block demonstrates the functionality of the AsciiArt class.
    # It will only run when the script is executed directly.
    print("--- ASCII Art Generator ---")

    try:
        # Example 1: Draw a square
        print("\n[+] Square (5x5, '#'):")
        print(AsciiArt.draw_square(5, "#"))

        # Example 2: Draw a rectangle
        print("\n[+] Rectangle (10x4, '*'):")
        print(AsciiArt.draw_rectangle(10, 4, "*"))

        # Example 3: Draw a parallelogram
        print("\n[+] Parallelogram (8x5, '@'):")
        print(AsciiArt.draw_parallelogram(8, 5, "@"))

        # Example 4: Draw a right-angled triangle
        print("\n[+] Right-Angled Triangle (width=10, height=5, '+'):")
        print(AsciiArt.draw_triangle(10, 5, "+"))

        # Example 5: Draw another right-angled triangle (width=height)
        print("\n[+] Right-Angled Triangle (width=7, height=7, '^'):")
        print(AsciiArt.draw_triangle(7, 7, "^"))

        # Example 6: Draw a pyramid
        print("\n[+] Pyramid (height=6, '$'):")
        print(AsciiArt.draw_pyramid(6, "$"))

        # Example 7: Demonstrate error handling for invalid dimensions
        print("\n[+] Testing invalid input (negative width)...")
        AsciiArt.draw_square(-3, "X")

    except (ValueError, TypeError) as e:
        print(f"\n[!] An error occurred as expected: {e}")

    try:
        # Example 8: Demonstrate error handling for invalid symbol
        print("\n[+] Testing invalid input (multi-character symbol)...")
        AsciiArt.draw_square(3, "XX")

    except (ValueError, TypeError) as e:
        print(f"\n[!] An error occurred as expected: {e}")
