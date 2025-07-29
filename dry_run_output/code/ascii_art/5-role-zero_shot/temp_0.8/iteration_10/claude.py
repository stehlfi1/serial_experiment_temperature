
"""
ASCII Art Generator - A console-based 2D ASCII art application.

This module provides functionality to generate various ASCII art shapes
including squares, rectangles, parallelograms, triangles, and pyramids.
Follows ISO/IEC 25010 quality standards for maintainable software.
"""

from typing import Union


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    
    This class provides methods to create various geometric shapes using
    ASCII characters. All shapes are filled with the specified symbol.
    """
    
    def __init__(self):
        """Initialize the AsciiArt generator."""
        pass
    
    def _validate_dimensions(self, width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width: Width of the shape (optional)
            height: Height of the shape (optional)
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is negative or zero
        """
        for dimension, name in [(width, 'width'), (height, 'height')]:
            if dimension is not None:
                if not isinstance(dimension, int):
                    raise TypeError(f"{name} must be an integer")
                if dimension <= 0:
                    raise ValueError(f"{name} must be positive")
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the drawing symbol.
        
        Args:
            symbol: The character to use for drawing
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one printable character
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("symbol cannot be a whitespace character")
        
        if not symbol.isprintable():
            raise ValueError("symbol must be a printable character")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square using the specified symbol.
        
        Args:
            width: The width and height of the square
            symbol: The character to use for drawing
            
        Returns:
            str: Multi-line string representation of the square
            
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
        
        # Generate square by creating width rows of width symbols each
        lines = [symbol * width for _ in range(width)]
        return '\n'.join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width: The width of the rectangle
            height: The height of the rectangle
            symbol: The character to use for drawing
            
        Returns:
            str: Multi-line string representation of the rectangle
            
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
        
        # Generate rectangle by creating height rows of width symbols each
        lines = [symbol * width for _ in range(height)]
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from 
        the top-left corner. Each row is shifted by one space to the right.
        
        Args:
            width: The width of each row
            height: The height of the parallelogram
            symbol: The character to use for drawing
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '*'))
            ***
             ***
              ***
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Add leading spaces for the diagonal shift
            spaces = ' ' * row
            # Add the symbols for this row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the 
        top-left corner with one symbol and expanding by one symbol per row.
        
        Args:
            width: The maximum width of the triangle base
            height: The height of the triangle
            symbol: The character to use for drawing
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, '*'))
            *
            **
            ***
            ****
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols for this row (1 to width, but not exceeding width)
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        The top row has 1 symbol, and each subsequent row has 2 more symbols.
        
        Args:
            height: The height of the pyramid
            symbol: The character to use for drawing
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '*'))
              *
             ***
            *****
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)
        
        lines = []
        # Calculate the width of the base (bottom row)
        base_width = 2 * height - 1
        
        for row in range(height):
            # Calculate symbols for this row (1, 3, 5, 7, ...)
            symbols_count = 2 * row + 1
            # Calculate leading spaces for centering
            spaces_count = (base_width - symbols_count) // 2
            
            # Build the line with centering spaces and symbols
            line = ' ' * spaces_count + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration of the AsciiArt class functionality.
    
    This function provides a simple interactive demo of all available shapes.
    """
    try:
        art = AsciiArt()
        
        print("ASCII Art Generator Demo")
        print("=" * 30)
        
        # Demo square
        print("\nSquare (5x5, '*'):")
        print(art.draw_square(5, '*'))
        
        # Demo rectangle
        print("\nRectangle (6x3, '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        
        # Demo parallelogram
        print("\nParallelogram (4x4, '+'):")
        print(art.draw_parallelogram(4, 4, '+'))
        
        # Demo triangle
        print("\nTriangle (5x5, '='):")
        print(art.draw_triangle(5, 5, '='))
        
        # Demo pyramid
        print("\nPyramid (height 4, '^'):")
        print(art.draw_pyramid(4, '^'))
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
