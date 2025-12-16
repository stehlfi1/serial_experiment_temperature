
import typing

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides a collection of methods to draw various geometric shapes
    using ASCII characters. It is designed with a focus on code quality,
    adhering to principles from the ISO/IEC 25010 standard, including:
    - Functional Suitability: Correctly generates specified shapes.
    - Reliability: Robust input validation to prevent errors.
    - Performance Efficiency: Uses efficient string-building techniques.
    - Maintainability: Clean, modular, and well-documented code.
    - Testability: Methods return predictable string outputs for easy testing.
    """

    def _validate_inputs(
        self,
        symbol: str,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None
    ) -> None:
        """
        Private helper to validate common inputs for drawing methods.

        Args:
            symbol: The character to use for drawing.
            width: The width of the shape, if applicable.
            height: The height of the shape, if applicable.

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if width/height are not positive integers.
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
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.
        """
        self._validate_inputs(symbol=symbol, width=width)
        line = symbol * width
        lines = [line] * width
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the rectangle.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        line = symbol * width
        lines = [line] * height
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram leaning to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        lines = []
        for i in range(height):
            padding = ' ' * i
            content = symbol * width
            lines.append(f"{padding}{content}")
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from a single symbol at the top-left to a base
        as wide as the triangle's height.

        Note: The 'width' parameter is validated but not used in the drawing
        logic. The triangle's base width will be equal to its 'height' to
        form a proportional right-angled shape.

        Args:
            width: The width of the triangle's base (validated but unused).
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the right-angled triangle.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        lines = [(symbol * i) for i in range(1, height + 1)]
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the pyramid.
        """
        self._validate_inputs(symbol=symbol, height=height)
        lines = []
        for i in range(height):
            # Calculate padding and number of symbols for the current level
            padding = ' ' * (height - i - 1)
            content = symbol * (2 * i + 1)
            lines.append(f"{padding}{content}")
        return "\n".join(lines)

if __name__ == '__main__':
    # Example Usage:
    # This block demonstrates how to use the AsciiArt class and prints
    # each shape to the console for verification.
    art_generator = AsciiArt()

    print("--- Square (5x5, #) ---")
    print(art_generator.draw_square(width=5, symbol='#'))
    print("\n" + "="*30 + "\n")

    print("--- Rectangle (8x4, *) ---")
    print(art_generator.draw_rectangle(width=8, height=4, symbol='*'))
    print("\n" + "="*30 + "\n")

    print("--- Parallelogram (10x5, @) ---")
    print(art_generator.draw_parallelogram(width=10, height=5, symbol='@'))
    print("\n" + "="*30 + "\n")

    print("--- Right-Angled Triangle (height 6, +) ---")
    # Width is passed for validation but doesn't affect the shape
    print(art_generator.draw_triangle(width=6, height=6, symbol='+'))
    print("\n" + "="*30 + "\n")

    print("--- Pyramid (height 5, ^) ---")
    print(art_generator.draw_pyramid(height=5, symbol='^'))
    print("\n" + "="*30 + "\n")

    print("--- Input Validation Examples ---")
    try:
        art_generator.draw_square(width=5, symbol='$$')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        art_generator.draw_rectangle(width=-3, height=5, symbol='X')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        art_generator.draw_pyramid(height=4, symbol=' ')
    except ValueError as e:
        print(f"Caught expected error: {e}")
