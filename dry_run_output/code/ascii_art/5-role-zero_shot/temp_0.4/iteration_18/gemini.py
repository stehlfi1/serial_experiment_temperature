
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements an interface for drawing
various geometric shapes using ASCII characters. The implementation prioritizes
code quality characteristics as defined by the ISO/IEC 25010 standard:

- Functional Suitability: Each function correctly generates the specified shape.
- Performance Efficiency: String generation uses efficient methods (`str.join`).
- Reliability & Safety: Robust input validation prevents errors from invalid arguments.
- Maintainability & Modularity: Logic is encapsulated within a class, with a
  centralized private static method for validation to reduce redundancy.
- Testability: Methods are pure functions that return strings, making them easy
  to verify in unit tests.
- Readability: The code is documented with docstrings, type hints, and clear
  variable names.
"""

from typing import List


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a collection of methods to draw filled geometric shapes
    like squares, rectangles, and pyramids as multi-line strings.
    """

    @staticmethod
    def _validate_inputs(symbol: str, **dimensions: int) -> None:
        """
        Validates the symbol and dimension inputs for all drawing methods.

        This private static method ensures that the provided symbol is a single,
        non-whitespace character and that all dimension arguments (e.g., width,
        height) are positive integers.

        Args:
            symbol: The character to use for drawing.
            **dimensions: A keyword dictionary of dimension names and their
                          integer values (e.g., width=5, height=10).

        Raises:
            TypeError: If a dimension is not an integer or the symbol is not a string.
            ValueError: If the symbol is not a single character, is whitespace,
                        or if any dimension is non-positive (<= 0).
        """
        if not isinstance(symbol, str):
            raise TypeError("The 'symbol' argument must be a string.")
        if len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The '{name}' argument must be an integer.")
            if value <= 0:
                raise ValueError(f"The '{name}' argument must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.
        """
        self._validate_inputs(symbol, width=width)
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

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
        row: str = symbol * width
        rows: List[str] = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is shifted one space to the right relative to the
        row above it.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows: List[str] = []
        base_row: str = symbol * width
        for i in range(height):
            padding = " " * i
            rows.append(f"{padding}{base_row}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle starts at the top-left and grows towards the bottom-right.
        The width of each row is scaled proportionally to its vertical position
        to ensure the base has the specified `width`.

        Args:
            width: The width of the triangle's base (the last row).
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the right-angled triangle.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows: List[str] = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            # The ratio (i + 1) / height determines the row's progress,
            # which is then scaled by the final width.
            # We use max(1, ...) to ensure even the first row has at least one symbol.
            current_width = max(1, int(((i + 1) / height) * width))
            rows.append(symbol * current_width)
        return "\n".join(rows)

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
        rows: List[str] = []
        # The width of the pyramid's base
        base_width = 2 * height - 1
        for i in range(height):
            # Number of symbols in the current row (1, 3, 5, ...)
            num_symbols = 2 * i + 1
            # Number of spaces on each side for centering
            padding = " " * ((base_width - num_symbols) // 2)
            row_symbols = symbol * num_symbols
            rows.append(f"{padding}{row_symbols}")
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    artist = AsciiArt()
    
    print("--- Demonstrating Shape Drawing ---")
    
    print("\nSquare (5x5, symbol '#'):")
    print(artist.draw_square(width=5, symbol="#"))
    
    print("\nRectangle (8x4, symbol '@'):")
    print(artist.draw_rectangle(width=8, height=4, symbol="@"))
    
    print("\nParallelogram (10x5, symbol '='):")
    print(artist.draw_parallelogram(width=10, height=5, symbol="="))

    print("\nRight-Angled Triangle (width=10, height=5, symbol '*'):")
    print(artist.draw_triangle(width=10, height=5, symbol="*"))
    
    print("\nPyramid (height=6, symbol '^'):")
    print(artist.draw_pyramid(height=6, symbol="^"))

    print("\n--- Demonstrating Input Validation ---")

    try:
        print("\nAttempting to draw with an invalid symbol (multi-character)...")
        artist.draw_square(5, "!!")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with an invalid dimension (negative width)...")
        artist.draw_rectangle(-5, 5, "x")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with a non-integer height...")
        artist.draw_pyramid(height=4.5, symbol="o")
    except TypeError as e:
        print(f"Caught expected error: {e}")

