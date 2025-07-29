
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes using configurable symbols.

This module adheres to ISO/IEC 25010 quality standards focusing on:
- Functional Suitability
- Performance Efficiency
- Compatibility
- Usability
- Reliability
- Security
- Maintainability
- Portability
"""

import string
from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art representations of geometric shapes.
    
    This class provides methods to draw various shapes including squares,
    rectangles, parallelograms, triangles, and pyramids using customizable
    symbols.
    
    All methods validate input parameters and return multi-line strings
    representing the requested shapes.
    """
    
    def __init__(self):
        """Initialize the AsciiArt generator."""
        self._printable_chars = set(string.printable) - {' ', '\t', '\n', '\r', '\v', '\f'}
    
    def _validate_dimensions(self, width: int, height: int = None) -> None:
        """
        Validate dimensional parameters.
        
        Args:
            width (int): Width dimension to validate
            height (int, optional): Height dimension to validate
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is not positive
        """
        if not isinstance(width, int):
            raise TypeError(f"Width must be an integer, got {type(width).__name__}")
        
        if width <= 0:
            raise ValueError(f"Width must be positive, got {width}")
        
        if height is not None:
            if not isinstance(height, int):
                raise TypeError(f"Height must be an integer, got {type(height).__name__}")
            
            if height <= 0:
                raise ValueError(f"Height must be positive, got {height}")
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the drawing symbol.
        
        Args:
            symbol (str): Symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one printable character
        """
        if not isinstance(symbol, str):
            raise TypeError(f"Symbol must be a string, got {type(symbol).__name__}")
        
        if len(symbol) != 1:
            raise ValueError(f"Symbol must be exactly one character, got length {len(symbol)}")
        
        if symbol not in self._printable_chars:
            raise ValueError(f"Symbol must be a printable non-whitespace character, got '{symbol}'")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): Width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        
        # Generate square using list comprehension for efficiency
        lines = [symbol * width for _ in range(width)]
        return '\n'.join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): Width of the rectangle (must be positive)
            height (int): Height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate rectangle using list comprehension for efficiency
        lines = [symbol * width for _ in range(height)]
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each subsequent row is shifted one space to the right.
        
        Args:
            width (int): Width of each row (must be positive)
            height (int): Height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '@'))
            @@@
             @@@
              @@@
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate parallelogram with progressive indentation
        lines = [' ' * i + symbol * width for i in range(height)]
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the
        top-left corner with a single symbol and expanding by one symbol
        per row.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): Height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate triangle with increasing width per row
        # Ensure we don't exceed the specified width
        lines = []
        for i in range(height):
            current_width = min(i + 1, width)
            lines.append(symbol * current_width)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered with the apex at the top and base at the bottom.
        Each row contains an odd number of symbols (1, 3, 5, 7, ...).
        
        Args:
            height (int): Height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        
        # Calculate maximum width (base of pyramid)
        max_width = 2 * height - 1
        
        # Generate pyramid with centered alignment
        lines = []
        for i in range(height):
            # Current row width: 1, 3, 5, 7, ...
            current_width = 2 * i + 1
            # Calculate leading spaces for centering
            leading_spaces = (max_width - current_width) // 2
            line = ' ' * leading_spaces + symbol * current_width
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function provides examples of all available shapes and includes
    basic error handling to demonstrate the validation capabilities.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    try:
        # Demonstrate square
        print("\n1. Square (5x5, symbol='*'):")
        print(art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\n2. Rectangle (6x3, symbol='#'):")
        print(art.draw_rectangle(6, 3, '#'))
        
        # Demonstrate parallelogram
        print("\n3. Parallelogram (4x4, symbol='@'):")
        print(art.draw_parallelogram(4, 4, '@'))
        
        # Demonstrate triangle
        print("\n4. Triangle (5x5, symbol='+'):")
        print(art.draw_triangle(5, 5, '+'))
        
        # Demonstrate pyramid
        print("\n5. Pyramid (height=5, symbol='^'):")
        print(art.draw_pyramid(5, '^'))
        
        # Demonstrate error handling
        print("\n6. Error Handling Examples:")
        
        # Invalid symbol (multiple characters)
        try:
            art.draw_square(3, '**')
        except ValueError as e:
            print(f"   Multi-character symbol error: {e}")
        
        # Invalid symbol (whitespace)
        try:
            art.draw_square(3, ' ')
        except ValueError as e:
            print(f"   Whitespace symbol error: {e}")
        
        # Invalid dimensions
        try:
            art.draw_rectangle(-1, 3, '*')
        except ValueError as e:
            print(f"   Negative dimension error: {e}")
        
        # Type validation
        try:
            art.draw_triangle("invalid", 3, '*')
        except TypeError as e:
            print(f"   Type validation error: {e}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
