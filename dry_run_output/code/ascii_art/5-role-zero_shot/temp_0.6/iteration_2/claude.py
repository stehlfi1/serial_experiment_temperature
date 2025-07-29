
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes using customizable symbols.

Author: Senior Software Developer
Standard: ISO/IEC 25010 compliant
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art representations of geometric shapes.
    
    This class provides methods to draw various shapes including squares,
    rectangles, parallelograms, triangles, and pyramids using customizable
    symbols.
    
    All methods validate input parameters and return multi-line strings
    representing the ASCII art.
    """
    
    @staticmethod
    def _validate_dimensions(width: int, height: int = None) -> None:
        """
        Validate dimension parameters for shape drawing.
        
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
        Validate the symbol parameter for shape drawing.
        
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
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
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
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each row is shifted by one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '@'))
            @@@
             @@@
              @@@
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the
        top-left corner. Each row increases in width by one symbol.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, '+'))
            +
            ++
            +++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate the number of symbols for this row
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row increases in width by 2 symbols (one on each side).
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters have incorrect types
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        
        lines = []
        max_width = 2 * height - 1
        
        for row in range(height):
            # Calculate symbols for this row (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row + 1
            
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Main function demonstrating the AsciiArt class functionality.
    
    This function serves as an example of how to use the AsciiArt class
    and can be used for basic testing of the implementation.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    try:
        # Demonstrate square
        print("\nSquare (5x5, symbol '*'):")
        print(art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\nRectangle (6x3, symbol '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        
        # Demonstrate parallelogram
        print("\nParallelogram (4x4, symbol '@'):")
        print(art.draw_parallelogram(4, 4, '@'))
        
        # Demonstrate triangle
        print("\nTriangle (5x5, symbol '+'):")
        print(art.draw_triangle(5, 5, '+'))
        
        # Demonstrate pyramid
        print("\nPyramid (height 4, symbol '^'):")
        print(art.draw_pyramid(4, '^'))
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


# Example usage and testing
if __name__ == "__main__":
    # Additional examples for testing
    art_generator = AsciiArt()
    
    # Test error handling
    try:
        # This should raise a ValueError (negative width)
        art_generator.draw_square(-1, '*')
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    try:
        # This should raise a ValueError (multi-character symbol)
        art_generator.draw_square(3, 'ab')
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    try:
        # This should raise a ValueError (whitespace symbol)
        art_generator.draw_square(3, ' ')
    except ValueError as e:
        print(f"Caught expected error: {e}")
