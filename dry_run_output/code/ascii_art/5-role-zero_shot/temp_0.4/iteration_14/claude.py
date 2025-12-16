
"""
ASCII Art Generator Module

This module provides functionality to generate various ASCII art shapes
including squares, rectangles, parallelograms, triangles, and pyramids.
Implements ISO/IEC 25010 quality standards for maintainable software.
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes using specified symbols.
    
    This class provides methods to create various geometric shapes
    represented as ASCII art strings. All shapes are filled with
    the specified symbol character.
    """
    
    def __init__(self) -> None:
        """Initialize the AsciiArt generator."""
        pass
    
    def _validate_dimensions(self, width: int, height: Union[int, None] = None) -> None:
        """
        Validate dimension parameters.
        
        Args:
            width (int): Width dimension to validate
            height (Union[int, None]): Height dimension to validate (optional)
            
        Raises:
            TypeError: If dimensions are not integers
            ValueError: If dimensions are not positive
        """
        if not isinstance(width, int):
            raise TypeError("Width must be an integer")
        
        if width <= 0:
            raise ValueError("Width must be positive")
            
        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer")
            
            if height <= 0:
                raise ValueError("Height must be positive")
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate symbol parameter.
        
        Args:
            symbol (str): Symbol character to validate
            
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
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): Width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(width))
    
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
            TypeError: If parameters are of incorrect type
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from
        the top-left corner. Each row is shifted by one space to the right.
        
        Args:
            width (int): Width of the parallelogram base (must be positive)
            height (int): Height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(4, 3, '+'))
            ++++
             ++++
              ++++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            spaces = ' ' * row
            shape_line = symbol * width
            lines.append(spaces + shape_line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the
        top-left corner with a single symbol and expanding by one symbol
        per row until reaching the specified width.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): Height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, 'o'))
            o
            oo
            ooo
            oooo
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols per row, ensuring we don't exceed width
            symbols_count = min(row + 1, width)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        The top row has 1 symbol, and each subsequent row has 2 more symbols
        than the previous row.
        
        Args:
            height (int): Height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters have invalid values
            
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
        
        lines = []
        max_width = 2 * height - 1  # Width of the base
        
        for row in range(height):
            symbols_count = 2 * row + 1  # Odd numbers: 1, 3, 5, 7, ...
            spaces_count = (max_width - symbols_count) // 2
            
            line = ' ' * spaces_count + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main() -> None:
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates various ASCII art shapes and displays them
    to demonstrate the functionality of the AsciiArt class.
    """
    art_generator = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    try:
        # Demonstrate square
        print("\nSquare (5x5) with '*':")
        print(art_generator.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\nRectangle (6x4) with '#':")
        print(art_generator.draw_rectangle(6, 4, '#'))
        
        # Demonstrate parallelogram
        print("\nParallelogram (5x4) with '+':")
        print(art_generator.draw_parallelogram(5, 4, '+'))
        
        # Demonstrate triangle
        print("\nTriangle (6x6) with 'o':")
        print(art_generator.draw_triangle(6, 6, 'o'))
        
        # Demonstrate pyramid
        print("\nPyramid (height 5) with '^':")
        print(art_generator.draw_pyramid(5, '^'))
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
