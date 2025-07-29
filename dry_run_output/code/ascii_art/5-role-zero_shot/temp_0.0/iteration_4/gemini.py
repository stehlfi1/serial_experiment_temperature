
import math
from typing import Optional

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class provides a collection of methods to draw simple geometric shapes
    using ASCII characters. It is designed with a focus on code quality,
    adhering to principles of modularity, safety, and readability as outlined
    in the ISO/IEC 25010 standard.

    Each drawing method validates its inputs to ensure correctness and prevent
    runtime errors from invalid arguments.
    """

    @staticmethod
    def _validate_inputs(
        symbol: str,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> None:
        """
        Validates the common inputs for drawing functions.

        This private helper method centralizes input validation to ensure
        consistency and reduce code duplication, contributing to the
        maintainability of the class.

        Args:
            symbol: The character to use for drawing.
            width: The width of the shape (if applicable).
            height: The height of the shape (if applicable).

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character.
            ValueError: If width or height (when provided) are not positive integers.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        if width is not None and (not isinstance(width, int) or width <= 0):
            raise ValueError("The 'width' must be a positive integer.")

        if height is not None and (not isinstance(height, int) or height <= 0):
            raise ValueError("The 'height' must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method provides a convenient way to draw a square, promoting
        code reuse by calling the more generic draw_rectangle method.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII square.
        """
        self._validate_inputs(symbol=symbol, width=width)
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        The implementation uses a list comprehension and string joining, which is
        an efficient way to build multi-line strings in Python.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is indented by one additional space to create the
        slanted effect.

        Args:
            width: The width of the parallelogram's top and bottom sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing the parallelogram.

        Returns:
            A multi-line string representing the ASCII parallelogram.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        shape_body = symbol * width
        rows = [" " * i + shape_body for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner. The width of each row is
        calculated proportionally to the overall width and height, using
        math.ceil to ensure the base reaches the full specified width.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing the triangle.

        Returns:
            A multi-line string representing the ASCII right-angled triangle.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            # Using ceil ensures a clean "stair-step" pattern and that the
            # final row (i = height - 1) has the correct width.
            current_width = math.ceil((i + 1) * (width / height))
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        The algorithm calculates the necessary padding for each row to center
        the pyramid. The pyramid's base width will be (2 * height - 1).

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.
        """
        self._validate_inputs(symbol=symbol, height=height)
        # The maximum width of the pyramid is at its base.
        max_width = 2 * height - 1
        rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            padding = (max_width - num_symbols) // 2
            rows.append(" " * padding + symbol * num_symbols)
        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It serves as a simple, informal test and example.
    # For formal verification, unit tests should be written.
    
    art_generator = AsciiArt()
    
    print("--- ASCII Art Shape Generator ---")

    try:
        print("\nSquare (5x5, symbol='S'):")
        print(art_generator.draw_square(width=5, symbol='S'))

        print("\nRectangle (8x4, symbol='R'):")
        print(art_generator.draw_rectangle(width=8, height=4, symbol='R'))

        print("\nParallelogram (10x5, symbol='P'):")
        print(art_generator.draw_parallelogram(width=10, height=5, symbol='P'))

        print("\nRight-Angled Triangle (width=7, height=7, symbol='T'):")
        print(art_generator.draw_triangle(width=7, height=7, symbol='T'))
        
        print("\nWide Right-Angled Triangle (width=12, height=6, symbol='W'):")
        print(art_generator.draw_triangle(width=12, height=6, symbol='W'))

        print("\nTall Right-Angled Triangle (width=6, height=12, symbol='L'):")
        print(art_generator.draw_triangle(width=6, height=12, symbol='L'))

        print("\nPyramid (height=6, symbol='^'):")
        print(art_generator.draw_pyramid(height=6, symbol='^'))

        # Example of error handling
        print("\n--- Testing Error Handling ---")
        print("Attempting to draw with an invalid symbol...")
        art_generator.draw_square(5, "@@")

    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print("\nAttempting to draw with a negative width...")
        art_generator.draw_rectangle(-5, 5, '*')
        
    except ValueError as e:
        print(f"Caught expected error: {e}")
