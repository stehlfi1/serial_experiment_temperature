
"""
ASCII Art Generator

A high-quality Python application for generating 2D ASCII art shapes.
Implements various geometric shapes using object-oriented programming principles
and adheres to ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

import re
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
    
    This class provides methods to create various geometric shapes using ASCII characters.
    All shapes are filled with the specified symbol and returned as multi-line strings.
    
    The class ensures input validation and follows best practices for maintainability
    and performance.
    """
    
    # Class constants for validation
    MIN_DIMENSION = 1
    MAX_DIMENSION = 1000  # Reasonable upper limit for performance
    
    def __init__(self):
        """Initialize the AsciiArt generator."""
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
            raise InvalidSymbolError("Symbol cannot be whitespace")
        
        if not symbol.isprintable():
            raise InvalidSymbolError("Symbol must be printable")
    
    def _validate_dimension(self, dimension: int, name: str) -> None:
        """
        Validate dimension values.
        
        Args:
            dimension (int): The dimension to validate
            name (str): The name of the dimension for error messages
            
        Raises:
            InvalidDimensionError: If dimension is invalid
        """
        if not isinstance(dimension, int):
            raise InvalidDimensionError(f"{name} must be an integer")
        
        if dimension < self.MIN_DIMENSION:
            raise InvalidDimensionError(f"{name} must be at least {self.MIN_DIMENSION}")
        
        if dimension > self.MAX_DIMENSION:
            raise InvalidDimensionError(f"{name} cannot exceed {self.MAX_DIMENSION}")
    
    def _validate_common_inputs(self, width: int, height: int, symbol: str) -> None:
        """
        Validate common inputs for shape drawing methods.
        
        Args:
            width (int): The width dimension
            height (int): The height dimension
            symbol (str): The drawing symbol
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square
            symbol (str): The symbol to fill the square with
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            InvalidDimensionError: If width is invalid
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)
        
        # Create each row of the square
        row = symbol * width
        return '\n'.join(row for _ in range(width))
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle
            height (int): The height of the rectangle
            symbol (str): The symbol to fill the rectangle with
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            InvalidDimensionError: If width or height is invalid
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_common_inputs(width, height, symbol)
        
        # Create each row of the rectangle
        row = symbol * width
        return '\n'.join(row for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right.
        
        Args:
            width (int): The width of the parallelogram base
            height (int): The height of the parallelogram
            symbol (str): The symbol to fill the parallelogram with
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            InvalidDimensionError: If width or height is invalid
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '*'))
            ***
             ***
              ***
        """
        self._validate_common_inputs(width, height, symbol)
        
        rows = []
        base_row = symbol * width
        
        for row_index in range(height):
            # Add leading spaces for the parallelogram shift
            leading_spaces = ' ' * row_index
            rows.append(leading_spaces + base_row)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        Each row increases in width by one symbol.
        
        Args:
            width (int): The maximum width of the triangle base
            height (int): The height of the triangle
            symbol (str): The symbol to fill the triangle with
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            InvalidDimensionError: If width or height is invalid
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, '*'))
            *
            **
            ***
        """
        self._validate_common_inputs(width, height, symbol)
        
        rows = []
        
        for row_index in range(height):
            # Calculate the number of symbols for this row
            # Ensure we don't exceed the specified width
            symbols_in_row = min(row_index + 1, width)
            row = symbol * symbols_in_row
            rows.append(row)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        
        Args:
            height (int): The height of the pyramid
            symbol (str): The symbol to fill the pyramid with
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            InvalidDimensionError: If height is invalid
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '*'))
              *
             ***
            *****
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        rows = []
        
        for row_index in range(height):
            # Calculate the number of symbols for this row (odd numbers: 1, 3, 5, ...)
            symbols_in_row = 2 * row_index + 1
            
            # Calculate leading spaces for centering
            leading_spaces = height - row_index - 1
            
            # Create the row
            row = ' ' * leading_spaces + symbol * symbols_in_row
            rows.append(row)
        
        return '\n'.join(rows)


def main():
    """
    Main function to demonstrate the ASCII Art generator.
    
    This function provides a simple console interface for testing
    the various shape drawing capabilities.
    """
    try:
        art_generator = AsciiArt()
        
        print("ASCII Art Generator Demo")
        print("=" * 25)
        
        # Demonstrate each shape
        print("\n1. Square (5x5 with '*'):")
        print(art_generator.draw_square(5, '*'))
        
        print("\n2. Rectangle (6x4 with '#'):")
        print(art_generator.draw_rectangle(6, 4, '#'))
        
        print("\n3. Parallelogram (4x4 with '+'):")
        print(art_generator.draw_parallelogram(4, 4, '+'))
        
        print("\n4. Triangle (5x5 with '='):")
        print(art_generator.draw_triangle(5, 5, '='))
        
        print("\n5. Pyramid (height 6 with '^'):")
        print(art_generator.draw_pyramid(6, '^'))
        
    except (InvalidSymbolError, InvalidDimensionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
