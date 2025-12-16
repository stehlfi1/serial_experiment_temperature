
# -*- coding: utf-8 -*-
"""
ascii_art.py

A Python module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which offers a simple interface to
create various geometric shapes as multi-line strings. The implementation
focuses on code quality, adhering to principles outlined in ISO/IEC 25010,
such as correctness, performance, safety, and maintainability.
"""

from typing import Dict


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides methods to draw filled shapes like squares, rectangles,
    and pyramids using a specified character. It adheres to high-quality code
    standards, including input validation, modularity, and clear documentation.

    Attributes:
        None
    """

    def _validate_inputs(self, symbol: str, **dimensions: int) -> None:
        """
        Validates common inputs for drawing methods. (Modularity, Safety)

        This private helper ensures that the symbol and dimension parameters meet
        the required criteria before any drawing logic is executed, promoting
        code reuse and robust error handling.

        Args:
            symbol (str): The character to use for drawing.
            **dimensions (int): Keyword arguments for shape dimensions
                                (e.g., width, height).

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single, printable, non-whitespace
                        character, or if any dimension is not a positive integer.
        """
        # Symbol validation
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1 or not symbol.isprintable() or symbol.isspace():
            raise ValueError(
                "Symbol must be a single, printable, non-whitespace character."
            )

        # Dimensions validation
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square. (Correctness)

        Args:
            width (int): The width and height of the square. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled square.
        """
        self._validate_inputs(symbol, width=width)
        row = symbol * width
        # Use a list comprehension for efficient row generation (Performance)
        rows = [row for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle. (Correctness)

        Args:
            width (int): The width of the rectangle. Must be a positive integer.
            height (int): The height of the rectangle. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled rectangle.
        """
        self._validate_inputs(symbol, width=width, height=height)
        row = symbol * width
        rows = [row for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, shifted to the right. (Correctness)

        Each subsequent row is indented by one additional space.

        Args:
            width (int): The width of the parallelogram. Must be a positive integer.
            height (int): The height of the parallelogram. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled parallelogram.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows = []
        line = symbol * width
        for i in range(height):
            padding = " " * i
            rows.append(f"{padding}{line}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle. (Correctness)

        The triangle grows from the top-left corner, scaling its width
        linearly to match the specified base width and height.

        Args:
            width (int): The base width of the triangle. Must be a positive integer.
            height (int): The height of the triangle. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled triangle.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Scale the width for the current row linearly. (Performance, Correctness)
            # The `+ 0.5` and `int()` combination effectively rounds the result.
            # `max(1, ...)` ensures that each row has at least one symbol.
            progress_ratio = (i + 1) / height
            current_width = max(1, int(progress_ratio * width + 0.5))
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid. (Correctness)

        Args:
            height (int): The height of the pyramid. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the filled pyramid.
        """
        self._validate_inputs(symbol, height=height)
        rows = []
        # The width of the pyramid's base is `2 * height - 1`.
        for i in range(height):
            num_symbols = 2 * i + 1
            # Calculate leading spaces for centering the line.
            padding = " " * (height - 1 - i)
            rows.append(f"{padding}{symbol * num_symbols}")
        return "\n".join(rows)


# --- Example Usage ---
# This block demonstrates the functionality and allows for easy testing.
# (Testability, Readability)
if __name__ == "__main__":
    # Instantiate the AsciiArt class
    artist = AsciiArt()
    symbol = "*"

    print("--- ASCII Art Generator ---")

    try:
        # --- Draw a Square ---
        print("\n[Square (5x5)]")
        square = artist.draw_square(width=5, symbol=symbol)
        print(square)

        # --- Draw a Rectangle ---
        print("\n[Rectangle (10x4)]")
        rectangle = artist.draw_rectangle(width=10, height=4, symbol="#")
        print(rectangle)

        # --- Draw a Parallelogram ---
        print("\n[Parallelogram (8x5)]")
        parallelogram = artist.draw_parallelogram(width=8, height=5, symbol="=")
        print(parallelogram)

        # --- Draw a Triangle ---
        print("\n[Right-Angled Triangle (12x6)]")
        triangle = artist.draw_triangle(width=12, height=6, symbol="+")
        print(triangle)

        # --- Draw a Pyramid ---
        print("\n[Pyramid (height 7)]")
        pyramid = artist.draw_pyramid(height=7, symbol="^")
        print(pyramid)
        
        # --- Example of Invalid Input ---
        print("\n[Testing Invalid Input: width=0]")
        try:
            artist.draw_square(width=0, symbol=symbol)
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\n[Testing Invalid Input: symbol='ab']")
        try:
            artist.draw_square(width=5, symbol='ab')
        except ValueError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}")
