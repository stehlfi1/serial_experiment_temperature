
"""
ascii_art_generator.py

This module provides the AsciiArt class for generating various 2D shapes
using ASCII characters.

The implementation adheres to the principles of the ISO/IEC 25010 standard
for software product quality, focusing on:
- Functional Suitability: Correctly generates the specified shapes.
- Performance Efficiency: Uses efficient string and list operations.
- Reliability (Fault Tolerance): Robustly handles invalid user inputs.
- Maintainability: Code is modular, readable, and well-documented.
- Usability: A clear and predictable API.
"""

import math

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various geometric shapes using
    a specified symbol. It includes validation to ensure that the inputs
    are sensible and the output is predictable. Each method returns a
    multi-line string representing the generated shape.
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates the symbol for drawing.

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

    def _validate_dimensions(self, **dimensions: int) -> None:
        """
        Validates that dimensions are positive integers.

        Args:
            **dimensions: Keyword arguments representing dimensions (e.g., width=5).

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive number (> 0).
        """
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"Dimension '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"Dimension '{name}' must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.
        """
        # A square is a rectangle with equal width and height.
        # This promotes code reuse and reduces redundancy.
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
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)

        row = symbol * width
        # Use a list comprehension and join for efficient string building.
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)

        shape_rows = []
        for i in range(height):
            padding = " " * i
            content = symbol * width
            shape_rows.append(f"{padding}{content}")

        return "\n".join(shape_rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle's base is determined by 'width' and its height by 'height'.
        The number of symbols in each row is scaled proportionally.

        Args:
            width: The width of the triangle's base (last row).
            height: The height of the triangle (number of rows).
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the right-angled triangle.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)

        shape_rows = []
        for i in range(1, height + 1):
            # Calculate the number of symbols for the current row, ensuring
            # it scales correctly from 1 to the final width.
            # Using max(1, ...) ensures the first row is never empty.
            num_symbols = max(1, math.ceil(i * width / height))
            shape_rows.append(symbol * num_symbols)

        return "\n".join(shape_rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid (number of rows).
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the pyramid.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(height=height)

        shape_rows = []
        # The total width of the pyramid's base is 2 * height - 1
        for i in range(1, height + 1):
            num_symbols = 2 * i - 1
            padding = " " * (height - i)
            shape_rows.append(f"{padding}{symbol * num_symbols}")

        return "\n".join(shape_rows)


# --- Main execution block for demonstration ---
if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class and serves as
    # a basic manual test. It will only run when the script is executed directly.

    art = AsciiArt()
    print("--- ASCII Art Generator Demonstration ---")

    # --- 1. Successful Shape Drawing ---
    print("\n[+] Drawing a 5x5 Square with '#':")
    print(art.draw_square(width=5, symbol="#"))

    print("\n[+] Drawing a 10x4 Rectangle with '@':")
    print(art.draw_rectangle(width=10, height=4, symbol="@"))

    print("\n[+] Drawing a 12x5 Parallelogram with '=':")
    print(art.draw_parallelogram(width=12, height=5, symbol="="))

    print("\n[+] Drawing a Right-Angled Triangle (W:10, H:5) with '*':")
    print(art.draw_triangle(width=10, height=5, symbol="*"))

    print("\n[+] Drawing a Pyramid (H:6) with '^':")
    print(art.draw_pyramid(height=6, symbol="^"))

    # --- 2. Error Handling Demonstration ---
    print("\n--- Error Handling Tests ---")

    def test_error(description: str, function_call):
        """Helper function to test for expected errors."""
        print(f"\n[!] Testing: {description}")
        try:
            function_call()
        except (ValueError, TypeError) as e:
            print(f"   -> Successfully caught expected error: {e}")

    test_error(
        "Invalid Symbol (multiple characters)",
        lambda: art.draw_square(5, "##")
    )
    test_error(
        "Invalid Symbol (whitespace)",
        lambda: art.draw_square(5, " ")
    )
    test_error(
        "Invalid Dimension (negative width)",
        lambda: art.draw_rectangle(-5, 5, "X")
    )
    test_error(
        "Invalid Dimension (zero height)",
        lambda: art.draw_pyramid(0, "$")
    )
    test_error(
        "Invalid Type (float dimension)",
        lambda: art.draw_triangle(5.5, 5, "T")
    )
