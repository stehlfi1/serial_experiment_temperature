
"""
ASCII Art Generator - A console-based 2D ASCII art application.

This module provides functionality to generate various ASCII art shapes
including squares, rectangles, parallelograms, triangles, and pyramids.
Adheres to ISO/IEC 25010 quality standards.
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using
    ASCII characters. All shapes are filled with the specified symbol.
    """
    
    def __init__(self) -> None:
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the symbol parameter.
        
        Args:
            symbol: The character to use for drawing
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one printable character
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
        
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")
    
    def _validate_dimensions(self, width: int = None, height: int = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width: Width dimension (optional)
            height: Height dimension (optional)
            
        Raises:
            TypeError: If dimensions are not integers
            ValueError: If dimensions are not positive
        """
        for dimension, name in [(width, "width"), (height, "height")]:
            if dimension is not None:
                if not isinstance(dimension, int):
                    raise TypeError(f"{name.capitalize()} must be an integer")
                if dimension <= 0:
                    raise ValueError(f"{name.capitalize()} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square with the specified width and symbol.
        
        Args:
            width: The width and height of the square
            symbol: The character to fill the square with
            
        Returns:
            A string representation of the ASCII square
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
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
        Draw a filled rectangle with the specified dimensions and symbol.
        
        Args:
            width: The width of the rectangle
            height: The height of the rectangle
            symbol: The character to fill the rectangle with
            
        Returns:
            A string representation of the ASCII rectangle
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
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
        Draw a filled parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner, with each subsequent
        row shifted one space to the right.
        
        Args:
            width: The width of each row in the parallelogram
            height: The height of the parallelogram
            symbol: The character to fill the parallelogram with
            
        Returns:
            A string representation of the ASCII parallelogram
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '@'))
            @@@
             @@@
              @@@
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            padding = ' ' * row
            line = padding + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol,
        and each row adds one more symbol.
        
        Args:
            width: The maximum width of the triangle base
            height: The height of the triangle
            symbol: The character to fill the triangle with
            
        Returns:
            A string representation of the ASCII triangle
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values or width < height
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        if width < height:
            raise ValueError("Width must be greater than or equal to height for triangle")
        
        lines = []
        for row in range(height):
            line = symbol * (row + 1)
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        The top row has one symbol, and each subsequent row adds two more symbols.
        
        Args:
            height: The height of the pyramid
            symbol: The character to fill the pyramid with
            
        Returns:
            A string representation of the ASCII pyramid
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
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
            symbols_count = 2 * row + 1
            padding_count = (max_width - symbols_count) // 2
            padding = ' ' * padding_count
            line = padding + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main() -> None:
    """
    Main function to demonstrate the ASCII art functionality.
    
    This function provides a simple interactive interface for users
    to test different shapes and symbols.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator")
    print("==================")
    
    try:
        # Demonstrate each shape
        print("\n1. Square (3x3) with '*':")
        print(art.draw_square(3, '*'))
        
        print("\n2. Rectangle (5x3) with '#':")
        print(art.draw_rectangle(5, 3, '#'))
        
        print("\n3. Parallelogram (4x3) with '@':")
        print(art.draw_parallelogram(4, 3, '@'))
        
        print("\n4. Triangle (4x4) with '+':")
        print(art.draw_triangle(4, 4, '+'))
        
        print("\n5. Pyramid (height 4) with '^':")
        print(art.draw_pyramid(4, '^'))
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
