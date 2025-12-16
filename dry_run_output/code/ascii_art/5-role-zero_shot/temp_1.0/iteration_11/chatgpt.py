
"""
ASCII Art Drawing Application

This module provides the AsciiArt class, which allows generating various 2D ASCII art shapes
by following best practices, ensuring maintainability, testability, and adherence to software
quality standards such as ISO/IEC 25010.

Shapes supported:
- Square
- Rectangle
- Parallelogram
- Right-angled Triangle
- Pyramid

Author: Senior Software Developer
"""

class AsciiArt:
    """
    A class to generate 2D ASCII art shapes for console output.
    """

    def __init__(self):
        """
        No initialization required for ASCII art generation.
        """
        pass

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validate that the symbol is a single, non-whitespace, printable character.

        Raises:
            TypeError: If symbol is not a string.
            ValueError: If symbol is not a single, non-whitespace printable character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_dimension(value: int, name: str):
        """
        Validate that a given dimension is an integer > 0.

        Args:
            value: The value to validate.
            name: The name of the dimension.

        Raises:
            TypeError: If value is not an integer.
            ValueError: If value is not greater than 0.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be greater than 0.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square of given width using the specified symbol.

        Args:
            width: Width (and height) of the square.
            symbol: Single, non-whitespace printable character.

        Returns:
            Multi-line string representing the square.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        # Square: width by width grid, filled with symbol
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle of given width and height using the specified symbol.

        Args:
            width: Width of the rectangle.
            height: Height of the rectangle.
            symbol: Single, non-whitespace printable character.

        Returns:
            Multi-line string representing the rectangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram (growing diagonally right) of given width/height using the symbol.

        Each line starts with an increasing number of spaces.

        Args:
            width: Width of the parallelogram.
            height: Height of the parallelogram.
            symbol: Single, non-whitespace printable character.

        Returns:
            Multi-line string representing the parallelogram.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        # Each row is shifted right (0 to height-1 spaces)
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle (right angle at top-left, growing rightwards and down).

        The triangle fits within width and height. Each row i has min(width, i+1) symbols.

        Args:
            width: Width of the triangle's base.
            height: Height of the triangle.
            symbol: Single, non-whitespace printable character.

        Returns:
            Multi-line string representing the right-angled triangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        # Each row i: min(i + 1, width) symbols, starting from 1 up to min(width, height)
        lines = [symbol * min(i + 1, width) for i in range(height)]
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid of specified height, fully filled with the given symbol.

        Args:
            height: Height of the pyramid.
            symbol: Single, non-whitespace printable character.

        Returns:
            Multi-line string representing the pyramid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        # Pyramid: For line i (i from 0), print (height-1-i) spaces, then (2*i+1) symbols
        lines = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols + spaces)
        return "\n".join(lines)


# Example test usage (for demonstration and testability):
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n", art.draw_square(4, "*"), sep="")
    print("\nRectangle:\n", art.draw_rectangle(6, 3, "#"), sep="")
    print("\nParallelogram:\n", art.draw_parallelogram(5, 4, "@"), sep="")
    print("\nTriangle:\n", art.draw_triangle(5, 4, "+"), sep="")
    print("\nPyramid:\n", art.draw_pyramid(5, "$"), sep="")
