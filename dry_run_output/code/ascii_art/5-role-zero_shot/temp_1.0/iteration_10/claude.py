
"""
ASCII Art Generator Module

This module provides a class for generating various ASCII art shapes including
squares, rectangles, parallelograms, triangles, and pyramids.

The implementation follows ISO/IEC 25010 quality standards focusing on:
- Functional suitability
- Performance efficiency
- Maintainability
- Reliability
- Usability
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using ASCII
    characters. All shapes are filled with the specified symbol.
    
    Attributes:
        None
        
    Methods:
        draw_square: Creates a square shape
        draw_rectangle: Creates a rectangle shape
        draw_parallelogram: Creates a parallelogram shape
        draw_triangle: Creates a right-angled triangle
        draw_pyramid: Creates a symmetrical pyramid
    """
    
    @staticmethod
    def _validate_dimensions(width: int, height: int = None) -> None:
        """
        Validate dimensional parameters for shape drawing.
        
        Args:
            width (int): The width of the shape
            height (int, optional): The height of the shape
            
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

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate the symbol parameter for shape drawing.
        
        Args:
            symbol (str): The character to use for drawing
            
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
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representing the ASCII square
            
        Raises:
            TypeError: If width is not an integer or symbol is not a string
            ValueError: If width is not positive, symbol is not one character,
                      symbol is whitespace, or symbol is not printable
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, "*"))
            ***
            ***
            ***
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        
        # Generate each row of the square
        rows = [symbol * width for _ in range(width)]
        return '\n'.join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representing the ASCII rectangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive, symbol is not one character,
                      symbol is whitespace, or symbol is not printable
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, "#"))
            ####
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate each row of the rectangle
        rows = [symbol * width for _ in range(height)]
        return '\n'.join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each subsequent row is shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representing the ASCII parallelogram
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive, symbol is not one character,
                      symbol is whitespace, or symbol is not printable
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, "*"))
            ***
             ***
              ***
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate each row with increasing indentation
        rows = [' ' * i + symbol * width for i in range(height)]
        return '\n'.join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left
        corner. Each row contains one more symbol than the previous row.
        The triangle will have 'height' rows, with the bottom row containing
        'width' symbols.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): Height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representing the ASCII triangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive, symbol is not one character,
                      symbol is whitespace, or symbol is not printable
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, "*"))
            *
            **
            ***
            ****
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Calculate symbols per row to reach 'width' symbols at the bottom
        rows = []
        for i in range(height):
            # Linear interpolation from 1 to width over height rows
            symbols_in_row = 1 + (width - 1) * i // (height - 1) if height > 1 else width
            rows.append(symbol * symbols_in_row)
        
        return '\n'.join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered, with each row having an odd number of symbols.
        The top row has 1 symbol, and each subsequent row adds 2 more symbols.
        
        Args:
            height (int): Height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representing the ASCII pyramid
            
        Raises:
            TypeError: If height is not an integer or symbol is not a string
            ValueError: If height is not positive, symbol is not one character,
                      symbol is whitespace, or symbol is not printable
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, "*"))
               *
              ***
             *****
            *******
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        
        rows = []
        max_width = 2 * height - 1  # Width of the bottom row
        
        for i in range(height):
            # Number of symbols in current row (1, 3, 5, 7, ...)
            symbols_count = 2 * i + 1
            # Number of spaces for centering
            spaces_count = (max_width - symbols_count) // 2
            
            row = ' ' * spaces_count + symbol * symbols_count
            rows.append(row)
        
        return '\n'.join(rows)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates instances of various shapes and prints them
    to demonstrate the functionality of the AsciiArt class.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    try:
        print("\n1. Square (5x5) with '*':")
        print(art.draw_square(5, '*'))
        
        print("\n2. Rectangle (6x4) with '#':")
        print(art.draw_rectangle(6, 4, '#'))
        
        print("\n3. Parallelogram (4x5) with '@':")
        print(art.draw_parallelogram(4, 5, '@'))
        
        print("\n4. Triangle (6x4) with '+':")
        print(art.draw_triangle(6, 4, '+'))
        
        print("\n5. Pyramid (height=5) with '▲':")
        print(art.draw_pyramid(5, '▲'))
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
