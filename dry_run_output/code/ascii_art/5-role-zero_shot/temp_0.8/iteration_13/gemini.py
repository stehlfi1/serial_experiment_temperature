
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains methods for drawing
various geometric shapes using text characters. It is designed with a focus
on correctness, efficiency, and maintainability, adhering to best practices
and the ISO/IEC 25010 standard for software quality.

Author: AI Assistant (Senior Software Developer)
Version: 1.0.0
"""

import math
from typing import List

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides a suite of methods to draw various geometric shapes
    using a specified character. It ensures all inputs are valid and produces
    string representations of the shapes, ready for console output.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Implements all required shape-drawing functions.
    - Performance Efficiency: Uses efficient string-building techniques (`str.join`).
    - Reliability (Maturity, Fault Tolerance): Includes robust input validation
      to handle incorrect inputs gracefully by raising appropriate errors.
    - Maintainability (Modularity, Reusability, Analyzability, Modifiability):
      Code is modular (class-based), reusable (e.g., square uses rectangle),
      and clearly documented with docstrings and type hints.
    - Usability (Learnability): The API is straightforward and well-documented.
    """

    @staticmethod
    def _validate_inputs(symbol: str, **dimensions: int) -> None:
        """
        Private helper to validate common inputs for shape drawing functions.

        This method centralizes input validation to ensure consistency and
        adherence to the DRY (Don't Repeat Yourself) principle.

        Args:
            symbol: The character to use for drawing.
            **dimensions: Keyword arguments representing shape dimensions (e.g., width, height).

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if any dimension is not a positive integer.
            TypeError: If any dimension is not an integer.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")

        for name, value in dimensions.items():
            if not isinstance(value, int):
                # Using TypeError for incorrect type is more specific.
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII art square.
        
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        # A square is a special case of a rectangle. This promotes code reuse.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII art rectangle.
            
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        
        row = symbol * width
        # Using a list comprehension and str.join is more performant
        # than repeated string concatenation in a loop.
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that slants to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's top/bottom edge.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art parallelogram.
            
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        
        shape_rows: List[str] = []
        base_row = symbol * width
        for i in range(height):
            padding = " " * i
            shape_rows.append(f"{padding}{base_row}")
        
        return "\n".join(shape_rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner, with its width scaling
        proportionally to its height. The final row will have the specified width.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art triangle.
            
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        
        shape_rows: List[str] = []
        for i in range(1, height + 1):
            # Calculate the number of symbols for the current row based on a
            # linear slope. math.ceil ensures the shape is filled and grows.
            num_symbols = math.ceil(i * width / height)
            shape_rows.append(symbol * num_symbols)
            
        return "\n".join(shape_rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art pyramid.
            
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol=symbol, height=height)
        
        shape_rows: List[str] = []
        # The width of the pyramid's base determines the padding for all rows.
        max_width = (2 * (height - 1)) + 1
        
        for i in range(height):
            num_symbols = (2 * i) + 1
            padding_width = (max_width - num_symbols) // 2
            padding = " " * padding_width
            row_symbols = symbol * num_symbols
            shape_rows.append(f"{padding}{row_symbols}")
            
        return "\n".join(shape_rows)


if __name__ == "__main__":
    """
    Main execution block to demonstrate the AsciiArt class functionality.
    
    This block serves as a basic smoke test and usage example. For comprehensive
    verification, dedicated unit tests should be used.
    """
    # Instantiate the drawing class
    artist = AsciiArt()
    
    print("--- ASCII Art Shape Generator ---")
    
    try:
        # --- Demonstration of valid shapes ---
        print("\n[+] 5x5 Square with '#':")
        print(artist.draw_square(width=5, symbol="#"))
        
        print("\n[+] 8x4 Rectangle with '*':")
        print(artist.draw_rectangle(width=8, height=4, symbol="*"))

        print("\n[+] 6x5 Parallelogram with '%':")
        print(artist.draw_parallelogram(width=6, height=5, symbol="%"))

        print("\n[+] 10x5 Right-Angled Triangle with '+':")
        print(artist.draw_triangle(width=10, height=5, symbol="+"))

        print("\n[+] 6-level Pyramid with '^':")
        print(artist.draw_pyramid(height=6, symbol="^"))
        
        # --- Demonstration of error handling ---
        print("\n--- Testing Error Handling ---")
        
        print("\n[!] Attempting to draw with an invalid symbol (multi-character)...")
        try:
            artist.draw_square(width=3, symbol="XX")
        except ValueError as e:
            print(f"    Caught expected error: {e}")

        print("\n[!] Attempting to draw with an invalid symbol (whitespace)...")
        try:
            artist.draw_square(width=3, symbol=" ")
        except ValueError as e:
            print(f"    Caught expected error: {e}")

        print("\n[!] Attempting to draw with a negative dimension...")
        try:
            artist.draw_rectangle(width=-5, height=4, symbol="$")
        except ValueError as e:
            print(f"    Caught expected error: {e}")

        print("\n[!] Attempting to draw with a non-integer dimension...")
        try:
            artist.draw_pyramid(height=4.5, symbol="&")
        except TypeError as e:
            print(f"    Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

