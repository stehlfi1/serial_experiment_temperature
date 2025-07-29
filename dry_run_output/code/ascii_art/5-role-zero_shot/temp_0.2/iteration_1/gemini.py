
"""
ascii_art_generator.py

This module provides a class for generating 2D ASCII art shapes.

It is designed with the ISO/IEC 25010 standard in mind, emphasizing:
- Functional Suitability: Correctly generates specified ASCII shapes.
- Performance Efficiency: Uses efficient string operations.
- Reliability: Robust input validation prevents common errors.
- Usability: A clear and simple API with comprehensive documentation.
- Maintainability: The code is modular, readable, and easily extensible.
- Portability: Uses only standard Python libraries.
"""

import math
from typing import Dict, Any

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class encapsulates the logic for drawing geometric shapes as multi-line
    string representations. It provides a clean interface and ensures all inputs
    are validated for safety and correctness.
    """

    def _validate_input(self, symbol: str, dimensions: Dict[str, Any]) -> None:
        """
        Private helper method to validate input parameters.

        This centralized validation method ensures that the symbol and dimensions
        meet the required criteria, promoting code reusability and reliability.

        Args:
            symbol (str): The character to be used for drawing.
            dimensions (Dict[str, Any]): A dictionary of dimension names and their values.

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character.
            ValueError: If any dimension is not a positive integer.
            TypeError: If any dimension is not an integer.
        """
        # Validate symbol
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        # Validate dimensions
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The dimension '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"The dimension '{name}' must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is not positive or symbol is invalid.
            TypeError: If width is not an integer.
        """
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle. Must be a positive integer.
            height (int): The height of the rectangle. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
            TypeError: If width/height are not integers.
        """
        self._validate_input(symbol, {"width": width, "height": height})
        
        row = symbol * width
        # Use a list comprehension and join for performance and readability
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is indented by one additional space.

        Args:
            width (int): The width of the parallelogram. Must be a positive integer.
            height (int): The height of the parallelogram. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
            TypeError: If width/height are not integers.
        """
        self._validate_input(symbol, {"width": width, "height": height})
        
        shape_rows = []
        base_row = symbol * width
        for i in range(height):
            # Prepend 'i' spaces to create the skew
            indent = " " * i
            shape_rows.append(f"{indent}{base_row}")
            
        return "\n".join(shape_rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner. The width of each row is
        calculated based on the overall width and height to create a smooth slope.

        Args:
            width (int): The base width of the triangle. Must be a positive integer.
            height (int): The height of the triangle. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
            TypeError: If width/height are not integers.
        """
        self._validate_input(symbol, {"width": width, "height": height})
        
        shape_rows = []
        for i in range(height):
            # Calculate the width of the current row based on the slope
            # (i + 1) ensures the first row is not zero-width
            # math.ceil ensures a filled shape that reaches the full width
            current_width = math.ceil((i + 1) * width / height)
            shape_rows.append(symbol * current_width)
            
        return "\n".join(shape_rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is not positive or symbol is invalid.
            TypeError: If height is not an integer.
        """
        self._validate_input(symbol, {"height": height})
        
        shape_rows = []
        for i in range(height):
            # Number of symbols in the current row (1, 3, 5, ...)
            num_symbols = 2 * i + 1
            # Number of leading spaces for centering
            num_spaces = height - 1 - i
            
            indent = " " * num_spaces
            symbols = symbol * num_symbols
            shape_rows.append(f"{indent}{symbols}")
            
        return "\n".join(shape_rows)


# --- Example Usage ---
# This block demonstrates how to use the AsciiArt class and is executed
# only when the script is run directly. It serves as a basic test and
# usage guide.
if __name__ == "__main__":
    artist = AsciiArt()
    
    print("--- ASCII Art Generator ---")

    try:
        print("\n[+] Drawing a 5x5 Square with '#':")
        print(artist.draw_square(width=5, symbol="#"))

        print("\n[+] Drawing a 10x4 Rectangle with '*':")
        print(artist.draw_rectangle(width=10, height=4, symbol="*"))

        print("\n[+] Drawing a 12x5 Parallelogram with '=':")
        print(artist.draw_parallelogram(width=12, height=5, symbol="="))

        print("\n[+] Drawing a 10x5 Right-Angled Triangle with 'A':")
        print(artist.draw_triangle(width=10, height=5, symbol="A"))

        print("\n[+] Drawing a Pyramid of height 6 with 'O':")
        print(artist.draw_pyramid(height=6, symbol="O"))

        # --- Error Handling Demonstration ---
        print("\n--- Testing Error Handling ---")
        
        print("\n[!] Testing with invalid symbol (multi-character)...")
        try:
            artist.draw_square(3, "@@")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\n[!] Testing with invalid symbol (whitespace)...")
        try:
            artist.draw_square(3, " ")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\n[!] Testing with invalid dimension (negative)...")
        try:
            artist.draw_rectangle(-5, 5, "$")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("\n[!] Testing with invalid dimension type (float)...")
        try:
            artist.draw_pyramid(4.5, "X") # type: ignore
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}")

