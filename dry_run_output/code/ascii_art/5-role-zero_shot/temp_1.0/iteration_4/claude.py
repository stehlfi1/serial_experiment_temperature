
"""
ASCII Art Drawing Application

This module provides functionality to draw various ASCII shapes including squares,
rectangles, parallelograms, triangles, and pyramids.

The implementation follows ISO/IEC 25010 quality standards with focus on:
- Functional Suitability
- Reliability 
- Usability
- Performance Efficiency
- Maintainability
- Portability
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using ASCII characters.
    All shapes are filled with the specified symbol and returned as multi-line strings.
    
    The class ensures input validation and follows defensive programming practices
    to maintain reliability and robustness.
    """
    
    @staticmethod
    def _validate_dimensions(width: int, height: int = None) -> None:
        """
        Validate shape dimensions.
        
        Args:
            width (int): The width of the shape
            height (int, optional): The height of the shape
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is negative or zero
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
        Validate the drawing symbol.
        
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
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If width is not positive or symbol is invalid
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        
        # Efficient single-pass generation using list comprehension
        return '\n'.join([symbol * width for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Pre-compute the row to avoid repeated string multiplication
        row = symbol * width
        return '\n'.join([row for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each subsequent row
        shifted one space to the right from the previous row.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Generate rows with progressive indentation
        base_row = symbol * width
        return '\n'.join([' ' * row_num + base_row for row_num in range(height)])
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally from the top-left corner, with each row
        containing one more symbol than the previous row.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_triangle(3, 3, 'o'))
            o
            oo
            ooo
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Calculate symbols per row based on position and constraints
        rows = []
        for row_num in range(height):
            symbols_in_row = min(row_num + 1, width)
            rows.append(symbol * symbols_in_row)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows wider towards the base, with each row
        containing two more symbols than the previous row.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters are not of expected types
            ValueError: If height is not positive or symbol is invalid
            
        Example:
            >>> ascii_art = AsciiArt()
            >>> print(ascii_art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        
        # Calculate maximum width for centering
        max_width = 2 * height - 1
        rows = []
        
        for row_num in range(height):
            # Number of symbols in current row (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row_num + 1
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            row = ' ' * leading_spaces + symbol * symbols_count
            rows.append(row)
        
        return '\n'.join(rows)


def main():
    """
    Demonstration function showcasing the AsciiArt class functionality.
    
    This function provides examples of all available shapes and demonstrates
    proper usage patterns for the AsciiArt class.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Drawing Application")
    print("=" * 40)
    
    try:
        # Demonstrate square
        print("\n1. Square (5x5, symbol '*'):")
        print(ascii_art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\n2. Rectangle (6x3, symbol '#'):")
        print(ascii_art.draw_rectangle(6, 3, '#'))
        
        # Demonstrate parallelogram
        print("\n3. Parallelogram (4x4, symbol '+'):")
        print(ascii_art.draw_parallelogram(4, 4, '+'))
        
        # Demonstrate triangle
        print("\n4. Right-angled Triangle (5x5, symbol 'o'):")
        print(ascii_art.draw_triangle(5, 5, 'o'))
        
        # Demonstrate pyramid
        print("\n5. Pyramid (height 4, symbol '^'):")
        print(ascii_art.draw_pyramid(4, '^'))
        
        # Demonstrate error handling
        print("\n6. Error Handling Examples:")
        
        # Invalid symbol length
        try:
            ascii_art.draw_square(3, '**')
        except ValueError as e:
            print(f"   Error - Multi-character symbol: {e}")
        
        # Whitespace symbol
        try:
            ascii_art.draw_square(3, ' ')
        except ValueError as e:
            print(f"   Error - Whitespace symbol: {e}")
        
        # Negative dimension
        try:
            ascii_art.draw_square(-1, '*')
        except ValueError as e:
            print(f"   Error - Negative dimension: {e}")
        
        # Invalid type
        try:
            ascii_art.draw_square("3", '*')
        except TypeError as e:
            print(f"   Error - Invalid type: {e}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
