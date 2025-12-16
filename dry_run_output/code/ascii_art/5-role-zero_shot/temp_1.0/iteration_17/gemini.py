
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains methods for drawing
various geometric shapes using a specified character. The implementation adheres
to high-quality software standards, focusing on correctness, efficiency, and
maintainability as outlined in ISO/IEC 25010.
"""

import sys
from typing import final


@final
class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a suite of methods to draw filled geometric shapes
    as multi-line strings. It emphasizes robust input validation and clean,
    maintainable, and efficient code.
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, printable, non-whitespace character.

        Args:
            symbol: The character to be used for drawing.

        Raises:
            ValueError: If the symbol is not a single character, is whitespace,
                        or is not printable.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError(
                "Symbol must be a printable, non-whitespace character."
            )

    def _validate_positive_integer(self, value: int, name: str) -> None:
        """
        Validates that a given dimension is a positive integer.

        Args:
            value: The integer value to validate.
            name: The name of the parameter, used for a descriptive error message.

        Raises:
            ValueError: If the value is not a positive integer.
            TypeError: If the value is not an integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method is a convenience wrapper around draw_rectangle.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the square.

        Raises:
            ValueError: On invalid width or symbol.
            TypeError: If width is not an integer or symbol is not a string.
        """
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            ValueError: On invalid width, height, or symbol.
            TypeError: If dimensions are not integers or symbol is not a string.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        # Use a list comprehension and join for efficient string building.
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's parallel sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            ValueError: On invalid width, height, or symbol.
            TypeError: If dimensions are not integers or symbol is not a string.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            padding = " " * i
            content = symbol * width
            rows.append(f"{padding}{content}")
        return "\n".join(rows)

    def draw_triangle(self, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left, increasing its width by one
        symbol per row. The base of the triangle will be `height` characters wide.

        Args:
            height: The height (and also the base width) of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the triangle.

        Raises:
            ValueError: On invalid height or symbol.
            TypeError: If height is not an integer or symbol is not a string.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        # In this context, width is implicitly determined by height for a
        # simple right-angled ASCII triangle.
        return "\n".join([symbol * (i + 1) for i in range(height)])

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The number of rows in the pyramid.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            ValueError: On invalid height or symbol.
            TypeError: If height is not an integer or symbol is not a string.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Calculate padding and number of symbols for the current level.
            padding_count = height - 1 - i
            symbol_count = 2 * i + 1
            
            padding = " " * padding_count
            content = symbol * symbol_count
            rows.append(f"{padding}{content}")
        return "\n".join(rows)


def main() -> None:
    """
    Main function to demonstrate the AsciiArt class functionality.
    This function is executed when the script is run directly.
    """
    art = AsciiArt()
    print("--- ASCII Art Shape Generator ---")

    try:
        # --- Demonstration of valid shapes ---
        print("\n[1] Square (5x5, #)")
        print(art.draw_square(width=5, symbol="#"))

        print("\n[2] Rectangle (8x4, @)")
        print(art.draw_rectangle(width=8, height=4, symbol="@"))
        
        print("\n[3] Parallelogram (7x5, *)")
        print(art.draw_parallelogram(width=7, height=5, symbol="*"))

        print("\n[4] Right-Angled Triangle (height 6, +)")
        print(art.draw_triangle(height=6, symbol="+"))

        print("\n[5] Pyramid (height 5, ^)")
        print(art.draw_pyramid(height=5, symbol="^"))

        # --- Demonstration of error handling ---
        print("\n--- Testing Error Handling ---")
        try:
            print("\nAttempting to draw with an invalid symbol (multi-character)...")
            art.draw_square(3, "XX")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            print("\nAttempting to draw with an invalid symbol (whitespace)...")
            art.draw_square(3, " ")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            print("\nAttempting to draw with a negative dimension...")
            art.draw_rectangle(width=-4, height=5, symbol="X")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            print("\nAttempting to draw with a non-integer dimension...")
            art.draw_pyramid(height=4.5, symbol="^")
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
