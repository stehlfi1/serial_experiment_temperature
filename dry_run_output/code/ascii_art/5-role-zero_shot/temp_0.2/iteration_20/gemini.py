
"""
ascii_art_generator.py

A module for generating 2D ASCII art shapes. This module provides the AsciiArt
class with static methods for creating various geometric shapes as multi-line
strings.

This code is designed with the ISO/IEC 25010 standard in mind, focusing on:
- Functional Suitability: Correctly implements all required drawing functions.
- Performance Efficiency: Uses efficient string building techniques.
- Reliability (Fault Tolerance): Includes robust validation for all inputs.
- Maintainability (Modularity, Reusability, Readability): Organized as a
  class with clear, documented, and reusable components.
- Testability: Functions are pure, returning strings, which are easy to verify.
"""

from typing import Dict, Any

class AsciiArt:
    """
    A utility class for generating 2D ASCII art shapes.

    This class provides a collection of static methods to draw various geometric
    shapes using a specified character. It acts as a namespace for the drawing
    functionality, ensuring logical grouping. All methods are stateless and
    do not require an instance of the class to be created.
    """

    @staticmethod
    def _validate_inputs(symbol: str, **kwargs: Any) -> None:
        """
        Private helper to validate common inputs for drawing methods.

        This method centralizes input validation to ensure consistency and
        reduce code duplication (Modularity, Reusability).

        Args:
            symbol (str): The character to use for drawing.
            **kwargs: Keyword arguments representing dimensions (e.g., width, height).

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if any dimension is not a positive integer.
        """
        # Safety: Validate symbol type, length, and content
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        # Safety: Validate dimension types and values
        for name, value in kwargs.items():
            if not isinstance(value, int):
                raise TypeError(f"Dimension '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"Dimension '{name}' must be a positive integer.")

    @staticmethod
    def draw_square(width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square. Must be a positive integer.
            symbol (str): The single, non-whitespace character to draw the square with.

        Returns:
            str: A multi-line string representing the ASCII square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        # Correctness is ensured by reusing the validated rectangle logic.
        # This also demonstrates reusability.
        AsciiArt._validate_inputs(symbol, width=width)
        return AsciiArt.draw_rectangle(width, width, symbol)

    @staticmethod
    def draw_rectangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle. Must be a positive integer.
            height (int): The height of the rectangle. Must be a positive integer.
            symbol (str): The single, non-whitespace character to draw the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)
        
        # Performance: Building a list and joining is more efficient than
        # repeated string concatenation in a loop.
        row = symbol * width
        art_lines = [row] * height
        return "\n".join(art_lines)

    @staticmethod
    def draw_parallelogram(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right relative to the one above it.

        Args:
            width (int): The width of the parallelogram's parallel sides. Must be a positive integer.
            height (int): The height of the parallelogram. Must be a positive integer.
            symbol (str): The single, non-whitespace character to draw with.

        Returns:
            str: A multi-line string representing the ASCII parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)
        
        art_lines = []
        # Readability: Clear variable names like 'i' for index are standard.
        for i in range(height):
            padding = ' ' * i
            row = symbol * width
            art_lines.append(f"{padding}{row}")
            
        return "\n".join(art_lines)

    @staticmethod
    def draw_triangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle starts with one symbol at the top-left and grows downwards.
        For this specific implementation, width and height must be equal to form
        a proper 45-degree right-angled triangle.

        Args:
            width (int): The width of the triangle's base. Must be a positive integer.
            height (int): The height of the triangle. Must be a positive integer.
            symbol (str): The single, non-whitespace character to draw with.

        Returns:
            str: A multi-line string representing the ASCII triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive, symbol is invalid,
                        or if width and height are not equal.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)
        
        # Correctness: Enforce constraint for a visually correct shape.
        if width != height:
            raise ValueError(
                "For this right-angled triangle, width and height must be equal."
            )
            
        # The loop starts from 1 to control the number of symbols directly.
        art_lines = [symbol * i for i in range(1, height + 1)]
        return "\n".join(art_lines)

    @staticmethod
    def draw_pyramid(height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        Args:
            height (int): The height of the pyramid. Must be a positive integer.
            symbol (str): The single, non-whitespace character to draw with.

        Returns:
            str: A multi-line string representing the ASCII pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        AsciiArt._validate_inputs(symbol, height=height)
        
        art_lines = []
        # The total width of the pyramid's base is 2 * height - 1.
        # This is used to calculate the necessary padding for each row.
        for i in range(height):
            # Readability: Logic for padding and symbol count is explicit.
            symbol_count = 2 * i + 1
            padding_size = height - 1 - i
            
            padding = ' ' * padding_size
            symbols = symbol * symbol_count
            art_lines.append(f"{padding}{symbols}")
            
        return "\n".join(art_lines)


if __name__ == '__main__':
    """
    Example usage of the AsciiArt class when the script is run directly.
    This demonstrates the functionality and serves as a quick visual test.
    """
    print("--- AsciiArt Demo ---")

    try:
        print("\nSquare (5x5, '#'):")
        print(AsciiArt.draw_square(5, '#'))

        print("\nRectangle (8x4, '*'):")
        print(AsciiArt.draw_rectangle(8, 4, '*'))

        print("\nParallelogram (10x5, '+'):")
        print(AsciiArt.draw_parallelogram(10, 5, '+'))

        print("\nTriangle (6x6, '^'):")
        print(AsciiArt.draw_triangle(6, 6, '^'))

        print("\nPyramid (height 7, '@'):")
        print(AsciiArt.draw_pyramid(7, '@'))

        print("\n--- Error Handling Demo ---")
        print("Attempting to draw a square with negative width...")
        try:
            AsciiArt.draw_square(-3, 'X')
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\nAttempting to draw with a multi-character symbol...")
        try:
            AsciiArt.draw_rectangle(5, 5, '@@')
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("\nAttempting to draw a triangle with unequal width and height...")
        try:
            AsciiArt.draw_triangle(5, 7, 'T')
        except ValueError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during the demo: {e}")

