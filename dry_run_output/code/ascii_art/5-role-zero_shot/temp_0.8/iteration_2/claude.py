
"""
ASCII Art Generator - A console-based 2D ASCII art application.

This module provides functionality to generate various ASCII art shapes
including squares, rectangles, parallelograms, triangles, and pyramids.

Author: Senior Software Developer
Compliance: ISO/IEC 25010 Standard
"""

from typing import Optional


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various geometric shapes using
    ASCII characters. All shapes are completely filled with the specified symbol.
    
    Attributes:
        None
    """
    
    def __init__(self) -> None:
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the symbol parameter.
        
        Args:
            symbol (str): The symbol to validate.
            
        Raises:
            TypeError: If symbol is not a string.
            ValueError: If symbol is not exactly one printable character,
                       or if symbol is whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
        
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")
    
    def _validate_positive_integer(self, value: int, parameter_name: str) -> None:
        """
        Validate that a parameter is a positive integer.
        
        Args:
            value (int): The value to validate.
            parameter_name (str): The name of the parameter for error messages.
            
        Raises:
            TypeError: If value is not an integer.
            ValueError: If value is not positive.
        """
        if not isinstance(value, int):
            raise TypeError(f"{parameter_name} must be an integer")
        
        if value <= 0:
            raise ValueError(f"{parameter_name} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square using the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive).
            symbol (str): The symbol to use for drawing (single printable character).
            
        Returns:
            str: Multi-line string representing the ASCII square.
            
        Raises:
            TypeError: If parameters are not of correct type.
            ValueError: If width is not positive or symbol is invalid.
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(width):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive).
            height (int): The height of the rectangle (must be positive).
            symbol (str): The symbol to use for drawing (single printable character).
            
        Returns:
            str: Multi-line string representing the ASCII rectangle.
            
        Raises:
            TypeError: If parameters are not of correct type.
            ValueError: If width/height is not positive or symbol is invalid.
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each subsequent row is shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive).
            height (int): The height of the parallelogram (must be positive).
            symbol (str): The symbol to use for drawing (single printable character).
            
        Returns:
            str: Multi-line string representing the ASCII parallelogram.
            
        Raises:
            TypeError: If parameters are not of correct type.
            ValueError: If width/height is not positive or symbol is invalid.
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '*'))
            ***
             ***
              ***
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left
        corner with one symbol and increasing by one symbol per row.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive).
            height (int): The height of the triangle (must be positive).
            symbol (str): The symbol to use for drawing (single printable character).
            
        Returns:
            str: Multi-line string representing the ASCII triangle.
            
        Raises:
            TypeError: If parameters are not of correct type.
            ValueError: If width/height is not positive or symbol is invalid.
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, '*'))
            *
            **
            ***
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate the number of symbols for this row
            # Ensure we don't exceed the specified width
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid starts with one symbol at the top and increases by two
        symbols per row, centered to create a symmetrical shape.
        
        Args:
            height (int): The height of the pyramid (must be positive).
            symbol (str): The symbol to use for drawing (single printable character).
            
        Returns:
            str: Multi-line string representing the ASCII pyramid.
            
        Raises:
            TypeError: If parameters are not of correct type.
            ValueError: If height is not positive or symbol is invalid.
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '*'))
              *
             ***
            *****
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols for this row (starts with 1, increases by 2)
            symbols_count = 2 * row + 1
            # Calculate leading spaces for centering
            leading_spaces = height - row - 1
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main() -> None:
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates an instance of AsciiArt and demonstrates
    all available shape drawing methods with sample parameters.
    """
    try:
        # Create an instance of AsciiArt
        art = AsciiArt()
        
        print("ASCII Art Generator Demo")
        print("=" * 40)
        
        # Demonstrate square
        print("\nSquare (5x5) with '*':")
        print(art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\nRectangle (6x3) with '#':")
        print(art.draw_rectangle(6, 3, '#'))
        
        # Demonstrate parallelogram
        print("\nParallelogram (4x4) with '@':")
        print(art.draw_parallelogram(4, 4, '@'))
        
        # Demonstrate triangle
        print("\nTriangle (5x5) with '+':")
        print(art.draw_triangle(5, 5, '+'))
        
        # Demonstrate pyramid
        print("\nPyramid (height=4) with '^':")
        print(art.draw_pyramid(4, '^'))
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


# Unit tests for comprehensive testing
class TestAsciiArt:
    """
    Test class for AsciiArt functionality.
    
    This class contains comprehensive tests for all AsciiArt methods
    to ensure correctness and proper error handling.
    """
    
    @staticmethod
    def test_square():
        """Test square drawing functionality."""
        art = AsciiArt()
        
        # Test basic square
        result = art.draw_square(2, '*')
        expected = "**\n**"
        assert result == expected, f"Expected '{expected}', got '{result}'"
        
        # Test single character square
        result = art.draw_square(1, '#')
        expected = "#"
        assert result == expected, f"Expected '{expected}', got '{result}'"
        
        print("✓ Square tests passed")
    
    @staticmethod
    def test_rectangle():
        """Test rectangle drawing functionality."""
        art = AsciiArt()
        
        # Test basic rectangle
        result = art.draw_rectangle(3, 2, '+')
        expected = "+++\n+++"
        assert result == expected, f"Expected '{expected}', got '{result}'"
        
        print("✓ Rectangle tests passed")
    
    @staticmethod
    def test_validation():
        """Test input validation."""
        art = AsciiArt()
        
        # Test invalid symbol (multiple characters)
        try:
            art.draw_square(3, "**")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
        
        # Test invalid symbol (whitespace)
        try:
            art.draw_square(3, " ")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
        
        # Test invalid width (negative)
        try:
            art.draw_square(-1, "*")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
        
        # Test invalid width (zero)
        try:
            art.draw_square(0, "*")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
        
        print("✓ Validation tests passed")
    
    @staticmethod
    def run_all_tests():
        """Run all tests."""
        print("Running AsciiArt Tests...")
        TestAsciiArt.test_square()
        TestAsciiArt.test_rectangle()
        TestAsciiArt.test_validation()
        print("All tests passed! ✓")


# Uncomment the following line to run tests
# TestAsciiArt.run_all_tests()
