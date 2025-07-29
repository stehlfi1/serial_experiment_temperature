
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes using ASCII characters.

Author: Senior Software Developer
Standard: ISO/IEC 25010 compliant
"""

import re
from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art representations of geometric shapes.
    
    This class provides methods to draw various shapes including squares,
    rectangles, parallelograms, triangles, and pyramids using ASCII characters.
    All methods include comprehensive input validation and return formatted
    multi-line strings.
    """
    
    # Class constants for validation
    MIN_DIMENSION = 1
    MAX_DIMENSION = 100  # Reasonable limit for console output
    
    def __init__(self) -> None:
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate that the symbol is a single printable character.
        
        Args:
            symbol (str): The character to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one character or is whitespace
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
        
        # Check if symbol is printable (excluding whitespace)
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a printable non-whitespace character")
    
    def _validate_dimension(self, dimension: int, dimension_name: str) -> None:
        """
        Validate that a dimension is a positive integer within reasonable bounds.
        
        Args:
            dimension (int): The dimension value to validate
            dimension_name (str): Name of the dimension for error messages
            
        Raises:
            TypeError: If dimension is not an integer
            ValueError: If dimension is not positive or exceeds maximum
        """
        if not isinstance(dimension, int):
            raise TypeError(f"{dimension_name} must be an integer")
        
        if dimension < self.MIN_DIMENSION:
            raise ValueError(f"{dimension_name} must be at least {self.MIN_DIMENSION}")
        
        if dimension > self.MAX_DIMENSION:
            raise ValueError(f"{dimension_name} cannot exceed {self.MAX_DIMENSION}")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square using the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If width is not an integer or symbol is not a string
            ValueError: If width is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)
        
        # Generate square: each row is the same
        rows = [symbol * width for _ in range(width)]
        return '\n'.join(rows)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        # Generate rectangle: each row has the same width
        rows = [symbol * width for _ in range(height)]
        return '\n'.join(rows)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner, with each subsequent
        row shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        # Generate parallelogram: each row is shifted by its row index
        rows = []
        for row_index in range(height):
            spaces = ' ' * row_index
            row_content = symbol * width
            rows.append(spaces + row_content)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol,
        and each row adds one more symbol.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, 'o'))
            o
            oo
            ooo
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        # Generate triangle: each row has (row_index + 1) symbols
        rows = []
        for row_index in range(height):
            # Calculate symbols for this row, but don't exceed width
            symbols_count = min(row_index + 1, width)
            row_content = symbol * symbols_count
            rows.append(row_content)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid.
        
        The pyramid is centered, with the top having one symbol and each
        subsequent row having two more symbols than the previous row.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If height is not an integer or symbol is not a string
            ValueError: If height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        # Generate pyramid: each row has (2 * row_index + 1) symbols
        # and is centered based on the bottom row width
        rows = []
        max_width = 2 * height - 1  # Width of the bottom row
        
        for row_index in range(height):
            symbols_count = 2 * row_index + 1
            spaces_count = (max_width - symbols_count) // 2
            
            spaces = ' ' * spaces_count
            row_content = symbol * symbols_count
            rows.append(spaces + row_content)
        
        return '\n'.join(rows)


def main() -> None:
    """
    Main function to demonstrate the AsciiArt class functionality.
    
    This function provides a simple console interface for testing
    the various shape drawing methods.
    """
    try:
        art = AsciiArt()
        
        print("ASCII Art Generator Demo")
        print("=" * 25)
        
        # Demonstrate each shape
        print("\n1. Square (5x5, '*'):")
        print(art.draw_square(5, '*'))
        
        print("\n2. Rectangle (6x3, '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        
        print("\n3. Parallelogram (4x4, '+'):")
        print(art.draw_parallelogram(4, 4, '+'))
        
        print("\n4. Triangle (5x5, 'o'):")
        print(art.draw_triangle(5, 5, 'o'))
        
        print("\n5. Pyramid (height=4, '^'):")
        print(art.draw_pyramid(4, '^'))
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


# Unit tests for comprehensive testing
def test_ascii_art() -> None:
    """
    Comprehensive test suite for the AsciiArt class.
    
    Tests all methods with various inputs including edge cases
    and error conditions to ensure robustness.
    """
    art = AsciiArt()
    
    # Test valid inputs
    assert art.draw_square(1, 'X') == 'X'
    assert art.draw_square(2, '*') == '**\n**'
    
    assert art.draw_rectangle(3, 2, '#') == '###\n###'
    assert art.draw_rectangle(1, 1, 'o') == 'o'
    
    assert art.draw_parallelogram(2, 2, '+') == '++\n ++'
    assert art.draw_triangle(3, 3, 'A') == 'A\nAA\nAAA'
    assert art.draw_pyramid(2, '^') == ' ^\n^^^'
    
    # Test error conditions
    try:
        art.draw_square(-1, '*')
        assert False, "Should raise ValueError for negative width"
    except ValueError:
        pass
    
    try:
        art.draw_rectangle(5, 3, '  ')
        assert False, "Should raise ValueError for multi-character symbol"
    except ValueError:
        pass
    
    try:
        art.draw_triangle(3, 2, ' ')
        assert False, "Should raise ValueError for whitespace symbol"
    except ValueError:
        pass
    
    try:
        art.draw_pyramid('invalid', '*')
        assert False, "Should raise TypeError for non-integer height"
    except TypeError:
        pass
    
    print("All tests passed!")


# Uncomment the line below to run tests
# test_ascii_art()
