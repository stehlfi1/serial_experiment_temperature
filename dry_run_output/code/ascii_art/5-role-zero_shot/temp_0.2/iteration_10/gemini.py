
"""
A module for generating various 2D ASCII art shapes.

This module provides the AsciiArt class, which implements an interface for
drawing filled, console-based shapes like squares, rectangles, and pyramids.
The implementation prioritizes code quality, adhering to ISO/IEC 25010
characteristics such as reliability, maintainability, and performance efficiency.
"""

import math
from typing import Dict, Any

class AsciiArt:
    """
    A class to generate 2D ASCII art shapes.

    This class provides a collection of methods to draw various geometric shapes
    using a specified character. It includes input validation to ensure the
    integrity of the generated output and follows best practices for
    readability and maintainability.
    """

    def _validate_inputs(self, symbol: str, **dimensions: Dict[str, Any]) -> None:
        """
        Private helper method to validate input parameters.

        This method centralizes input validation, checking for correct types and
        valid value ranges for symbols and dimensions. This improves
        maintainability (DRY principle) and safety.

        Args:
            symbol: The character to use for drawing.
            dimensions: A dictionary of dimension names (e.g., 'width') and
                        their integer values.

        Raises:
            TypeError: If a dimension is not an integer or the symbol is not a string.
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if a dimension is not a positive integer.
        """
        # Safety & Reliability: Validate symbol type and value
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        # Safety & Reliability: Validate dimension types and values
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value < 1:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method demonstrates reusability by calling the draw_rectangle method.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.
        """
        # Correctness: A square is a rectangle with equal width and height.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the rectangle.
        """
        self._validate_inputs(symbol, width=width, height=height)

        # Performance Efficiency: Building a row once and repeating it.
        row = symbol * width
        # Performance Efficiency: Joining a list is faster than string concatenation.
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is indented by one additional space.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.
        """
        self._validate_inputs(symbol, width=width, height=height)
        lines = []
        base_row = symbol * width
        for i in range(height):
            # Readability: Clear logic for indentation.
            indent = " " * i
            lines.append(f"{indent}{base_row}")
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner to fit within the specified
        width and height bounding box.

        Args:
            width: The maximum width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the triangle.
        """
        self._validate_inputs(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            # Correctness: Calculate the width of the current row proportionally.
            # math.ceil ensures the triangle grows steadily and reaches full width.
            current_width = math.ceil((i + 1) * width / height)
            lines.append(symbol * current_width)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the pyramid.
        """
        self._validate_inputs(symbol, height=height)
        lines = []
        # The pyramid's base width is 2*height - 1. This is used for centering.
        max_width = 2 * height - 1
        for i in range(height):
            # Correctness: The number of symbols in each row follows the pattern 1, 3, 5...
            num_symbols = 2 * i + 1
            row_str = symbol * num_symbols
            # Readability & Correctness: Center the row within the max_width.
            lines.append(row_str.center(max_width))
        return "\n".join(lines)


# --- Main Execution Block ---
# This block demonstrates the usage of the AsciiArt class and serves as a
# simple test case for each function, including error handling.
# This improves the Testability and Usability of the module.
if __name__ == "__main__":
    artist = AsciiArt()

    print("--- ASCII Art Generator ---")

    # --- Successful Cases ---
    print("\n1. Square (5x5, symbol '#')")
    print(artist.draw_square(width=5, symbol="#"))

    print("\n2. Rectangle (8x4, symbol '*')")
    print(artist.draw_rectangle(width=8, height=4, symbol="*"))

    print("\n3. Parallelogram (10x5, symbol '=')")
    print(artist.draw_parallelogram(width=10, height=5, symbol="="))

    print("\n4. Right-Angled Triangle (width=7, height=7, symbol 'T')")
    print(artist.draw_triangle(width=7, height=7, symbol="T"))

    print("\n5. Pyramid (height=6, symbol '^')")
    print(artist.draw_pyramid(height=6, symbol="^"))

    # --- Error Handling Cases ---
    print("\n--- Testing Error Handling ---")
    try:
        print("\nAttempting to draw with an invalid symbol (multi-character)...")
        artist.draw_square(5, "@@")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with an invalid dimension (negative width)...")
        artist.draw_rectangle(-5, 5, "$")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with a non-integer height...")
        artist.draw_pyramid(height=4.5, symbol="%") # type: ignore
    except TypeError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with a whitespace symbol...")
        artist.draw_triangle(width=5, height=5, symbol=" ")
    except ValueError as e:
        print(f"Caught expected error: {e}")
