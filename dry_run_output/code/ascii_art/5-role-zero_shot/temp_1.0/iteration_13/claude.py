
"""
ASCII Art Generator

A console-based 2D ASCII art application that generates various geometric shapes
using user-specified symbols. Implements ISO/IEC 25010 quality standards for
maintainability, reliability, and performance.

Author: Senior Software Developer
Version: 1.0
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes with specified symbols.
    
    This class provides methods to draw various geometric shapes including
    squares, rectangles, parallelograms, triangles, and pyramids using
    ASCII characters.
    
    All methods validate inputs and return multi-line strings representing
    the requested ASCII art shapes.
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the provided symbol is a single printable character.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one character or is whitespace
        """
        if not isinstance(symbol, str):
            raise TypeError(f"Symbol must be a string, got {type(symbol).__name__}")
        
        if len(symbol) != 1:
            raise ValueError(f"Symbol must be exactly one character, got {len(symbol)} characters")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
    
    @staticmethod
    def _validate_dimensions(width: int = None, height: int = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int, optional): Width to validate
            height (int, optional): Height to validate
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is negative or zero
        """
        for dimension, name in [(width, 'width'), (height, 'height')]:
            if dimension is not None:
                if not isinstance(dimension, int):
                    raise TypeError(f"{name.capitalize()} must be an integer, got {type(dimension).__name__}")
                if dimension <= 0:
                    raise ValueError(f"{name.capitalize()} must be positive, got {dimension}")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square with the specified width and symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters are not of the correct type
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
        
        return '\n'.join([symbol * width for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle with the specified dimensions and symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If parameters are not of the correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        return '\n'.join([symbol * width for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner, with each subsequent
        row shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters are not of the correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with a single symbol,
        expanding by one symbol per row until reaching the specified width.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters are not of the correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, '&'))
            &
            &&
            &&&
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols per row, ensuring we don't exceed the width
            symbols_in_row = min(row + 1, width)
            line = symbol * symbols_in_row
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid centered on each row.
        
        The pyramid starts with a single symbol at the top and expands
        symmetrically, adding two symbols per row (one on each side).
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters are not of the correct type
            ValueError: If height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)
        
        lines = []
        max_width = 2 * height - 1
        
        for row in range(height):
            symbols_in_row = 2 * row + 1
            spaces_before = (max_width - symbols_in_row) // 2
            line = ' ' * spaces_before + symbol * symbols_in_row
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function provides examples of all available shapes with different
    symbols and dimensions.
    """
    art = AsciiArt()
    
    print("=== ASCII Art Generator Demo ===\n")
    
    try:
        # Demonstrate square
        print("Square (5x5 with '*'):")
        print(art.draw_square(5, '*'))
        print()
        
        # Demonstrate rectangle
        print("Rectangle (6x3 with '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        print()
        
        # Demonstrate parallelogram
        print("Parallelogram (4x4 with '+'):")
        print(art.draw_parallelogram(4, 4, '+'))
        print()
        
        # Demonstrate triangle
        print("Triangle (5x5 with '&'):")
        print(art.draw_triangle(5, 5, '&'))
        print()
        
        # Demonstrate pyramid
        print("Pyramid (height 4 with '^'):")
        print(art.draw_pyramid(4, '^'))
        print()
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


# Unit tests for comprehensive testing
class TestAsciiArt:
    """
    Test suite for AsciiArt class ensuring correctness and robustness.
    
    This class contains comprehensive tests for all methods including
    edge cases and error conditions.
    """
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.art = AsciiArt()
    
    def test_draw_square_valid_input(self):
        """Test draw_square with valid inputs."""
        result = self.art.draw_square(3, '*')
        expected = "***\n***\n***"
        assert result == expected
        
        # Test single character square
        result = self.art.draw_square(1, 'X')
        expected = "X"
        assert result == expected
    
    def test_draw_square_invalid_input(self):
        """Test draw_square with invalid inputs."""
        # Test invalid width
        try:
            self.art.draw_square(0, '*')
            assert False, "Should raise ValueError"
        except ValueError:
            pass
        
        try:
            self.art.draw_square(-1, '*')
            assert False, "Should raise ValueError"
        except ValueError:
            pass
        
        # Test invalid symbol
        try:
            self.art.draw_square(3, '')
            assert False, "Should raise ValueError"
        except ValueError:
            pass
        
        try:
            self.art.draw_square(3, 'ab')
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    def test_draw_rectangle_valid_input(self):
        """Test draw_rectangle with valid inputs."""
        result = self.art.draw_rectangle(4, 2, '#')
        expected = "####\n####"
        assert result == expected
    
    def test_draw_parallelogram_valid_input(self):
        """Test draw_parallelogram with valid inputs."""
        result = self.art.draw_parallelogram(3, 2, '+')
        expected = "+++\n +++"
        assert result == expected
    
    def test_draw_triangle_valid_input(self):
        """Test draw_triangle with valid inputs."""
        result = self.art.draw_triangle(3, 3, '&')
        expected = "&\n&&\n&&&"
        assert result == expected
        
        # Test triangle where height > width
        result = self.art.draw_triangle(2, 4, 'O')
        expected = "O\nOO\nOO\nOO"
        assert result == expected
    
    def test_draw_pyramid_valid_input(self):
        """Test draw_pyramid with valid inputs."""
        result = self.art.draw_pyramid(3, '^')
        expected = "  ^\n ^^^\n^^^^^"
        assert result == expected
    
    def test_symbol_validation(self):
        """Test symbol validation across all methods."""
        methods_to_test = [
            (self.art.draw_square, [3]),
            (self.art.draw_rectangle, [3, 3]),
            (self.art.draw_parallelogram, [3, 3]),
            (self.art.draw_triangle, [3, 3]),
            (self.art.draw_pyramid, [3])
        ]
        
        invalid_symbols = ['', 'ab', ' ', '\t', '\n']
        
        for method, args in methods_to_test:
            for invalid_symbol in invalid_symbols:
                try:
                    method(*(args + [invalid_symbol]))
                    assert False, f"Should raise ValueError for symbol '{invalid_symbol}'"
                except ValueError:
                    pass


# Performance test helper
def performance_test():
    """
    Simple performance test to ensure algorithms scale reasonably.
    
    This function tests the performance of drawing large shapes to ensure
    the algorithms remain efficient for reasonable input sizes.
    """
    import time
    
    art = AsciiArt()
    
    # Test large shapes
    start_time = time.time()
    
    # Large square
    result = art.draw_square(100, '*')
    assert len(result.split('\n')) == 100
    
    # Large pyramid
    result = art.draw_pyramid(100, '^')
    assert len(result.split('\n')) == 100
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Performance test completed in {execution_time:.4f} seconds")
    assert execution_time < 1.0, "Performance test should complete quickly"


if __name__ == "__main__":
    # Run main demonstration
    main()
    
    # Run basic tests
    test = TestAsciiArt()
    test.setup_method()
    test.test_draw_square_valid_input()
    test.test_draw_rectangle_valid_input()
    test.test_draw_parallelogram_valid_input()
    test.test_draw_triangle_valid_input()
    test.test_draw_pyramid_valid_input()
    
    print("\n=== All tests passed! ===")
    
    # Run performance test
    print("\n=== Running performance test ===")
    performance_test()
    print("Performance test passed!")
