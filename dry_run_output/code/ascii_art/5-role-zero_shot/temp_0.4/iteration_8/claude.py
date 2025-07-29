
"""
ASCII Art Generator

A console-based 2D ASCII art application that generates various geometric shapes
using user-specified symbols. Implements ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using ASCII characters.
    All shapes are completely filled with the specified symbol and returned as 
    multi-line strings.
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate the input symbol.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one printable character or is whitespace
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
        
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")
    
    @staticmethod
    def _validate_dimensions(width: Union[int, None] = None, height: Union[int, None] = None) -> None:
        """
        Validate width and height dimensions.
        
        Args:
            width (int, optional): Width to validate
            height (int, optional): Height to validate
            
        Raises:
            TypeError: If dimensions are not integers
            ValueError: If dimensions are not positive
        """
        for dimension, name in [(width, "width"), (height, "height")]:
            if dimension is not None:
                if not isinstance(dimension, int):
                    raise TypeError(f"{name.capitalize()} must be an integer")
                if dimension <= 0:
                    raise ValueError(f"{name.capitalize()} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): Single printable character to fill the square
            
        Returns:
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If width is not an integer or symbol is not a string
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
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If width/height are not integers or symbol is not a string
            ValueError: If width/height are not positive or symbol is invalid
            
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
        
        The parallelogram starts from the top-left corner, with each subsequent
        row shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If width/height are not integers or symbol is not a string
            ValueError: If width/height are not positive or symbol is invalid
            
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
            spaces = ' ' * row
            shape_line = symbol * width
            lines.append(spaces + shape_line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol,
        and each row adds one more symbol to the right.
        
        Args:
            width (int): Maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If width/height are not integers or symbol is not a string
            ValueError: If width/height are not positive or symbol is invalid
            
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
            # Calculate the number of symbols for this row
            symbols_count = min(row + 1, width)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid.
        
        The pyramid is centered with the apex at the top and grows symmetrically
        downward. Each row has an odd number of symbols.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If height is not an integer or symbol is not a string
            ValueError: If height is not positive or symbol is invalid
            
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
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates instances of various shapes and displays them
    to demonstrate the functionality of the AsciiArt class.
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
