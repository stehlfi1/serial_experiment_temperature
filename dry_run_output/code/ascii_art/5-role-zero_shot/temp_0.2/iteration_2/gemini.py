
"""
This module provides the AsciiArt class for generating 2D ASCII art shapes.

The implementation adheres to the ISO/IEC 25010 standard for software quality,
focusing on:
- Functional Suitability: Correctly generates specified ASCII shapes.
- Performance Efficiency: Uses efficient string and list operations.
- Reliability (Fault Tolerance): Includes robust input validation to handle
  improper arguments gracefully.
- Usability (for the developer): Offers a clear, well-documented, and
  easy-to-use class-based interface.
- Maintainability: Employs a modular, readable, and testable code structure
  with clear separation of concerns.
"""

import math

class AsciiArt:
    """
    A class for drawing various 2D shapes using ASCII characters.

    This class provides a collection of methods to generate string representations
    of common geometric shapes, such as squares, rectangles, and pyramids.
    All methods are designed to be pure functions that return a string,
    making them predictable and easy to test.
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, printable, non-whitespace character.

        Args:
            symbol: The character to be used for drawing.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single character, is whitespace,
                        or is not printable.
        """
        if not isinstance(symbol, str):
            raise TypeError("The drawing symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("The drawing symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("The drawing symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("The drawing symbol must be a printable character.")

    def _validate_positive_integer(self, value: int, name: str) -> None:
        """
        Validates that a given dimension is a positive integer.

        Args:
            value: The dimension value (e.g., width, height).
            name: The name of the dimension for use in error messages.

        Raises:
            TypeError: If the value is not an integer.
            ValueError: If the value is not a positive integer (i.e., > 0).
        """
        if not isinstance(value, int):
            raise TypeError(f"The {name} must be an integer.")
        if value <= 0:
            raise ValueError(f"The {name} must be a positive integer greater than 0.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)

        row = symbol * width
        art_lines = [row] * width
        return "\n".join(art_lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        art_lines = [row] * height
        return "\n".join(art_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram skewed to the right.

        Each subsequent row is indented by one additional space.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        content = symbol * width
        art_lines = [" " * i + content for i in range(height)]
        return "\n".join(art_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle.

        The triangle grows from the top-left corner. The number of symbols
        in each row is scaled proportionally based on the total width and height.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing the triangle.

        Returns:
            A multi-line string representing the right-angled triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        art_lines = []
        for i in range(height):
            # Calculate the number of symbols for the current row proportionally
            # and ensure the first row has at least one symbol.
            num_symbols = max(1, round((i + 1) * width / height))
            art_lines.append(symbol * num_symbols)
        return "\n".join(art_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing the pyramid.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        art_lines = []
        for i in range(height):
            indent = " " * (height - 1 - i)
            content = symbol * (2 * i + 1)
            art_lines.append(indent + content)
        return "\n".join(art_lines)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class and its methods.
    # It serves as a basic functional check and example.
    artist = AsciiArt()
    symbol = "*"

    print("--- ASCII Art Shape Generator ---")

    print("\n[+] Square (5x5):")
    print(artist.draw_square(5, symbol))

    print("\n[+] Rectangle (8x4):")
    print(artist.draw_rectangle(8, 4, symbol))

    print("\n[+] Parallelogram (10x5):")
    print(artist.draw_parallelogram(10, 5, symbol))

    print("\n[+] Right-Angled Triangle (width=10, height=5):")
    print(artist.draw_triangle(10, 5, symbol))

    print("\n[+] Right-Angled Triangle (width=6, height=6):")
    print(artist.draw_triangle(6, 6, symbol))

    print("\n[+] Pyramid (height=6):")
    print(artist.draw_pyramid(6, symbol))

    print("\n--- Testing Error Handling ---")

    try:
        print("\n[!] Testing invalid width (-5):")
        artist.draw_square(-5, symbol)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\n[!] Testing invalid symbol ('##'):")
        artist.draw_rectangle(5, 5, "##")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\n[!] Testing invalid symbol type (123):")
        artist.draw_pyramid(5, 123)
    except TypeError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\n[!] Testing invalid height type ('abc'):")
        artist.draw_pyramid("abc", symbol)
    except TypeError as e:
        print(f"Caught expected error: {e}")
