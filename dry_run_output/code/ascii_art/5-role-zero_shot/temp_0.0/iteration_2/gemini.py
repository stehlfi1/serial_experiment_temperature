
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements an interface for
drawing various geometric shapes using ASCII characters. The implementation
adheres to the principles of the ISO/IEC 25010 standard for software quality,
focusing on:

- Functional Suitability: Correctly generates the specified shapes.
- Performance Efficiency: Uses efficient string operations and algorithms.
- Reliability (Fault Tolerance): Includes robust input validation to handle
  invalid arguments gracefully.
- Usability: Features a clear, well-documented, and easy-to-use API.
- Maintainability: The code is modular, readable, and easily extensible.
- Portability: Uses only the Python standard library, ensuring it runs on any
  platform with a Python interpreter.
"""

import math
from typing import Dict


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a collection of methods to draw filled geometric shapes
    like squares, rectangles, and pyramids as multi-line strings.
    """

    def _validate_inputs(self, symbol: str, dimensions: Dict[str, int]) -> None:
        """
        A private helper method to validate input parameters.

        This method centralizes input validation logic to ensure that the symbol
        and dimensions (width, height) meet the required criteria, promoting
        code reusability and reliability.

        Args:
            symbol: The character to use for drawing.
            dimensions: A dictionary of dimension names and their integer values.

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if any dimension is not a positive integer.
            TypeError: If a dimension is not of type int.
        """
        # Symbol validation
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        # Dimension validation
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.
        
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, {'width': width})
        row = symbol * width
        # Create a list of rows and join them with newlines for efficiency
        return "\n".join([row] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        row = symbol * width
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram leaning to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's top/bottom side.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        # Use a list comprehension for concise and readable row generation
        lines = [" " * i + symbol * width for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle's slope is determined by the width and height, growing
        from the top-left corner.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the right-angled triangle.

        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        lines = []
        for i in range(height):
            # Calculate the number of symbols for the current row based on the slope
            # math.ceil ensures that the triangle starts with at least one symbol
            num_symbols = math.ceil((i + 1) * (width / height))
            # Ensure the number of symbols does not exceed the specified width
            num_symbols = min(num_symbols, width)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, {'height': height})
        lines = []
        for i in range(height):
            padding = " " * (height - 1 - i)
            body = symbol * (2 * i + 1)
            lines.append(f"{padding}{body}")
        return "\n".join(lines)


# --- Main execution block for demonstration ---
if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class and also serves
    # as a simple visual test of the output.
    
    artist = AsciiArt()
    
    print("--- ASCII Art Generator ---")

    try:
        print("\nSquare (5x5, '#'):")
        print(artist.draw_square(5, "#"))

        print("\nRectangle (8x4, '*'):")
        print(artist.draw_rectangle(8, 4, "*"))

        print("\nParallelogram (10x5, '='):")
        print(artist.draw_parallelogram(10, 5, "="))

        print("\nRight-Angled Triangle (width=10, height=5, '+'):")
        print(artist.draw_triangle(10, 5, "+"))
        
        print("\nRight-Angled Triangle (width=7, height=7, 'T'):")
        print(artist.draw_triangle(7, 7, "T"))

        print("\nPyramid (height=6, '^'):")
        print(artist.draw_pyramid(6, "^"))

        # --- Demonstration of Error Handling ---
        print("\n--- Testing Error Handling ---")
        try:
            print("Attempting to draw with an invalid symbol ('@@')...")
            artist.draw_square(3, "@@")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            print("Attempting to draw with a whitespace symbol (' ')...")
            artist.draw_square(3, " ")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            print("Attempting to draw with a negative width (-4)...")
            artist.draw_rectangle(-4, 5, "$")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        try:
            print("Attempting to draw with a non-integer height (5.5)...")
            artist.draw_rectangle(4, 5.5, "$") # type: ignore
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}")

