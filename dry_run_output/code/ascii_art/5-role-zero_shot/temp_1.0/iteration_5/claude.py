
"""
ASCII Art Generator Module

This module provides functionality for generating various ASCII art shapes
including squares, rectangles, parallelograms, triangles, and pyramids.

The implementation follows ISO/IEC 25010 standards for code quality,
ensuring reliability, maintainability, and performance.
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes using specified symbols.
    
    This class provides methods to create various geometric shapes
    using ASCII characters, with proper input validation and error handling.
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single printable character.
        
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
    
    @staticmethod
    def _validate_dimensions(width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate width and height dimensions.
        
        Args:
            width (int, optional): Width to validate
            height (int, optional): Height to validate
            
        Raises:
            ValueError: If dimensions are negative or zero
            TypeError: If dimensions are not integers
        """
        for dimension, name in [(width, "Width"), (height, "Height")]:
            if dimension is not None:
                if not isinstance(dimension, int):
                    raise TypeError(f"{name} must be an integer")
                if dimension <= 0:
                    raise ValueError(f"{name} must be positive (greater than 0)")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square
            symbol (str): Single character to fill the square with
            
        Returns:
            str: Multi-line string representing the ASCII square
            
        Raises:
            ValueError: If width is negative/zero or symbol is invalid
            TypeError: If arguments are of wrong type
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        # Generate square by creating width number of rows,
        # each containing width number of symbols
        return '\n'.join([symbol * width for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle
            height (int): The height of the rectangle
            symbol (str): Single character to fill the rectangle with
            
        Returns:
            str: Multi-line string representing the ASCII rectangle
            
        Raises:
            ValueError: If width/height is negative/zero or symbol is invalid
            TypeError: If arguments are of wrong type
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        # Generate rectangle by creating height number of rows,
        # each containing width number of symbols
        return '\n'.join([symbol * width for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner, with each
        subsequent row shifted one space to the right.
        
        Args:
            width (int): The width of each row
            height (int): The height of the parallelogram
            symbol (str): Single character to fill the parallelogram with
            
        Returns:
            str: Multi-line string representing the ASCII parallelogram
            
        Raises:
            ValueError: If width/height is negative/zero or symbol is invalid
            TypeError: If arguments are of wrong type
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_parallelogram(3, 3, '@'))
            @@@
             @@@
              @@@
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Add leading spaces equal to the current row number
            # followed by width number of symbols
            spaces = ' ' * row
            symbols = symbol * width
            lines.append(spaces + symbols)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts with one symbol at the top-left corner,
        with each row adding one more symbol.
        
        Args:
            width (int): Maximum width of the triangle base
            height (int): The height of the triangle
            symbol (str): Single character to fill the triangle with
            
        Returns:
            str: Multi-line string representing the ASCII triangle
            
        Raises:
            ValueError: If width/height is negative/zero or symbol is invalid
            TypeError: If arguments are of wrong type
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_triangle(4, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Each row has (row + 1) symbols, but limited by width
            symbols_count = min(row + 1, width)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid centered with the specified symbol.
        
        The pyramid starts with one symbol at the top center and
        expands symmetrically with each row.
        
        Args:
            height (int): The height of the pyramid
            symbol (str): Single character to fill the pyramid with
            
        Returns:
            str: Multi-line string representing the ASCII pyramid
            
        Raises:
            ValueError: If height is negative/zero or symbol is invalid
            TypeError: If arguments are of wrong type
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)
        
        lines = []
        max_width = 2 * height - 1  # Width of the base
        
        for row in range(height):
            # Calculate number of symbols in current row (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row + 1
            # Calculate leading spaces to center the row
            leading_spaces = (max_width - symbols_count) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates instances of various shapes and displays them
    to showcase the functionality of the ASCII art generator.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 50)
    
    try:
        # Demonstrate square
        print("\nSquare (5x5) with '*':")
        print(ascii_art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\nRectangle (6x3) with '#':")
        print(ascii_art.draw_rectangle(6, 3, '#'))
        
        # Demonstrate parallelogram
        print("\nParallelogram (4x3) with '@':")
        print(ascii_art.draw_parallelogram(4, 3, '@'))
        
        # Demonstrate triangle
        print("\nTriangle (5x4) with '+':")
        print(ascii_art.draw_triangle(5, 4, '+'))
        
        # Demonstrate pyramid
        print("\nPyramid (height=4) with '^':")
        print(ascii_art.draw_pyramid(4, '^'))
        
        # Demonstrate error handling
        print("\nError handling demo:")
        try:
            ascii_art.draw_square(-1, '*')
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        try:
            ascii_art.draw_rectangle(3, 3, '  ')  # Two spaces
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
