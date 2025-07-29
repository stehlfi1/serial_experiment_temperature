
from typing import Optional


class AsciiArt:
    """
    A class for drawing filled ASCII 2D shapes.

    Provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a single, printable symbol.

    Methods validate their inputs and raise ValueError or TypeError
    for invalid arguments according to ISO/IEC 25010 quality standard requirements.

    All drawing methods return a multiline string representation of the ASCII art.
    """

    def _validate_positive_int(self, value: int, name: str) -> None:
        """
        Validate that a value is an integer and greater than zero.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be positive and greater than zero.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate that the symbol is a single, non-whitespace, printable character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width with the provided symbol.

        Args:
            width (int): Side length (> 0) of the square.
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the square.
        """
        self._validate_positive_int(width, "Width")
        self._validate_symbol(symbol)
        # Build square line by line
        line = symbol * width
        return "\n".join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of width x height with the provided symbol.

        Args:
            width (int): Rectangle width (> 0).
            height (int): Rectangle height (> 0).
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the rectangle.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, shifted by one space per row (top to bottom).

        Args:
            width (int): Horizontal size of the parallelogram (> 0).
            height (int): Number of rows (> 0).
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the parallelogram.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        # Each line is shifted right by its row index
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle (right angle at top-left),
        growing rightward. The base does not extend beyond width.

        Args:
            width (int): The maximum width (> 0).
            height (int): The height of the triangle (> 0).
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the triangle.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            count = min(width, (i + 1) * width // height)
            count = max(count, 1)
            lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid of specified height.

        Args:
            height (int): Height of the pyramid (> 0).
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: Multiline string representing the pyramid.
        """
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        width = height * 2 - 1  # base width
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            spaces = (width - num_symbols) // 2
            lines.append(" " * spaces + symbol * num_symbols + " " * spaces)
        return "\n".join(lines)


# Example usage (for manual testing/import):
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n", art.draw_square(4, "*"))
    print("\nRectangle:\n", art.draw_rectangle(5, 3, "#"))
    print("\nParallelogram:\n", art.draw_parallelogram(5, 4, "@"))
    print("\nTriangle:\n", art.draw_triangle(6, 4, "$"))
    print("\nPyramid:\n", art.draw_pyramid(5, "&"))
