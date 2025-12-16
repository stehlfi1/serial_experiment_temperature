
import math
from typing import Dict

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a collection of methods to draw filled, geometric shapes
    using a specified character. It adheres to high-quality code standards,
    including robust input validation, efficiency, and clear documentation.
    """

    def _validate_inputs(self, symbol: str, dimensions: Dict[str, int]) -> None:
        """
        Private helper to validate symbol and dimension inputs.

        This method centralizes input validation to ensure that all drawing
        methods are safe from invalid arguments, promoting code reuse and
        reliability.

        Args:
            symbol: The character to be used for drawing.
            dimensions: A dictionary containing dimension names (e.g., 'width')
                        and their integer values.

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single character, is whitespace,
                        or if a dimension is not a positive integer.
        """
        # Validate symbol
        if not isinstance(symbol, str):
            raise TypeError("The 'symbol' must be a string.")
        if len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        # Validate dimensions
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The '{name}' dimension must be an integer.")
            if value <= 0:
                raise ValueError(f"The '{name}' dimension must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII square.

        Raises:
            TypeError, ValueError: via _validate_inputs.

        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '#'))
            ###
            ###
            ###
        """
        self._validate_inputs(symbol, {'width': width})
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.

        Raises:
            TypeError, ValueError: via _validate_inputs.

        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(5, 3, '*'))
            *****
            *****
            *****
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that slants to the right.

        Each subsequent row is shifted one space to the right compared to the
        previous one.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII parallelogram.

        Raises:
            TypeError, ValueError: via _validate_inputs.

        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(4, 3, '%'))
            %%%%
             %%%%
              %%%%
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        rows = [' ' * i + symbol * width for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner, fitting within the
        specified width and height bounding box. The width of each row is
        calculated proportionally.

        Args:
            width: The final width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII triangle.

        Raises:
            TypeError, ValueError: via _validate_inputs.

        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(5, 5, '+'))
            +
            ++
            +++
            ++++
            +++++
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        rows = []
        for i in range(height):
            # Calculate proportional width for the current row
            # Use math.ceil to ensure the shape is filled and grows correctly
            current_width = math.ceil((i + 1) * width / height)
            rows.append(symbol * current_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII pyramid.

        Raises:
            TypeError, ValueError: via _validate_inputs.

        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_inputs(symbol, {'height': height})
        rows = []
        for i in range(height):
            padding_size = height - 1 - i
            symbol_count = 2 * i + 1
            padding = ' ' * padding_size
            symbols = symbol * symbol_count
            rows.append(padding + symbols)
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    art_maker = AsciiArt()
    print("--- ASCII Art Generator ---")

    # --- Valid Examples ---
    print("\n1. Square (4x4, symbol: '#')")
    print(art_maker.draw_square(4, '#'))

    print("\n2. Rectangle (6x3, symbol: '=')")
    print(art_maker.draw_rectangle(6, 3, '='))

    print("\n3. Parallelogram (5x4, symbol: '@')")
    print(art_maker.draw_parallelogram(5, 4, '@'))

    print("\n4. Right-Angled Triangle (width=7, height=7, symbol: 'T')")
    print(art_maker.draw_triangle(7, 7, 'T'))

    print("\n5. Asymmetrical Right-Angled Triangle (width=10, height=4, symbol: '>')")
    print(art_maker.draw_triangle(10, 4, '>'))

    print("\n6. Pyramid (height=5, symbol: 'A')")
    print(art_maker.draw_pyramid(5, 'A'))

    # --- Invalid Input Examples (Error Handling) ---
    print("\n--- Testing Error Handling ---")
    try:
        art_maker.draw_square(5, '@@')
    except ValueError as e:
        print(f"Caught expected error for multi-character symbol: {e}")

    try:
        art_maker.draw_rectangle(-3, 5, '*')
    except ValueError as e:
        print(f"Caught expected error for negative width: {e}")

    try:
        art_maker.draw_pyramid(0, '*')
    except ValueError as e:
        print(f"Caught expected error for zero height: {e}")

    try:
        art_maker.draw_triangle(5, 5.5, '$')
    except TypeError as e:
        print(f"Caught expected error for non-integer dimension: {e}")

    try:
        art_maker.draw_square(4, ' ')
    except ValueError as e:
        print(f"Caught expected error for whitespace symbol: {e}")
