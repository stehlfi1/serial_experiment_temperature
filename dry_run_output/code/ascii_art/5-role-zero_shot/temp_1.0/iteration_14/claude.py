
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes using object-oriented programming
and follows ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

import string
from typing import Union


class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    
    This class provides methods to draw different geometric shapes using
    ASCII characters. All shapes are filled and returned as multi-line strings.
    
    The class ensures input validation and follows best practices for
    maintainability and performance.
    """
    
    # Class constants for validation
    MAX_DIMENSION = 1000  # Reasonable limit for performance
    MIN_DIMENSION = 1
    
    def __init__(self) -> None:
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_dimensions(self, width: int = None, height: int = None) -> None:
        """
        Validate dimension parameters.
        
        Args:
            width (int, optional): Width dimension to validate
            height (int, optional): Height dimension to validate
            
        Raises:
            TypeError: If dimensions are not integers
            ValueError: If dimensions are out of valid range
        """
        for dim_name, dim_value in [("width", width), ("height", height)]:
            if dim_value is not None:
                if not isinstance(dim_value, int):
                    raise TypeError(f"{dim_name} must be an integer, got {type(dim_value).__name__}")
                
                if dim_value < self.MIN_DIMENSION:
                    raise ValueError(f"{dim_name} must be at least {self.MIN_DIMENSION}, got {dim_value}")
                
                if dim_value > self.MAX_DIMENSION:
                    raise ValueError(f"{dim_name} cannot exceed {self.MAX_DIMENSION}, got {dim_value}")
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate symbol parameter.
        
        Args:
            symbol (str): Symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is invalid (wrong length, whitespace, or non-printable)
        """
        if not isinstance(symbol, str):
            raise TypeError(f"symbol must be a string, got {type(symbol).__name__}")
        
        if len(symbol) != 1:
            raise ValueError(f"symbol must be exactly one character, got {len(symbol)} characters")
        
        if symbol.isspace():
            raise ValueError("symbol cannot be a whitespace character")
        
        if symbol not in string.printable or symbol in string.whitespace:
            raise ValueError(f"symbol must be a printable non-whitespace character, got '{symbol}'")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square using the specified symbol.
        
        Args:
            width (int): Width and height of the square (must be >= 1)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters have wrong types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        # For a square, height equals width
        return self.draw_rectangle(width, width, symbol)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width (int): Width of the rectangle (must be >= 1)
            height (int): Height of the rectangle (must be >= 1)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If parameters have wrong types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        # Create each row and join with newlines
        row = symbol * width
        return '\n'.join(row for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row
        shifted by one space from the previous row.
        
        Args:
            width (int): Width of each row (must be >= 1)
            height (int): Height of the parallelogram (must be >= 1)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters have wrong types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '@'))
            @@@
             @@@
              @@@
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        row_content = symbol * width
        
        for row in range(height):
            # Add leading spaces for the diagonal shift
            leading_spaces = ' ' * row
            lines.append(leading_spaces + row_content)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        Each row has progressively more symbols.
        
        Args:
            width (int): Maximum width of the triangle base (must be >= 1)
            height (int): Height of the triangle (must be >= 1)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters have wrong types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        
        for row in range(height):
            # Calculate symbols for this row based on width and height
            symbols_in_row = min(row + 1, width)
            line = symbol * symbols_in_row
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows wider towards the base.
        Each row is centered relative to the base width.
        
        Args:
            height (int): Height of the pyramid (must be >= 1)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters have wrong types
            ValueError: If parameters have invalid values
            
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
        base_width = 2 * height - 1  # Maximum width at the base
        
        for row in range(height):
            # Calculate symbols for this row (odd numbers: 1, 3, 5, ...)
            symbols_in_row = 2 * row + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (base_width - symbols_in_row) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_in_row
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function for the AsciiArt class.
    
    This function showcases all available shapes and demonstrates
    error handling capabilities.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 50)
    
    # Demonstrate each shape
    shapes_demo = [
        ("Square (5x5)", lambda: art.draw_square(5, '*')),
        ("Rectangle (6x3)", lambda: art.draw_rectangle(6, 3, '#')),
        ("Parallelogram (4x4)", lambda: art.draw_parallelogram(4, 4, '@')),
        ("Triangle (5x4)", lambda: art.draw_triangle(5, 4, '+')),
        ("Pyramid (height=4)", lambda: art.draw_pyramid(4, '^')),
    ]
    
    for title, shape_func in shapes_demo:
        print(f"\n{title}:")
        print("-" * len(title))
        try:
            print(shape_func())
        except Exception as e:
            print(f"Error: {e}")
    
    # Demonstrate error handling
    print("\n" + "=" * 50)
    print("Error Handling Demo:")
    print("-" * 20)
    
    error_demos = [
        ("Invalid symbol (multiple chars)", lambda: art.draw_square(3, '**')),
        ("Invalid symbol (whitespace)", lambda: art.draw_square(3, ' ')),
        ("Invalid width (negative)", lambda: art.draw_square(-1, '*')),
        ("Invalid type (string width)", lambda: art.draw_square('3', '*')),
    ]
    
    for description, error_func in error_demos:
        try:
            error_func()
            print(f"{description}: No error (unexpected)")
        except Exception as e:
            print(f"{description}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
