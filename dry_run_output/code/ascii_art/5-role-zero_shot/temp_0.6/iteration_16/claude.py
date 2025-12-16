
"""
ASCII Art Generator Module

This module provides a class for generating various ASCII art shapes including
squares, rectangles, parallelograms, triangles, and pyramids.

Author: Senior Software Developer
Standard: ISO/IEC 25010 compliant
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various geometric shapes using ASCII
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
        """Initialize the AsciiArt generator."""
        pass
    
    def _validate_dimensions(self, width: int, height: int = None) -> None:
        """
        Validate dimension parameters.
        
        Args:
            width (int): Width of the shape
            height (int, optional): Height of the shape
            
        Raises:
            ValueError: If width or height is not a positive integer
            TypeError: If width or height is not an integer
        """
        if not isinstance(width, int):
            raise TypeError("Width must be an integer")
        
        if width <= 0:
            raise ValueError("Width must be a positive integer")
        
        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer")
            
            if height <= 0:
                raise ValueError("Height must be a positive integer")
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate symbol parameter.
        
        Args:
            symbol (str): The symbol to use for drawing
            
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
        Draw a filled square using the specified symbol.
        
        Args:
            width (int): Width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters are not of correct type
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
        
        # Generate square by creating width rows of width symbols each
        rows = [symbol * width for _ in range(width)]
        return '\n'.join(rows)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width (int): Width of the rectangle (must be positive)
            height (int): Height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate rectangle by creating height rows of width symbols each
        rows = [symbol * width for _ in range(height)]
        return '\n'.join(rows)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each subsequent row is shifted one space to the right.
        
        Args:
            width (int): Width of each row (must be positive)
            height (int): Height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate parallelogram with increasing indentation for each row
        rows = []
        for row_index in range(height):
            indent = ' ' * row_index
            row_content = symbol * width
            rows.append(indent + row_content)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left
        corner. Each row contains an increasing number of symbols.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): Height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, 'x'))
            x
            xx
            xxx
            xxxx
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate triangle with increasing width for each row
        rows = []
        for row_index in range(height):
            # Calculate symbols per row based on proportional growth
            symbols_in_row = min(row_index + 1, width)
            row_content = symbol * symbols_in_row
            rows.append(row_content)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row contains an odd number of symbols (1, 3, 5, 7, ...).
        
        Args:
            height (int): Height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters are not of correct type
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
        
        # Generate pyramid with centered rows of increasing odd widths
        rows = []
        max_width = 2 * height - 1  # Width of the base
        
        for row_index in range(height):
            # Calculate symbols in current row (odd numbers: 1, 3, 5, ...)
            symbols_in_row = 2 * row_index + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_in_row) // 2
            
            # Create the row
            row_content = ' ' * leading_spaces + symbol * symbols_in_row
            rows.append(row_content)
        
        return '\n'.join(rows)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function provides examples of how to use each method in the
    AsciiArt class and demonstrates error handling.
    """
    try:
        # Create an instance of AsciiArt
        art_generator = AsciiArt()
        
        print("=== ASCII Art Generator Demo ===\n")
        
        # Demonstrate square
        print("Square (5x5, '*'):")
        print(art_generator.draw_square(5, '*'))
        print()
        
        # Demonstrate rectangle
        print("Rectangle (6x4, '#'):")
        print(art_generator.draw_rectangle(6, 4, '#'))
        print()
        
        # Demonstrate parallelogram
        print("Parallelogram (4x5, '+'):")
        print(art_generator.draw_parallelogram(4, 5, '+'))
        print()
        
        # Demonstrate triangle
        print("Triangle (6x6, 'x'):")
        print(art_generator.draw_triangle(6, 6, 'x'))
        print()
        
        # Demonstrate pyramid
        print("Pyramid (height=6, '^'):")
        print(art_generator.draw_pyramid(6, '^'))
        print()
        
        # Demonstrate error handling
        print("=== Error Handling Examples ===")
        
        try:
            art_generator.draw_square(-1, '*')
        except ValueError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art_generator.draw_rectangle(5, 3, '  ')  # Multi-character symbol
        except ValueError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art_generator.draw_triangle(4, 3, ' ')  # Whitespace symbol
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
