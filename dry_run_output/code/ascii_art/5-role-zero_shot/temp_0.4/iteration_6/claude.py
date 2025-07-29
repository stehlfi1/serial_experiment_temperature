
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes using object-oriented programming
and adheres to ISO/IEC 25010 quality standards.
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using
    ASCII characters. All shapes are filled with the specified symbol.
    """
    
    def __init__(self):
        """Initialize the AsciiArt generator."""
        pass
    
    def _validate_dimensions(self, width: int, height: int = None) -> None:
        """
        Validate width and height parameters.
        
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
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the symbol parameter.
        
        Args:
            symbol (str): The symbol to use for drawing
            
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
        Draw a filled square using the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representing the ASCII square
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width)
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
            str: Multi-line string representing the ASCII rectangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_dimensions(width, height)
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
            str: Multi-line string representing the ASCII parallelogram
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(4, 3, '+'))
            ++++
             ++++
              ++++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            spaces = ' ' * row
            shape_line = symbol * width
            lines.append(spaces + shape_line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the
        top-left corner with one symbol and expanding by one symbol per row.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representing the ASCII triangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, 'o'))
            o
            oo
            ooo
            oooo
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols for this row, ensuring we don't exceed width
            symbols_count = min(row + 1, width)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        The top row has one symbol, and each subsequent row adds two symbols.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representing the ASCII pyramid
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        
        lines = []
        max_width = 2 * height - 1  # Width of the base
        
        for row in range(height):
            # Calculate symbols for this row
            symbols_count = 2 * row + 1
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration of the AsciiArt class functionality.
    
    This function showcases all available shapes with sample parameters.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 50)
    
    # Demonstrate square
    print("\n1. Square (5x5, symbol: '*'):")
    print(art.draw_square(5, '*'))
    
    # Demonstrate rectangle
    print("\n2. Rectangle (6x4, symbol: '#'):")
    print(art.draw_rectangle(6, 4, '#'))
    
    # Demonstrate parallelogram
    print("\n3. Parallelogram (5x4, symbol: '+'):")
    print(art.draw_parallelogram(5, 4, '+'))
    
    # Demonstrate triangle
    print("\n4. Right-angled Triangle (6x6, symbol: 'o'):")
    print(art.draw_triangle(6, 6, 'o'))
    
    # Demonstrate pyramid
    print("\n5. Pyramid (height: 5, symbol: '^'):")
    print(art.draw_pyramid(5, '^'))
    
    # Demonstrate error handling
    print("\n6. Error Handling Examples:")
    try:
        art.draw_square(-1, '*')
    except ValueError as e:
        print(f"ValueError caught: {e}")
    
    try:
        art.draw_rectangle(5, 3, '  ')  # Multi-character symbol
    except ValueError as e:
        print(f"ValueError caught: {e}")
    
    try:
        art.draw_triangle(3, 2, ' ')  # Whitespace symbol
    except ValueError as e:
        print(f"ValueError caught: {e}")


if __name__ == "__main__":
    main()
