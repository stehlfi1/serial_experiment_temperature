
import math

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class provides a collection of methods to draw geometric shapes
    using ASCII characters. It focuses on producing high-quality,
    maintainable, and reliable code by adhering to best practices,
    including robust input validation and clear documentation.

    Attributes:
        This class has no public attributes.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the symbol used for drawing.

        ISO/IEC 25010 Compliance:
        - Reliability (Maturity): Protects against invalid character inputs.
        - Usability (Error tolerance): Provides clear error messages.

        Args:
            symbol (str): The character to validate.

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
    def _validate_dimension(value: int, name: str = "dimension") -> None:
        """
        Validates a dimension (e.g., width, height).

        ISO/IEC 25010 Compliance:
        - Reliability (Maturity): Ensures dimensions are positive integers.
        - Usability (Error tolerance): Provides clear, named error messages.

        Args:
            value (int): The dimension value to validate.
            name (str): The name of the dimension for the error message.

        Raises:
            TypeError: If the dimension is not an integer.
            ValueError: If the dimension is not a positive integer (> 0).
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square. Must be > 0.
            symbol (str): The single, non-whitespace character to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        """
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        ISO/IEC 25010 Compliance:
        - Functional Suitability (Correctness): Accurately draws a rectangle.
        - Performance Efficiency (Time-behaviour): Uses efficient string and list
          operations (O(width * height)).

        Args:
            width (int): The width of the rectangle. Must be > 0.
            height (int): The height of the rectangle. Must be > 0.
            symbol (str): The single, non-whitespace character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is indented by one additional space.

        Args:
            width (int): The width of the parallelogram. Must be > 0.
            height (int): The height of the parallelogram. Must be > 0.
            symbol (str): The single, non-whitespace character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            indent = " " * i
            content = symbol * width
            rows.append(f"{indent}{content}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle's width grows linearly from top to bottom, fitting
        within the bounding box defined by `width` and `height`.

        Args:
            width (int): The width of the triangle's base. Must be > 0.
            height (int): The height of the triangle. Must be > 0.
            symbol (str): The single, non-whitespace character to use for drawing.

        Returns:
            str: A multi-line string representing the right-angled triangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Calculate the width of the current row based on linear growth.
            # Ensure at least one symbol is drawn per row.
            current_width = max(1, round((i + 1) * width / height))
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid. Must be > 0.
            symbol (str): The single, non-whitespace character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        # The full width of the pyramid's base is (2 * height - 1)
        for i in range(height):
            num_symbols = 2 * i + 1
            # Left padding to center the row
            padding = " " * (height - 1 - i)
            rows.append(f"{padding}{symbol * num_symbols}")
        return "\n".join(rows)


# --- Example Usage ---
# This block demonstrates how to use the AsciiArt class and its methods.
# It also serves as a basic visual test of the functionality.
if __name__ == "__main__":
    # ISO/IEC 25010 Compliance: Testability and Usability (Understandability)
    # The `if __name__ == "__main__"` block makes the file reusable as a module
    # while providing a clear entry point for demonstration or direct execution.

    artist = AsciiArt()
    print("--- ASCII Art Generator ---")

    try:
        # --- 1. Draw a Square ---
        print("\n[+] Drawing a 5x5 Square with '#':")
        square = artist.draw_square(width=5, symbol="#")
        print(square)

        # --- 2. Draw a Rectangle ---
        print("\n[+] Drawing a 10x4 Rectangle with '*':")
        rectangle = artist.draw_rectangle(width=10, height=4, symbol="*")
        print(rectangle)

        # --- 3. Draw a Parallelogram ---
        print("\n[+] Drawing a 12x5 Parallelogram with '=':")
        parallelogram = artist.draw_parallelogram(width=12, height=5, symbol="=")
        print(parallelogram)

        # --- 4. Draw a Right-Angled Triangle ---
        print("\n[+] Drawing a 10x5 Triangle with 'A':")
        triangle = artist.draw_triangle(width=10, height=5, symbol="A")
        print(triangle)

        # --- 5. Draw a Pyramid ---
        print("\n[+] Drawing a Pyramid of height 6 with 'O':")
        pyramid = artist.draw_pyramid(height=6, symbol="O")
        print(pyramid)
        
        # --- 6. Demonstrate Validation ---
        print("\n[+] Demonstrating validation by causing an error:")
        print("    Attempting to draw with a multi-character symbol 'XX'...")
        artist.draw_square(5, "XX")

    except (ValueError, TypeError) as e:
        print(f"\n[!] An error occurred as expected: {e}")
        print("    This demonstrates the application's input safety.")

