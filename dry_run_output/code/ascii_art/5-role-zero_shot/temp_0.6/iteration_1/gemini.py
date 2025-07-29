
import math
from typing import Optional

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides methods to draw simple geometric shapes like squares,
    rectangles, and pyramids using a specified character. It adheres to
    high-quality coding standards, including input validation, clear
    documentation, and a modular design, in line with ISO/IEC 25010
    principles for software quality.

    Attributes:
        This class has no public attributes.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Provides correct shape-drawing functions.
    - Performance Efficiency: Uses efficient string-building techniques.
    - Maintainability: Code is modular, readable, and well-documented.
    - Reliability: Robust input validation prevents common errors.
    - Usability: A clear and consistent API for generating art.
    - Testability: Methods are pure functions, making them easy to unit test.
    """

    def _validate_inputs(
        self,
        symbol: str,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> None:
        """
        Validates common inputs for drawing methods.

        This private helper method centralizes input validation to ensure
        code is not duplicated (Modularity) and that all drawing methods
        are protected against invalid inputs (Safety).

        Args:
            symbol: The character to use for drawing.
            width: The width of the shape, if applicable.
            height: The height of the shape, if applicable.

        Raises:
            ValueError: If the symbol is not a single character, is whitespace,
                        or if width/height are not positive.
            TypeError: If width or height are not integers.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer.")
            if width <= 0:
                raise ValueError("Width must be a positive integer.")

        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
            if height <= 0:
                raise ValueError("Height must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method leverages the draw_rectangle method for its implementation,
        promoting code reuse and maintainability.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII square.
        """
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.
        """
        self._validate_inputs(symbol, width=width, height=height)

        row = symbol * width
        # Using a list comprehension and join is more memory-efficient
        # for large heights than repeated string concatenation.
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
            symbol: The character to use for drawing the parallelogram.

        Returns:
            A multi-line string representing the ASCII parallelogram.
        """
        self._validate_inputs(symbol, width=width, height=height)

        shape_segment = symbol * width
        rows = []
        for i in range(height):
            leading_spaces = " " * i
            rows.append(f"{leading_spaces}{shape_segment}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from a single point at the top-left to a base
        of the specified width. The number of symbols per row is scaled
        proportionally.

        Args:
            width: The final width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing the triangle.

        Returns:
            A multi-line string representing the ASCII triangle.
        """
        self._validate_inputs(symbol, width=width, height=height)

        rows = []
        for i in range(1, height + 1):
            # Calculate symbols for the current row, scaling proportionally.
            # math.ceil ensures the triangle grows steadily and the final
            # row has the correct width.
            num_symbols = math.ceil(i * width / height)
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.
        """
        self._validate_inputs(symbol, height=height)

        rows = []
        # The total width of the pyramid's base
        base_width = 2 * height - 1

        for i in range(height):
            num_symbols = 2 * i + 1
            # Center the symbols by adding leading spaces
            padding = (base_width - num_symbols) // 2
            leading_spaces = " " * padding
            rows.append(f"{leading_spaces}{symbol * num_symbols}")
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It serves as a basic visual test and example for consumers of the class.
    art_generator = AsciiArt()

    print("--- ASCII Art Generator ---")

    # --- Successful Cases ---
    print("\n1. Square (5x5, symbol '#')")
    print(art_generator.draw_square(width=5, symbol="#"))

    print("\n2. Rectangle (8x4, symbol '*')")
    print(art_generator.draw_rectangle(width=8, height=4, symbol="*"))

    print("\n3. Parallelogram (10x5, symbol '=')")
    print(art_generator.draw_parallelogram(width=10, height=5, symbol="="))

    print("\n4. Right-Angled Triangle (width=7, height=7, symbol 'T')")
    print(art_generator.draw_triangle(width=7, height=7, symbol="T"))

    print("\n5. Scaled Right-Angled Triangle (width=10, height=5, symbol 'A')")
    print(art_generator.draw_triangle(width=10, height=5, symbol="A"))

    print("\n6. Pyramid (height=6, symbol '^')")
    print(art_generator.draw_pyramid(height=6, symbol="^"))

    # --- Error Handling Cases ---
    print("\n--- Testing Error Handling ---")
    try:
        print("\nAttempting to draw with an invalid symbol (multi-character)...")
        art_generator.draw_square(5, "@@")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with a whitespace symbol...")
        art_generator.draw_square(5, " ")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with a negative width...")
        art_generator.draw_rectangle(-5, 5, "X")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with a non-integer height...")
        art_generator.draw_pyramid(height=4.5, symbol="$") # type: ignore
    except TypeError as e:
        print(f"Caught expected error: {e}")
