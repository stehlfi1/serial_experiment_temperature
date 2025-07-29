
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which offers a suite of methods
for creating various geometric shapes using ASCII characters. The implementation
focuses on correctness, efficiency, and maintainability, adhering to best
practices and the ISO/IEC 25010 standard for software quality.
"""

from typing import List


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a clean interface for drawing filled geometric shapes
    such as squares, rectangles, triangles, and pyramids. It ensures robust
    input validation to maintain safety and correctness.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the symbol used for drawing.

        Args:
            symbol: The character to validate.

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

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates a dimension (width or height).

        Args:
            value: The dimension value to validate.
            name: The name of the dimension (e.g., 'width', 'height').

        Raises:
            TypeError: If the dimension is not an integer.
            ValueError: If the dimension is not a positive integer (> 0).
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method leverages the draw_rectangle method for implementation,
        promoting code reuse and consistency.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.

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
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        # Use a list comprehension and str.join for efficient string building.
        rows = [row for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous row.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows: List[str] = []
        base_row = symbol * width
        for i in range(height):
            # Prepend padding that increases with each row.
            padding = " " * i
            rows.append(f"{padding}{base_row}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle's width scales proportionally with its height, starting
        from the top-left corner. The final row will have the specified width.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the right-angled triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows: List[str] = []
        for i in range(height):
            # Calculate the width of the current row proportionally.
            # The ratio (i + 1) / height determines the current row's scale.
            # We ensure the width is at least 1 and round for smooth scaling.
            current_width = max(1, round((i + 1) * (width / height)))
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows: List[str] = []
        # The width of the pyramid's base.
        base_width = (height * 2) - 1

        for i in range(height):
            # Calculate the number of symbols for the current level.
            num_symbols = (i * 2) + 1
            # Calculate the padding needed on each side for centering.
            padding = " " * ((base_width - num_symbols) // 2)
            row_content = symbol * num_symbols
            rows.append(f"{padding}{row_content}")
        return "\n".join(rows)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    This function serves as a simple client of the AsciiArt class,
    showcasing its capabilities and providing a visual check.
    """
    art_generator = AsciiArt()
    print("--- ASCII Art Generator Demo ---")

    try:
        print("\n[+] Drawing a 5x5 Square with '#':")
        print(art_generator.draw_square(5, "#"))

        print("\n[+] Drawing a 10x4 Rectangle with '*':")
        print(art_generator.draw_rectangle(10, 4, "*"))

        print("\n[+] Drawing a 12x5 Parallelogram with '=':")
        print(art_generator.draw_parallelogram(12, 5, "="))

        print("\n[+] Drawing a 15x7 Right-Angled Triangle with '+':")
        print(art_generator.draw_triangle(15, 7, "+"))

        print("\n[+] Drawing a 6-level Pyramid with '^':")
        print(art_generator.draw_pyramid(6, "^"))

        print("\n--- Testing Error Handling ---")
        print("\n[!] Attempting to draw with an invalid symbol (e.g., '@@'):")
        try:
            art_generator.draw_square(3, "@@")
        except ValueError as e:
            print(f"    Caught expected error: {e}")

        print("\n[!] Attempting to draw with a negative dimension (e.g., width=-4):")
        try:
            art_generator.draw_rectangle(-4, 5, "X")
        except ValueError as e:
            print(f"    Caught expected error: {e}")

        print("\n[!] Attempting to draw with a non-integer dimension:")
        try:
            art_generator.draw_pyramid(5.5, "O")
        except TypeError as e:
            print(f"    Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
