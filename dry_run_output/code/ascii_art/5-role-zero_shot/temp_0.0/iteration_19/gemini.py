
"""
ascii_art_generator.py

A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements an interface for
drawing various geometric shapes using printable ASCII characters. The design
prioritizes clean, testable, and maintainable code, following best practices
and principles aligned with the ISO/IEC 25010 standard for software quality.
"""

import math

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides methods to draw simple geometric shapes like squares,
    rectangles, and pyramids using ASCII characters. It adheres to high-quality
    code standards, including robust input validation and clear documentation,
    aligning with the principles of ISO/IEC 25010.

    Attributes:
        None
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates the symbol used for drawing.

        Args:
            symbol (str): The character to validate.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def _validate_dimension(self, value: int, name: str) -> None:
        """
        Validates a dimension (e.g., width, height).

        Args:
            value (int): The dimension value to validate.
            name (str): The name of the dimension for error messages.

        Raises:
            TypeError: If the value is not an integer.
            ValueError: If the value is not a positive integer (> 0).
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        # A square is a rectangle with equal width and height.
        # Validation will be handled by draw_rectangle.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        # More efficient than building a list of identical strings in a loop
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width (int): The width of the parallelogram's top/bottom sides.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        shape_row = symbol * width
        rows = [f"{' ' * i}{shape_row}" for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from a single point at the top-left to a base
        of the specified width, distributed over the specified height.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        # Handle the edge case of a single-line shape to avoid division by zero.
        if height == 1:
            return symbol * width

        for i in range(height):
            # Use linear interpolation to calculate the width of each row.
            # This creates a straight-looking diagonal edge.
            # The formula ensures the first row has 1 symbol and the last has `width` symbols.
            num_symbols = (i * (width - 1)) // (height - 1) + 1
            rows.append(symbol * num_symbols)

        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            # The total width of the pyramid's base is (2 * height - 1).
            # Centering is achieved by adding leading spaces.
            num_spaces = height - 1 - i
            rows.append(f"{' ' * num_spaces}{symbol * num_symbols}")

        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It serves as a simple, informal test and example.
    
    # --- Configuration ---
    art_generator = AsciiArt()
    SHAPE_SYMBOL = '*'

    # --- Demonstration ---
    print("--- ASCII Art Shape Generator ---")

    try:
        print("\n[+] Square (5x5):")
        print(art_generator.draw_square(5, SHAPE_SYMBOL))

        print("\n[+] Rectangle (8x4):")
        print(art_generator.draw_rectangle(8, 4, '#'))

        print("\n[+] Parallelogram (10x5):")
        print(art_generator.draw_parallelogram(10, 5, '='))

        print("\n[+] Right-Angled Triangle (width=7, height=7):")
        print(art_generator.draw_triangle(7, 7, 'A'))
        
        print("\n[+] Right-Angled Triangle (width=10, height=5):")
        print(art_generator.draw_triangle(10, 5, 'B'))

        print("\n[+] Pyramid (height=6):")
        print(art_generator.draw_pyramid(6, '^'))

        # --- Error Handling Demonstration ---
        print("\n--- Testing Error Handling ---")
        
        print("\n[!] Testing invalid symbol (multi-char)...")
        art_generator.draw_square(3, "@@")

    except (ValueError, TypeError) as e:
        print(f"Successfully caught expected error: {e}")

    try:
        print("\n[!] Testing invalid dimension (negative)...")
        art_generator.draw_rectangle(-5, 5, SHAPE_SYMBOL)
        
    except (ValueError, TypeError) as e:
        print(f"Successfully caught expected error: {e}")

    try:
        print("\n[!] Testing invalid dimension type (float)...")
        art_generator.draw_pyramid(4.5, SHAPE_SYMBOL)

    except (ValueError, TypeError) as e:
        print(f"Successfully caught expected error: {e}")
