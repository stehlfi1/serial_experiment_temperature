
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes with customizable symbols.

Author: Senior Software Developer
Standard: ISO/IEC 25010 compliant
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using
    ASCII characters. All shapes are filled with the specified symbol.
    """
    
    @staticmethod
    def _validate_dimensions(width: int, height: int = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int): The width dimension
            height (int, optional): The height dimension
            
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
        Validate the symbol parameter.
        
        Args:
            symbol (str): The character to use for drawing
            
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
            str: Multi-line string representation of the square
            
        Raises:
            TypeError: If parameters are of incorrect type
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
        
        # Create each row of the square
        row = symbol * width
        return '\n'.join(row for _ in range(width))
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be positive)
            height (int): The height of the rectangle (must be positive)
            symbol (str): Single printable character to fill the rectangle
            
        Returns:
            str: Multi-line string representation of the rectangle
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        # Create each row of the rectangle
        row = symbol * width
        return '\n'.join(row for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the 
        top-left corner. Each subsequent row is shifted one space to the right.
        
        Args:
            width (int): The width of each row (must be positive)
            height (int): The height of the parallelogram (must be positive)
            symbol (str): Single printable character to fill the parallelogram
            
        Returns:
            str: Multi-line string representation of the parallelogram
            
        Raises:
            TypeError: If parameters are of incorrect type
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
            # Add leading spaces for the diagonal shift
            spaces = ' ' * row
            # Add the symbols for this row
            symbols = symbol * width
            lines.append(spaces + symbols)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left
        corner. Each row has an increasing number of symbols.
        
        Args:
            width (int): The maximum width of the triangle base (must be positive)
            height (int): The height of the triangle (must be positive)
            symbol (str): Single printable character to fill the triangle
            
        Returns:
            str: Multi-line string representation of the triangle
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters have invalid values
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, '+'))
            +
            ++
            +++
            ++++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate number of symbols for this row
            # Distribute symbols evenly across the height
            symbols_count = min(((row + 1) * width) // height, width)
            if symbols_count == 0:
                symbols_count = 1
            
            lines.append(symbol * symbols_count)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row has an increasing odd number of symbols.
        
        Args:
            height (int): The height of the pyramid (must be positive)
            symbol (str): Single printable character to fill the pyramid
            
        Returns:
            str: Multi-line string representation of the pyramid
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If parameters have invalid values
            
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
        for row in range(height):
            # Calculate number of symbols for this row (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row + 1
            
            # Calculate leading spaces for centering
            leading_spaces = height - row - 1
            
            # Create the row
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Main function to demonstrate the ASCII art functionality.
    
    This function provides a simple console interface for users to
    interact with the ASCII art generator.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator")
    print("=" * 30)
    
    # Demonstration of all shapes
    try:
        print("\nSquare (3x3, '*'):")
        print(art.draw_square(3, '*'))
        
        print("\nRectangle (5x3, '#'):")
        print(art.draw_rectangle(5, 3, '#'))
        
        print("\nParallelogram (4x3, '@'):")
        print(art.draw_parallelogram(4, 3, '@'))
        
        print("\nTriangle (5x4, '+'):")
        print(art.draw_triangle(5, 4, '+'))
        
        print("\nPyramid (5, '^'):")
        print(art.draw_pyramid(5, '^'))
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


# Unit tests for verification
def test_ascii_art():
    """
    Basic test suite for the AsciiArt class.
    
    This function contains basic tests to verify the correctness
    of the ASCII art generation methods.
    """
    art = AsciiArt()
    
    # Test square
    assert art.draw_square(2, 'X') == "XX\nXX"
    
    # Test rectangle
    assert art.draw_rectangle(3, 2, 'O') == "OOO\nOOO"
    
    # Test parallelogram
    expected_parallelogram = "AA\n AA\n  AA"
    assert art.draw_parallelogram(2, 3, 'A') == expected_parallelogram
    
    # Test triangle
    expected_triangle = "B\nBB"
    assert art.draw_triangle(2, 2, 'B') == expected_triangle
    
    # Test pyramid
    expected_pyramid = " C\nCCC"
    assert art.draw_pyramid(2, 'C') == expected_pyramid
    
    # Test validation errors
    try:
        art.draw_square(-1, 'X')
        assert False, "Should raise ValueError for negative width"
    except ValueError:
        pass
    
    try:
        art.draw_square(3, '  ')
        assert False, "Should raise ValueError for multi-character symbol"
    except ValueError:
        pass
    
    try:
        art.draw_square(3, ' ')
        assert False, "Should raise ValueError for whitespace symbol"
    except ValueError:
        pass
    
    print("All tests passed!")


# Uncomment the line below to run tests
# test_ascii_art()
