
"""
ASCII Art Generator

A console-based 2D ASCII art application that generates various geometric shapes
using user-specified symbols. Implements ISO/IEC 25010 quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Union


class AsciiArtError(Exception):
    """Base exception class for ASCII Art related errors."""
    pass


class InvalidSymbolError(AsciiArtError):
    """Raised when an invalid symbol is provided."""
    pass


class InvalidDimensionError(AsciiArtError):
    """Raised when invalid dimensions are provided."""
    pass


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    
    This class provides methods to draw various geometric shapes using ASCII
    characters. All shapes are filled with the specified symbol and returned
    as multi-line strings.
    """
    
    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate the input symbol.
        
        Args:
            symbol: The symbol to validate
            
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
    
    @staticmethod
    def _validate_dimensions(width: int = None, height: int = None) -> None:
        """
        Validate dimension parameters.
        
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
            A multi-line string representing the square
            
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
        
        return self.draw_rectangle(width, width, symbol)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width: The width of the rectangle
            height: The height of the rectangle
            symbol: The character to fill the rectangle with
            
        Returns:
            A multi-line string representing the rectangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        # Generate each row of the rectangle
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
            A multi-line string representing the parallelogram
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        rows = []
        for row_index in range(height):
            # Add leading spaces for the diagonal shift
            leading_spaces = ' ' * row_index
            row_content = symbol * width
            rows.append(leading_spaces + row_content)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the 
        top-left corner with one symbol and expanding by one symbol per row.
        
        Args:
            width: The maximum width of the triangle base
            height: The height of the triangle
            symbol: The character to fill the triangle with
            
        Returns:
            A multi-line string representing the triangle
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            InvalidDimensionError: If width or height is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, 'o'))
            o
            oo
            ooo
            oooo
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width=width, height=height)
        
        rows = []
        for row_index in range(height):
            # Calculate symbols per row (1-indexed, up to width)
            symbols_in_row = min(row_index + 1, width)
            rows.append(symbol * symbols_in_row)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid starts with one symbol at the top and expands symmetrically,
        adding two symbols per row (one on each side).
        
        Args:
            height: The height of the pyramid
            symbol: The character to fill the pyramid with
            
        Returns:
            A multi-line string representing the pyramid
            
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
            # Calculate symbols in current row (1, 3, 5, 7, ...)
            symbols_in_row = 2 * row_index + 1
            
            # Calculate leading spaces for centering
            leading_spaces = ' ' * (height - row_index - 1)
            
            row_content = symbol * symbols_in_row
            rows.append(leading_spaces + row_content)
        
        return '\n'.join(rows)


def main():
    """
    Main function demonstrating the ASCII Art generator functionality.
    
    This function provides a simple console interface for users to interact
    with the ASCII Art generator and test various shapes.
    """
    art_generator = AsciiArt()
    
    print("ASCII Art Generator")
    print("=" * 50)
    
    try:
        # Demonstrate all shapes with different symbols
        print("Square (5x5) with '*':")
        print(art_generator.draw_square(5, '*'))
        print()
        
        print("Rectangle (6x3) with '#':")
        print(art_generator.draw_rectangle(6, 3, '#'))
        print()
        
        print("Parallelogram (4x4) with '+':")
        print(art_generator.draw_parallelogram(4, 4, '+'))
        print()
        
        print("Triangle (5x5) with 'o':")
        print(art_generator.draw_triangle(5, 5, 'o'))
        print()
        
        print("Pyramid (height 6) with '^':")
        print(art_generator.draw_pyramid(6, '^'))
        print()
        
    except (InvalidSymbolError, InvalidDimensionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


# Unit tests for comprehensive testing
def test_ascii_art():
    """
    Comprehensive test suite for the AsciiArt class.
    
    Tests all functionality including edge cases and error conditions
    to ensure code correctness and reliability.
    """
    art = AsciiArt()
    
    # Test valid inputs
    assert art.draw_square(2, '*') == "**\n**"
    assert art.draw_rectangle(3, 2, '#') == "###\n###"
    assert art.draw_parallelogram(2, 2, '+') == "++\n ++"
    assert art.draw_triangle(3, 3, 'o') == "o\noo\nooo"
    assert art.draw_pyramid(3, '^') == "  ^\n ^^^\n^^^^^"
    
    # Test error conditions
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
        art.draw_square(3, '')
        assert False, "Should raise InvalidSymbolError"
    except InvalidSymbolError:
        pass
    
    print("All tests passed!")


# Uncomment the line below to run tests
# test_ascii_art()
