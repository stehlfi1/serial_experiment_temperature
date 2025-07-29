
"""
ASCII Art Generator

A console-based 2D ASCII art application that generates various geometric shapes
using user-specified symbols. This module implements the ISO/IEC 25010 standard
for software quality characteristics.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Union


class AsciiArtError(Exception):
    """Base exception class for ASCII Art related errors."""
    pass


class InvalidSymbolError(AsciiArtError):
    """Raised when an invalid symbol is provided."""
    pass


class InvalidDimensionError(AsciiArtError):
    """Raised when invalid dimensions are provided."""
    pass


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various geometric shapes using
    ASCII characters. All shapes are filled with the specified symbol.
    
    Attributes:
        None
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
            InvalidSymbolError: If symbol is invalid
        """
        if not isinstance(symbol, str):
            raise InvalidSymbolError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise InvalidSymbolError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise InvalidSymbolError("Symbol cannot be a whitespace character")
        
        if not symbol.isprintable():
            raise InvalidSymbolError("Symbol must be a printable character")
    
    def _validate_dimensions(self, **dimensions: int) -> None:
        """
        Validate dimension parameters.
        
        Args:
            **dimensions: Keyword arguments containing dimension values
            
        Raises:
            InvalidDimensionError: If any dimension is invalid
        """
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise InvalidDimensionError(f"{name} must be an integer")
            
            if value <= 0:
                raise InvalidDimensionError(f"{name} must be positive (got {value})")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            InvalidDimensionError: If width is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
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
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            InvalidDimensionError: If width or height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the 
        top-left corner. Each row is shifted by one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            InvalidDimensionError: If width or height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
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
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the 
        top-left corner with one symbol and increasing by one symbol per row.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            InvalidDimensionError: If width or height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
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
        for row in range(1, height + 1):
            # Ensure we don't exceed the specified width
            symbols_count = min(row, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row has an odd number of symbols (1, 3, 5, 7, ...).
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            InvalidDimensionError: If height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
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
        max_width = 2 * height - 1
        
        for row in range(height):
            symbols_count = 2 * row + 1
            spaces_count = (max_width - symbols_count) // 2
            
            line = ' ' * spaces_count + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Main function to demonstrate the ASCII Art functionality.
    
    This function provides a simple console interface for users to interact
    with the ASCII Art generator.
    """
    art_generator = AsciiArt()
    
    print("ASCII Art Generator")
    print("=" * 50)
    
    try:
        # Demonstrate each shape
        print("\n1. Square (5x5) with '*':")
        print(art_generator.draw_square(5, '*'))
        
        print("\n2. Rectangle (6x3) with '#':")
        print(art_generator.draw_rectangle(6, 3, '#'))
        
        print("\n3. Parallelogram (4x4) with '+':")
        print(art_generator.draw_parallelogram(4, 4, '+'))
        
        print("\n4. Triangle (5x5) with 'o':")
        print(art_generator.draw_triangle(5, 5, 'o'))
        
        print("\n5. Pyramid (height=5) with '^':")
        print(art_generator.draw_pyramid(5, '^'))
        
    except (InvalidSymbolError, InvalidDimensionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


# Unit tests for the AsciiArt class
def test_ascii_art():
    """
    Comprehensive test suite for the AsciiArt class.
    
    This function tests all methods with various inputs including edge cases
    and error conditions to ensure robustness and correctness.
    """
    art = AsciiArt()
    
    # Test valid inputs
    assert art.draw_square(2, '*') == "**\n**"
    assert art.draw_rectangle(3, 2, '#') == "###\n###"
    assert art.draw_parallelogram(2, 2, '+') == "++\n ++"
    assert art.draw_triangle(3, 3, 'o') == "o\noo\nooo"
    assert art.draw_pyramid(3, '^') == "  ^\n ^^^\n^^^^^"
    
    # Test error conditions
    try:
        art.draw_square(-1, '*')
        assert False, "Should raise InvalidDimensionError"
    except InvalidDimensionError:
        pass
    
    try:
        art.draw_square(3, '  ')  # Multi-character
        assert False, "Should raise InvalidSymbolError"
    except InvalidSymbolError:
        pass
    
    try:
        art.draw_square(3, ' ')  # Whitespace
        assert False, "Should raise InvalidSymbolError"
    except InvalidSymbolError:
        pass
    
    print("All tests passed!")


# Uncomment the line below to run tests
# test_ascii_art()
