
"""
ASCII Art Generator Module

This module provides functionality to generate various ASCII art shapes
including squares, rectangles, parallelograms, triangles, and pyramids.
Follows ISO/IEC 25010 quality standards for software development.
"""

import re
from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes with various symbols.
    
    This class provides methods to create different geometric shapes
    using ASCII characters, with comprehensive input validation and
    error handling.
    """
    
    def __init__(self):
        """Initialize the AsciiArt generator."""
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
        
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")
    
    def _validate_dimensions(self, **kwargs) -> None:
        """
        Validate dimension parameters (width, height).
        
        Args:
            **kwargs: Dimension parameters to validate
            
        Raises:
            TypeError: If any dimension is not an integer
            ValueError: If any dimension is less than 1
        """
        for name, value in kwargs.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer")
            
            if value < 1:
                raise ValueError(f"{name.capitalize()} must be at least 1")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be >= 1)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If width is not an integer or symbol is not a string
            ValueError: If width < 1, symbol is not one character, or symbol is whitespace
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(width):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be >= 1)
            height (int): The height of the rectangle (must be >= 1)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height < 1, symbol is not one character, or symbol is whitespace
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that grows diagonally to the right.
        
        Each row is shifted one space to the right from the previous row,
        starting from the top-left corner.
        
        Args:
            width (int): The width of each row (must be >= 1)
            height (int): The height of the parallelogram (must be >= 1)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height < 1, symbol is not one character, or symbol is whitespace
            
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
            shape_line = symbol * width
            lines.append(spaces + shape_line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol
        and grows by one symbol per row.
        
        Args:
            width (int): Maximum width of the triangle base (must be >= 1)
            height (int): The height of the triangle (must be >= 1)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height < 1, symbol is not one character, or symbol is whitespace
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, '&'))
            &
            &&
            &&&
            &&&&
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate the number of symbols for this row (1-indexed)
            symbols_count = min(row + 1, width)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid centered on each row.
        
        The pyramid starts with one symbol at the top and grows
        by two symbols per row, maintaining center alignment.
        
        Args:
            height (int): The height of the pyramid (must be >= 1)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If height is not an integer or symbol is not a string
            ValueError: If height < 1, symbol is not one character, or symbol is whitespace
            
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
            # Calculate number of symbols for this row (1, 3, 5, 7, ...)
            symbols_count = 2 * row + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function provides examples of all available shapes and
    demonstrates proper error handling.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    try:
        # Demonstrate square
        print("\nSquare (5x5) with '*':")
        print(art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\nRectangle (6x3) with '#':")
        print(art.draw_rectangle(6, 3, '#'))
        
        # Demonstrate parallelogram
        print("\nParallelogram (4x3) with '+':")
        print(art.draw_parallelogram(4, 3, '+'))
        
        # Demonstrate triangle
        print("\nTriangle (5x5) with '&':")
        print(art.draw_triangle(5, 5, '&'))
        
        # Demonstrate pyramid
        print("\nPyramid (height 6) with '^':")
        print(art.draw_pyramid(6, '^'))
        
        # Demonstrate error handling
        print("\nError Handling Examples:")
        print("-" * 30)
        
        try:
            art.draw_square(0, '*')
        except ValueError as e:
            print(f"Invalid width: {e}")
        
        try:
            art.draw_rectangle(3, 2, '  ')
        except ValueError as e:
            print(f"Invalid symbol: {e}")
        
        try:
            art.draw_triangle("5", 3, '*')
        except TypeError as e:
            print(f"Invalid type: {e}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
