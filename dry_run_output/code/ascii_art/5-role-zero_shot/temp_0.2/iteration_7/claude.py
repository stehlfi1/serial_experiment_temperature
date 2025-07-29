
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
    A class for generating ASCII art representations of geometric shapes.
    
    This class provides methods to draw various shapes including squares,
    rectangles, parallelograms, triangles, and pyramids using ASCII characters.
    All methods include input validation and return formatted string representations.
    """
    
    def __init__(self) -> None:
        """Initialize the AsciiArt generator."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
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
    
    def _validate_dimensions(self, width: Union[int, None] = None, 
                           height: Union[int, None] = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int, optional): Width to validate
            height (int, optional): Height to validate
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is negative or zero
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
            symbol (str): Single character to fill the square with
            
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
            symbol (str): Single character to fill the rectangle with
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
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
            lines.append(symbol * width)
        
        return '\n'.join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that grows diagonally to the right.
        
        Each row is shifted one space to the right compared to the previous row,
        starting from the top-left corner.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single character to fill the parallelogram with
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
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
            spaces = ' ' * row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol and
        increases by one symbol per row until it reaches the specified width.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single character to fill the triangle with
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If width/height is not an integer or symbol is not a string
            ValueError: If width/height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, 'o'))
            o
            oo
            ooo
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols per row, ensuring we don't exceed width
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid centered on each line.
        
        The pyramid starts with one symbol at the top and increases by two
        symbols per row, maintaining center alignment.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single character to fill the pyramid with
            
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
        max_width = 2 * height - 1  # Width of the base
        
        for row in range(height):
            symbols_count = 2 * row + 1  # Odd numbers: 1, 3, 5, ...
            spaces_count = (max_width - symbols_count) // 2
            
            line = ' ' * spaces_count + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main() -> None:
    """
    Main function to demonstrate the ASCII art generator.
    
    This function provides a simple interactive interface for users to
    generate different ASCII art shapes.
    """
    art_generator = AsciiArt()
    
    print("ASCII Art Generator")
    print("=" * 20)
    
    try:
        # Demonstrate each shape
        print("\n1. Square (5x5, '*'):")
        print(art_generator.draw_square(5, '*'))
        
        print("\n2. Rectangle (6x3, '#'):")
        print(art_generator.draw_rectangle(6, 3, '#'))
        
        print("\n3. Parallelogram (4x4, '+'):")
        print(art_generator.draw_parallelogram(4, 4, '+'))
        
        print("\n4. Triangle (5x5, 'o'):")
        print(art_generator.draw_triangle(5, 5, 'o'))
        
        print("\n5. Pyramid (height=4, '^'):")
        print(art_generator.draw_pyramid(4, '^'))
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


# Unit Tests
def test_ascii_art():
    """
    Comprehensive test suite for the AsciiArt class.
    
    Tests all methods with various inputs including edge cases and
    error conditions to ensure robustness and correctness.
    """
    art = AsciiArt()
    
    # Test square
    assert art.draw_square(1, 'X') == 'X'
    assert art.draw_square(2, 'A') == 'AA\nAA'
    
    # Test rectangle
    assert art.draw_rectangle(3, 2, 'B') == 'BBB\nBBB'
    assert art.draw_rectangle(1, 1, 'C') == 'C'
    
    # Test parallelogram
    assert art.draw_parallelogram(2, 2, 'D') == 'DD\n DD'
    
    # Test triangle
    assert art.draw_triangle(3, 3, 'E') == 'E\nEE\nEEE'
    
    # Test pyramid
    assert art.draw_pyramid(2, 'F') == ' F\nFFF'
    
    # Test error conditions
    try:
        art.draw_square(-1, 'X')
        assert False, "Should raise ValueError for negative width"
    except ValueError:
        pass
    
    try:
        art.draw_square(5, '  ')
        assert False, "Should raise ValueError for multi-character symbol"
    except ValueError:
        pass
    
    try:
        art.draw_square(5, ' ')
        assert False, "Should raise ValueError for whitespace symbol"
    except ValueError:
        pass
    
    print("All tests passed!")


# Uncomment the line below to run tests
# test_ascii_art()
