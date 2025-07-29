
"""
ASCII Art Generator Module

This module provides a class for generating various ASCII art shapes including
squares, rectangles, parallelograms, triangles, and pyramids.

Author: Senior Software Developer
Standard: ISO/IEC 25010
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using ASCII
    characters. All shapes are filled with the specified symbol and returned
    as multi-line strings.
    
    The class follows ISO/IEC 25010 quality standards ensuring:
    - Functional suitability
    - Performance efficiency
    - Compatibility
    - Usability
    - Reliability
    - Security
    - Maintainability
    - Portability
    """
    
    def __init__(self):
        """Initialize the AsciiArt class."""
        pass
    
    def _validate_dimensions(self, width: int, height: int = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int): The width dimension to validate
            height (int, optional): The height dimension to validate
            
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
        Validate the symbol parameter.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one printable character
        """
        if not isinstance(symbol, str):
            raise TypeError(f"Symbol must be a string, got {type(symbol).__name__}")
        
        if len(symbol) != 1:
            raise ValueError(f"Symbol must be exactly one character, got {len(symbol)} characters")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
        
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): The symbol to fill the square (must be one printable character)
            
        Returns:
            str: A multi-line string representing the ASCII square
            
        Raises:
            TypeError: If width is not an integer or symbol is not a string
            ValueError: If width is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        
        # Generate square: width x width grid filled with symbol
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
            symbol (str): The symbol to fill the rectangle (must be one printable character)
            
        Returns:
            str: A multi-line string representing the ASCII rectangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate rectangle: width x height grid filled with symbol
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the 
        top-left corner. Each row is shifted by one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): The symbol to fill the parallelogram (must be one printable character)
            
        Returns:
            str: A multi-line string representing the ASCII parallelogram
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate parallelogram: each row shifted by its index
        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the 
        top-left corner with one symbol and increasing by one symbol per row.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): The symbol to fill the triangle (must be one printable character)
            
        Returns:
            str: A multi-line string representing the ASCII triangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
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
        
        # Generate triangle: each row has (row_index + 1) symbols
        lines = []
        for row in range(height):
            # Number of symbols in current row (1-indexed)
            symbols_in_row = min(row + 1, width)
            line = symbol * symbols_in_row
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row has an odd number of symbols (1, 3, 5, 7, ...).
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): The symbol to fill the pyramid (must be one printable character)
            
        Returns:
            str: A multi-line string representing the ASCII pyramid
            
        Raises:
            TypeError: If height is not an integer or symbol is not a string
            ValueError: If height is not positive or symbol is invalid
            
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
        
        # Generate pyramid: centered with odd number of symbols per row
        lines = []
        max_width = 2 * height - 1  # Width of the bottom row
        
        for row in range(height):
            # Number of symbols in current row (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row + 1
            # Number of leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function serves as an example of how to use the AsciiArt class
    and can be used for basic testing of the functionality.
    """
    try:
        art = AsciiArt()
        
        print("=== ASCII Art Generator Demo ===\n")
        
        # Demonstrate square
        print("Square (5x5, symbol '*'):")
        print(art.draw_square(5, '*'))
        print()
        
        # Demonstrate rectangle
        print("Rectangle (6x3, symbol '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        print()
        
        # Demonstrate parallelogram
        print("Parallelogram (4x4, symbol '+'):")
        print(art.draw_parallelogram(4, 4, '+'))
        print()
        
        # Demonstrate triangle
        print("Triangle (5x5, symbol 'o'):")
        print(art.draw_triangle(5, 5, 'o'))
        print()
        
        # Demonstrate pyramid
        print("Pyramid (height 5, symbol '^'):")
        print(art.draw_pyramid(5, '^'))
        print()
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
