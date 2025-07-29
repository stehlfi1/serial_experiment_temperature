
"""
ASCII Art Generator Module

This module provides functionality to generate various ASCII art shapes
including squares, rectangles, parallelograms, triangles, and pyramids.

Author: Senior Software Developer
Standard: ISO/IEC 25010 compliant
"""

from typing import Union


class AsciiArtError(Exception):
    """Base exception class for ASCII art related errors."""
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
        Validate the symbol parameter.
        
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
    
    def _validate_positive_integer(self, value: int, name: str) -> None:
        """
        Validate that a value is a positive integer.
        
        Args:
            value (int): The value to validate
            name (str): The name of the parameter for error messages
            
        Raises:
            InvalidDimensionError: If value is not a positive integer
        """
        if not isinstance(value, int):
            raise InvalidDimensionError(f"{name} must be an integer")
        
        if value <= 0:
            raise InvalidDimensionError(f"{name} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): The symbol to fill the square with (single printable character)
            
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
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(width):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): The symbol to fill the rectangle with (single printable character)
            
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
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right compared to the previous row.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): The symbol to fill the parallelogram with (single printable character)
            
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
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        Each row has one more symbol than the previous row.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): The symbol to fill the triangle with (single printable character)
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            InvalidDimensionError: If width or height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, 'o'))
            o
            oo
            ooo
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols per row, ensuring we don't exceed width
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row has two more symbols than the previous row.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): The symbol to fill the pyramid with (single printable character)
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            InvalidDimensionError: If height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_positive_integer(height, "height")
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
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates various shapes and displays them to demonstrate
    the functionality of the AsciiArt class.
    """
    try:
        art = AsciiArt()
        
        print("ASCII Art Generator Demo")
        print("=" * 40)
        
        # Square demo
        print("\nSquare (5x5, symbol '*'):")
        print(art.draw_square(5, '*'))
        
        # Rectangle demo
        print("\nRectangle (6x3, symbol '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        
        # Parallelogram demo
        print("\nParallelogram (4x4, symbol '+'):")
        print(art.draw_parallelogram(4, 4, '+'))
        
        # Triangle demo
        print("\nTriangle (5x5, symbol 'o'):")
        print(art.draw_triangle(5, 5, 'o'))
        
        # Pyramid demo
        print("\nPyramid (height 4, symbol '^'):")
        print(art.draw_pyramid(4, '^'))
        
    except (InvalidSymbolError, InvalidDimensionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


art = AsciiArt()
print(art.draw_square(3, '*'))
print(art.draw_pyramid(4, '^'))
