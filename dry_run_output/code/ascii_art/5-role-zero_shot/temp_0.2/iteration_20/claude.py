
"""
ASCII Art Generator

A high-quality Python application for generating 2D ASCII art shapes.
Implements various geometric shapes using object-oriented programming principles
and adheres to ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

import string
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
    
    This class provides methods to draw various geometric shapes using ASCII characters.
    All shapes are filled with the specified symbol and returned as multi-line strings.
    """
    
    # Class constants for validation
    MIN_DIMENSION = 1
    MAX_DIMENSION = 1000  # Reasonable upper limit for performance
    
    def __init__(self):
        """Initialize the AsciiArt generator."""
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
        
        if symbol not in string.printable or symbol in '\n\r\t\v\f':
            raise InvalidSymbolError("Symbol must be a printable character")
    
    def _validate_dimension(self, dimension: int, name: str) -> None:
        """
        Validate dimension parameters.
        
        Args:
            dimension (int): The dimension value to validate
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
        
        # Generate square by creating width rows of width symbols each
        rows = [symbol * width for _ in range(width)]
        return '\n'.join(rows)
    
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
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        # Generate rectangle by creating height rows of width symbols each
        rows = [symbol * width for _ in range(height)]
        return '\n'.join(rows)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right compared to the previous row.
        
        Args:
            width (int): The width of each row
            height (int): The height of the parallelogram
            symbol (str): The symbol to fill the parallelogram with
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            InvalidDimensionError: If width or height is invalid
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '@'))
            @@@
             @@@
              @@@
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        rows = []
        for row_index in range(height):
            # Add leading spaces for the diagonal shift
            leading_spaces = ' ' * row_index
            row_content = symbol * width
            rows.append(leading_spaces + row_content)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        Each row contains one more symbol than the previous row.
        
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
            >>> print(art.draw_triangle(3, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        rows = []
        for row_index in range(height):
            # Calculate symbols per row, ensuring we don't exceed width
            symbols_in_row = min(row_index + 1, width)
            row_content = symbol * symbols_in_row
            rows.append(row_content)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row contains an odd number of symbols (1, 3, 5, 7, ...).
        
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
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        rows = []
        max_width = 2 * height - 1  # Width of the base
        
        for row_index in range(height):
            # Calculate symbols in current row (1, 3, 5, 7, ...)
            symbols_in_row = 2 * row_index + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_in_row) // 2
            
            # Build the row
            row_content = ' ' * leading_spaces + symbol * symbols_in_row
            rows.append(row_content)
        
        return '\n'.join(rows)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function provides examples of how to use each method and demonstrates
    error handling capabilities.
    """
    try:
        art = AsciiArt()
        
        print("=== ASCII Art Generator Demo ===\n")
        
        # Demonstrate square
        print("Square (5x5, '*'):")
        print(art.draw_square(5, '*'))
        print()
        
        # Demonstrate rectangle
        print("Rectangle (6x3, '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        print()
        
        # Demonstrate parallelogram
        print("Parallelogram (4x4, '@'):")
        print(art.draw_parallelogram(4, 4, '@'))
        print()
        
        # Demonstrate triangle
        print("Triangle (5x5, '+'):")
        print(art.draw_triangle(5, 5, '+'))
        print()
        
        # Demonstrate pyramid
        print("Pyramid (height=6, '^'):")
        print(art.draw_pyramid(6, '^'))
        print()
        
        # Demonstrate error handling
        print("=== Error Handling Demo ===")
        try:
            art.draw_square(-1, '*')
        except InvalidDimensionError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_rectangle(5, 3, '  ')  # Multi-character symbol
        except InvalidSymbolError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_triangle(3, 2, ' ')  # Whitespace symbol
        except InvalidSymbolError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
