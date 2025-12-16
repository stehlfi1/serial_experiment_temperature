
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
    
    This class provides methods to draw various geometric shapes using
    ASCII characters. All shapes are filled with the specified symbol
    and returned as multi-line strings.
    
    Attributes:
        None
        
    Methods:
        draw_square: Creates a filled square
        draw_rectangle: Creates a filled rectangle
        draw_parallelogram: Creates a filled parallelogram
        draw_triangle: Creates a filled right-angled triangle
        draw_pyramid: Creates a filled symmetrical pyramid
    """
    
    def __init__(self) -> None:
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate that the symbol is a single printable character.
        
        Args:
            symbol: The character to validate
            
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
    
    def _validate_dimensions(self, width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate width and/or height parameters.
        
        Args:
            width: Width dimension to validate (optional)
            height: Height dimension to validate (optional)
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is not positive
        """
        for dimension, name in [(width, "Width"), (height, "Height")]:
            if dimension is not None:
                if not isinstance(dimension, int):
                    raise TypeError(f"{name} must be an integer")
                if dimension <= 0:
                    raise ValueError(f"{name} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square with the specified width and symbol.
        
        Args:
            width: The width (and height) of the square
            symbol: The character to fill the square with
            
        Returns:
            A multi-line string representing the square
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If width is not positive or symbol is invalid
            
        Examples:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        lines = []
        row = symbol * width
        
        for _ in range(width):
            lines.append(row)
        
        return '\n'.join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle with the specified dimensions and symbol.
        
        Args:
            width: The width of the rectangle
            height: The height of the rectangle
            symbol: The character to fill the rectangle with
            
        Returns:
            A multi-line string representing the rectangle
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If dimensions are not positive or symbol is invalid
            
        Examples:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        row = symbol * width
        
        for _ in range(height):
            lines.append(row)
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner and each subsequent
        row is shifted one space to the right.
        
        Args:
            width: The width of each row
            height: The height (number of rows) of the parallelogram
            symbol: The character to fill the parallelogram with
            
        Returns:
            A multi-line string representing the parallelogram
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If dimensions are not positive or symbol is invalid
            
        Examples:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '@'))
            @@@
             @@@
              @@@
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        base_row = symbol * width
        
        for row_index in range(height):
            # Add leading spaces for diagonal effect
            spaces = ' ' * row_index
            lines.append(spaces + base_row)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol and
        grows by one symbol per row.
        
        Args:
            width: The maximum width of the triangle base
            height: The height (number of rows) of the triangle
            symbol: The character to fill the triangle with
            
        Returns:
            A multi-line string representing the triangle
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If dimensions are not positive or symbol is invalid
            
        Examples:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        
        for row_index in range(height):
            # Calculate symbols for this row, but don't exceed width
            symbols_count = min(row_index + 1, width)
            row = symbol * symbols_count
            lines.append(row)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid.
        
        The pyramid is centered and grows symmetrically from a single symbol
        at the top to the full base width at the bottom.
        
        Args:
            height: The height (number of rows) of the pyramid
            symbol: The character to fill the pyramid with
            
        Returns:
            A multi-line string representing the pyramid
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If height is not positive or symbol is invalid
            
        Examples:
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
        
        # Calculate the width of the base (bottom row)
        base_width = 2 * height - 1
        
        for row_index in range(height):
            # Calculate symbols for this row (1, 3, 5, 7, ...)
            symbols_count = 2 * row_index + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (base_width - symbols_count) // 2
            
            # Create the row
            row = ' ' * leading_spaces + symbol * symbols_count
            lines.append(row)
        
        return '\n'.join(lines)


def main() -> None:
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates instances of various shapes and displays them
    to demonstrate the functionality of the AsciiArt class.
    """
    art = AsciiArt()
    
    print("=== ASCII Art Generator Demo ===\n")
    
    try:
        # Demonstrate square
        print("Square (4x4 with '*'):")
        print(art.draw_square(4, '*'))
        print()
        
        # Demonstrate rectangle
        print("Rectangle (6x3 with '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        print()
        
        # Demonstrate parallelogram
        print("Parallelogram (5x4 with '@'):")
        print(art.draw_parallelogram(5, 4, '@'))
        print()
        
        # Demonstrate triangle
        print("Triangle (6x5 with '+'):")
        print(art.draw_triangle(6, 5, '+'))
        print()
        
        # Demonstrate pyramid
        print("Pyramid (height 5 with '^'):")
        print(art.draw_pyramid(5, '^'))
        print()
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
