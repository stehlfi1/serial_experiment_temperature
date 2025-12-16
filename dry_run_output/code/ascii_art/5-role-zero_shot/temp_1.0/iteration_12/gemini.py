
# -*- coding: utf-8 -*-
"""
ascii_art_generator.py

This module provides the AsciiArt class for generating
2D ASCII art shapes in a console environment.

The implementation prioritizes correctness, efficiency, safety, and maintainability,
aligning with the principles of the ISO/IEC 25010 software quality standard.
"""

import math
from typing import Dict, Any

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a suite of methods to draw simple geometric shapes like
    squares, rectangles, and pyramids using a user-specified character. It is
    designed with a focus on high-quality software engineering principles.

    Attributes:
        This class has no public attributes. State is not maintained between calls.

    ISO/IEC 25010 Compliance Notes:
        - Functional Suitability: Correctly implements the specified drawing functions.
        - Performance Efficiency: Uses efficient string building techniques
          (e.g., list comprehensions and `str.join`) to minimize overhead.
        - Reliability & Safety: Implements robust input validation to prevent
          crashes from invalid data (fault tolerance).
        - Maintainability & Modularity: Logic is encapsulated within a class.
          A private helper method modularizes validation logic for reusability.
        - Testability: Methods are pure functions (output depends only on input),
          making them easy to unit test.
        - Readability: Conforms to PEP 8, with clear variable names, type hints,
          and comprehensive docstrings.
    """

    def _validate_inputs(self, symbol: str, **dimensions: Any) -> None:
        """
        Private helper to validate common inputs for drawing methods.

        This method ensures that the symbol is a single printable character and
        that all provided dimensions (e.g., width, height) are positive integers.

        Args:
            symbol (str): The character to use for drawing.
            **dimensions (Any): A dictionary of named dimensions and their values.

        Raises:
            ValueError: If the symbol is not a single character, is whitespace,
                        or if any dimension is not a positive integer.
            TypeError: If a dimension is not of type int.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"The '{name}' must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width (int): The width and height of the square. Must be positive.
            symbol (str): The single character to fill the square with.

        Returns:
            str: A multi-line string representing the ASCII square.

        Raises:
            ValueError: For invalid width or symbol.
            TypeError: If width is not an integer.
        """
        self._validate_inputs(symbol, width=width)
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width (int): The width of the rectangle. Must be positive.
            height (int): The height of the rectangle. Must be positive.
            symbol (str): The single character to fill the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII rectangle.

        Raises:
            ValueError: For invalid width, height, or symbol.
            TypeError: If width or height is not an integer.
        """
        self._validate_inputs(symbol, width=width, height=height)
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram leaning to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width (int): The width of the parallelogram's parallel sides.
            height (int): The height of the parallelogram.
            symbol (str): The single character to fill the shape with.

        Returns:
            str: A multi-line string representing the ASCII parallelogram.
        
        Raises:
            ValueError: For invalid width, height, or symbol.
            TypeError: If width or height is not an integer.
        """
        self._validate_inputs(symbol, width=width, height=height)
        row_content = symbol * width
        rows = [(" " * i) + row_content for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from a narrow top to a wide base, fitting within the
        bounding box defined by width and height. The number of symbols in each
        row is calculated to create a smooth diagonal line.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The single character to fill the triangle with.

        Returns:
            str: A multi-line string representing the ASCII triangle.
        
        Raises:
            ValueError: For invalid width, height, or symbol.
            TypeError: If width or height is not an integer.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row to create
            # a linear slope from 1 to `width` over `height` rows.
            # We use ceiling to ensure the shape is properly filled.
            num_symbols = math.ceil(((i + 1) / height) * width)
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        The pyramid has a base width of (2 * height - 1) and is centered.

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The single character to fill the pyramid with.

        Returns:
            str: A multi-line string representing the ASCII pyramid.
        
        Raises:
            ValueError: For invalid height or symbol.
            TypeError: If height is not an integer.
        """
        self._validate_inputs(symbol, height=height)
        # The widest part of the pyramid (the base) determines the total width.
        total_width = (height * 2) - 1
        rows = []
        for i in range(height):
            num_symbols = (i * 2) + 1
            # Calculate padding to center the row.
            padding = (total_width - num_symbols) // 2
            rows.append(" " * padding + symbol * num_symbols)
        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    # --- Example Usage ---
    art = AsciiArt()
    
    print("--- Square (5x5, #) ---")
    print(art.draw_square(5, "#"))
    print("\n" + "="*20 + "\n")
    
    print("--- Rectangle (8x4, *) ---")
    print(art.draw_rectangle(8, 4, "*"))
    print("\n" + "="*20 + "\n")

    print("--- Parallelogram (10x5, @) ---")
    print(art.draw_parallelogram(10, 5, "@"))
    print("\n" + "="*20 + "\n")

    print("--- Triangle (width=10, height=5, +) ---")
    print(art.draw_triangle(10, 5, "+"))
    print("\n" + "="*20 + "\n")
    
    print("--- Pyramid (height=6, ^) ---")
    print(art.draw_pyramid(6, "^"))
    print("\n" + "="*20 + "\n")
    
    # --- Error Handling Example ---
    try:
        print("--- Testing Invalid Input ---")
        art.draw_square(-3, "X")
    except ValueError as e:
        print(f"Successfully caught expected error: {e}")

    try:
        art.draw_rectangle(5, 5, "&&")
    except ValueError as e:
        print(f"Successfully caught expected error: {e}")

    try:
        art.draw_pyramid(4, ' ')
    except ValueError as e:
        print(f"Successfully caught expected error: {e}")
