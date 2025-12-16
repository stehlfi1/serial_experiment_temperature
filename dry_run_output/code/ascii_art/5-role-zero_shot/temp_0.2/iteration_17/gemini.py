
import math
from typing import List

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various geometric shapes using a specified
    character. It adheres to high-quality code standards, ensuring reliability,
    maintainability, and efficiency.

    Attributes:
        MAX_DIMENSION (int): A class-level constant to limit the maximum size
                             of shapes to prevent excessive memory usage.
    """

    MAX_DIMENSION: int = 100

    def _validate_inputs(self, symbol: str, *dimensions: int) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper ensures that the symbol is a single, non-whitespace
        character and that all provided dimensions (width, height) are positive
        integers within a safe limit.

        Args:
            symbol (str): The character to use for drawing.
            *dimensions (int): A variable number of integer dimensions to validate.

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If the symbol is invalid (not a single character, is
                        whitespace) or if any dimension is not a positive integer
                        or exceeds MAX_DIMENSION.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")

        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError(f"Dimension must be an integer, but got {type(dim).__name__}.")
            if dim <= 0:
                raise ValueError(f"Dimension must be positive, but got {dim}.")
            if dim > self.MAX_DIMENSION:
                raise ValueError(
                    f"Dimension {dim} exceeds the maximum allowed size of {self.MAX_DIMENSION}."
                )

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width (int): The width and height of the square.
            symbol (str): The character used to draw the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If width is not an integer.
        """
        self._validate_inputs(symbol, width)
        row = symbol * width
        art_lines = [row] * width
        return "\n".join(art_lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used to draw the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If width or height are not integers.
        """
        self._validate_inputs(symbol, width, height)
        row = symbol * width
        art_lines = [row] * height
        return "\n".join(art_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram leaning to the right.

        Each subsequent row is shifted one space to the right relative to the
        row above it.

        Args:
            width (int): The width of the parallelogram's top/bottom sides.
            height (int): The height of the parallelogram.
            symbol (str): The character used to draw the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If width or height are not integers.
        """
        self._validate_inputs(symbol, width, height)
        row_content = symbol * width
        art_lines = [" " * i + row_content for i in range(height)]
        return "\n".join(art_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle has a vertical left edge and grows towards the right,
        with the base at the bottom. The width of each row is scaled
        proportionally to its position.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character used to draw the triangle.

        Returns:
            str: A multi-line string representing the right-angled triangle.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If width or height are not integers.
        """
        self._validate_inputs(symbol, width, height)
        art_lines: List[str] = []
        for i in range(height):
            # Calculate the width of the current row proportionally.
            # Using math.ceil ensures the final row has the correct 'width'
            # and that each row has at least one symbol.
            current_width = math.ceil((i + 1) * width / height)
            art_lines.append(symbol * int(current_width))
        return "\n".join(art_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The character used to draw the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If height is not an integer.
        """
        self._validate_inputs(symbol, height)
        art_lines: List[str] = []
        for i in range(height):
            # For row `i` (0-indexed):
            # Number of symbols = 2*i + 1
            # Number of leading spaces = height - 1 - i
            num_symbols = 2 * i + 1
            num_spaces = height - 1 - i
            art_lines.append(" " * num_spaces + symbol * num_symbols)
        return "\n".join(art_lines)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    artist = AsciiArt()

    print("--- ASCII Art Generator ---")

    try:
        print("\nSquare (5x5, '#'):")
        print(artist.draw_square(5, "#"))

        print("\nRectangle (10x4, '*'):")
        print(artist.draw_rectangle(10, 4, "*"))

        print("\nParallelogram (8x5, '+'):")
        print(artist.draw_parallelogram(8, 5, "+"))

        print("\nRight-Angled Triangle (width=10, height=5, '^'):")
        print(artist.draw_triangle(10, 5, "^"))
        
        print("\nRight-Angled Triangle (width=7, height=7, 'T'):")
        print(artist.draw_triangle(7, 7, "T"))

        print("\nPyramid (height=6, 'O'):")
        print(artist.draw_pyramid(6, "O"))

        # Example of error handling
        print("\n--- Testing Error Handling ---")
        try:
            artist.draw_square(-5, "X")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            artist.draw_rectangle(10, 5, "&&")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        try:
            artist.draw_pyramid(200, "$")
        except ValueError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}")

