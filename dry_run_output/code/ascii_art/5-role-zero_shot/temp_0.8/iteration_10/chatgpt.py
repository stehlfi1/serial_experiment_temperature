
"""
ascii_art.py

Implements ASCII art drawing using OOP principles,
adhering to ISO/IEC 25010 quality standards and best practices.
"""

from typing import Any


class AsciiArt:
    """
    Provides methods to render 2D ASCII shapes for console applications.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Draws a filled square of the given width with the specified symbol.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draws a filled rectangle of the given width and height.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draws a filled parallelogram (top-left aligned, shifted each row).

    draw_triangle(width: int, height: int, symbol: str) -> str
        Draws a filled right-angled triangle (top-left right angle).

    draw_pyramid(height: int, symbol: str) -> str
        Draws a filled, symmetrical pyramid.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of size width x width using the specified symbol.

        Parameters
        ----------
        width : int
            The width (and height) of the square. Must be >= 1.
        symbol : str
            The symbol to fill the square. Must be a single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art representation of the square.
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)

        line = symbol * width
        art_lines = [line for _ in range(width)]
        return "\n".join(art_lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of size width x height using the specified symbol.

        Parameters
        ----------
        width : int
            The width of the rectangle. Must be >= 1.
        height : int
            The height of the rectangle. Must be >= 1.
        symbol : str
            The symbol to fill the rectangle. Must be a single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art representation of the rectangle.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        line = symbol * width
        art_lines = [line for _ in range(height)]
        return "\n".join(art_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, left-aligned, each row shifted right by one space.

        Parameters
        ----------
        width : int
            The width of the parallelogram. Must be >= 1.
        height : int
            The number of rows. Must be >= 1.
        symbol : str
            The symbol to fill the parallelogram. Must be a single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art representation of the parallelogram.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        art_lines = []
        for row in range(height):
            spaces = " " * row
            art_lines.append(f"{spaces}{symbol * width}")
        return "\n".join(art_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle, right angle at top-left, growing to the right.

        Parameters
        ----------
        width : int
            The maximum width of the triangle base. Must be >= 1.
        height : int
            The height of the triangle. Must be >= 1.
        symbol : str
            The symbol to fill the triangle. Must be a single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art representation of the triangle.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        art_lines = []
        for row in range(height):
            # Calculate number of symbols for this row (linear scaling)
            symbols_in_row = max(1, round(width * (row + 1) / height))
            art_lines.append(symbol * symbols_in_row)
        return "\n".join(art_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Parameters
        ----------
        height : int
            The number of rows of the pyramid. Must be >= 1.
        symbol : str
            The symbol to fill the pyramid. Must be a single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art representation of the pyramid.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        art_lines = []
        for row in range(height):
            num_symbols = row * 2 + 1
            spaces = height - row - 1
            art_lines.append(" " * spaces + symbol * num_symbols)
        return "\n".join(art_lines)

    # --- Internal validation methods ---

    @staticmethod
    def _validate_positive_integer(value: Any, name: str) -> None:
        """
        Ensures the value is a positive integer.

        Raises
        ------
        TypeError
            If value is not an integer.
        ValueError
            If value is less than 1.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer (got {type(value).__name__})")
        if value < 1:
            raise ValueError(f"{name} must be >= 1 (got {value})")

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Ensures the symbol is a single, printable, non-whitespace character.

        Raises
        ------
        TypeError
            If symbol is not a string.
        ValueError
            If symbol is not a single, printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError(f"symbol must be a string (got {type(symbol).__name__})")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character")
        if symbol.isspace():
            raise ValueError("symbol must not be a whitespace character")
        if not symbol.isprintable():
            raise ValueError("symbol must be a printable character")


# --- Example usage (for testing) ---

if __name__ == "__main__":
    art = AsciiArt()
    print("Square:")
    print(art.draw_square(5, "#"))
    print("\nRectangle:")
    print(art.draw_rectangle(8, 3, "*"))
    print("\nParallelogram:")
    print(art.draw_parallelogram(6, 4, "+"))
    print("\nTriangle:")
    print(art.draw_triangle(7, 5, "@"))
    print("\nPyramid:")
    print(art.draw_pyramid(5, "$"))
