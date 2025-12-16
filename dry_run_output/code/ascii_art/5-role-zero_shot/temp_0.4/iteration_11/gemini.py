
import math
from typing import Dict, Any

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class provides a collection of methods to draw geometric shapes like
    squares, rectangles, and pyramids as multi-line strings. It emphasizes
    code quality, safety, and maintainability by adhering to principles
    outlined in ISO/IEC 25010.

    Attributes:
        None
    """

    @staticmethod
    def _validate_inputs(symbol: str, **dimensions: int) -> None:
        """
        Validates input parameters for drawing methods.

        This private static method centralizes input validation to ensure
        that dimensions are positive integers and the symbol is a single,
        printable, non-whitespace character. This promotes reliability and
        maintainability.

        Args:
            symbol: The character to use for drawing.
            **dimensions: A keyword dictionary of dimension names (e.g., 'width')
                          and their integer values.

        Raises:
            TypeError: If a dimension is not an integer or the symbol is not a string.
            ValueError: If a dimension is not positive, or if the symbol is
                        invalid (multi-character, whitespace, or non-printable).
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a printable, non-whitespace character.")

        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"Dimension '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"Dimension '{name}' must be a positive integer (> 0).")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.
        
        Raises:
            TypeError, ValueError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width)
        row = symbol * width
        rows = [row] * width
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the rectangle.
            
        Raises:
            TypeError, ValueError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.
            
        Raises:
            TypeError, ValueError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows = [f"{' ' * i}{symbol * width}" for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner, and its slope is
        determined by the overall width and height, creating a shape that
        fits within the specified bounding box.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the right-angled triangle.
            
        Raises:
            TypeError, ValueError: Propagated from input validation.
        """
        self._validate_inputs(symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row based on the
            # linear growth from 0 to the final width over the given height.
            # math.ceil ensures the shape is filled and grows correctly.
            current_width = math.ceil((i + 1) * width / height)
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        The pyramid has a height of `height` rows. The base of the pyramid
        has a width of (2 * height - 1) characters.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the pyramid.
            
        Raises:
            TypeError, ValueError: Propagated from input validation.
        """
        self._validate_inputs(symbol, height=height)
        rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            leading_spaces = height - 1 - i
            rows.append(f"{' ' * leading_spaces}{symbol * num_symbols}")
        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    # --- Correctness & Usability Demonstration ---
    # The API is clean and the output is as expected.
    
    art_generator = AsciiArt()
    
    print("--- Drawing a 5x5 Square with '#' ---")
    print(art_generator.draw_square(width=5, symbol='#'))
    print("\n" + "="*40 + "\n")

    print("--- Drawing a 7x4 Rectangle with '*' ---")
    print(art_generator.draw_rectangle(width=7, height=4, symbol='*'))
    print("\n" + "="*40 + "\n")

    print("--- Drawing a 10x5 Parallelogram with '%' ---")
    print(art_generator.draw_parallelogram(width=10, height=5, symbol='%'))
    print("\n" + "="*40 + "\n")

    print("--- Drawing a 10x5 Right-Angled Triangle with '@' ---")
    print(art_generator.draw_triangle(width=10, height=5, symbol='@'))
    print("\n" + "="*40 + "\n")
    
    print("--- Drawing a 5-level Pyramid with '^' ---")
    print(art_generator.draw_pyramid(height=5, symbol='^'))
    print("\n" + "="*40 + "\n")

    # --- Reliability & Safety Demonstration ---
    # The code handles invalid inputs gracefully by raising descriptive errors.
    
    print("--- Testing Invalid Inputs ---")
    try:
        art_generator.draw_square(width=-3, symbol='X')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        art_generator.draw_rectangle(width=5, height=3, symbol='&&')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        art_generator.draw_pyramid(height=4, symbol=' ')
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        art_generator.draw_triangle(width=5.5, height=3, symbol='T') # type: ignore
    except TypeError as e:
        print(f"Caught expected error: {e}")

