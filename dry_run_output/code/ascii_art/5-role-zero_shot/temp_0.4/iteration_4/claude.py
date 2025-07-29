
"""
ASCII Art Generator

A high-quality console-based 2D ASCII art application that generates various shapes
using user-specified symbols. Implements ISO/IEC 25010 quality standards.

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
    
    This class provides methods to create various 2D shapes using ASCII characters,
    including squares, rectangles, parallelograms, triangles, and pyramids.
    All shapes are completely filled with the specified symbol.
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate the input symbol.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            InvalidSymbolError: If symbol is invalid (not single printable character)
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
    def _validate_dimensions(width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate the input dimensions.
        
        Args:
            width (int, optional): Width to validate
            height (int, optional): Height to validate
            
        Raises:
            InvalidDimensionError: If dimensions are invalid (negative or zero)
        """
        if width is not None:
            if not isinstance(width, int):
                raise InvalidDimensionError("Width must be an integer")
            if width <= 0:
                raise InvalidDimensionError("Width must be positive")
        
        if height is not None:
            if not isinstance(height, int):
                raise InvalidDimensionError("Height must be an integer")
            if height <= 0:
                raise InvalidDimensionError("Height must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
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
        
        # Create each row of the square
        row = symbol * width
        return '\n'.join([row] * width)
    
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
        
        # Create each row of the rectangle
        row = symbol * width
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right compared to the previous row.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        lines = []
        base_row = symbol * width
        
        # Create each row with appropriate leading spaces
        for row_index in range(height):
            leading_spaces = ' ' * row_index
            lines.append(leading_spaces + base_row)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        Each row has one more symbol than the previous row.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, 'o'))
            o
            oo
            ooo
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        lines = []
        
        # Calculate symbols per row based on width and height
        for row_index in range(height):
            # Linear interpolation to determine symbols in current row
            symbols_in_row = max(1, int((row_index + 1) * width / height))
            lines.append(symbol * symbols_in_row)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows wider towards the base.
        Each row has an odd number of symbols to maintain symmetry.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(height=height)
        
        lines = []
        
        # Calculate the width of the base (always odd for symmetry)
        base_width = 2 * height - 1
        
        for row_index in range(height):
            # Calculate symbols in current row (always odd)
            symbols_in_row = 2 * row_index + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (base_width - symbols_in_row) // 2
            
            # Create the row
            row = ' ' * leading_spaces + symbol * symbols_in_row
            lines.append(row)
        
        return '\n'.join(lines)


def main():
    """
    Main function to demonstrate the ASCII Art functionality.
    
    This function provides a simple interactive interface for testing
    the various shape drawing methods.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator")
    print("==================")
    print()
    
    try:
        # Demonstrate each shape
        print("Square (3x3, '*'):")
        print(art.draw_square(3, '*'))
        print()
        
        print("Rectangle (5x3, '#'):")
        print(art.draw_rectangle(5, 3, '#'))
        print()
        
        print("Parallelogram (4x3, '+'):")
        print(art.draw_parallelogram(4, 3, '+'))
        print()
        
        print("Triangle (5x4, 'o'):")
        print(art.draw_triangle(5, 4, 'o'))
        print()
        
        print("Pyramid (4, '^'):")
        print(art.draw_pyramid(4, '^'))
        print()
        
    except (InvalidSymbolError, InvalidDimensionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
