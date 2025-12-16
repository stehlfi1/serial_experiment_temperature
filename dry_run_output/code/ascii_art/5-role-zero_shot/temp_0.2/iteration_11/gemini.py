
# -*- coding: utf-8 -*-
"""
A Python module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements an interface for
drawing various geometric shapes using ASCII characters. The implementation
prioritizes code quality, maintainability, and adherence to software
engineering best practices as outlined by ISO/IEC 25010.
"""

import math
from typing import List

# --- Constants ---
# Define a maximum dimension to prevent excessive memory and CPU usage,
# adhering to the 'Safety' and 'Performance Efficiency' quality characteristics.
MAX_DIMENSION = 100


class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class encapsulates the logic for drawing geometric shapes like squares,
    rectangles, and pyramids. It provides a clean, easy-to-use interface and
    includes robust input validation to ensure reliable operation.

    Attributes:
        None
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the drawing symbol.

        Ensures the symbol is a single, printable, non-whitespace character.
        This private helper method promotes modularity and reusability.

        Args:
            symbol: The character to be used for drawing.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single, printable,
                        non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError(
                "Symbol must be a printable, non-whitespace character."
            )

    def _validate_dimensions(self, *dimensions: int) -> None:
        """
        Validate shape dimensions (width, height).

        Ensures dimensions are positive integers within a reasonable limit.
        This method enhances safety by preventing resource exhaustion.

        Args:
            *dimensions: A variable number of integer dimensions to validate.

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive integer or exceeds
                        the defined MAX_DIMENSION.
        """
        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError("Dimensions must be integers.")
            if not 0 < dim <= MAX_DIMENSION:
                raise ValueError(
                    f"Dimensions must be positive and not exceed {MAX_DIMENSION}."
                )

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        This method leverages the draw_rectangle method, promoting code reuse
        and adhering to the DRY (Don't Repeat Yourself) principle.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the ASCII square.

        Raises:
            TypeError: On invalid input types for width or symbol.
            ValueError: On invalid values for width or symbol.
        """
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        The implementation uses a list comprehension and `str.join` for
        efficient string building, which is more performant than repeated
        string concatenation in a loop.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.

        Raises:
            TypeError: On invalid input types for dimensions or symbol.
            ValueError: On invalid values for dimensions or symbol.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        line = symbol * width
        lines = [line for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram.

        Each subsequent row is shifted one space to the right, creating a
        diagonal effect.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the shape.

        Returns:
            A multi-line string representing the ASCII parallelogram.

        Raises:
            TypeError: On invalid input types for dimensions or symbol.
            ValueError: On invalid values for dimensions or symbol.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        lines: List[str] = []
        for i in range(height):
            padding = " " * i
            content = symbol * width
            lines.append(f"{padding}{content}")
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows to the specified width and height. The number of
        symbols in each row is calculated to scale proportionally, ensuring
        the final row has the specified width.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the shape.

        Returns:
            A multi-line string representing the ASCII triangle.

        Raises:
            TypeError: On invalid input types for dimensions or symbol.
            ValueError: On invalid values for dimensions or symbol.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        lines: List[str] = []
        for i in range(height):
            # Calculate the number of symbols for the current row to scale
            # from 1 to `width` over `height` rows.
            # `math.ceil` ensures a smooth-looking progression.
            num_symbols = math.ceil((i + 1) * width / height)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        The pyramid's width is determined by its height. The base of a pyramid
        of `height` H has a width of 2*H - 1.

        Args:
            height: The height of the pyramid.
            symbol: The character used to draw the shape.

        Returns:
            A multi-line string representing the ASCII pyramid.

        Raises:
            TypeError: On invalid input types for height or symbol.
            ValueError: On invalid values for height or symbol.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)

        lines: List[str] = []
        for i in range(height):
            num_symbols = 2 * i + 1
            padding = " " * (height - 1 - i)
            lines.append(f"{padding}{symbol * num_symbols}")
        return "\n".join(lines)


def main() -> None:
    """
    Main function to demonstrate the AsciiArt class functionality.

    This function serves as an entry point and a simple client to showcase
    the drawing capabilities and error handling of the AsciiArt class.
    This separation of concerns makes the AsciiArt class highly testable
    and reusable.
    """
    print("--- ASCII Art Generator Demo ---")
    artist = AsciiArt()
    symbol = "*"

    # --- 1. Demonstrate Correct Drawing ---
    print("\n1. Drawing valid shapes:\n")

    print("--- Square (5x5) ---")
    print(artist.draw_square(5, symbol))

    print("\n--- Rectangle (8x4) ---")
    print(artist.draw_rectangle(8, 4, symbol))

    print("\n--- Parallelogram (10x5) ---")
    print(artist.draw_parallelogram(10, 5, "@"))

    print("\n--- Right-Angled Triangle (width=12, height=6) ---")
    print(artist.draw_triangle(12, 6, "#"))

    print("\n--- Pyramid (height=7) ---")
    print(artist.draw_pyramid(7, "^"))

    # --- 2. Demonstrate Input Validation and Error Handling ---
    print("\n\n2. Demonstrating error handling for invalid inputs:\n")

    test_cases = [
        ("Square with negative width", lambda: artist.draw_square(-3, symbol)),
        ("Rectangle with zero height", lambda: artist.draw_rectangle(5, 0, symbol)),
        ("Pyramid with oversized height", lambda: artist.draw_pyramid(101, symbol)),
        ("Triangle with float dimension", lambda: artist.draw_triangle(5.5, 4, symbol)),
        ("Shape with multi-char symbol", lambda: artist.draw_square(5, "@@")),
        ("Shape with whitespace symbol", lambda: artist.draw_square(5, " ")),
        ("Shape with non-printable symbol", lambda: artist.draw_square(5, "\t")),
    ]

    for description, action in test_cases:
        try:
            action()
        except (ValueError, TypeError) as e:
            print(f"- Test Case: {description}")
            print(f"  Successfully caught expected error: {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
