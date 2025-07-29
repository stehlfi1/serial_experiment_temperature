
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains methods for drawing
various geometric shapes using ASCII characters. The implementation prioritizes
code quality, maintainability, and adherence to software engineering best
practices as outlined by ISO/IEC 25010.

Key Quality Characteristics Addressed (ISO/IEC 25010):
- Functional Suitability: Correctly generates specified ASCII shapes.
- Performance Efficiency: Uses efficient string building techniques.
- Reliability: Robust input validation prevents crashes from invalid data.
- Usability: Clear API and documentation make the class easy to use.
- Maintainability: Code is modular, readable, and well-documented,
  making it easy to test, modify, and extend.
- Security: Input validation protects against trivial vulnerabilities.
"""

import math

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a collection of static methods to draw geometric
    shapes like squares, rectangles, and pyramids. It enforces strict input
    validation to ensure functional correctness and reliability.
    """

    @staticmethod
    def _validate_inputs(symbol: str, **dimensions: int) -> None:
        """
        Validates the common inputs for drawing functions.

        This private helper method ensures that the symbol is a single,
        printable character and that all dimensional arguments (e.g., width,
        height) are positive integers.

        Args:
            symbol: The character to use for drawing.
            **dimensions: A keyword dictionary of dimension names and their
                          integer values (e.g., width=5, height=10).

        Raises:
            ValueError: If the symbol is not a single character, is whitespace,
                        or if any dimension is not a positive integer.
            TypeError: If any dimension is not an integer.
        """
        # --- Symbol Validation (Safety, Correctness) ---
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        # --- Dimensions Validation (Safety, Correctness) ---
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method leverages the draw_rectangle method for implementation,
        promoting code reusability.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the square.
        
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        # Reuses draw_rectangle for a DRY implementation (Maintainability)
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        
        # Efficiently creates each row string (Performance)
        row = symbol * width
        
        # Efficiently joins all rows with newlines (Performance)
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram leaning to the right.

        Each subsequent row is indented by one additional space.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the parallelogram.
            
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        
        lines = []
        for i in range(height):
            indent = " " * i
            content = symbol * width
            lines.append(f"{indent}{content}")
            
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner towards the bottom-right.
        The number of symbols per row is scaled based on the overall width
        and height to form the desired shape.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the triangle.
            
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        
        lines = []
        for i in range(height):
            # Calculate symbols for the current row to scale correctly
            # (i+1) is the current row number (1-indexed)
            # We use math.ceil to ensure the base has the correct width
            # and the shape fills properly.
            num_symbols = math.ceil((i + 1) * width / height)
            lines.append(symbol * num_symbols)
            
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the pyramid.
            
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, height=height)
        
        lines = []
        # The full width of the pyramid's base
        base_width = 2 * height - 1
        
        for i in range(height):
            # Calculate symbols and padding for the current level
            num_symbols = 2 * i + 1
            padding = (base_width - num_symbols) // 2
            
            # Construct the line with clear variable names (Readability)
            indent = " " * padding
            content = symbol * num_symbols
            lines.append(f"{indent}{content}")
            
        return "\n".join(lines)


if __name__ == "__main__":
    # --- Demonstration of the AsciiArt class ---
    # This block serves as a basic usage example and informal test harness.
    # (Testability)
    
    artist = AsciiArt()
    
    print("--- ASCII Art Shape Generator ---")
    
    try:
        print("\nSquare (5x5, #):")
        print(artist.draw_square(width=5, symbol="#"))
        
        print("\nRectangle (8x4, @):")
        print(artist.draw_rectangle(width=8, height=4, symbol="@"))
        
        print("\nParallelogram (10x5, =):")
        print(artist.draw_parallelogram(width=10, height=5, symbol="="))
        
        print("\nRight-Angled Triangle (width=10, height=5, *):")
        print(artist.draw_triangle(width=10, height=5, symbol="*"))

        print("\nRight-Angled Triangle (width=7, height=7, T):")
        print(artist.draw_triangle(width=7, height=7, symbol="T"))
        
        print("\nPyramid (height=6, ^):")
        print(artist.draw_pyramid(height=6, symbol="^"))

        # --- Example of Input Validation ---
        print("\n--- Testing Error Handling ---")
        try:
            artist.draw_square(width=-3, symbol="X")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        try:
            artist.draw_rectangle(width=5, height=5, symbol="?!")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            artist.draw_pyramid(height=5, symbol=" ")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

