
import math
from typing import Dict, Any

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class provides a collection of methods to draw geometric shapes like squares,
    rectangles, and pyramids using ASCII characters. It is designed with a focus on
    code quality, adhering to principles of modularity, readability, and safety
    by validating all user inputs.

    Attributes:
        None

    ISO/IEC 25010 Compliance Notes:
        - Functional Suitability: Provides correct shape-drawing functions as specified.
        - Performance Efficiency: Uses efficient string building techniques (`list.join`).
        - Reliability: Implements robust input validation to handle invalid arguments
          gracefully by raising descriptive errors.
        - Maintainability: Code is modular (validation is centralized), documented
          with docstrings, and uses clear variable names.
        - Testability: Methods are pure functions, returning predictable output for
          a given input, making them easy to unit test.
    """

    def _validate_inputs(self, symbol: str, **dimensions: Any) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper method centralizes input validation to ensure that the
        symbol and dimensions (width, height) meet the required criteria,
        promoting code reuse and maintainability (DRY principle).

        Args:
            symbol (str): The character to use for drawing.
            **dimensions: Keyword arguments for dimensions (e.g., width=5, height=10).

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if any dimension is not a positive integer.
            TypeError: If any dimension is not of type 'int'.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width (int): The width and height of the square. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII square.
        
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width)
        row = symbol * width
        rows = [row] * width
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width (int): The width of the rectangle. Must be a positive integer.
            height (int): The height of the rectangle. Must be a positive integer.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII rectangle.
        
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right relative to the
        row above it.

        Args:
            width (int): The width of the parallelogram's parallel sides.
            height (int): The height of the parallelogram.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII parallelogram.
        
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows = []
        for i in range(height):
            padding = " " * i
            content = symbol * width
            rows.append(padding + content)
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner towards the bottom-right. The
        width of each row is calculated to create a straight hypotenuse from the
        top-left to the bottom-right of the specified bounding box.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII triangle.
        
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row to approximate a
            # straight line for the hypotenuse.
            # (i + 1) is the current row number (1-indexed).
            # We use math.ceil to ensure the shape is filled and the base has the correct width.
            num_symbols = math.ceil((i + 1) * width / height)
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII pyramid.
        
        Raises:
            ValueError, TypeError: Propagated from input validation.
        """
        self._validate_inputs(symbol, height=height)
        rows = []
        # The width of the pyramid's base is 2 * height - 1
        for i in range(height):
            # Number of symbols in the current row (1, 3, 5, ...)
            num_symbols = 2 * i + 1
            # Calculate padding to center the symbols
            padding_size = height - 1 - i
            padding = " " * padding_size
            rows.append(padding + (symbol * num_symbols))
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    artist = AsciiArt()
    
    print("--- ASCII Art Generator ---")

    try:
        print("\nSquare (5x5, '#'):")
        print(artist.draw_square(5, "#"))

        print("\nRectangle (8x4, '*'):")
        print(artist.draw_rectangle(8, 4, "*"))

        print("\nParallelogram (10x5, '='):")
        print(artist.draw_parallelogram(10, 5, "="))

        print("\nRight-Angled Triangle (width=7, height=7, '+'):")
        print(artist.draw_triangle(7, 7, "+"))
        
        print("\nScaled Right-Angled Triangle (width=15, height=5, 'A'):")
        print(artist.draw_triangle(15, 5, "A"))

        print("\nPyramid (height=6, '^'):")
        print(artist.draw_pyramid(6, "^"))
        
        # --- Demonstration of Error Handling ---
        print("\n--- Testing Error Handling ---")
        
        print("\nTesting invalid symbol (multi-char):")
        try:
            artist.draw_square(3, "@@")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        print("\nTesting invalid dimension (negative):")
        try:
            artist.draw_rectangle(-5, 5, "%")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("\nTesting invalid dimension type (float):")
        try:
            artist.draw_pyramid(4.5, "$") # type: ignore
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

