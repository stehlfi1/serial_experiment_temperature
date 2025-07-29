
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods to draw
various geometric shapes using ASCII characters. The implementation focuses on
code quality, adhering to principles of the ISO/IEC 25010 standard, including
functional suitability, performance efficiency, reliability, and maintainability.
"""

import math
from typing import List


class AsciiArt:
    """
    A class to generate various ASCII art shapes.

    This class provides a clean interface for creating string representations of
    common geometric shapes. All methods are stateless and deterministic. Input
    validation is performed to ensure robustness and provide clear error
    feedback.
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates the symbol used for drawing.

        Args:
            symbol: The character to be used for drawing the shape.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def _validate_dimensions(self, **kwargs: int) -> None:
        """
        Validates the dimensions (width, height) for a shape.

        Args:
            **kwargs: Keyword arguments representing dimensions (e.g., width=5).

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive integer (> 0).
        """
        for name, value in kwargs.items():
            if not isinstance(value, int):
                raise TypeError(f"Dimension '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"Dimension '{name}' must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the square.

        Raises:
            TypeError: If inputs have an invalid type.
            ValueError: If inputs have an invalid value.
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        
        line = symbol * width
        lines = [line for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            TypeError: If inputs have an invalid type.
            ValueError: If inputs have an invalid value.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        line = symbol * width
        lines = [line for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram skewed to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width: The width of the parallelogram's top/bottom side.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            TypeError: If inputs have an invalid type.
            ValueError: If inputs have an invalid value.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines = [" " * i + symbol * width for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner to fit within the specified
        width and height. The number of symbols per row is scaled proportionally.

        Args:
            width: The final base width of the triangle.
            height: The total height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the right-angled triangle.

        Raises:
            TypeError: If inputs have an invalid type.
            ValueError: If inputs have an invalid value.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        
        lines: List[str] = []
        for i in range(height):
            # Scale the number of symbols for the current row proportionally
            # to the overall width and height. math.ceil ensures the final
            # row has the correct width.
            num_symbols = math.ceil((i + 1) * width / height)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            TypeError: If inputs have an invalid type.
            ValueError: If inputs have an invalid value.
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)

        lines: List[str] = []
        for i in range(height):
            padding = " " * (height - 1 - i)
            body = symbol * (2 * i + 1)
            lines.append(f"{padding}{body}")
        return "\n".join(lines)


def main() -> None:
    """
    Main function to demonstrate the AsciiArt class functionality.
    """
    art = AsciiArt()
    print("--- ASCII Art Generator ---")

    # --- 1. Demonstrate Valid Shapes ---
    print("\n[+] Drawing a 5x5 Square with '#':")
    print(art.draw_square(5, "#"))

    print("\n[+] Drawing a 7x4 Rectangle with '*':")
    print(art.draw_rectangle(7, 4, "*"))
    
    print("\n[+] Drawing a 10x5 Parallelogram with '=':")
    print(art.draw_parallelogram(10, 5, "="))

    print("\n[+] Drawing a Right-Angled Triangle (W:10, H:5) with '+':")
    print(art.draw_triangle(10, 5, "+"))
    
    print("\n[+] Drawing a Right-Angled Triangle (W:5, H:5) with 'T':")
    print(art.draw_triangle(5, 5, "T"))

    print("\n[+] Drawing a Pyramid (H:6) with '^':")
    print(art.draw_pyramid(6, "^"))
    
    # --- 2. Demonstrate Input Validation ---
    print("\n--- Testing Error Handling ---")
    
    # Test case 1: Invalid dimension
    try:
        print("\n[-] Attempting to draw a square with width=0...")
        art.draw_square(0, "#")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    # Test case 2: Invalid symbol length
    try:
        print("\n[-] Attempting to draw a rectangle with a multi-char symbol '@@'...")
        art.draw_rectangle(5, 5, "@@")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    # Test case 3: Invalid symbol type (whitespace)
    try:
        print("\n[-] Attempting to draw a pyramid with a space character...")
        art.draw_pyramid(4, " ")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Test case 4: Invalid dimension type
    try:
        print("\n[-] Attempting to draw a triangle with a float height...")
        art.draw_triangle(5, 3.5, "X") # type: ignore
    except TypeError as e:
        print(f"Caught expected error: {e}")


if __name__ == "__main__":
    main()

