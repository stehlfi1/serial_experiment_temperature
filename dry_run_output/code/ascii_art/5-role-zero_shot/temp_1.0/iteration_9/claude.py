
"""
ASCII Art Generator Module

A comprehensive module for generating various ASCII art shapes including squares,
rectangles, parallelograms, triangles, and pyramids. Implements ISO/IEC 25010
standards for software quality.
"""

from typing import Union


class AsciiArtError(Exception):
    """Base exception class for ASCII art related errors."""
    pass


class InvalidSymbolError(AsciiArtError):
    """Raised when an invalid symbol is provided."""
    pass


class InvalidDimensionError(AsciiArtError):
    """Raised when invalid dimensions are provided."""
    pass


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art patterns including
    squares, rectangles, parallelograms, triangles, and pyramids using a 
    specified symbol.
    
    All methods validate inputs and return multi-line strings representing
    the requested ASCII art shapes.
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the provided symbol is acceptable for ASCII art.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            InvalidSymbolError: If symbol is invalid (not single char, whitespace, etc.)
        """
        if not isinstance(symbol, str):
            raise InvalidSymbolError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise InvalidSymbolError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise InvalidSymbolError("Symbol cannot be whitespace")
        
        if not symbol.isprintable():
            raise InvalidSymbolError("Symbol must be printable")
    
    @staticmethod
    def _validate_dimension(dimension: int, name: str) -> None:
        """
        Validates that a dimension is positive.
        
        Args:
            dimension (int): The dimension value to validate
            name (str): The name of the dimension for error messages
            
        Raises:
            InvalidDimensionError: If dimension is not a positive integer
        """
        if not isinstance(dimension, int):
            raise InvalidDimensionError(f"{name} must be an integer")
        
        if dimension <= 0:
            raise InvalidDimensionError(f"{name} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square using the specified symbol.
        
        Args:
            width (int): Width and height of the square (must be positive)
            symbol (str): Single printable character to draw with
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            InvalidDimensionError: If width is not positive
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(width))
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle using the specified symbol.
        
        Args:
            width (int): Width of the rectangle (must be positive)
            height (int): Height of the rectangle (must be positive)
            symbol (str): Single printable character to draw with
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            InvalidDimensionError: If width or height is not positive
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram using the specified symbol.
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right.
        
        Args:
            width (int): Width of the parallelogram base (must be positive)
            height (int): Height of the parallelogram (must be positive)
            symbol (str): Single printable character to draw with
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            InvalidDimensionError: If width or height is not positive
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(4, 3, '@'))
            @@@@
             @@@@
              @@@@
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            leading_spaces = ' ' * row
            shape_line = symbol * width
            lines.append(leading_spaces + shape_line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle using the specified symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): Maximum width of the triangle (must be positive)
            height (int): Height of the triangle (must be positive)
            symbol (str): Single printable character to draw with
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            InvalidDimensionError: If width or height is not positive
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate the number of symbols for this row
            # Ensure we don't exceed the specified width
            symbols_count = min(row + 1, width)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid using the specified symbol.
        The pyramid is centered and grows wider towards the base.
        
        Args:
            height (int): Height of the pyramid (must be positive)
            symbol (str): Single printable character to draw with
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            InvalidDimensionError: If height is not positive
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate number of symbols for this row (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row + 1
            
            # Calculate leading spaces to center the pyramid
            leading_spaces = ' ' * (height - row - 1)
            
            # Create the line
            line = leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    """
    try:
        art = AsciiArt()
        
        print("ASCII Art Generator Demo")
        print("=" * 30)
        
        print("\n1. Square (5x5) with '*':")
        print(art.draw_square(5, '*'))
        
        print("\n2. Rectangle (6x3) with '#':")
        print(art.draw_rectangle(6, 3, '#'))
        
        print("\n3. Parallelogram (5x4) with '@':")
        print(art.draw_parallelogram(5, 4, '@'))
        
        print("\n4. Triangle (6x4) with '+':")
        print(art.draw_triangle(6, 4, '+'))
        
        print("\n5. Pyramid (height 5) with '^':")
        print(art.draw_pyramid(5, '^'))
        
    except (InvalidSymbolError, InvalidDimensionError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
