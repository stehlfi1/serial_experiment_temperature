
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which offers a suite of methods
to draw various geometric shapes using user-defined symbols. The implementation
focuses on code quality, robustness, and adherence to best practices.
"""

import math
from typing import List

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a simple interface for creating filled, geometric shapes
    as multi-line strings. It includes validation to ensure that the generated
    art is based on valid, safe inputs.
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates the symbol used for drawing.

        Args:
            symbol: The character to be used for drawing the shape.

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
                "Symbol must be a single, printable, non-whitespace character."
            )

    def _validate_dimensions(self, *dims: int) -> None:
        """
        Validates the dimensions (width, height) for a shape.

        Args:
            *dims: A variable number of integer dimensions to validate.

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive integer (> 0).
        """
        for dim in dims:
            if not isinstance(dim, int):
                raise TypeError("Dimensions (width, height) must be integers.")
            if dim <= 0:
                raise ValueError("Dimensions (width, height) must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        A square is a special case of a rectangle where width equals height.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the square.
        """
        # A square is a rectangle with equal sides. We can reuse the rectangle logic.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the rectangle.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width, height)

        row: str = symbol * width
        art_lines: List[str] = [row] * height
        return "\n".join(art_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's top and bottom sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the parallelogram.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width, height)

        art_lines: List[str] = []
        base_row: str = symbol * width
        for i in range(height):
            # Prepend 'i' spaces to shift the row to the right
            line = " " * i + base_row
            art_lines.append(line)
        return "\n".join(art_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner, expanding to the specified
        width at its base over the given height.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the right-angled triangle.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width, height)

        art_lines: List[str] = []
        for i in range(1, height + 1):
            # Calculate the number of symbols for the current row based on a
            # linear growth from 1 to `width` over `height` rows.
            # math.ceil ensures the shape is filled and grows correctly.
            num_symbols = math.ceil(i * width / height)
            line = symbol * num_symbols
            art_lines.append(line)
        return "\n".join(art_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the pyramid.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(height)

        art_lines: List[str] = []
        for i in range(height):
            # For row `i` (0-indexed):
            # Number of symbols is 2*i + 1
            # Leading spaces for centering is (height - 1 - i)
            num_symbols = 2 * i + 1
            num_spaces = height - 1 - i
            line = " " * num_spaces + symbol * num_symbols
            art_lines.append(line)
        return "\n".join(art_lines)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    # --- Demonstration ---
    # Create an instance of the AsciiArt class
    artist = AsciiArt()
    
    print("--- ASCII Art Shape Generator ---")

    try:
        print("\nSquare (5x5, symbol '#'):")
        print(artist.draw_square(5, "#"))

        print("\nRectangle (8x4, symbol '*'):")
        print(artist.draw_rectangle(8, 4, "*"))

        print("\nParallelogram (10x5, symbol '='):")
        print(artist.draw_parallelogram(10, 5, "="))

        print("\nRight-Angled Triangle (width=10, height=5, symbol '+'):")
        print(artist.draw_triangle(10, 5, "+"))

        print("\nPyramid (height=6, symbol '^'):")
        print(artist.draw_pyramid(6, "^"))

        # --- Demonstration of Error Handling ---
        print("\n--- Testing Error Handling ---")
        
        print("\nAttempting to draw with an invalid symbol...")
        try:
            artist.draw_square(3, "@@")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\nAttempting to draw with a negative dimension...")
        try:
            artist.draw_rectangle(5, -3, "%")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("\nAttempting to draw with a non-integer dimension...")
        try:
            artist.draw_pyramid(4.5, "$") # type: ignore
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

