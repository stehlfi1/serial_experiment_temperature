
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class with methods to draw various
geometric shapes using ASCII characters, adhering to high-quality code
standards as defined by ISO/IEC 25010.
"""

import math
from typing import Final

# --- Constants for clear error messages ---
ERROR_SYMBOL_TYPE: Final[str] = "Symbol must be a string."
ERROR_SYMBOL_LENGTH: Final[str] = "Symbol must be a single character."
ERROR_SYMBOL_WHITESPACE: Final[str] = "Symbol cannot be a whitespace character."
ERROR_DIMENSION_TYPE: Final[str] = "{name} must be an integer."
ERROR_DIMENSION_VALUE: Final[str] = "{name} must be a positive integer greater than 0."


class AsciiArt:
    """
    A collection of static methods for drawing 2D ASCII art shapes.

    This class provides a clean, object-oriented interface for generating
    console-based ASCII art. Each method is self-contained, validates its
    inputs, and returns a multi-line string representation of the requested shape.
    The methods are implemented as static methods as they do not depend on
    the state of a class instance, making them efficient and easy to use directly.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the symbol used for drawing. (Safety, Reliability)

        Args:
            symbol: The character to be used for drawing.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single character or is a whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError(ERROR_SYMBOL_TYPE)
        if len(symbol) != 1:
            raise ValueError(ERROR_SYMBOL_LENGTH)
        if symbol.isspace():
            raise ValueError(ERROR_SYMBOL_WHITESPACE)

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates a dimension (width or height). (Safety, Reliability)

        Args:
            value: The integer value of the dimension.
            name: The name of the dimension (e.g., 'width', 'height') for error messages.

        Raises:
            TypeError: If the dimension is not an integer.
            ValueError: If the dimension is not a positive integer (> 0).
        """
        if not isinstance(value, int):
            raise TypeError(ERROR_DIMENSION_TYPE.format(name=name.capitalize()))
        if value <= 0:
            raise ValueError(ERROR_DIMENSION_VALUE.format(name=name.capitalize()))

    @staticmethod
    def draw_square(width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the ASCII square.
        
        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive, or if symbol is invalid.
        """
        AsciiArt._validate_dimension(width, 'width')
        AsciiArt._validate_symbol(symbol)
        
        # A square is a rectangle with equal width and height.
        return AsciiArt.draw_rectangle(width=width, height=width, symbol=symbol)

    @staticmethod
    def draw_rectangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive, or if symbol is invalid.
        """
        AsciiArt._validate_dimension(width, 'width')
        AsciiArt._validate_dimension(height, 'height')
        AsciiArt._validate_symbol(symbol)

        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    @staticmethod
    def draw_parallelogram(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right relative to the one above it.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the ASCII parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive, or if symbol is invalid.
        """
        AsciiArt._validate_dimension(width, 'width')
        AsciiArt._validate_dimension(height, 'height')
        AsciiArt._validate_symbol(symbol)

        rows = []
        base_row = symbol * width
        for i in range(height):
            padding = ' ' * i
            rows.append(f"{padding}{base_row}")
        
        return "\n".join(rows)

    @staticmethod
    def draw_triangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle starts at the top-left and grows towards the bottom-right,
        with the final row having the specified width.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the ASCII triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive, or if symbol is invalid.
        """
        AsciiArt._validate_dimension(width, 'width')
        AsciiArt._validate_dimension(height, 'height')
        AsciiArt._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            # This scaling ensures the final row has the correct width.
            # math.ceil ensures a smooth-as-possible growth for discrete characters.
            num_symbols = math.ceil((i + 1) * width / height)
            rows.append(symbol * num_symbols)
        
        return "\n".join(rows)

    @staticmethod
    def draw_pyramid(height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive, or if symbol is invalid.
        """
        AsciiArt._validate_dimension(height, 'height')
        AsciiArt._validate_symbol(symbol)

        rows = []
        for i in range(height):
            padding = ' ' * (height - 1 - i)
            num_symbols = 2 * i + 1
            rows.append(f"{padding}{symbol * num_symbols}")
            
        return "\n".join(rows)


if __name__ == "__main__":
    """
    Demonstrates the functionality of the AsciiArt class.
    This block serves as a simple manual test and usage example.
    """
    
    print("--- Demonstrating Shape Drawing ---")

    print("\n[+] Drawing a 5x5 Square with '#':")
    print(AsciiArt.draw_square(width=5, symbol='#'))

    print("\n[+] Drawing a 10x4 Rectangle with '*':")
    print(AsciiArt.draw_rectangle(width=10, height=4, symbol='*'))

    print("\n[+] Drawing a 7x5 Parallelogram with '=':")
    print(AsciiArt.draw_parallelogram(width=7, height=5, symbol='='))

    print("\n[+] Drawing a Right-Angled Triangle (h=6, w=12) with 'A':")
    print(AsciiArt.draw_triangle(width=12, height=6, symbol='A'))

    print("\n[+] Drawing a Pyramid (h=6) with 'O':")
    print(AsciiArt.draw_pyramid(height=6, symbol='O'))

    print("\n--- Demonstrating Input Validation ---")

    try:
        print("\n[-] Attempting to draw with an invalid symbol (multi-character)...")
        AsciiArt.draw_square(3, '@@')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\n[-] Attempting to draw with an invalid symbol (whitespace)...")
        AsciiArt.draw_square(3, ' ')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\n[-] Attempting to draw with a negative width...")
        AsciiArt.draw_rectangle(-5, 5, '*')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\n[-] Attempting to draw with a non-integer height...")
        AsciiArt.draw_pyramid(height=4.5, symbol='^') # type: ignore
    except TypeError as e:
        print(f"Caught expected error: {e}")
