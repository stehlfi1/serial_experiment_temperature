
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class with static methods to draw various
geometric shapes. It is designed with a focus on code quality, adhering to
the principles of the ISO/IEC 25010 standard, including:
- Functional Suitability: Correctly generates the specified shapes.
- Performance Efficiency: Uses efficient string-building techniques.
- Reliability & Safety: Implements robust input validation.
- Maintainability & Modularity: Organized into a class with reusable helpers.
- Testability: Methods are pure functions whose output can be easily asserted.
- Readability: Documented with docstrings, type hints, and clear variable names.
"""

import math
from typing import Dict, Any

class AsciiArt:
    """
    A utility class for generating 2D ASCII art shapes.

    This class provides a collection of static methods to draw various
    geometric shapes using a specified character symbol. It acts as a namespace
    for the drawing functions, ensuring logical grouping and modularity.
    """

    @staticmethod
    def _validate_inputs(symbol: str, **dimensions: Dict[str, Any]) -> None:
        """
        Private helper to validate common inputs for drawing methods.

        This method ensures that the provided symbol and dimensions meet the
        required criteria for drawing, promoting safety and fault tolerance.

        Args:
            symbol (str): The character symbol to be used for drawing.
            **dimensions: A dictionary of dimension names (e.g., 'width')
                          and their integer values.

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if any dimension is not a positive integer.
            TypeError: If a dimension value is not an integer.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")

        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"The '{name}' must be a positive integer.")

    @staticmethod
    def draw_square(width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width (int): The width and height of the square. Must be a
                         positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        """
        # A square is a rectangle with equal width and height.
        # This reuses the logic of draw_rectangle for better maintainability.
        return AsciiArt.draw_rectangle(width, width, symbol)

    @staticmethod
    def draw_rectangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width (int): The width of the rectangle. Must be a positive integer.
            height (int): The height of the rectangle. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)
        
        row = symbol * width
        rows = [row] * height
        
        return "\n".join(rows)

    @staticmethod
    def draw_parallelogram(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram leaning to the right.

        Each subsequent row is shifted one space to the right relative to
        the row above it.

        Args:
            width (int): The width of the parallelogram's top/bottom sides.
                         Must be a positive integer.
            height (int): The height of the parallelogram. Must be a positive
                          integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)

        rows = [
            ' ' * i + symbol * width
            for i in range(height)
        ]
        
        return "\n".join(rows)

    @staticmethod
    def draw_triangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left, stretching to fill the
        specified width and height. The number of symbols in each row is
        scaled proportionally.

        Args:
            width (int): The final width of the triangle's base.
                         Must be a positive integer.
            height (int): The height of the triangle. Must be a positive
                          integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the right-angled triangle.
        """
        AsciiArt._validate_inputs(symbol, width=width, height=height)
        
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row proportionally.
            # Using ceiling ensures the final row has the full width.
            num_symbols = math.ceil((i + 1) * width / height)
            rows.append(symbol * num_symbols)
            
        return "\n".join(rows)

    @staticmethod
    def draw_pyramid(height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid. Must be a positive
                          integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        AsciiArt._validate_inputs(symbol, height=height)
        
        # The total width of the pyramid's base is (2 * height - 1)
        total_width = 2 * height - 1
        
        rows = []
        for i in range(height):
            # The number of symbols in each row follows the pattern 1, 3, 5, ...
            num_symbols = 2 * i + 1
            # The padding is calculated to center the symbols
            padding = (total_width - num_symbols) // 2
            rows.append(' ' * padding + symbol * num_symbols)
            
        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class and allows
    # for easy visual testing of the generated shapes.
    
    print("--- ASCII Art Shape Generator ---")
    
    try:
        print("\nSquare (5x5, #):")
        print(AsciiArt.draw_square(width=5, symbol='#'))

        print("\nRectangle (8x4, *):")
        print(AsciiArt.draw_rectangle(width=8, height=4, symbol='*'))

        print("\nParallelogram (10x5, @):")
        print(AsciiArt.draw_parallelogram(width=10, height=5, symbol='@'))

        print("\nRight-Angled Triangle (Stretched, width=10, height=5, +):")
        print(AsciiArt.draw_triangle(width=10, height=5, symbol='+'))
        
        print("\nRight-Angled Triangle (Classic, width=6, height=6, T):")
        print(AsciiArt.draw_triangle(width=6, height=6, symbol='T'))

        print("\nPyramid (height=6, ^):")
        print(AsciiArt.draw_pyramid(height=6, symbol='^'))
        
        print("\n--- Testing Invalid Inputs ---")
        try:
            print("Testing negative width...")
            AsciiArt.draw_square(-3, 'X')
        except ValueError as e:
            print(f"Successfully caught error: {e}")

        try:
            print("Testing multi-character symbol...")
            AsciiArt.draw_rectangle(5, 5, 'XX')
        except ValueError as e:
            print(f"Successfully caught error: {e}")
            
        try:
            print("Testing whitespace symbol...")
            AsciiArt.draw_pyramid(5, ' ')
        except ValueError as e:
            print(f"Successfully caught error: {e}")
            
        try:
            print("Testing non-integer height...")
            AsciiArt.draw_parallelogram(5, 'a', '$')
        except TypeError as e:
            print(f"Successfully caught error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

