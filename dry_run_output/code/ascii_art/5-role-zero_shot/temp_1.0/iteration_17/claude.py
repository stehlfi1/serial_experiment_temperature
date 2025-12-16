
"""
ASCII Art Generator

A high-quality console-based ASCII art application that creates 2D shapes
following ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using ASCII characters.
    All shapes are completely filled with the specified symbol and returned as multi-line strings.
    
    Attributes:
        None
        
    Methods:
        draw_square: Creates a filled square
        draw_rectangle: Creates a filled rectangle
        draw_parallelogram: Creates a filled parallelogram
        draw_triangle: Creates a filled right-angled triangle
        draw_pyramid: Creates a filled symmetrical pyramid
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the drawing symbol.
        
        Args:
            symbol (str): The character to use for drawing
            
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
        Validates width and height parameters.
        
        Args:
            width (int, optional): Width dimension to validate
            height (int, optional): Height dimension to validate
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is less than or equal to 0
        """
        for dimension, name in [(width, "Width"), (height, "Height")]:
            if dimension is not None:
                if not isinstance(dimension, int):
                    raise TypeError(f"{name} must be an integer")
                if dimension <= 0:
                    raise ValueError(f"{name} must be positive (greater than 0)")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square with the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be positive)
            symbol (str): The character to fill the square with (must be single printable character)
            
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
        Draws a filled rectangle with the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): The character to fill the rectangle with (must be single printable character)
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each subsequent row is shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): The character to fill the parallelogram with (must be single printable character)
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
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
            # Add leading spaces for diagonal shift
            leading_spaces = ' ' * row
            # Add the filled row
            shape_row = symbol * width
            lines.append(leading_spaces + shape_row)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        Each row contains an increasing number of symbols.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): The character to fill the triangle with (must be single printable character)
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
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
            # Calculate symbols count for current row
            # Distribute width across height rows
            symbols_count = min(width, ((row + 1) * width + height - 1) // height)
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid with the specified symbol.
        
        The pyramid is centered and grows wider towards the base.
        Each row is centered relative to the base width.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): The character to fill the pyramid with (must be single printable character)
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If height is not an integer or symbol is not a string
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
        base_width = 2 * height - 1  # Maximum width at the base
        
        for row in range(height):
            # Calculate symbols count for current row (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row + 1
            # Calculate leading spaces for centering
            leading_spaces = (base_width - symbols_count) // 2
            # Build the row
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration function showing usage of the AsciiArt class.
    
    This function creates various ASCII art shapes and displays them
    to demonstrate the functionality of each method.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    # Demonstrate square
    print("\n1. Square (5x5) with '*':")
    try:
        square = art.draw_square(5, '*')
        print(square)
    except (TypeError, ValueError) as e:
        print(f"Error creating square: {e}")
    
    # Demonstrate rectangle
    print("\n2. Rectangle (6x4) with '#':")
    try:
        rectangle = art.draw_rectangle(6, 4, '#')
        print(rectangle)
    except (TypeError, ValueError) as e:
        print(f"Error creating rectangle: {e}")
    
    # Demonstrate parallelogram
    print("\n3. Parallelogram (4x5) with '@':")
    try:
        parallelogram = art.draw_parallelogram(4, 5, '@')
        print(parallelogram)
    except (TypeError, ValueError) as e:
        print(f"Error creating parallelogram: {e}")
    
    # Demonstrate triangle
    print("\n4. Triangle (6x6) with '+':")
    try:
        triangle = art.draw_triangle(6, 6, '+')
        print(triangle)
    except (TypeError, ValueError) as e:
        print(f"Error creating triangle: {e}")
    
    # Demonstrate pyramid
    print("\n5. Pyramid (height=6) with '^':")
    try:
        pyramid = art.draw_pyramid(6, '^')
        print(pyramid)
    except (TypeError, ValueError) as e:
        print(f"Error creating pyramid: {e}")
    
    # Demonstrate error handling
    print("\n6. Error Handling Examples:")
    try:
        art.draw_square(-1, '*')
    except ValueError as e:
        print(f"Expected error for negative width: {e}")
    
    try:
        art.draw_rectangle(5, 3, '  ')
    except ValueError as e:
        print(f"Expected error for multi-character symbol: {e}")
    
    try:
        art.draw_triangle(4, 3, ' ')
    except ValueError as e:
        print(f"Expected error for whitespace symbol: {e}")


if __name__ == "__main__":
    main()
