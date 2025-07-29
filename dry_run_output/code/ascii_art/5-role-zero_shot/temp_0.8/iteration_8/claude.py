
"""
ASCII Art Generator Module

This module provides a class for generating various ASCII art shapes including
squares, rectangles, parallelograms, triangles, and pyramids.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using ASCII
    characters. All shapes are filled with the specified symbol and returned
    as multi-line strings.
    
    Attributes:
        None
    """
    
    def __init__(self) -> None:
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the symbol parameter.
        
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
    
    def _validate_dimensions(self, width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int, optional): The width to validate
            height (int, optional): The height to validate
            
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
            symbol (str): The symbol to fill the square with (single character)
            
        Returns:
            str: A multi-line string representing the ASCII square
            
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
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(width))
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): The symbol to fill the rectangle with (single character)
            
        Returns:
            str: A multi-line string representing the ASCII rectangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that grows diagonally to the right.
        
        The parallelogram starts from the top-left corner and each subsequent
        row is shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): The symbol to fill the parallelogram with (single character)
            
        Returns:
            str: A multi-line string representing the ASCII parallelogram
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Add leading spaces for the diagonal shift
            leading_spaces = ' ' * row
            shape_line = symbol * width
            lines.append(leading_spaces + shape_line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol and
        grows by one symbol per row until it reaches the specified width.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): The symbol to fill the triangle with (single character)
            
        Returns:
            str: A multi-line string representing the ASCII triangle
            
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
        self._validate_dimensions(width=width, height=height)
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
        Draw a symmetrical pyramid.
        
        The pyramid starts with one symbol at the top and grows symmetrically
        with each row having two more symbols than the previous row, centered.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): The symbol to fill the pyramid with (single character)
            
        Returns:
            str: A multi-line string representing the ASCII pyramid
            
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
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols for this row (1, 3, 5, 7, ...)
            symbols_count = 2 * row + 1
            
            # Calculate leading spaces for centering
            leading_spaces = ' ' * (height - row - 1)
            
            # Create the line
            line = leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstrate the ASCII Art generator with example usage.
    
    This function serves as a demonstration and testing interface for the
    AsciiArt class functionality.
    """
    try:
        # Create an instance of AsciiArt
        art = AsciiArt()
        
        print("ASCII Art Generator Demo")
        print("=" * 40)
        
        # Demonstrate square
        print("\n1. Square (5x5, symbol '*'):")
        print(art.draw_square(5, '*'))
        
        # Demonstrate rectangle
        print("\n2. Rectangle (6x3, symbol '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        
        # Demonstrate parallelogram
        print("\n3. Parallelogram (4x4, symbol '+'):")
        print(art.draw_parallelogram(4, 4, '+'))
        
        # Demonstrate triangle
        print("\n4. Triangle (5x5, symbol 'o'):")
        print(art.draw_triangle(5, 5, 'o'))
        
        # Demonstrate pyramid
        print("\n5. Pyramid (height 6, symbol '^'):")
        print(art.draw_pyramid(6, '^'))
        
        # Demonstrate error handling
        print("\n6. Error handling demonstration:")
        try:
            art.draw_square(-1, '*')  # Should raise ValueError
        except ValueError as e:
            print(f"Caught expected error: {e}")
        
        try:
            art.draw_rectangle(5, 3, '  ')  # Should raise ValueError
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
