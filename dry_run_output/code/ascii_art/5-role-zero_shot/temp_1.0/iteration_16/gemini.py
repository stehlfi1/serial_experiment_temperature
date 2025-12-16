
"""
A Python module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods to draw
various geometric shapes using a specified printable character. The implementation
adheres to high-quality code standards, including clear documentation, robust input
validation, and efficient algorithms.
"""

import sys
from typing import Optional


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a suite of methods for drawing geometric shapes like
    squares, rectangles, and pyramids as multi-line strings. It emphasizes
    code quality, safety through input validation, and adherence to a
    clean, object-oriented design.
    """

    def _validate_inputs(
        self,
        symbol: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper ensures that dimensions are positive integers and
        the symbol is a single, printable, non-whitespace character.

        Args:
            symbol (str): The character to use for drawing.
            width (Optional[int]): The width of the shape.
            height (Optional[int]): The height of the shape.

        Raises:
            ValueError: If any of the validation checks fail.
        """
        if width is not None and (not isinstance(width, int) or width <= 0):
            raise ValueError("Width must be a positive integer.")

        if height is not None and (not isinstance(height, int) or height <= 0):
            raise ValueError("Height must be a positive integer.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")

        if not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a printable, non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square.
            symbol (str): The character used to draw the square.

        Returns:
            str: A multi-line string representing the square.
        
        Raises:
            ValueError: If width is not a positive integer or symbol is invalid.
        """
        # A square is a rectangle with equal width and height.
        # We can reuse the draw_rectangle logic for maintainability.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used to draw the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If dimensions are not positive integers or symbol is invalid.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        row = symbol * width
        # Create a list of rows and join them with newlines for efficiency.
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width (int): The width of the parallelogram's top/bottom edge.
            height (int): The height of the parallelogram.
            symbol (str): The character used to draw the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If dimensions are not positive integers or symbol is invalid.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        rows = []
        for i in range(height):
            leading_spaces = " " * i
            content = symbol * width
            rows.append(f"{leading_spaces}{content}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """

        Draws a filled, right-angled triangle.

        The triangle grows from the top-left, reaching the specified
        width at its base over the specified height.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character used to draw the triangle.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If dimensions are not positive integers or symbol is invalid.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row based on a
            # linear scale from 1 to width over the total height.
            # Using round() provides a smooth, visually appealing slope.
            # max(1, ...) ensures at least one symbol is always drawn per row.
            num_symbols = max(1, round((i + 1) * (width / height)))
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The character used to draw the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If height is not a positive integer or symbol is invalid.
        """
        self._validate_inputs(symbol=symbol, height=height)
        rows = []
        # The base of the pyramid will have a width of (2 * height - 1)
        for i in range(height):
            # Number of leading spaces decreases with each row.
            leading_spaces = " " * (height - 1 - i)
            # Number of symbols increases by 2 with each row (1, 3, 5, ...).
            num_symbols = 2 * i + 1
            rows.append(f"{leading_spaces}{symbol * num_symbols}")
        return "\n".join(rows)


if __name__ == "__main__":
    """
    Demonstration of the AsciiArt class.
    
    This block is executed when the script is run directly. It showcases
    the drawing capabilities and the built-in input validation.
    """
    drawer = AsciiArt()
    symbol = "*"
    
    print("--- ASCII Art Shape Generator ---")

    print("\n[1] Drawing a 5x5 Square:")
    print(drawer.draw_square(width=5, symbol=symbol))

    print("\n[2] Drawing a 10x4 Rectangle:")
    print(drawer.draw_rectangle(width=10, height=4, symbol="#"))

    print("\n[3] Drawing a 12x5 Parallelogram:")
    print(drawer.draw_parallelogram(width=12, height=5, symbol="@"))
    
    print("\n[4] Drawing a Right-Angled Triangle (Width=8, Height=8):")
    print(drawer.draw_triangle(width=8, height=8, symbol="+"))
    
    print("\n[5] Drawing a Right-Angled Triangle (Width=15, Height=7):")
    print(drawer.draw_triangle(width=15, height=7, symbol="T"))

    print("\n[6] Drawing a Pyramid (Height=6):")
    print(drawer.draw_pyramid(height=6, symbol="^"))

    print("\n--- Testing Input Validation ---")
    
    try:
        print("\n[7] Attempting to draw with an invalid width (-5):")
        drawer.draw_square(width=-5, symbol=symbol)
    except ValueError as e:
        print(f"   Successfully caught error: {e}", file=sys.stderr)

    try:
        print("\n[8] Attempting to draw with an invalid symbol ('$$'):")
        drawer.draw_rectangle(width=5, height=5, symbol="$$")
    except ValueError as e:
        print(f"   Successfully caught error: {e}", file=sys.stderr)
        
    try:
        print("\n[9] Attempting to draw with a whitespace symbol (' '):")
        drawer.draw_pyramid(height=4, symbol=" ")
    except ValueError as e:
        print(f"   Successfully caught error: {e}", file=sys.stderr)
