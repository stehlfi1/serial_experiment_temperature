
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains methods for drawing
various geometric shapes using printable ASCII characters. The implementation
emphasizes code quality, adhering to principles of modularity, safety, and
readability as outlined by ISO/IEC 25010.

Example:
    art_generator = AsciiArt()
    square = art_generator.draw_square(5, '#')
    print(square)
"""

from typing import List

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides methods to draw filled shapes like squares, rectangles,
    parallelograms, triangles, and pyramids using a specified character.
    It adheres to high-quality code standards, including input validation,
    modularity, and clear documentation.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the symbol used for drawing. (Internal Safety Check)

        Args:
            symbol: The character to validate.

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
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates a dimension (e.g., width, height). (Internal Safety Check)

        Args:
            value: The integer value of the dimension.
            name: The name of the dimension for use in error messages.

        Raises:
            TypeError: If the dimension is not an integer.
            ValueError: If the dimension is not a positive integer (> 0).
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square. Must be a positive integer.
            symbol: The single, non-whitespace character to fill the square with.

        Returns:
            A multi-line string representing the ASCII art square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive, or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)
        
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width: The width of the rectangle. Must be a positive integer.
            height: The height of the rectangle. Must be a positive integer.
            symbol: The single, non-whitespace character to fill the rectangle with.

        Returns:
            A multi-line string representing the ASCII art rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive, or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        row: str = symbol * width
        # Performance: Using a list and join is more efficient than string concatenation.
        rows: List[str] = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is indented by one additional space.

        Args:
            width: The width of the parallelogram. Must be a positive integer.
            height: The height of the parallelogram. Must be a positive integer.
            symbol: The single, non-whitespace character to fill the shape with.

        Returns:
            A multi-line string representing the ASCII art parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive, or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows: List[str] = []
        content: str = symbol * width
        for i in range(height):
            indent: str = " " * i
            rows.append(f"{indent}{content}")
        
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from a single point at the top-left, expanding
        to the specified width at the final row.

        Args:
            width: The final width of the triangle's base. Must be a positive integer.
            height: The height of the triangle. Must be a positive integer.
            symbol: The single, non-whitespace character to fill the shape with.

        Returns:
            A multi-line string representing the ASCII art triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive, or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        rows: List[str] = []
        for i in range(height):
            # Calculate the width for the current row, scaling proportionally.
            # We ensure at least one symbol is drawn, even for tall, thin triangles.
            # The formula `(i + 1) * width / height` maps the row index to the target width.
            current_width = max(1, ((i + 1) * width) // height)
            rows.append(symbol * current_width)
            
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid. Must be a positive integer.
            symbol: The single, non-whitespace character to fill the shape with.

        Returns:
            A multi-line string representing the ASCII art pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive, or symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        rows: List[str] = []
        for i in range(height):
            # Number of symbols in the current row.
            num_symbols = 1 + (i * 2)
            # Spaces needed on the left for centering.
            padding_spaces = height - 1 - i
            
            padding = " " * padding_spaces
            content = symbol * num_symbols
            rows.append(f"{padding}{content}")
            
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It also serves as a quick visual test for the drawing functions.
    
    art = AsciiArt()
    
    print("--- ASCII Art Shape Generator ---")
    
    try:
        print("\n[+] Square (5x5, symbol='S')")
        print(art.draw_square(5, 'S'))
        
        print("\n[+] Rectangle (8x4, symbol='R')")
        print(art.draw_rectangle(8, 4, 'R'))
        
        print("\n[+] Parallelogram (10x5, symbol='P')")
        print(art.draw_parallelogram(10, 5, 'P'))
        
        print("\n[+] Right-Angled Triangle (width=12, height=6, symbol='T')")
        print(art.draw_triangle(12, 6, 'T'))

        print("\n[+] Pyramid (height=7, symbol='^')")
        print(art.draw_pyramid(7, '^'))

        # Example of error handling
        print("\n--- Testing Error Handling ---")
        print("Attempting to draw with an invalid symbol (should raise ValueError)...")
        try:
            art.draw_square(3, '@@')
        except ValueError as e:
            print(f"Successfully caught expected error: {e}")

        print("\nAttempting to draw with a negative dimension (should raise ValueError)...")
        try:
            art.draw_rectangle(-5, 5, '*')
        except ValueError as e:
            print(f"Successfully caught expected error: {e}")
            
        print("\nAttempting to draw with a non-integer dimension (should raise TypeError)...")
        try:
            art.draw_pyramid(4.5, '*') # type: ignore
        except TypeError as e:
            print(f"Successfully caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

