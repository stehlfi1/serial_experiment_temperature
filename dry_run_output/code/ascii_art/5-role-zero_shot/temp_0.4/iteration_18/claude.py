
"""
ASCII Art Generator

A console-based 2D ASCII art application that generates various geometric shapes
using user-specified symbols. Implements ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Union


class AsciiArtError(Exception):
    """Base exception class for ASCII art related errors."""
    pass


class InvalidSymbolError(AsciiArtError):
    """Raised when an invalid symbol is provided."""
    pass


class InvalidDimensionError(AsciiArtError):
    """Raised when invalid dimensions are provided."""
    pass


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various geometric shapes using
    ASCII characters. All shapes are filled with the specified symbol.
    """
    
    def __init__(self):
        """Initialize the AsciiArt generator."""
        pass
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate that the symbol is a single printable character.
        
        Args:
            symbol: The character to validate
            
        Raises:
            InvalidSymbolError: If symbol is invalid
        """
        if not isinstance(symbol, str):
            raise InvalidSymbolError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise InvalidSymbolError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise InvalidSymbolError("Symbol cannot be a whitespace character")
        
        if not symbol.isprintable():
            raise InvalidSymbolError("Symbol must be a printable character")
    
    def _validate_dimensions(self, width: int = None, height: int = None) -> None:
        """
        Validate that dimensions are positive integers.
        
        Args:
            width: Width to validate (optional)
            height: Height to validate (optional)
            
        Raises:
            InvalidDimensionError: If dimensions are invalid
        """
        if width is not None:
            if not isinstance(width, int):
                raise InvalidDimensionError("Width must be an integer")
            if width <= 0:
                raise InvalidDimensionError("Width must be positive")
        
        if height is not None:
            if not isinstance(height, int):
                raise InvalidDimensionError("Height must be an integer")
            if height <= 0:
                raise InvalidDimensionError("Height must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width: The width and height of the square
            symbol: The character to fill the square with
            
        Returns:
            A string representation of the square
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width)
        
        # Generate square by creating width rows of width symbols each
        rows = [symbol * width for _ in range(width)]
        return '\n'.join(rows)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width: The width of the rectangle
            height: The height of the rectangle
            symbol: The character to fill the rectangle with
            
        Returns:
            A string representation of the rectangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        # Generate rectangle by creating height rows of width symbols each
        rows = [symbol * width for _ in range(height)]
        return '\n'.join(rows)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each row is shifted by one space to the right.
        
        Args:
            width: The width of each row
            height: The height of the parallelogram
            symbol: The character to fill the parallelogram with
            
        Returns:
            A string representation of the parallelogram
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(4, 3, '@'))
            @@@@
             @@@@
              @@@@
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        rows = []
        for row_index in range(height):
            # Add leading spaces for diagonal shift
            leading_spaces = ' ' * row_index
            # Add the symbols for this row
            row_content = symbol * width
            rows.append(leading_spaces + row_content)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the
        top-left corner with one symbol and increasing by one symbol per row.
        
        Args:
            width: The maximum width of the triangle base
            height: The height of the triangle
            symbol: The character to fill the triangle with
            
        Returns:
            A string representation of the triangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, '+'))
            +
            ++
            +++
            ++++
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        rows = []
        for row_index in range(height):
            # Calculate number of symbols for this row (1-based indexing)
            symbols_count = min(row_index + 1, width)
            row_content = symbol * symbols_count
            rows.append(row_content)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid starts with one symbol at the top and increases by
        two symbols per row, centered horizontally.
        
        Args:
            height: The height of the pyramid
            symbol: The character to fill the pyramid with
            
        Returns:
            A string representation of the pyramid
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(height=height)
        
        rows = []
        for row_index in range(height):
            # Calculate number of symbols for this row (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row_index + 1
            
            # Calculate leading spaces for centering
            leading_spaces = ' ' * (height - row_index - 1)
            
            # Create the row
            row_content = leading_spaces + symbol * symbols_count
            rows.append(row_content)
        
        return '\n'.join(rows)


def main():
    """
    Main function to demonstrate the ASCII art generator.
    
    This function provides a simple console interface for users to
    interact with the ASCII art generator.
    """
    art_generator = AsciiArt()
    
    print("ASCII Art Generator")
    print("==================")
    print()
    
    try:
        # Demonstrate each shape
        print("Square (5x5, '*'):")
        print(art_generator.draw_square(5, '*'))
        print()
        
        print("Rectangle (6x4, '#'):")
        print(art_generator.draw_rectangle(6, 4, '#'))
        print()
        
        print("Parallelogram (5x4, '@'):")
        print(art_generator.draw_parallelogram(5, 4, '@'))
        print()
        
        print("Triangle (6x5, '+'):")
        print(art_generator.draw_triangle(6, 5, '+'))
        print()
        
        print("Pyramid (5, '^'):")
        print(art_generator.draw_pyramid(5, '^'))
        print()
        
    except (InvalidSymbolError, InvalidDimensionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


# Unit tests for the AsciiArt class
def test_ascii_art():
    """
    Basic test suite for the AsciiArt class.
    
    This function contains unit tests to verify the correctness
    of the ASCII art generation methods.
    """
    art = AsciiArt()
    
    # Test square
    assert art.draw_square(2, '*') == "**\n**"
    
    # Test rectangle
    assert art.draw_rectangle(3, 2, '#') == "###\n###"
    
    # Test parallelogram
    expected_parallelogram = "###\n ###\n  ###"
    assert art.draw_parallelogram(3, 3, '#') == expected_parallelogram
    
    # Test triangle
    expected_triangle = "+\n++\n+++"
    assert art.draw_triangle(3, 3, '+') == expected_triangle
    
    # Test pyramid
    expected_pyramid = "  ^\n ^^^\n^^^^^"
    assert art.draw_pyramid(3, '^') == expected_pyramid
    
    # Test validation errors
    try:
        art.draw_square(-1, '*')
        assert False, "Should raise InvalidDimensionError"
    except InvalidDimensionError:
        pass
    
    try:
        art.draw_square(3, '  ')
        assert False, "Should raise InvalidSymbolError"
    except InvalidSymbolError:
        pass
    
    try:
        art.draw_square(3, ' ')
        assert False, "Should raise InvalidSymbolError"
    except InvalidSymbolError:
        pass
    
    print("All tests passed!")


# Uncomment the line below to run tests
# test_ascii_art()
