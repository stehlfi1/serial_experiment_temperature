
#!/usr/bin/env python3
"""
ASCII Art Generator Application

A console-based application for generating 2D ASCII art shapes including
squares, rectangles, parallelograms, triangles, and pyramids.

This module adheres to ISO/IEC 25010 quality standards for software systems.
"""

import re
from typing import Optional


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
    ASCII characters. All shapes are drawn using a specified symbol and
    are completely filled.
    
    Attributes:
        None
        
    Methods:
        draw_square: Creates a square shape
        draw_rectangle: Creates a rectangle shape
        draw_parallelogram: Creates a parallelogram shape
        draw_triangle: Creates a right-angled triangle
        draw_pyramid: Creates a symmetrical pyramid
    """
    
    def __init__(self):
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the drawing symbol.
        
        Args:
            symbol: The character to use for drawing
            
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
    
    def _validate_dimensions(self, width: Optional[int] = None, 
                           height: Optional[int] = None) -> None:
        """
        Validate width and height dimensions.
        
        Args:
            width: The width dimension (optional)
            height: The height dimension (optional)
            
        Raises:
            InvalidDimensionError: If dimensions are invalid
        """
        if width is not None:
            if not isinstance(width, int):
                raise InvalidDimensionError("Width must be an integer")
            if width <= 0:
                raise InvalidDimensionError("Width must be positive")
        
        if height is not None:
            if not isinstance(height, int):
                raise InvalidDimensionError("Height must be an integer")
            if height <= 0:
                raise InvalidDimensionError("Height must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width: The width and height of the square
            symbol: The character to use for drawing
            
        Returns:
            A string representation of the square
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width)
        
        lines = []
        for _ in range(width):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width: The width of the rectangle
            height: The height of the rectangle
            symbol: The character to use for drawing
            
        Returns:
            A string representation of the rectangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row
        shifted by one space from the previous row.
        
        Args:
            width: The width of the parallelogram base
            height: The height of the parallelogram
            symbol: The character to use for drawing
            
        Returns:
            A string representation of the parallelogram
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        lines = []
        for row in range(height):
            # Add leading spaces for diagonal shift
            spaces = ' ' * row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the
        top-left corner with one symbol and expanding by one symbol
        per row.
        
        Args:
            width: Maximum width of the triangle base
            height: The height of the triangle
            symbol: The character to use for drawing
            
        Returns:
            A string representation of the triangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, 'o'))
            o
            oo
            ooo
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        lines = []
        for row in range(height):
            # Calculate symbols for current row (1-based, capped at width)
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows from a single symbol at the top
        to a base of (2 * height - 1) symbols.
        
        Args:
            height: The height of the pyramid
            symbol: The character to use for drawing
            
        Returns:
            A string representation of the pyramid
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(height=height)
        
        lines = []
        max_width = 2 * height - 1
        
        for row in range(height):
            # Calculate symbols for current row
            symbols_count = 2 * row + 1
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Main function to demonstrate the ASCII art functionality.
    
    This function provides a simple console interface for users to
    interact with the ASCII art generator.
    """
    art_generator = AsciiArt()
    
    print("ASCII Art Generator")
    print("==================")
    print()
    
    try:
        while True:
            print("Available shapes:")
            print("1. Square")
            print("2. Rectangle") 
            print("3. Parallelogram")
            print("4. Triangle")
            print("5. Pyramid")
            print("6. Exit")
            print()
            
            choice = input("Select a shape (1-6): ").strip()
            
            if choice == '6':
                print("Goodbye!")
                break
            
            if choice not in ['1', '2', '3', '4', '5']:
                print("Invalid choice. Please select 1-6.")
                print()
                continue
            
            # Get symbol input
            symbol = input("Enter a symbol to draw with: ").strip()
            
            try:
                if choice == '1':  # Square
                    width = int(input("Enter width: "))
                    result = art_generator.draw_square(width, symbol)
                    
                elif choice == '2':  # Rectangle
                    width = int(input("Enter width: "))
                    height = int(input("Enter height: "))
                    result = art_generator.draw_rectangle(width, height, symbol)
                    
                elif choice == '3':  # Parallelogram
                    width = int(input("Enter width: "))
                    height = int(input("Enter height: "))
                    result = art_generator.draw_parallelogram(width, height, symbol)
                    
                elif choice == '4':  # Triangle
                    width = int(input("Enter max width: "))
                    height = int(input("Enter height: "))
                    result = art_generator.draw_triangle(width, height, symbol)
                    
                elif choice == '5':  # Pyramid
                    height = int(input("Enter height: "))
                    result = art_generator.draw_pyramid(height, symbol)
                
                print("\nGenerated ASCII Art:")
                print("-" * 20)
                print(result)
                print("-" * 20)
                print()
                
            except (ValueError, AsciiArtError) as e:
                print(f"Error: {e}")
                print()
                
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")


if __name__ == "__main__":
    main()
