
# -*- coding: utf-8 -*-
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods for drawing
various geometric shapes using ASCII characters. It is designed with a focus
on code quality, maintainability, and adherence to best practices.

ISO/IEC 25010 Compliance:
- Functional Suitability: Provides correct shape-drawing functionality.
- Performance Efficiency: Uses efficient string-building techniques.
- Reliability: Includes robust input validation to prevent errors.
- Usability: Offers a clear and well-documented API.
- Maintainability: Code is modular, readable, and easily extensible.
- Portability: Uses only the Python standard library.
"""

import math
from typing import List

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class provides methods to draw simple geometric shapes like squares,
    rectangles, and pyramids using ASCII characters. It adheres to high
    code quality standards, focusing on correctness, readability, and safety
    by validating all inputs.
    """

    def _validate_inputs(self, symbol: str, dimensions: List[int]) -> None:
        """
        Private helper to validate common inputs for drawing methods.

        This method ensures that the symbol is a single, non-whitespace
        character and that all provided dimensions are positive integers.

        Args:
            symbol: The character to use for drawing.
            dimensions: A list of integer dimensions (e.g., width, height).

        Raises:
            ValueError: If the symbol is invalid or if any dimension is
                        not a positive integer.
            TypeError: If inputs are not of the expected type.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError("Dimensions must be integers.")
            if dim <= 0:
                raise ValueError("Dimensions (width, height) must be positive integers.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        A square is a special case of a rectangle where height equals width.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the ASCII square.
        
        Raises:
            ValueError: If width is non-positive or symbol is invalid.
            TypeError: If width is not an integer.
        """
        # A square is a rectangle with equal width and height.
        # Validation is implicitly handled by draw_rectangle.
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

        Raises:
            ValueError: If dimensions are non-positive or symbol is invalid.
            TypeError: If dimensions are not integers.
        """
        self._validate_inputs(symbol, [width, height])
        
        row = symbol * width
        # Use a list comprehension and join for performance and readability.
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram.

        The shape grows diagonally to the right, with each subsequent row
        being shifted one space to the right relative to the one above it.

        Args:
            width: The width of the parallelogram's parallel sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the ASCII parallelogram.

        Raises:
            ValueError: If dimensions are non-positive or symbol is invalid.
            TypeError: If dimensions are not integers.
        """
        self._validate_inputs(symbol, [width, height])
        
        rows = []
        base_row = symbol * width
        for i in range(height):
            padding = " " * i
            rows.append(f"{padding}{base_row}")
        
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle, scaled to width and height.

        The triangle starts at the top-left and grows towards the bottom-right.
        The number of symbols in each row is scaled proportionally to ensure
        the final row has the specified 'width'.

        Args:
            width: The final width of the triangle's base.
            height: The total height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the ASCII triangle.
        
        Raises:
            ValueError: If dimensions are non-positive or symbol is invalid.
            TypeError: If dimensions are not integers.
        """
        self._validate_inputs(symbol, [width, height])
        
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row (i is 0-indexed).
            # This formula scales the growth to match the target width and height.
            # math.ceil ensures the shape is "filled" and grows steadily.
            num_symbols = math.ceil(((i + 1) / height) * width)
            rows.append(symbol * num_symbols)
            
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        The pyramid has a height of 'height' rows. The base of the pyramid
        will have a width of (2 * height - 1) symbols.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.

        Raises:
            ValueError: If height is non-positive or symbol is invalid.
            TypeError: If height is not an integer.
        """
        self._validate_inputs(symbol, [height])
        
        rows = []
        # The total width of the pyramid's base determines the padding.
        total_width = 2 * height - 1
        
        for i in range(height):
            # Number of symbols in the current row (1, 3, 5, ...)
            num_symbols = 2 * i + 1
            # Calculate padding to center the symbols.
            padding_count = (total_width - num_symbols) // 2
            padding = " " * padding_count
            
            row_symbols = symbol * num_symbols
            rows.append(f"{padding}{row_symbols}")
            
        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    # --- Configuration ---
    art_generator = AsciiArt()
    SHAPE_SYMBOL = "#"

    # --- Demonstration ---
    print("--- ASCII Art Generator Demonstration ---")

    try:
        print("\n[+] Drawing a 5x5 Square:")
        square = art_generator.draw_square(width=5, symbol=SHAPE_SYMBOL)
        print(square)

        print("\n[+] Drawing a 10x4 Rectangle:")
        rectangle = art_generator.draw_rectangle(width=10, height=4, symbol="@")
        print(rectangle)

        print("\n[+] Drawing a 8x5 Parallelogram:")
        parallelogram = art_generator.draw_parallelogram(width=8, height=5, symbol="=")
        print(parallelogram)

        print("\n[+] Drawing a Right-Angled Triangle (Width=10, Height=5):")
        triangle = art_generator.draw_triangle(width=10, height=5, symbol="*")
        print(triangle)

        print("\n[+] Drawing a Pyramid (Height=6):")
        pyramid = art_generator.draw_pyramid(height=6, symbol="^")
        print(pyramid)

        # --- Error Handling Demonstration ---
        print("\n--- Error Handling Examples ---")
        
        print("\n[!] Attempting to draw with an invalid symbol (multi-char)...")
        try:
            art_generator.draw_square(5, "##")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\n[!] Attempting to draw with an invalid dimension (zero)...")
        try:
            art_generator.draw_rectangle(10, 0, "$")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("\n[!] Attempting to draw with an invalid dimension type (float)...")
        try:
            art_generator.draw_pyramid(4.5, "A")
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

