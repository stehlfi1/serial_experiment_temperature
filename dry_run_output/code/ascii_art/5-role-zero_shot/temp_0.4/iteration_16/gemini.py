
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods for drawing
various geometric shapes using text characters. The implementation prioritizes
code quality, maintainability, and adherence to software engineering best
practices as outlined by ISO/IEC 25010.

Key quality characteristics addressed:
- Functional Suitability: Correctly generates the specified shapes.
- Performance Efficiency: Uses efficient string-building techniques.
- Reliability: Robust input validation prevents crashes from invalid data.
- Usability: A clear and consistent API with helpful error messages.
- Maintainability: Code is modular, readable, and well-documented.
- Portability: Uses only standard Python libraries for cross-platform compatibility.
"""


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a suite of methods to draw simple geometric shapes like
    squares, rectangles, and pyramids using a specified character. It is designed
    for clarity, efficiency, and robustness, with comprehensive input validation
    to ensure safe and predictable behavior.
    """

    @staticmethod
    def _validate_drawing_inputs(symbol: str, **dimensions: int) -> None:
        """
        Private helper to validate common inputs for drawing methods.

        This method centralizes input validation to ensure that the symbol and
        dimensional parameters meet the required criteria, promoting code reuse
        and safety (Reliability, Maintainability).

        Args:
            symbol: The character to use for drawing.
            dimensions: A keyword dictionary of dimension names (e.g., 'width')
                        and their integer values.

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single character, is whitespace,
                        or if any dimension is not a positive integer.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        This method leverages the draw_rectangle method, showcasing code reuse
        and adhering to the Don't Repeat Yourself (DRY) principle.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the ASCII square.

        Raises:
            TypeError, ValueError: Via _validate_drawing_inputs.
        """
        # Validation is handled by the called method.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        This implementation is performance-efficient, creating a list of strings
        and joining them at the end, which is faster than repeated string
        concatenation in a loop.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.

        Raises:
            TypeError, ValueError: Via _validate_drawing_inputs.
        """
        self._validate_drawing_inputs(symbol, width=width, height=height)
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram leaning to the right.

        Each subsequent row is indented by one additional space to create the
        skewed effect.

        Args:
            width: The width of the parallelogram's top and bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the ASCII parallelogram.

        Raises:
            TypeError, ValueError: Via _validate_drawing_inputs.
        """
        self._validate_drawing_inputs(symbol, width=width, height=height)
        shape_row = symbol * width
        rows = [" " * i + shape_row for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from a single symbol at the top-left to a base
        of the specified width. The slope is determined by both width and height,
        calculated using linear interpolation for a smooth appearance.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the ASCII triangle.

        Raises:
            TypeError, ValueError: Via _validate_drawing_inputs.
        """
        self._validate_drawing_inputs(symbol, width=width, height=height)

        if height == 1:
            return symbol * width

        rows = []
        for i in range(height):
            # Linearly interpolate the number of symbols for the current row.
            # This ensures the base has the correct width and the slope is
            # distributed as evenly as possible.
            num_symbols = round(1 + i * (width - 1) / (height - 1))
            rows.append(symbol * num_symbols)

        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        The pyramid has a height as specified, and its width is determined
        by the height. The algorithm correctly calculates padding and symbol
        count for each level to create a symmetrical shape.

        Args:
            height: The height of the pyramid (number of rows).
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.

        Raises:
            TypeError, ValueError: Via _validate_drawing_inputs.
        """
        self._validate_drawing_inputs(symbol, height=height)
        rows = []
        for i in range(height):
            padding = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            rows.append(padding + symbols)
        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It is executed only when the script is run directly, making the class
    # importable without running demo code. (Testability)
    
    art_generator = AsciiArt()
    symbol = "*"

    print("--- ASCII Art Generator Demo ---")

    try:
        print("\n[ Square (5x5) ]")
        print(art_generator.draw_square(5, symbol))

        print("\n[ Rectangle (8x4) ]")
        print(art_generator.draw_rectangle(8, 4, symbol))

        print("\n[ Parallelogram (10x5) ]")
        print(art_generator.draw_parallelogram(10, 5, "#"))

        print("\n[ Triangle (width=12, height=6) ]")
        print(art_generator.draw_triangle(12, 6, "A"))

        print("\n[ Pyramid (height=7) ]")
        print(art_generator.draw_pyramid(7, "O"))

        print("\n--- Testing Error Handling ---")

        print("\nTesting invalid symbol (multi-character)...")
        try:
            art_generator.draw_square(5, "@@")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\nTesting invalid dimension (negative)...")
        try:
            art_generator.draw_rectangle(-5, 5, symbol)
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("\nTesting invalid type...")
        try:
            art_generator.draw_pyramid(5.5, symbol) # type: ignore
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during the demo: {e}")

