
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods for drawing
various geometric shapes using ASCII characters. The implementation adheres to
high-quality code standards, focusing on correctness, efficiency, safety,
and maintainability as outlined by ISO/IEC 25010.

Classes:
    AsciiArt: A class to generate ASCII art representations of shapes.
"""

import math

class AsciiArt:
    """
    A class to generate ASCII art representations of various shapes.

    This class encapsulates the logic for creating string representations of
    geometric shapes like squares, rectangles, and pyramids. It emphasizes
    input validation to ensure reliability and produces predictable, correct
    output.

    Methods:
        draw_square(width, symbol): Draws a filled square.
        draw_rectangle(width, height, symbol): Draws a filled rectangle.
        draw_parallelogram(width, height, symbol): Draws a filled parallelogram.
        draw_triangle(width, height, symbol): Draws a filled right-angled triangle.
        draw_pyramid(height, symbol): Draws a filled pyramid.
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates the drawing symbol.

        ISO/IEC 25010 Compliance:
        - Reliability (Fault Tolerance): Protects methods from invalid symbol
          input, preventing unexpected behavior or errors during drawing.

        Args:
            symbol: The character to be used for drawing.

        Raises:
            ValueError: If the symbol is not a single, printable,
                        non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError(
                "Symbol must be a printable, non-whitespace character."
            )

    def _validate_dimension(self, value: int, name: str = "dimension") -> None:
        """
        Validates a spatial dimension (e.g., width, height).

        ISO/IEC 25010 Compliance:
        - Reliability (Fault Tolerance): Ensures that dimensions are positive
          integers, preventing errors like negative ranges or zero-size shapes
          that could lead to infinite loops or incorrect output.

        Args:
            value: The dimension value to validate.
            name: The name of the dimension (e.g., 'width', 'height').

        Raises:
            ValueError: If the dimension is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        ISO/IEC 25010 Compliance:
        - Functional Suitability (Correctness): Correctly generates a square
          by leveraging the rectangle drawing logic.
        - Maintainability (Reusability): Reuses the `draw_rectangle` method,
          promoting DRY (Don't Repeat Yourself) principles.

        Args:
            width: The width and height of the square.
            symbol: The character to draw the square with.

        Returns:
            A multi-line string representing the ASCII square.
        """
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle of given width and height.

        ISO/IEC 25010 Compliance:
        - Performance Efficiency: Uses efficient string multiplication and
          list joining, which is faster than repeated string concatenation
          for building the final output.
        - Testability: The method is a pure function with no side effects,
          making it easy to unit test.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to draw the rectangle with.

        Returns:
            A multi-line string representing the ASCII rectangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        # Create a list of rows and join them with newlines.
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram.

        Each subsequent row is shifted one space to the right.

        ISO/IEC 25010 Compliance:
        - Functional Suitability (Correctness): The algorithm correctly
          calculates the indentation for each row to produce the slanted shape.
        - Readability: The use of a list comprehension and f-strings makes
          the logic clear and concise.

        Args:
            width: The width of the parallelogram's top/bottom side.
            height: The height of the parallelogram.
            symbol: The character to draw the parallelogram with.

        Returns:
            A multi-line string representing the ASCII parallelogram.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        shape_rows = []
        for i in range(height):
            # Prepend 'i' spaces to shift the row to the right.
            indent = " " * i
            content = symbol * width
            shape_rows.append(f"{indent}{content}")

        return "\n".join(shape_rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner, fitting within the
        specified width and height. The base of the triangle will have
        the specified width.

        ISO/IEC 25010 Compliance:
        - Functional Suitability (Correctness): The scaling logic ensures
          the triangle's dimensions match the inputs, with the final row
          having the correct width.
        - Maintainability (Analysability): The logic for scaling each row
          is commented to explain the algorithm.

        Args:
            width: The width of the triangle's base.
            height: The total height of the triangle.
            symbol: The character to draw the triangle with.

        Returns:
            A multi-line string representing the ASCII triangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        shape_rows = []
        for i in range(1, height + 1):
            # Scale the number of symbols for the current row linearly.
            # Use math.ceil to ensure the shape grows progressively and the
            # last row has `width` symbols.
            num_symbols = math.ceil(i * width / height)
            shape_rows.append(symbol * num_symbols)

        return "\n".join(shape_rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        ISO/IEC 25010 Compliance:
        - Functional Suitability (Correctness): The algorithm correctly
          calculates the leading spaces and the number of symbols for each
          level of the pyramid to ensure symmetry.
        - Readability: Variable names like `leading_spaces` and `num_symbols`
          make the algorithm easy to understand.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to draw the pyramid with.

        Returns:
            A multi-line string representing the ASCII pyramid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        shape_rows = []
        for i in range(1, height + 1):
            # For row `i`, there are `height - i` leading spaces.
            leading_spaces = " " * (height - i)
            # The number of symbols is `2*i - 1`.
            num_symbols = symbol * (2 * i - 1)
            shape_rows.append(f"{leading_spaces}{num_symbols}")

        return "\n".join(shape_rows)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.

    This function serves as a simple, runnable example and a visual test case
    for the drawing methods.

    ISO/IEC 25010 Compliance:
    - Usability (Learnability): Provides a clear example of how to instantiate
      and use the AsciiArt class.
    """
    art_generator = AsciiArt()
    print("--- ASCII Art Generator Demo ---")

    try:
        print("\n[+] Drawing a 5x5 Square with '#':")
        print(art_generator.draw_square(width=5, symbol="#"))

        print("\n[+] Drawing a 10x4 Rectangle with '*':")
        print(art_generator.draw_rectangle(width=10, height=4, symbol="*"))

        print("\n[+] Drawing a 7x5 Parallelogram with '=':")
        print(art_generator.draw_parallelogram(width=7, height=5, symbol="="))

        print("\n[+] Drawing a Right-Angled Triangle (W:10, H:5) with '+':")
        print(art_generator.draw_triangle(width=10, height=5, symbol="+"))

        print("\n[+] Drawing a Pyramid (H:6) with '^':")
        print(art_generator.draw_pyramid(height=6, symbol="^"))

        print("\n--- Testing Validations ---")
        print("\n[!] Attempting to draw with an invalid symbol (should fail):")
        art_generator.draw_square(3, "@@")

    except (ValueError, TypeError) as e:
        print(f"Successfully caught expected error: {e}")

    try:
        print("\n[!] Attempting to draw with a negative dimension (should fail):")
        art_generator.draw_rectangle(-5, 5, "x")

    except (ValueError, TypeError) as e:
        print(f"Successfully caught expected error: {e}")


if __name__ == "__main__":
    main()
