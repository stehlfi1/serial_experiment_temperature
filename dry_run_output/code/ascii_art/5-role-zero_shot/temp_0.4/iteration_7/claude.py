
"""
ASCII Art Generator

A high-quality Python application for generating 2D ASCII art shapes.
Implements geometric shapes using object-oriented programming principles
and adheres to ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art representations of geometric shapes.
    
    This class provides methods to create various 2D shapes using ASCII characters,
    including squares, rectangles, parallelograms, triangles, and pyramids.
    All methods include comprehensive input validation and error handling.
    """
    
    # Class constants for validation
    MIN_DIMENSION = 1
    MAX_DIMENSION = 1000  # Reasonable upper limit to prevent memory issues
    
    def __init__(self) -> None:
        """Initialize the AsciiArt generator."""
        pass
    
    def _validate_dimensions(self, width: int = None, height: int = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int, optional): Width dimension to validate
            height (int, optional): Height dimension to validate
            
        Raises:
            TypeError: If dimensions are not integers
            ValueError: If dimensions are out of valid range
        """
        dimensions = {}
        if width is not None:
            dimensions['width'] = width
        if height is not None:
            dimensions['height'] = height
            
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
            if value < self.MIN_DIMENSION:
                raise ValueError(f"{name} must be at least {self.MIN_DIMENSION}, got {value}")
            if value > self.MAX_DIMENSION:
                raise ValueError(f"{name} must not exceed {self.MAX_DIMENSION}, got {value}")
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the drawing symbol parameter.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is invalid (empty, whitespace, or multi-character)
        """
        if not isinstance(symbol, str):
            raise TypeError(f"symbol must be a string, got {type(symbol).__name__}")
        
        if len(symbol) == 0:
            raise ValueError("symbol cannot be empty")
        
        if len(symbol) > 1:
            raise ValueError(f"symbol must be exactly one character, got {len(symbol)} characters")
        
        if symbol.isspace():
            raise ValueError("symbol cannot be whitespace")
    
    def _create_line(self, length: int, symbol: str, leading_spaces: int = 0) -> str:
        """
        Create a single line of ASCII art with optional leading spaces.
        
        Args:
            length (int): Length of the line in characters
            symbol (str): Symbol to use for drawing
            leading_spaces (int): Number of leading spaces
            
        Returns:
            str: A line of ASCII art
        """
        return ' ' * leading_spaces + symbol * length
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square using the specified symbol.
        
        Args:
            width (int): Width and height of the square (1-1000)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters are out of valid range
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(width):
            lines.append(self._create_line(width, symbol))
        
        return '\n'.join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width (int): Width of the rectangle (1-1000)
            height (int): Height of the rectangle (1-1000)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters are out of valid range
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for _ in range(height):
            lines.append(self._create_line(width, symbol))
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each subsequent row is shifted one space to the right.
        
        Args:
            width (int): Width of each row (1-1000)
            height (int): Height of the parallelogram (1-1000)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters are out of valid range
            
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
        for row in range(height):
            lines.append(self._create_line(width, symbol, leading_spaces=row))
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        Each row increases in width by one character.
        
        Args:
            width (int): Maximum width of the triangle base (1-1000)
            height (int): Height of the triangle (1-1000)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters are out of valid range
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate the width for this row, ensuring it doesn't exceed max width
            current_width = min(row + 1, width)
            lines.append(self._create_line(current_width, symbol))
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row increases in width by 2 characters (one on each side).
        
        Args:
            height (int): Height of the pyramid (1-1000)
            symbol (str): Single printable character to use for drawing
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters are out of valid range
            
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
        max_width = 2 * height - 1  # Width of the base
        
        for row in range(height):
            current_width = 2 * row + 1  # Odd numbers: 1, 3, 5, ...
            leading_spaces = (max_width - current_width) // 2
            lines.append(self._create_line(current_width, symbol, leading_spaces))
        
        return '\n'.join(lines)


def main() -> None:
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function provides examples of all available shapes and demonstrates
    proper error handling for invalid inputs.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    try:
        # Demonstrate each shape
        shapes_demo = [
            ("Square (5x5)", lambda: art.draw_square(5, '*')),
            ("Rectangle (6x3)", lambda: art.draw_rectangle(6, 3, '#')),
            ("Parallelogram (4x3)", lambda: art.draw_parallelogram(4, 3, '@')),
            ("Triangle (5x4)", lambda: art.draw_triangle(5, 4, '+')),
            ("Pyramid (height 4)", lambda: art.draw_pyramid(4, '^')),
        ]
        
        for description, shape_func in shapes_demo:
            print(f"\n{description}:")
            print(shape_func())
        
        # Demonstrate error handling
        print("\n" + "=" * 40)
        print("Error Handling Examples:")
        
        error_examples = [
            ("Invalid symbol (empty)", lambda: art.draw_square(3, '')),
            ("Invalid symbol (whitespace)", lambda: art.draw_square(3, ' ')),
            ("Invalid symbol (multiple chars)", lambda: art.draw_square(3, '**')),
            ("Invalid width (negative)", lambda: art.draw_square(-1, '*')),
            ("Invalid width (zero)", lambda: art.draw_square(0, '*')),
        ]
        
        for description, error_func in error_examples:
            try:
                error_func()
            except (ValueError, TypeError) as e:
                print(f"\n{description}: {type(e).__name__}: {e}")
                
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
