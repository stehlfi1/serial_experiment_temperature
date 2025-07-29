
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements an interface for
drawing various geometric shapes using ASCII characters. It is designed with a
focus on code quality, adhering to the principles of the ISO/IEC 25010 standard,
including correctness, performance efficiency, modularity, and safety.
"""

from typing import Optional


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a collection of methods to draw filled geometric shapes
    like squares, rectangles, and pyramids as multi-line strings. It ensures
    all inputs are validated for safety and correctness before drawing.

    Attributes:
        None
    """

    def _validate_inputs(
        self,
        symbol: str,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper method centralizes input validation to ensure
        symbols and dimensions are appropriate, promoting code reusability
        and maintainability (ISO/IEC 25010: Maintainability, Reliability).

        Args:
            symbol: The character to use for drawing.
            width: The width of the shape, if applicable.
            height: The height of the shape, if applicable.

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if dimensions are not positive integers.
            TypeError: If dimensions are not integers.
        """
        # Validate symbol
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        # Validate dimensions
        dimensions = {'width': width, 'height': height}
        for name, value in dimensions.items():
            if value is not None:
                if not isinstance(value, int):
                    raise TypeError(f"The '{name}' must be an integer.")
                if value <= 0:
                    raise ValueError(f"The '{name}' must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the ASCII square.

        Raises:
            ValueError: On invalid symbol or non-positive width.
            TypeError: If width is not an integer.
        """
        self._validate_inputs(symbol=symbol, width=width)
        row = symbol * width
        # Efficiently creates the multi-line string (ISO/IEC 25010: Performance)
        return "\n".join([row] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.

        Raises:
            ValueError: On invalid symbol or non-positive dimensions.
            TypeError: If dimensions are not integers.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        row = symbol * width
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the shape.

        Returns:
            A multi-line string representing the ASCII parallelogram.

        Raises:
            ValueError: On invalid symbol or non-positive dimensions.
            TypeError: If dimensions are not integers.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        rows = [
            ' ' * i + symbol * width
            for i in range(height)
        ]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner. For a non-distorted
        right-angled triangle, width must be equal to height.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the shape.

        Returns:
            A multi-line string representing the ASCII triangle.

        Raises:
            ValueError: If width and height are not equal, or on other
                        invalid inputs.
            TypeError: If dimensions are not integers.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        if width != height:
            raise ValueError(
                "For a right-angled triangle, 'width' must be equal to 'height'."
            )

        rows = [
            symbol * (i + 1)
            for i in range(height)
        ]
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.

        Raises:
            ValueError: On invalid symbol or non-positive height.
            TypeError: If height is not an integer.
        """
        self._validate_inputs(symbol=symbol, height=height)
        rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            padding = ' ' * (height - 1 - i)
            rows.append(f"{padding}{symbol * num_symbols}")
        return "\n".join(rows)


# --- Demonstration ---
# This block demonstrates the usage of the AsciiArt class and serves as a
# simple functional check. (ISO/IEC 25010: Testability, Usability)
if __name__ == "__main__":
    artist = AsciiArt()
    print("--- Welcome to the ASCII Art Generator ---\n")

    try:
        # --- Correct Usage Examples ---
        print("Square (5x5, '#'):")
        print(artist.draw_square(5, '#'))
        print("\n" + "="*40 + "\n")

        print("Rectangle (8x4, '*'):")
        print(artist.draw_rectangle(8, 4, '*'))
        print("\n" + "="*40 + "\n")

        print("Parallelogram (10x5, '+'):")
        print(artist.draw_parallelogram(10, 5, '+'))
        print("\n" + "="*40 + "\n")

        print("Right-Angled Triangle (height=6, '@'):")
        print(artist.draw_triangle(6, 6, '@'))
        print("\n" + "="*40 + "\n")

        print("Pyramid (height=7, '^'):")
        print(artist.draw_pyramid(7, '^'))
        print("\n" + "="*40 + "\n")

        # --- Error Handling Examples ---
        print("--- Testing Error Handling ---\n")

        print("Attempting to draw with an invalid symbol ('AB'):")
        try:
            artist.draw_square(3, "AB")
        except ValueError as e:
            print(f"Caught expected error: {e}\n")

        print("Attempting to draw with a negative width (-4):")
        try:
            artist.draw_rectangle(-4, 5, '%')
        except ValueError as e:
            print(f"Caught expected error: {e}\n")

        print("Attempting to draw a triangle with mismatched width/height (w=5, h=3):")
        try:
            artist.draw_triangle(5, 3, 'T')
        except ValueError as e:
            print(f"Caught expected error: {e}\n")

    except (ValueError, TypeError) as e:
        print(f"An unexpected error occurred: {e}")

