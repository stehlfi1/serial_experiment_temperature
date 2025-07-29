
"""
ASCII Art Generator Module

This module provides a console-based 2D ASCII art generator that creates
various geometric shapes using user-specified symbols.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art representations of geometric shapes.
    
    This class provides methods to draw various shapes including squares,
    rectangles, parallelograms, triangles, and pyramids using ASCII characters.
    All shapes are filled with the specified symbol.
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single printable character.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one character or is whitespace
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
    
    @staticmethod
    def _validate_dimensions(width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate width and height dimensions.
        
        Args:
            width (int, optional): Width to validate
            height (int, optional): Height to validate
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is not positive
        """
        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer")
            if width <= 0:
                raise ValueError("Width must be positive")
        
        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer")
            if height <= 0:
                raise ValueError("Height must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If width is not an integer or symbol is not a string
            ValueError: If width is not positive, symbol is not one character,
                      or symbol is whitespace
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        # Create each row of the square
        row = symbol * width
        return '\n'.join(row for _ in range(width))
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive, symbol is not one character,
                      or symbol is whitespace
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        # Create each row of the rectangle
        row = symbol * width
        return '\n'.join(row for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner and each subsequent
        row is shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive, symbol is not one character,
                      or symbol is whitespace
                      
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
            # Add leading spaces for the diagonal effect
            spaces = ' ' * row
            shape_row = symbol * width
            lines.append(spaces + shape_row)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol and
        grows by one symbol per row until it reaches the specified width.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive, symbol is not one character,
                      or symbol is whitespace
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, '+'))
            +
            ++
            +++
            ++++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols for current row (1-based, capped at width)
            symbols_count = min(row + 1, width)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid centered on its base.
        
        The pyramid starts with one symbol at the top and grows symmetrically
        until the base has (2 * height - 1) symbols.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If height is not an integer or symbol is not a string
            ValueError: If height is not positive, symbol is not one character,
                      or symbol is whitespace
                      
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)
        
        lines = []
        max_width = 2 * height - 1
        
        for row in range(height):
            # Calculate symbols for current row (odd numbers: 1, 3, 5, ...)
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
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 50)
    
    try:
        # Demonstrate each shape
        print("\n1. Square (5x5, symbol: '*'):")
        print(art.draw_square(5, '*'))
        
        print("\n2. Rectangle (6x3, symbol: '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        
        print("\n3. Parallelogram (4x4, symbol: '@'):")
        print(art.draw_parallelogram(4, 4, '@'))
        
        print("\n4. Triangle (5x5, symbol: '+'):")
        print(art.draw_triangle(5, 5, '+'))
        
        print("\n5. Pyramid (height: 6, symbol: '^'):")
        print(art.draw_pyramid(6, '^'))
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
