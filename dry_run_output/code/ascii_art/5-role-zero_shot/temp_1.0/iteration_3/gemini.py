
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods to draw
various geometric shapes using a specified character. It is designed with a
focus on code quality, adhering to principles of the ISO/IEC 25010 standard,
including correctness, efficiency, modularity, and safety.
"""

import math
from typing import List


class AsciiArt:
    """
    A class to generate various filled ASCII art shapes.

    This class provides a clean interface for creating string representations of
    common geometric shapes. All methods ensure that inputs are valid before
    drawing, providing a reliable and safe implementation.
    """

    def _validate_inputs(self, symbol: str, *dims: int) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper method centralizes input validation to ensure
        consistency and reduce code duplication, enhancing maintainability.

        Args:
            symbol (str): The character to use for drawing.
            *dims (int): A variable number of integer dimensions (e.g., width, height).

        Raises:
            TypeError: If the symbol is not a string or dimensions are not integers.
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if any dimension is not a positive integer.
        """
        if not isinstance(symbol, str):
            raise TypeError("The 'symbol' must be a string.")
        if len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        for dim in dims:
            if not isinstance(dim, int):
                raise TypeError("Dimensions must be integers.")
            if dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method leverages the draw_rectangle method for its implementation,
        promoting code reuse and modularity.

        Args:
            width (int): The width and height of the square.
            symbol (str): The single character used to draw the square.

        Returns:
            str: A multi-line string representing the filled square.

        Raises:
            TypeError: See _validate_inputs documentation.
            ValueError: See _validate_inputs documentation.
        """
        self._validate_inputs(symbol, width)
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        The implementation is efficient, creating each row once and then
        building the final string, avoiding inefficient string concatenation.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The single character used to draw the rectangle.

        Returns:
            str: A multi-line string representing the filled rectangle.

        Raises:
            TypeError: See _validate_inputs documentation.
            ValueError: See _validate_inputs documentation.
        """
        self._validate_inputs(symbol, width, height)
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is indented by one additional space.

        Args:
            width (int): The width of the parallelogram's top/bottom sides.
            height (int): The height of the parallelogram.
            symbol (str): The single character used to draw the shape.

        Returns:
            str: A multi-line string representing the filled parallelogram.

        Raises:
            TypeError: See _validate_inputs documentation.
            ValueError: See _validate_inputs documentation.
        """
        self._validate_inputs(symbol, width, height)
        rows: List[str] = []
        for i in range(height):
            indent = " " * i
            content = symbol * width
            rows.append(f"{indent}{content}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: anInt, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner. The width and height
        parameters determine the final dimensions, and the number of symbols
        per row is scaled proportionally.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The single character used to draw the triangle.

        Returns:
            str: A multi-line string representing the filled triangle.

        Raises:
            TypeError: See _validate_inputs documentation.
            ValueError: See _validate_inputs documentation.
        """
        self._validate_inputs(symbol, width, height)
        rows: List[str] = []
        for i in range(height):
            # Calculate the number of symbols for the current row proportionally.
            # Using math.ceil ensures the shape gradually expands and the last
            # row has the specified 'width'. We use max(1, ...) to avoid empty rows.
            current_width = max(1, math.ceil((i + 1) * width / height))
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        The pyramid has a base width of (2 * height - 1).

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The single character used to draw the pyramid.

        Returns:
            str: A multi-line string representing the filled pyramid.

        Raises:
            TypeError: See _validate_inputs documentation.
            ValueError: See _validate_inputs documentation.
        """
        self._validate_inputs(symbol, height)
        rows: List[str] = []
        # The total width of the pyramid's base is (2 * height - 1)
        for i in range(height):
            # Number of symbols for the current level (0-indexed)
            num_symbols = 2 * i + 1
            # Number of leading spaces for centering
            num_spaces = height - 1 - i
            
            indent = " " * num_spaces
            content = symbol * num_symbols
            rows.append(f"{indent}{content}")
        return "\n".join(rows)


def main():
    """
    Main function to demonstrate the capabilities of the AsciiArt class.
    
    This function showcases how to use each drawing method and how the
    built-in validation handles incorrect inputs gracefully.
    """
    art = AsciiArt()
    print("--- ASCII Art Shape Generator ---")

    # --- 1. Demonstrate Valid Shapes ---
    print("\n--- 1. Drawing Valid Shapes ---\n")

    print("Square (5x5, symbol '#'):")
    print(art.draw_square(5, "#"))
    print("-" * 20)

    print("Rectangle (8x4, symbol '*'):")
    print(art.draw_rectangle(8, 4, "*"))
    print("-" * 20)

    print("Parallelogram (10x5, symbol '='):")
    print(art.draw_parallelogram(10, 5, "="))
    print("-" * 20)

    print("Right-Angled Triangle (width=10, height=5, symbol '+'):")
    print(art.draw_triangle(10, 5, "+"))
    print("-" * 20)

    print("Pyramid (height=6, symbol '^'):")
    print(art.draw_pyramid(6, "^"))
    print("-" * 20)

    # --- 2. Demonstrate Input Validation ---
    print("\n--- 2. Testing Input Validation ---\n")

    test_cases = [
        ("Negative width", lambda: art.draw_square(-3, "X")),
        ("Multi-character symbol", lambda: art.draw_rectangle(5, 5, "XX")),
        ("Whitespace symbol", lambda: art.draw_parallelogram(5, 5, " ")),
        ("Non-integer dimension", lambda: art.draw_triangle(5.5, 5, "&")),
        ("Non-string symbol", lambda: art.draw_pyramid(5, 123)),
    ]

    for description, test_func in test_cases:
        try:
            print(f"Testing: {description}")
            test_func()
        except (ValueError, TypeError) as e:
            print(f"  -> Successfully caught an error: {e}\n")


if __name__ == "__main__":
    main()
