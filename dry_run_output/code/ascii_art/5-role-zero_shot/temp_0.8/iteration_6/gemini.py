
import math

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a suite of methods to draw common geometric shapes
    using a user-specified symbol. It is designed for reliability and
    maintainability, with robust input validation and clear, modular
    methods. This design aligns with the quality characteristics defined
    in the ISO/IEC 25010 standard.

    Methods:
        draw_square(width, symbol): Draws a solid square.
        draw_rectangle(width, height, symbol): Draws a solid rectangle.
        draw_parallelogram(width, height, symbol): Draws a solid parallelogram.
        draw_triangle(width, height, symbol): Draws a solid right-angled triangle.
        draw_pyramid(height, symbol): Draws a solid pyramid.
    """

    def _validate_inputs(self, symbol: str, dimensions: dict[str, int]) -> None:
        """
        Private helper method to validate common inputs for drawing functions.

        This method centralizes input validation to ensure code is not repeated
        (DRY principle), which improves maintainability and testability.

        Args:
            symbol (str): The character to use for drawing.
            dimensions (dict[str, int]): A dictionary mapping dimension names
                                         (e.g., 'width') to their integer values.

        Raises:
            TypeError: If a dimension is not an integer or the symbol is not a string.
            ValueError: If a dimension is non-positive, or if the symbol is not
                        a single, non-whitespace character.
        """
        # --- Symbol Validation (Reliability: Fault Tolerance) ---
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        # --- Dimension Validation (Reliability: Fault Tolerance) ---
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Generates a string representing a solid square.

        Args:
            width (int): The width and height of the square.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        
        Raises:
            TypeError, ValueError: Via _validate_inputs on invalid arguments.
        """
        self._validate_inputs(symbol, {'width': width})
        line = symbol * width
        # Performance: Using a list comprehension and join is efficient for building strings.
        lines = [line for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a string representing a solid rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            TypeError, ValueError: Via _validate_inputs on invalid arguments.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        line = symbol * width
        lines = [line for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a string for a parallelogram leaning to the right.
        Each subsequent row is shifted one space to the right.

        Args:
            width (int): The width of the parallelogram's parallel sides.
            height (int): The height of the parallelogram.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            TypeError, ValueError: Via _validate_inputs on invalid arguments.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        lines = []
        shape_segment = symbol * width
        for i in range(height):
            padding = ' ' * i
            lines.append(f"{padding}{shape_segment}")
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a string for a right-angled triangle.

        The triangle grows from the top-left, fitting within the specified
        width and height. The number of symbols per row increases linearly.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            TypeError, ValueError: Via _validate_inputs on invalid arguments.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        lines = []
        for i in range(height):
            # Correctness: Calculate symbols per row based on progress through height.
            # `max(1, ...)` ensures the first row is never empty.
            # `round(...)` creates a visually smoother triangle for various ratios.
            num_symbols = max(1, round((i + 1) * width / height))
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Generates a string representing a symmetrical, solid pyramid.

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            TypeError, ValueError: Via _validate_inputs on invalid arguments.
        """
        self._validate_inputs(symbol, {'height': height})
        lines = []
        for i in range(height):
            # Readability: Clear variable names for pyramid logic.
            num_symbols = 2 * i + 1
            padding_size = height - 1 - i
            padding = ' ' * padding_size
            lines.append(f"{padding}{symbol * num_symbols}")
        return "\n".join(lines)


def main():
    """
    Main function to demonstrate the capabilities of the AsciiArt class.
    This also serves as a simple manual test suite.
    """
    # Testability: The class is easy to instantiate and use.
    art_generator = AsciiArt()
    print("--- ASCII Art Generator Demo ---")

    try:
        # --- Valid Shape Demonstrations ---
        print("\n[1] Square (5x5, symbol '#')")
        print(art_generator.draw_square(5, '#'))

        print("\n[2] Rectangle (8x4, symbol '*')")
        print(art_generator.draw_rectangle(8, 4, '*'))

        print("\n[3] Parallelogram (10x5, symbol '=')")
        print(art_generator.draw_parallelogram(10, 5, '='))
        
        print("\n[4] Right-Angled Triangle (6x6, symbol '+')")
        print(art_generator.draw_triangle(6, 6, '+'))

        print("\n[5] Right-Angled Triangle (10x5, symbol 'T') - Ratio example")
        print(art_generator.draw_triangle(10, 5, 'T'))

        print("\n[6] Pyramid (height 6, symbol '^')")
        print(art_generator.draw_pyramid(6, '^'))

        # --- Error Handling Demonstrations ---
        print("\n--- Error Handling Tests ---")

        print("\n[7] Testing invalid dimension (negative width)...")
        try:
            art_generator.draw_square(-3, 'X')
        except ValueError as e:
            print(f"   Successfully caught expected error: {e}")

        print("\n[8] Testing invalid symbol (multi-character)...")
        try:
            art_generator.draw_rectangle(5, 5, '@@')
        except ValueError as e:
            print(f"   Successfully caught expected error: {e}")
            
        print("\n[9] Testing invalid symbol (whitespace)...")
        try:
            art_generator.draw_pyramid(5, ' ')
        except ValueError as e:
            print(f"   Successfully caught expected error: {e}")

        print("\n[10] Testing invalid type for dimension...")
        try:
            art_generator.draw_rectangle(5, 'four', '*')
        except TypeError as e:
            print(f"   Successfully caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

if __name__ == "__main__":
    main()
