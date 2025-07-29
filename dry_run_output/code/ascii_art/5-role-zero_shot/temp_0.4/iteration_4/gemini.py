
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements an interface for
drawing various geometric shapes using ASCII characters. The design emphasizes
code quality, adhering to principles outlined in the ISO/IEC 25010 standard:

- Functional Suitability: Correctly generates the specified shapes.
- Performance Efficiency: Uses efficient string-building techniques.
- Reliability (Fault Tolerance, Maturity): Includes robust input validation
  to handle erroneous inputs gracefully by raising specific errors.
- Usability: A clear and well-documented API makes the class easy to use.
- Maintainability (Modularity, Reusability, Testability): Logic is
  encapsulated within a class. Validation logic is reused, and each method
  is a pure function, making the code easy to test and maintain.
- Portability: Uses only the Python standard library, ensuring it runs on any
  platform with a Python interpreter.
"""

import math
from typing import NoReturn


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a collection of methods to draw filled geometric
    shapes as multi-line strings, ready for console output.
    """

    def _validate_symbol(self, symbol: str) -> None | NoReturn:
        """
        Validates that the symbol is a single, printable, non-whitespace character.

        Args:
            symbol (str): The character to use for drawing.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single character or is not
                        printable/is whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError(
                "Symbol must be a printable, non-whitespace character."
            )

    def _validate_dimension(self, value: int, name: str) -> None | NoReturn:
        """
        Validates that a dimension (e.g., width, height) is a positive integer.

        Args:
            value (int): The dimension's value.
            name (str): The name of the dimension (e.g., 'width').

        Raises:
            TypeError: If the value is not an integer.
            ValueError: If the value is not positive (i.e., <= 0).
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        # Use a list comprehension and join for efficient string building.
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width (int): The width of the parallelogram's top/bottom sides.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        shape_row = symbol * width
        rows = [" " * i + shape_row for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner and is scaled to fit
        the specified width and height.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Scale the number of symbols for the current row.
            # math.ceil ensures the final row has the correct width.
            current_width = math.ceil((i + 1) * (width / height))
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        # The width of the pyramid's base is 2 * height - 1
        for i in range(height):
            num_symbols = 2 * i + 1
            padding = " " * (height - 1 - i)
            rows.append(f"{padding}{symbol * num_symbols}")
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    art_generator = AsciiArt()
    print("--- ASCII Art Generator Demo ---")

    try:
        # --- Draw Square ---
        print("\n1. Square (5x5, symbol '#')")
        square = art_generator.draw_square(width=5, symbol="#")
        print(square)

        # --- Draw Rectangle ---
        print("\n2. Rectangle (10x4, symbol '*')")
        rectangle = art_generator.draw_rectangle(width=10, height=4, symbol="*")
        print(rectangle)

        # --- Draw Parallelogram ---
        print("\n3. Parallelogram (8x5, symbol '=')")
        parallelogram = art_generator.draw_parallelogram(
            width=8, height=5, symbol="="
        )
        print(parallelogram)

        # --- Draw Triangle ---
        print("\n4. Right-Angled Triangle (width=12, height=6, symbol 'A')")
        triangle = art_generator.draw_triangle(width=12, height=6, symbol="A")
        print(triangle)

        # --- Draw Pyramid ---
        print("\n5. Pyramid (height=7, symbol 'O')")
        pyramid = art_generator.draw_pyramid(height=7, symbol="O")
        print(pyramid)

        # --- Demonstrate Input Validation ---
        print("\n6. Demonstrating Error Handling (invalid width)")
        try:
            art_generator.draw_square(width=-3, symbol="$")
        except ValueError as e:
            print(f"   Caught expected error: {e}")

        print("\n7. Demonstrating Error Handling (invalid symbol)")
        try:
            art_generator.draw_rectangle(width=5, height=5, symbol="?!")
        except ValueError as e:
            print(f"   Caught expected error: {e}")

        print("\n8. Demonstrating Error Handling (invalid type)")
        try:
            art_generator.draw_pyramid(height=4.5, symbol="^") # type: ignore
        except TypeError as e:
            print(f"   Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during the demo: {e}")
