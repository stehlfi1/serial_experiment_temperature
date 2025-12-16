
"""
ASCII Art Generator - A console-based 2D ASCII art application.

This module provides functionality to generate various ASCII shapes including
squares, rectangles, parallelograms, triangles, and pyramids.

Author: Senior Software Developer
Standard: ISO/IEC 25010 compliant
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various geometric shapes using ASCII
    characters. All shapes are filled with the specified symbol and returned
    as multi-line strings.
    
    Attributes:
        None
        
    Methods:
        draw_square: Creates a filled square
        draw_rectangle: Creates a filled rectangle
        draw_parallelogram: Creates a filled parallelogram
        draw_triangle: Creates a filled right-angled triangle
        draw_pyramid: Creates a filled symmetrical pyramid
    """
    
    def __init__(self):
        """Initialize the AsciiArt class."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the symbol parameter.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one printable character
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
        
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")
    
    def _validate_dimensions(self, width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int, optional): Width to validate
            height (int, optional): Height to validate
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is not positive
        """
        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer")
            if width <= 0:
                raise ValueError("Width must be positive")
        
        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer")
            if height <= 0:
                raise ValueError("Height must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square using the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representing the ASCII square
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(width))
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representing the ASCII rectangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the 
        top-left corner. Each subsequent row is shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representing the ASCII parallelogram
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(4, 3, '+'))
            ++++
             ++++
              ++++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            spaces = ' ' * row
            shape_line = symbol * width
            lines.append(spaces + shape_line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left
        corner. Each row has an increasing number of symbols.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representing the ASCII triangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, 'o'))
            o
            oo
            ooo
            oooo
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols per row, ensuring we don't exceed width
            symbols_count = min(row + 1, width)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row has an odd number of symbols (1, 3, 5, 7, ...).
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representing the ASCII pyramid
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)
        
        lines = []
        max_width = 2 * height - 1  # Width of the base
        
        for row in range(height):
            symbols_count = 2 * row + 1  # Odd numbers: 1, 3, 5, 7, ...
            spaces_count = (max_width - symbols_count) // 2
            
            line = ' ' * spaces_count + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates instances of various ASCII shapes and displays them.
    It also demonstrates error handling for invalid inputs.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    try:
        # Demonstrate square
        print("\n1. Square (5x5 with '*'):")
        print(art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\n2. Rectangle (6x4 with '#'):")
        print(art.draw_rectangle(6, 4, '#'))
        
        # Demonstrate parallelogram
        print("\n3. Parallelogram (5x4 with '+'):")
        print(art.draw_parallelogram(5, 4, '+'))
        
        # Demonstrate triangle
        print("\n4. Triangle (6x5 with 'o'):")
        print(art.draw_triangle(6, 5, 'o'))
        
        # Demonstrate pyramid
        print("\n5. Pyramid (height=6 with '^'):")
        print(art.draw_pyramid(6, '^'))
        
        # Demonstrate error handling
        print("\n6. Error Handling Examples:")
        
        try:
            art.draw_square(-1, '*')
        except ValueError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_rectangle(5, 3, '  ')  # Multi-character symbol
        except ValueError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_triangle(4, 3, ' ')  # Whitespace symbol
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()


# Unit tests for comprehensive testing
import unittest


class TestAsciiArt(unittest.TestCase):
    """
    Unit tests for the AsciiArt class.
    
    These tests ensure correctness, validate error handling, and verify
    the expected output formats for all shape drawing methods.
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.art = AsciiArt()
    
    def test_draw_square_valid_input(self):
        """Test square drawing with valid inputs."""
        result = self.art.draw_square(3, '*')
        expected = "***\n***\n***"
        self.assertEqual(result, expected)
    
    def test_draw_rectangle_valid_input(self):
        """Test rectangle drawing with valid inputs."""
        result = self.art.draw_rectangle(4, 2, '#')
        expected = "####\n####"
        self.assertEqual(result, expected)
    
    def test_draw_parallelogram_valid_input(self):
        """Test parallelogram drawing with valid inputs."""
        result = self.art.draw_parallelogram(3, 3, '+')
        expected = "+++\n +++\n  +++"
        self.assertEqual(result, expected)
    
    def test_draw_triangle_valid_input(self):
        """Test triangle drawing with valid inputs."""
        result = self.art.draw_triangle(4, 4, 'o')
        expected = "o\noo\nooo\noooo"
        self.assertEqual(result, expected)
    
    def test_draw_pyramid_valid_input(self):
        """Test pyramid drawing with valid inputs."""
        result = self.art.draw_pyramid(3, '^')
        expected = "  ^\n ^^^\n^^^^^"
        self.assertEqual(result, expected)
    
    def test_invalid_symbol_multichar(self):
        """Test error handling for multi-character symbols."""
        with self.assertRaises(ValueError):
            self.art.draw_square(3, '**')
    
    def test_invalid_symbol_whitespace(self):
        """Test error handling for whitespace symbols."""
        with self.assertRaises(ValueError):
            self.art.draw_square(3, ' ')
    
    def test_invalid_symbol_empty(self):
        """Test error handling for empty symbols."""
        with self.assertRaises(ValueError):
            self.art.draw_square(3, '')
    
    def test_invalid_dimensions_negative(self):
        """Test error handling for negative dimensions."""
        with self.assertRaises(ValueError):
            self.art.draw_square(-1, '*')
    
    def test_invalid_dimensions_zero(self):
        """Test error handling for zero dimensions."""
        with self.assertRaises(ValueError):
            self.art.draw_rectangle(0, 5, '*')
    
    def test_invalid_type_symbol(self):
        """Test error handling for non-string symbols."""
        with self.assertRaises(TypeError):
            self.art.draw_square(3, 123)
    
    def test_invalid_type_dimensions(self):
        """Test error handling for non-integer dimensions."""
        with self.assertRaises(TypeError):
            self.art.draw_square(3.5, '*')


# Performance test for large shapes
def performance_test():
    """
    Basic performance test for large shapes.
    
    This function tests the performance of the ASCII art generation
    for reasonably large shapes to ensure efficiency.
    """
    import time
    
    art = AsciiArt()
    
    print("\nPerformance Test Results:")
    print("-" * 30)
    
    # Test large square
    start_time = time.time()
    result = art.draw_square(100, '*')
    end_time = time.time()
    print(f"Large square (100x100): {end_time - start_time:.4f} seconds")
    
    # Test large pyramid
    start_time = time.time()
    result = art.draw_pyramid(100, '^')
    end_time = time.time()
    print(f"Large pyramid (height=100): {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    # Run main demo
    main()
    
    # Run performance test
    performance_test()
    
    # Uncomment the following line to run unit tests
    # unittest.main(argv=[''], exit=False, verbosity=2)
