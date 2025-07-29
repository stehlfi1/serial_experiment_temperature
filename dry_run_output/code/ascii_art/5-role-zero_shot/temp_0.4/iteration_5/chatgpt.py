
from typing import Any


class AsciiArt:
    """
    A class for generating various filled ASCII art shapes.
    Provides methods to draw squares, rectangles, parallelograms, triangles, and pyramids.

    Methods raise exceptions on invalid input for reliability and robustness per ISO/IEC 25010 requirements.
    """

    def _validate_dimensions(self, width: int = None, height: int = None) -> None:
        """
        Validates that width and height (when supplied) are positive integers.

        Raises:
            ValueError: If any dimension is less than 1.
            TypeError: If any dimension is not an integer.
        """
        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer.")
            if width < 1:
                raise ValueError("Width must be at least 1.")
        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
            if height < 1:
                raise ValueError("Height must be at least 1.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that symbol is a single, non-whitespace printable character.

        Raises:
            ValueError: If symbol is not a single, non-whitespace, printable character.
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
        Draws a square of the given width, filled with the supplied symbol.

        Args:
            width: The width and height of the square (must be > 0).
            symbol: The fill symbol, must be a single printable non-whitespace character.

        Returns:
            A string representing the square.
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)

        lines = []
        for _ in range(width):
            line = symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height, filled with symbol.

        Args:
            width: The width of the rectangle (must be > 0).
            height: The height of the rectangle (must be > 0).
            symbol: The fill symbol.

        Returns:
            A string representing the rectangle.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        lines = []
        for _ in range(height):
            line = symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram growing diagonally to the right,
        each row is shifted by one extra space.

        Args:
            width: Width of each row (must be > 0).
            height: Number of rows (must be > 0).
            symbol: The fill symbol.

        Returns:
            A string representing the parallelogram.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            spaces = " " * row
            line = f"{spaces}{symbol * width}"
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle growing to the right,
        where the height and width determine the sides of the triangle.

        Args:
            width: The base of the triangle (must be > 0).
            height: The height of the triangle (must be > 0).
            symbol: The fill symbol.

        Returns:
            A string representing the triangle.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            num_symbols = ((row + 1) * width) // height
            num_symbols = max(1, num_symbols)
            if row == height - 1:
                num_symbols = width  # Ensure the base is fully filled
            line = symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled pyramid of a given height, centered.

        Args:
            height: The number of rows in the pyramid (must be > 0).
            symbol: The fill symbol.

        Returns:
            A string representing the pyramid.
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)

        width = 2 * height - 1
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            spaces = (width - num_symbols) // 2
            line = " " * spaces + symbol * num_symbols + " " * spaces
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    # Example manual tests
    art = AsciiArt()

    print("Square:\n")
    print(art.draw_square(4, "#"))

    print("\nRectangle:\n")
    print(art.draw_rectangle(6, 3, "*"))

    print("\nParallelogram:\n")
    print(art.draw_parallelogram(5, 4, "@"))

    print("\nTriangle:\n")
    print(art.draw_triangle(5, 4, "+"))

    print("\nPyramid:\n")
    print(art.draw_pyramid(5, "$"))
