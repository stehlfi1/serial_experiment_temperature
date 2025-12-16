
# -*- coding: utf-8 -*-
"""
ascii_art_generator.py

This module provides a utility class, AsciiArt, for generating various 2D
ASCII art shapes. It is designed with a focus on code quality, maintainability,
and adherence to the ISO/IEC 25010 standard.

Key Quality Attributes (ISO/IEC 25010):
- Functional Suitability: Correctly generates the specified ASCII shapes.
- Performance Efficiency: Uses efficient string-building techniques.
- Reliability (Fault Tolerance): Robustly handles invalid inputs by raising
  appropriate exceptions.
- Maintainability (Modularity, Reusability): Logic is modularized within a
  class, and common validation logic is reused.
- Usability (Readability & Documentation): All methods are documented with
  clear docstrings, type hints, and descriptive variable names.
- Security: Input validation protects against unexpected or malformed inputs.
"""

import math

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class provides a collection of static methods to draw filled shapes
    like squares, rectangles, and pyramids using a specified character. It
    ensures all inputs are valid before proceeding with drawing operations.
    """

    @staticmethod
    def _validate_inputs(symbol: str, **dimensions: int) -> None:
        """
        Validates the symbol and dimension inputs for drawing functions.

        This private helper ensures that the symbol is a single, printable,
        non-whitespace character and that all provided dimensions (e.g., width,
        height) are positive integers.

        Args:
            symbol (str): The character to use for drawing.
            **dimensions (int): Keyword arguments for shape dimensions
                                (e.g., width=5, height=10).

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single character, is whitespace,
                        is not printable, or if a dimension is not a positive integer.
        """
        # Validate symbol
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError(
                "Symbol must be a single, printable, non-whitespace character."
            )

        # Validate dimensions
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    @staticmethod
    def draw_square(width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width (int): The width and height of the square. Must be positive.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        AsciiArt._validate_inputs(symbol, width=width)
        # A square is a rectangle with equal width and height.
        return AsciiArt.draw_rectangle(width, width, symbol)

    @staticmethod
    def draw_rectangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width (int): The width of the rectangle. Must be positive.
            height (int): The height of the rectangle. Must be positive.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled rectangle.

        Raises:
            TypeError: If width/height is not an integer or symbol is not a string.
            ValueError: If width/height is not positive or symbol is invalid.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)
        row = symbol * width
        # Efficiently create the shape by joining a list of identical rows.
        return "\n".join([row] * height)

    @staticmethod
    def draw_parallelogram(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that slants to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width (int): The width of the parallelogram's parallel sides.
            height (int): The height of the parallelogram.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled parallelogram.
        
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string.
            ValueError: If width/height is not positive or symbol is invalid.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Prepend spaces to shift the row to the right.
            padding = " " * i
            content = symbol * width
            rows.append(f"{padding}{content}")
        return "\n".join(rows)

    @staticmethod
    def draw_triangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle starts at the top-left and grows towards the bottom-right,
        reaching the specified width at the final row.

        Args:
            width (int): The final width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled triangle.

        Raises:
            TypeError: If width/height is not an integer or symbol is not a string.
            ValueError: If width/height is not positive or symbol is invalid.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row based on a
            # consistent slope, ensuring it reaches `width` at the last row.
            # `math.ceil` ensures the shape is "filled" and grows smoothly.
            current_width = math.ceil((i + 1) * width / height)
            rows.append(symbol * current_width)
        return "\n".join(rows)

    @staticmethod
    def draw_pyramid(height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        The pyramid is centered, with a base width of (2 * height - 1).

        Args:
            height (int): The height of the pyramid.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        AsciiArt._validate_inputs(symbol, height=height)
        rows = []
        max_width = 2 * height - 1
        for i in range(height):
            # Calculate symbols and padding for each level of the pyramid.
            num_symbols = 2 * i + 1
            row_content = symbol * num_symbols
            # `str.center()` is a clean way to add symmetrical padding.
            rows.append(row_content.center(max_width))
        return "\n".join(rows)

# --- Example Usage ---
# This section demonstrates how to use the AsciiArt class and can be used for
# manual testing. It is not part of the core library code.
if __name__ == "__main__":
    drawer = AsciiArt()

    print("--- Square (5x5, symbol '#') ---")
    print(drawer.draw_square(5, "#"))
    print("\n" + "="*30 + "\n")

    print("--- Rectangle (8x4, symbol '*') ---")
    print(drawer.draw_rectangle(8, 4, "*"))
    print("\n" + "="*30 + "\n")
    
    print("--- Parallelogram (10x5, symbol '@') ---")
    print(drawer.draw_parallelogram(10, 5, "@"))
    print("\n" + "="*30 + "\n")

    print("--- Right-Angled Triangle (w=10, h=5, symbol '+') ---")
    print(drawer.draw_triangle(10, 5, "+"))
    print("\n" + "="*30 + "\n")

    print("--- Pyramid (height=6, symbol '^') ---")
    print(drawer.draw_pyramid(6, "^"))
    print("\n" + "="*30 + "\n")

    print("--- Input Validation Examples ---")
    try:
        drawer.draw_square(-3, "X")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        drawer.draw_rectangle(5, 5, "&&")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        drawer.draw_pyramid(5, " ")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        drawer.draw_triangle(5.5, 3, "$")
    except TypeError as e:
        print(f"Caught expected error: {e}")
