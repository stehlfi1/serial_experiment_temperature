
"""
ASCII Art Generator Module

This module provides functionality to generate various ASCII art shapes including
squares, rectangles, parallelograms, triangles, and pyramids.

Author: Senior Software Developer
Standards: ISO/IEC 25010 compliant
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
    
    This class provides methods to create various geometric shapes using ASCII
    characters. All shapes are filled with the specified symbol and returned
    as multi-line strings.
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single printable character.
        
        Args:
            symbol: The character to validate
            
        Raises:
            InvalidSymbolError: If symbol is invalid
        """
        if not isinstance(symbol, str):
            raise InvalidSymbolError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise InvalidSymbolError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise InvalidSymbolError("Symbol cannot be a whitespace character")
        
        if not symbol.isprintable():
            raise InvalidSymbolError("Symbol must be a printable character")
    
    @staticmethod
    def _validate_dimensions(**kwargs) -> None:
        """
        Validate dimension parameters.
        
        Args:
            **kwargs: Dimension parameters (width, height) to validate
            
        Raises:
            InvalidDimensionError: If any dimension is invalid
        """
        for param_name, value in kwargs.items():
            if not isinstance(value, int):
                raise InvalidDimensionError(f"{param_name} must be an integer")
            
            if value <= 0:
                raise InvalidDimensionError(f"{param_name} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width: The width and height of the square (must be positive)
            symbol: The character to fill the square with
            
        Returns:
            Multi-line string representing the square
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width)
        
        return '\n'.join(symbol * width for _ in range(width))
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width: The width of the rectangle (must be positive)
            height: The height of the rectangle (must be positive)
            symbol: The character to fill the rectangle with
            
        Returns:
            Multi-line string representing the rectangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each subsequent row is shifted one space to the right.
        
        Args:
            width: The width of each row (must be positive)
            height: The height of the parallelogram (must be positive)
            symbol: The character to fill the parallelogram with
            
        Returns:
            Multi-line string representing the parallelogram
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '@'))
            @@@
             @@@
              @@@
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left
        corner. Each row has one more symbol than the previous row.
        
        Args:
            width: The maximum width of the triangle base (must be positive)
            height: The height of the triangle (must be positive)
            symbol: The character to fill the triangle with
            
        Returns:
            Multi-line string representing the triangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, '+'))
            +
            ++
            +++
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        lines = []
        for row in range(height):
            # Calculate symbols for this row, ensuring we don't exceed width
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row has two more symbols than the previous row.
        
        Args:
            height: The height of the pyramid (must be positive)
            symbol: The character to fill the pyramid with
            
        Returns:
            Multi-line string representing the pyramid
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(height=height)
        
        lines = []
        max_width = 2 * height - 1
        
        for row in range(height):
            # Calculate symbols for this row (1, 3, 5, 7, ...)
            symbols_count = 2 * row + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    """
    try:
        art = AsciiArt()
        
        print("=== ASCII Art Generator Demo ===\n")
        
        # Demonstrate square
        print("Square (5x5 with '*'):")
        print(art.draw_square(5, '*'))
        print()
        
        # Demonstrate rectangle
        print("Rectangle (6x3 with '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        print()
        
        # Demonstrate parallelogram
        print("Parallelogram (4x4 with '@'):")
        print(art.draw_parallelogram(4, 4, '@'))
        print()
        
        # Demonstrate triangle
        print("Triangle (5x5 with '+'):")
        print(art.draw_triangle(5, 5, '+'))
        print()
        
        # Demonstrate pyramid
        print("Pyramid (height 5 with '^'):")
        print(art.draw_pyramid(5, '^'))
        print()
        
        # Demonstrate error handling
        print("=== Error Handling Demo ===")
        try:
            art.draw_square(-1, '*')
        except InvalidDimensionError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_rectangle(5, 3, '  ')  # Multi-character symbol
        except InvalidSymbolError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_triangle(3, 2, ' ')  # Whitespace symbol
        except InvalidSymbolError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
