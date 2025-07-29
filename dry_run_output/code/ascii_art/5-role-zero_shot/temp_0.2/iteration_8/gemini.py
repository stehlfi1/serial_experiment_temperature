
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains methods for drawing
various geometric shapes using ASCII characters. The implementation prioritizes
code quality, adhering to principles of the ISO/IEC 25010 standard, including:
- Functional Suitability: Correctly generates the specified shapes.
- Performance Efficiency: Uses efficient string and list operations.
- Reliability: Implements robust input validation and error handling.
- Maintainability: Features a modular, object-oriented design with clear,
  documented, and testable code.
- Usability: Provides a clear and consistent API.
"""

from typing import Tuple


class AsciiArt:
    """
    A utility class for generating various 2D ASCII art shapes.

    This class provides a collection of stateless methods to draw geometric
    shapes like squares, rectangles, and pyramids. All methods validate
    their inputs and return the resulting shape as a multi-line string.
    """

    def _validate_inputs(self, symbol: str, *dims: int) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper ensures that the symbol is a single, non-whitespace
        character and that all dimensional arguments (like width, height) are
        positive integers.

        Args:
            symbol: The character to use for drawing.
            *dims: A variable number of integer dimensions (e.g., width, height).

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single character, is whitespace,
                        or if any dimension is not a positive number.
        """
        # Validate symbol type
        if not isinstance(symbol, str):
            raise TypeError("The 'symbol' argument must be a string.")

        # Validate symbol properties
        if len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        # Validate dimension types and values
        for i, dim in enumerate(dims):
            if not isinstance(dim, int):
                # Providing a more specific error message
                arg_names = ('width', 'height')
                arg_name = arg_names[i] if i < len(arg_names) else f"dimension {i+1}"
                raise TypeError(f"The '{arg_name}' argument must be an integer.")
            if dim <= 0:
                arg_names = ('width', 'height')
                arg_name = arg_names[i] if i < len(arg_names) else f"dimension {i+1}"
                raise ValueError(f"The '{arg_name}' argument must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the square.

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If inputs have invalid values.
        """
        # A square is a rectangle with equal width and height.
        # This promotes code reuse and reduces redundancy.
        return self.draw_rectangle(width, width, symbol)

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
            TypeError: If inputs have incorrect types.
            ValueError: If inputs have invalid values.
        """
        self._validate_inputs(symbol, width, height)
        row = symbol * width
        # Using a list comprehension and join is more efficient than
        # repeated string concatenation in a loop.
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width: The width of the parallelogram's parallel sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If inputs have invalid values.
        """
        self._validate_inputs(symbol, width, height)
        shape_part = symbol * width
        rows = [" " * i + shape_part for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle's base will have the specified width, and it will grow
        linearly from a single point at the top-left to the full width at the base.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the right-angled triangle.

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If inputs have invalid values.
        """
        self._validate_inputs(symbol, width, height)
        rows = []
        for i in range(height):
            # Calculate the width of the current row using linear interpolation.
            # This ensures the triangle scales correctly to the given width and height.
            # The formula `(a * b + c - 1) // c` is a robust way to calculate
            # ceiling division `ceil(a * b / c)` for positive integers.
            current_width = ((i + 1) * width + height - 1) // height
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        The pyramid has a base width of (2 * height - 1).

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If inputs have invalid values.
        """
        # For a pyramid, only height is needed as width is derived from it.
        self._validate_inputs(symbol, height)
        
        # The total width of the pyramid's base
        base_width = 2 * height - 1
        
        rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            padding = (base_width - num_symbols) // 2
            rows.append(" " * padding + symbol * num_symbols)
        return "\n".join(rows)


if __name__ == "__main__":
    # This block serves as a demonstration of the AsciiArt class functionality.
    # It is executed only when the script is run directly.
    
    artist = AsciiArt()
    
    print("--- ASCII Art Generator Demo ---")

    try:
        print("\n[+] Drawing a 5x5 Square with '#':")
        print(artist.draw_square(5, "#"))

        print("\n[+] Drawing a 10x4 Rectangle with '*':")
        print(artist.draw_rectangle(10, 4, "*"))

        print("\n[+] Drawing a 8x5 Parallelogram with '=':")
        print(artist.draw_parallelogram(8, 5, "="))

        print("\n[+] Drawing a 10x5 Right-Angled Triangle with '+':")
        print(artist.draw_triangle(10, 5, "+"))

        print("\n[+] Drawing a Pyramid of height 6 with '^':")
        print(artist.draw_pyramid(6, "^"))

        # --- Demonstration of Error Handling ---
        print("\n--- Testing Error Handling ---")
        
        print("\n[!] Testing invalid symbol (multiple characters)...")
        try:
            artist.draw_square(5, "@@")
        except ValueError as e:
            print(f"   Caught expected error: {e}")

        print("\n[!] Testing invalid symbol (whitespace)...")
        try:
            artist.draw_square(5, " ")
        except ValueError as e:
            print(f"   Caught expected error: {e}")
            
        print("\n[!] Testing invalid dimension (zero)...")
        try:
            artist.draw_rectangle(0, 5, "X")
        except ValueError as e:
            print(f"   Caught expected error: {e}")

        print("\n[!] Testing invalid dimension type (float)...")
        try:
            artist.draw_pyramid(4.5, "O")
        except TypeError as e:
            print(f"   Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during the demo: {e}")

