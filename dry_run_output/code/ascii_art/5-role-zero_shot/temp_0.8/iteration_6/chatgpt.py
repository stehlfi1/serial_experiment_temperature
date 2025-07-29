
from typing import Any


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes for the console.

    Provides methods to draw:
      - Square
      - Rectangle
      - Parallelogram
      - Right-angled Triangle
      - Pyramid

    Each shape is represented as a multi-line string and can be drawn with any
    printable single-character symbol.
    """

    def __init__(self) -> None:
        """Initialize the AsciiArt generator."""
        pass

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled ASCII square.

        Args:
            width (int): Width (and height) of the square, must be >= 1.
            symbol (str): Single, non-whitespace character to fill the square.

        Returns:
            str: The ASCII art string of the square.

        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)
        # Square: all sides are equal
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled ASCII rectangle.

        Args:
            width (int): Width of the rectangle, must be >= 1.
            height (int): Height of the rectangle, must be >= 1.
            symbol (str): Single, non-whitespace character.

        Returns:
            str: The ASCII art string of the rectangle.

        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        # Each line: symbol * width, repeated height times
        line = symbol * width
        lines = [line for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled ASCII parallelogram, growing diagonally to the right.

        Each row is shifted by one space right from the previous row.

        Args:
            width (int): Width of the parallelogram, >= 1.
            height (int): Height of the parallelogram, >= 1.
            symbol (str): Single, non-whitespace character.

        Returns:
            str: The ASCII art string of the parallelogram.

        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            line = " " * row + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled ASCII right-angled triangle (top-left angle).

        The triangle grows diagonally to the right, with rows increasing from 1 to width.

        Args:
            width (int): Width (base) of the triangle, >= 1.
            height (int): Height of the triangle, >= 1.
            symbol (str): Single, non-whitespace character.

        Returns:
            str: The ASCII art string of the triangle.

        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        # For each row, the number of symbols is determined by linear interpolation
        # from 1 (top) to width (bottom)
        lines = []
        for row in range(height):
            # Interpolate number of symbols for each row
            # Last row gets 'width', first row gets at least 1
            n_symbols = max(1, int(round(1 + (width - 1) * row / max(1, height - 1))))
            line = symbol * n_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled ASCII symmetrical pyramid.

        Args:
            height (int): Height of the pyramid, >= 1.
            symbol (str): Single, non-whitespace character.

        Returns:
            str: The ASCII art string of the pyramid.

        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            n_symbols = 2 * row + 1
            n_spaces = height - row - 1
            line = " " * n_spaces + symbol * n_symbols + " " * n_spaces
            lines.append(line)
        return "\n".join(lines)

    # --- Validation Helpers ---

    @staticmethod
    def _validate_positive_int(value: Any, name: str) -> None:
        """Raise ValueError if 'value' is not a positive integer."""
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer (>= 1); got {value!r}")

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """Raise ValueError if 'symbol' is not a single, non-whitespace printable character."""
        if not isinstance(symbol, str):
            raise ValueError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be whitespace.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")


# --- Example Usage and Simple Tests ---

if __name__ == "__main__":
    art = AsciiArt()

    print("Square (5):")
    print(art.draw_square(5, "#"))
    print("\nRectangle (7x3):")
    print(art.draw_rectangle(7, 3, "*"))
    print("\nParallelogram (5x4):")
    print(art.draw_parallelogram(5, 4, "@"))
    print("\nTriangle (6x4):")
    print(art.draw_triangle(6, 4, "+"))
    print("\nPyramid (5):")
    print(art.draw_pyramid(5, "$"))

    # Validation demonstration (uncomment to see exceptions)
    # art.draw_square(0, "*")        # Should raise ValueError
    # art.draw_rectangle(4, 3, "##") # Should raise ValueError
    # art.draw_pyramid(3, " ")       # Should raise ValueError
