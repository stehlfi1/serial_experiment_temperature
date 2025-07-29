
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods for drawing
various geometric shapes using user-specified symbols. The implementation
adheres to high-quality coding standards, focusing on correctness,
efficiency, and maintainability as outlined by ISO/IEC 25010.
"""

import math
from typing import List

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class encapsulates methods for drawing simple geometric shapes like
    squares, rectangles, and pyramids. It ensures that all inputs are
    validated to produce reliable and predictable output.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace character.

        Args:
            symbol: The character to use for drawing.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single character or is whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    @staticmethod
    def _validate_dimension(*dims: int) -> None:
        """
        Validates that one or more dimensions are positive integers.

        Args:
            *dims: A variable number of integer dimensions to validate.

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive number (i.e., <= 0).
        """
        for dim in dims:
            if not isinstance(dim, int):
                raise TypeError("Dimensions must be integers.")
            if dim <= 0:
                raise ValueError("Dimensions must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the square.
        """
        # A square is a rectangle with equal width and height.
        # This promotes code reuse and reduces maintenance.
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
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)
        
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width: The width of the parallelogram's top/bottom edge.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the parallelogram.
        """
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)

        rows: List[str] = []
        for i in range(height):
            padding = " " * i
            line = symbol * width
            rows.append(f"{padding}{line}")
        
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner. The width of each row
        is calculated to scale linearly, ensuring the base of the triangle
        reaches the specified width at the final row.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the right-angled triangle.
        """
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)

        rows: List[str] = []
        for i in range(1, height + 1):
            # Calculate the number of symbols for the current row to scale
            # linearly from 1 to the final width.
            # math.ceil ensures the shape is filled and the final row has the correct width.
            current_width = math.ceil(i * width / height)
            rows.append(symbol * current_width)
            
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid (number of rows).
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the pyramid.
        """
        self._validate_dimension(height)
        self._validate_symbol(symbol)

        rows: List[str] = []
        # The width of the pyramid's base is 2*height - 1
        for i in range(height):
            num_symbols = 2 * i + 1
            # Leading spaces for centering the pyramid
            padding = " " * (height - 1 - i)
            rows.append(f"{padding}{symbol * num_symbols}")
            
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class
    # and serves as a quick visual test of the output.
    
    art_generator = AsciiArt()
    
    print("--- ASCII Art Shape Generator ---")
    
    try:
        print("\n[+] Drawing a 5x5 Square with '#':")
        print(art_generator.draw_square(5, "#"))

        print("\n[+] Drawing a 10x4 Rectangle with '*':")
        print(art_generator.draw_rectangle(10, 4, "*"))
        
        print("\n[+] Drawing a 12x5 Parallelogram with '=':")
        print(art_generator.draw_parallelogram(12, 5, "="))

        print("\n[+] Drawing a 10x5 Right-Angled Triangle with '+':")
        print(art_generator.draw_triangle(10, 5, "+"))
        
        print("\n[+] Drawing a 7-level Pyramid with '^':")
        print(art_generator.draw_pyramid(7, "^"))

        # --- Example of Error Handling ---
        print("\n--- Testing Error Handling ---")
        
        print("\n[!] Attempting to draw with an invalid symbol '@@':")
        try:
            art_generator.draw_square(3, "@@")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\n[!] Attempting to draw with a negative width '-5':")
        try:
            art_generator.draw_rectangle(-5, 5, "$")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("\n[!] Attempting to draw with a non-integer dimension '3.5':")
        try:
            art_generator.draw_pyramid(3.5) # type: ignore
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}")

