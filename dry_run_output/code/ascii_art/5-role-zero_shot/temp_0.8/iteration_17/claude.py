
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes using object-oriented design principles
and adheres to ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0
"""

from typing import Union


class AsciiArtError(Exception):
    """Custom exception class for ASCII Art related errors."""
    pass


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using ASCII characters.
    All shapes are completely filled with the specified symbol and returned as
    multi-line strings.
    """
    
    def __init__(self):
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the input symbol.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            AsciiArtError: If symbol is invalid
        """
        if not isinstance(symbol, str):
            raise AsciiArtError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise AsciiArtError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise AsciiArtError("Symbol cannot be whitespace")
        
        if not symbol.isprintable():
            raise AsciiArtError("Symbol must be printable")
    
    def _validate_dimensions(self, width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int, optional): Width to validate
            height (int, optional): Height to validate
            
        Raises:
            AsciiArtError: If dimensions are invalid
        """
        if width is not None:
            if not isinstance(width, int):
                raise AsciiArtError("Width must be an integer")
            if width <= 0:
                raise AsciiArtError("Width must be positive")
        
        if height is not None:
            if not isinstance(height, int):
                raise AsciiArtError("Height must be an integer")
            if height <= 0:
                raise AsciiArtError("Height must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            AsciiArtError: If input parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        # Generate square by creating width identical rows
        rows = []
        for _ in range(width):
            rows.append(symbol * width)
        
        return '\n'.join(rows)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            AsciiArtError: If input parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        # Generate rectangle by creating height rows of width symbols
        rows = []
        for _ in range(height):
            rows.append(symbol * width)
        
        return '\n'.join(rows)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner and each subsequent
        row is shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            AsciiArtError: If input parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(4, 3, '+'))
            ++++
             ++++
              ++++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        # Generate parallelogram with increasing indentation
        rows = []
        for row_index in range(height):
            spaces = ' ' * row_index
            symbols = symbol * width
            rows.append(spaces + symbols)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol and
        grows by one symbol per row until reaching the specified width.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            AsciiArtError: If input parameters are invalid
            
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
        
        # Generate triangle with increasing width per row
        rows = []
        for row_index in range(height):
            # Calculate symbols count for current row
            symbols_count = min(row_index + 1, width)
            rows.append(symbol * symbols_count)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid centered with the specified symbol.
        
        The pyramid starts with one symbol at the top and grows symmetrically
        with each row having two more symbols than the previous row.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            AsciiArtError: If input parameters are invalid
            
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
        
        # Generate pyramid with centered rows
        rows = []
        max_width = 2 * height - 1  # Width of the base
        
        for row_index in range(height):
            # Calculate symbols count for current row (1, 3, 5, 7, ...)
            symbols_count = 2 * row_index + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            row = ' ' * leading_spaces + symbol * symbols_count
            rows.append(row)
        
        return '\n'.join(rows)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    
    This function provides a simple console interface for testing
    the various shape drawing methods.
    """
    art = AsciiArt()
    
    try:
        print("ASCII Art Generator Demo")
        print("=" * 30)
        
        # Demonstrate square
        print("\nSquare (5x5, symbol '*'):")
        print(art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\nRectangle (6x4, symbol '#'):")
        print(art.draw_rectangle(6, 4, '#'))
        
        # Demonstrate parallelogram
        print("\nParallelogram (5x4, symbol '+'):")
        print(art.draw_parallelogram(5, 4, '+'))
        
        # Demonstrate triangle
        print("\nTriangle (6x6, symbol 'o'):")
        print(art.draw_triangle(6, 6, 'o'))
        
        # Demonstrate pyramid
        print("\nPyramid (height 5, symbol '^'):")
        print(art.draw_pyramid(5, '^'))
        
    except AsciiArtError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


# Unit tests for the AsciiArt class
def test_ascii_art():
    """
    Comprehensive test suite for the AsciiArt class.
    
    Tests all methods with valid inputs and validates error handling
    for invalid inputs.
    """
    import unittest
    
    class TestAsciiArt(unittest.TestCase):
        """Test cases for AsciiArt class."""
        
        def setUp(self):
            """Set up test fixtures before each test method."""
            self.art = AsciiArt()
        
        def test_draw_square_valid(self):
            """Test square drawing with valid inputs."""
            result = self.art.draw_square(3, '*')
            expected = "***\n***\n***"
            self.assertEqual(result, expected)
        
        def test_draw_rectangle_valid(self):
            """Test rectangle drawing with valid inputs."""
            result = self.art.draw_rectangle(4, 2, '#')
            expected = "####\n####"
            self.assertEqual(result, expected)
        
        def test_draw_parallelogram_valid(self):
            """Test parallelogram drawing with valid inputs."""
            result = self.art.draw_parallelogram(3, 3, '+')
            expected = "+++\n +++\n  +++"
            self.assertEqual(result, expected)
        
        def test_draw_triangle_valid(self):
            """Test triangle drawing with valid inputs."""
            result = self.art.draw_triangle(4, 4, 'o')
            expected = "o\noo\nooo\noooo"
            self.assertEqual(result, expected)
        
        def test_draw_pyramid_valid(self):
            """Test pyramid drawing with valid inputs."""
            result = self.art.draw_pyramid(3, '^')
            expected = "  ^\n ^^^\n^^^^^"
            self.assertEqual(result, expected)
        
        def test_invalid_symbol_multichar(self):
            """Test error handling for multi-character symbols."""
            with self.assertRaises(AsciiArtError):
                self.art.draw_square(3, '**')
        
        def test_invalid_symbol_whitespace(self):
            """Test error handling for whitespace symbols."""
            with self.assertRaises(AsciiArtError):
                self.art.draw_square(3, ' ')
        
        def test_invalid_dimensions_negative(self):
            """Test error handling for negative dimensions."""
            with self.assertRaises(AsciiArtError):
                self.art.draw_square(-1, '*')
        
        def test_invalid_dimensions_zero(self):
            """Test error handling for zero dimensions."""
            with self.assertRaises(AsciiArtError):
                self.art.draw_rectangle(0, 5, '*')
        
        def test_invalid_dimensions_non_integer(self):
            """Test error handling for non-integer dimensions."""
            with self.assertRaises(AsciiArtError):
                self.art.draw_square(3.5, '*')
    
    # Run tests if this module is executed directly
    if __name__ == "__main__":
        unittest.main()


# Performance testing and benchmarking
def benchmark_ascii_art():
    """
    Performance benchmark for AsciiArt methods.
    
    Measures execution time for various shape sizes to ensure
    efficient algorithm performance.
    """
    import time
    
    art = AsciiArt()
    
    print("Performance Benchmarks:")
    print("-" * 30)
    
    # Benchmark large shapes
    sizes = [10, 50, 100]
    
    for size in sizes:
        # Benchmark square
        start_time = time.perf_counter()
        art.draw_square(size, '*')
        end_time = time.perf_counter()
        print(f"Square {size}x{size}: {(end_time - start_time) * 1000:.2f}ms")
        
        # Benchmark pyramid
        start_time = time.perf_counter()
        art.draw_pyramid(size, '^')
        end_time = time.perf_counter()
        print(f"Pyramid height {size}: {(end_time - start_time) * 1000:.2f}ms")


if __name__ == "__main__":
    # Run main demo
    main()
    
    # Optionally run benchmarks
    print("\n" + "=" * 50)
    benchmark_ascii_art()
