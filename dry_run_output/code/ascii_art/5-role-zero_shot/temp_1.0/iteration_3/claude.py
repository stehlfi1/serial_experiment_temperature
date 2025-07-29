
"""
ASCII Art Generator

A console-based 2D ASCII art application that generates various geometric shapes
using ASCII characters. Implements ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Union


class AsciiArtError(Exception):
    """Base exception class for ASCII Art related errors."""
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
    characters, including squares, rectangles, parallelograms, triangles, and pyramids.
    """
    
    def __init__(self):
        """Initialize the AsciiArt generator."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the input symbol.
        
        Args:
            symbol (str): The symbol to validate
            
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
    
    def _validate_positive_dimension(self, value: int, name: str) -> None:
        """
        Validate that a dimension value is positive.
        
        Args:
            value (int): The value to validate
            name (str): The name of the dimension for error messages
            
        Raises:
            InvalidDimensionError: If dimension is invalid
        """
        if not isinstance(value, int):
            raise InvalidDimensionError(f"{name} must be an integer")
        
        if value <= 0:
            raise InvalidDimensionError(f"{name} must be positive (greater than 0)")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): The symbol to fill the square with (single printable character)
            
        Returns:
            str: Multi-line string representing the ASCII square
            
        Raises:
            InvalidDimensionError: If width is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_positive_dimension(width, "width")
        self._validate_symbol(symbol)
        
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
            symbol (str): The symbol to fill the rectangle with (single printable character)
            
        Returns:
            str: Multi-line string representing the ASCII rectangle
            
        Raises:
            InvalidDimensionError: If width or height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_positive_dimension(width, "width")
        self._validate_positive_dimension(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner, with each subsequent
        row shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): The symbol to fill the parallelogram with (single printable character)
            
        Returns:
            str: Multi-line string representing the ASCII parallelogram
            
        Raises:
            InvalidDimensionError: If width or height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '%'))
            %%%
             %%%
              %%%
        """
        self._validate_positive_dimension(width, "width")
        self._validate_positive_dimension(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Add leading spaces for the diagonal shift
            leading_spaces = ' ' * row
            line = leading_spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol,
        and each row adds one more symbol on the right side.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): The symbol to fill the triangle with (single printable character)
            
        Returns:
            str: Multi-line string representing the ASCII triangle
            
        Raises:
            InvalidDimensionError: If width or height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
        Note:
            The actual width used will be min(width, height) to ensure proper triangle shape.
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, '&'))
            &
            &&
            &&&
            &&&&
        """
        self._validate_positive_dimension(width, "width")
        self._validate_positive_dimension(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        # Use the minimum of width and height to ensure proper triangle shape
        actual_width = min(width, height)
        
        for row in range(height):
            # Calculate number of symbols for this row
            symbols_count = min(row + 1, actual_width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid centered on each line.
        
        The pyramid starts with one symbol at the top and grows by two symbols
        per row, maintaining symmetry around the center.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): The symbol to fill the pyramid with (single printable character)
            
        Returns:
            str: Multi-line string representing the ASCII pyramid
            
        Raises:
            InvalidDimensionError: If height is not a positive integer
            InvalidSymbolError: If symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_positive_dimension(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        
        for row in range(height):
            # Calculate number of symbols for this row (1, 3, 5, 7, ...)
            symbols_count = (2 * row) + 1
            
            # Calculate leading spaces to center the pyramid
            leading_spaces = height - row - 1
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage examples of the AsciiArt class.
    
    This function provides interactive examples of all available shapes
    and demonstrates error handling capabilities.
    """
    art = AsciiArt()
    
    print("=== ASCII Art Generator Demo ===\n")
    
    try:
        # Demonstrate square
        print("Square (5x5) with '*':")
        print(art.draw_square(5, '*'))
        print()
        
        # Demonstrate rectangle
        print("Rectangle (6x4) with '#':")
        print(art.draw_rectangle(6, 4, '#'))
        print()
        
        # Demonstrate parallelogram
        print("Parallelogram (4x3) with '%':")
        print(art.draw_parallelogram(4, 3, '%'))
        print()
        
        # Demonstrate triangle
        print("Triangle (5x5) with '&':")
        print(art.draw_triangle(5, 5, '&'))
        print()
        
        # Demonstrate pyramid
        print("Pyramid (height 6) with '^':")
        print(art.draw_pyramid(6, '^'))
        print()
        
        # Demonstrate error handling
        print("=== Error Handling Examples ===")
        
        try:
            art.draw_square(-1, '*')
        except InvalidDimensionError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_rectangle(3, 3, '  ')  # Multi-character symbol
        except InvalidSymbolError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_triangle(5, 5, ' ')  # Whitespace symbol
        except InvalidSymbolError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
