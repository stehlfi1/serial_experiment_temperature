
"""
ASCII Art Generator Module

This module provides functionality to create various ASCII art shapes including
squares, rectangles, parallelograms, triangles, and pyramids.

Author: Senior Software Developer
Version: 1.0.0
Compliance: ISO/IEC 25010 Software Quality Standard
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various geometric shapes using ASCII
    characters. All shapes are filled with the specified symbol and returned
    as multi-line strings.
    
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
        Validate the symbol parameter.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            ValueError: If symbol is not a single printable character
            TypeError: If symbol is not a string
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
        
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")
    
    def _validate_dimensions(self, **dimensions: int) -> None:
        """
        Validate dimension parameters.
        
        Args:
            **dimensions: Keyword arguments containing dimension values
            
        Raises:
            ValueError: If any dimension is not positive
            TypeError: If any dimension is not an integer
        """
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer")
            
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square using the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            ValueError: If width is not positive or symbol is invalid
            TypeError: If parameters are not of correct type
            
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
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid
            TypeError: If parameters are not of correct type
            
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
        Draw a filled parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each row is shifted by one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid
            TypeError: If parameters are not of correct type
            
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
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left
        corner. Each row has one more symbol than the previous row.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid
            TypeError: If parameters are not of correct type
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, 'o'))
            o
            oo
            ooo
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols per row, ensuring we don't exceed width
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row has two more symbols than the previous row.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            ValueError: If height is not positive or symbol is invalid
            TypeError: If parameters are not of correct type
            
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
            # Calculate symbols for current row (1, 3, 5, 7, ...)
            symbols_count = 2 * row + 1
            # Calculate leading spaces for centering
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
    try:
        # Create an instance of AsciiArt
        art = AsciiArt()
        
        print("ASCII Art Generator Demo")
        print("=" * 40)
        
        # Demonstrate square
        print("\n1. Square (5x5) with '*':")
        print(art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\n2. Rectangle (6x3) with '#':")
        print(art.draw_rectangle(6, 3, '#'))
        
        # Demonstrate parallelogram
        print("\n3. Parallelogram (4x4) with '+':")
        print(art.draw_parallelogram(4, 4, '+'))
        
        # Demonstrate triangle
        print("\n4. Triangle (5x5) with 'o':")
        print(art.draw_triangle(5, 5, 'o'))
        
        # Demonstrate pyramid
        print("\n5. Pyramid (height 4) with '^':")
        print(art.draw_pyramid(4, '^'))
        
        # Demonstrate error handling
        print("\n6. Error handling demonstration:")
        try:
            art.draw_square(-1, '*')  # Should raise ValueError
        except ValueError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_rectangle(3, 3, '  ')  # Should raise ValueError
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
