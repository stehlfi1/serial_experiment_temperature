
# -*- coding: utf-8 -*-
"""
A Python module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods to draw
various geometric shapes using printable characters. The implementation adheres
to high-quality code standards, focusing on correctness, efficiency, and
maintainability as outlined by ISO/IEC 25010.
"""

import math
from typing import Dict, Any, List

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class provides a clean interface to draw filled shapes like squares,
    rectangles, triangles, and pyramids. It incorporates robust input
    validation to ensure reliability and produces string representations of
    the shapes, making it easy to use and test.

    ISO/IEC 25010 Considerations:
    - Functional Suitability: Provides correct ASCII representations for the
      specified shapes.
    - Performance Efficiency: Uses efficient string operations and list
      comprehensions to minimize resource usage.
    - Reliability (Fault Tolerance): Implements strict input validation to
      prevent errors from invalid arguments.
    - Maintainability (Modularity, Testability): Encapsulates drawing logic
      within a single class. Each method is a pure function, returning a
      string, which simplifies unit testing. A private validation helper
      reduces code duplication.
    - Usability (Readability): Employs clear naming, type hints, and
      comprehensive docstrings for ease of understanding and use.
    """

    def _validate_input(self, symbol: str, dimensions: Dict[str, Any]) -> None:
        """
        Private helper to validate input parameters for drawing functions.

        Args:
            symbol (str): The character symbol to use for drawing.
            dimensions (Dict[str, Any]): A dictionary of dimension names and
                                         their integer values (e.g., {'width': 5}).

        Raises:
            TypeError: If the symbol is not a string or dimensions are not integers.
            ValueError: If the symbol is not a single, printable, non-whitespace
                        character, or if dimensions are not positive integers.
        """
        # --- Symbol Validation ---
        if not isinstance(symbol, str):
            raise TypeError("The 'symbol' must be a string.")
        if len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError(
                "The 'symbol' must be a printable, non-whitespace character."
            )

        # --- Dimension Validation ---
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The '{name}' dimension must be an integer.")
            if value <= 0:
                raise ValueError(f"The '{name}' dimension must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width (int): The width and height of the square. Must be a positive integer.
            symbol (str): The single character used to draw the square.

        Returns:
            str: A multi-line string representing the ASCII square.
        """
        self._validate_input(symbol, {'width': width})
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width (int): The width of the rectangle. Must be a positive integer.
            height (int): The height of the rectangle. Must be a positive integer.
            symbol (str): The single character used to draw the rectangle.

        Returns:
            str: A multi-line string representing the ASCII rectangle.
        """
        self._validate_input(symbol, {'width': width, 'height': height})

        row: str = symbol * width
        # Efficiently create the full shape by joining rows with newlines.
        art_lines: List[str] = [row] * height
        return "\n".join(art_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that slants to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width (int): The width of the parallelogram's parallel sides.
                         Must be a positive integer.
            height (int): The height of the parallelogram. Must be a positive integer.
            symbol (str): The single character used to draw the parallelogram.

        Returns:
            str: A multi-line string representing the ASCII parallelogram.
        """
        self._validate_input(symbol, {'width': width, 'height': height})

        shape_part: str = symbol * width
        # Use a list comprehension for readable and efficient line generation.
        art_lines: List[str] = [
            ' ' * i + shape_part for i in range(height)
        ]
        return "\n".join(art_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left, with its width scaling proportionally
        to its height to fit the specified dimensions.

        Args:
            width (int): The width of the triangle's base. Must be a positive integer.
            height (int): The height of the triangle. Must be a positive integer.
            symbol (str): The single character used to draw the triangle.

        Returns:
            str: A multi-line string representing the ASCII triangle.
        """
        self._validate_input(symbol, {'width': width, 'height': height})
        
        art_lines: List[str] = []
        for i in range(1, height + 1):
            # Calculate the number of symbols for the current row based on the
            # overall width/height ratio. math.ceil ensures a non-jagged edge.
            current_width = math.ceil(i * width / height)
            art_lines.append(symbol * current_width)

        return "\n".join(art_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid. Must be a positive integer.
            symbol (str): The single character used to draw the pyramid.

        Returns:
            str: A multi-line string representing the ASCII pyramid.
        """
        self._validate_input(symbol, {'height': height})

        art_lines: List[str] = []
        for i in range(height):
            # Calculate leading spaces for centering the pyramid level.
            spaces = ' ' * (height - 1 - i)
            # Calculate the number of symbols for the current level.
            symbols = symbol * (2 * i + 1)
            art_lines.append(spaces + symbols)

        return "\n".join(art_lines)

# --- Example Usage ---
if __name__ == "__main__":
    # This block demonstrates how to use the AsciiArt class and provides
    # visual output for verification. It will only run when the script is
    # executed directly.
    
    artist = AsciiArt()
    
    print("--- Square (5x5, '#') ---")
    print(artist.draw_square(5, '#'))
    print("\n" + "="*30 + "\n")

    print("--- Rectangle (8x4, '*') ---")
    print(artist.draw_rectangle(8, 4, '*'))
    print("\n" + "="*30 + "\n")

    print("--- Parallelogram (10x5, '=') ---")
    print(artist.draw_parallelogram(10, 5, '='))
    print("\n" + "="*30 + "\n")

    print("--- Triangle (width=12, height=6, '+') ---")
    print(artist.draw_triangle(12, 6, '+'))
    print("\n" + "="*30 + "\n")

    print("--- Pyramid (height=7, '^') ---")
    print(artist.draw_pyramid(7, '^'))
    print("\n" + "="*30 + "\n")

    # Example of input validation
    print("--- Testing Invalid Input ---")
    try:
        artist.draw_square(-3, 'X')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        artist.draw_rectangle(5, 5, '@@')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        artist.draw_pyramid(5, ' ')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        artist.draw_triangle(5.5, 3, '%') # type: ignore
    except TypeError as e:
        print(f"Caught expected error: {e}")

