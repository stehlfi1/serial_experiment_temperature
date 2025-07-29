
"""
ascii_art.py

A console-based 2D ASCII Art application with shape-drawing features,
designed and implemented according to ISO/IEC 25010 quality standards.
"""

from typing import Any


class AsciiArt:
    """
    A class to draw various filled 2D ASCII art shapes using a specified symbol.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Returns a string representation of a filled square.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Returns a string representation of a filled rectangle.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Returns a string representation of a filled parallelogram.

    draw_triangle(width: int, height: int, symbol: str) -> str
        Returns a string representation of a filled right-angled triangle.

    draw_pyramid(height: int, symbol: str) -> str
        Returns a string representation of a filled, symmetrical pyramid.
    """

    def __init__(self) -> None:
        pass  # No state required; class used as namespace

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square with the given width and symbol.

        Parameters
        ----------
        width : int
            The width (and height) of the square. Must be >= 1.
        symbol : str
            Single, non-whitespace printable character to fill the square.

        Returns
        -------
        str
            Multiline string representation of the square.

        Raises
        ------
        ValueError
            If inputs are invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)
        return self._draw_filled_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle with the given width, height, and symbol.

        Parameters
        ----------
        width : int
            The width of the rectangle. Must be >= 1.
        height : int
            The height of the rectangle. Must be >= 1.
        symbol : str
            Single, non-whitespace printable character.

        Returns
        -------
        str
            Multiline string representation of the rectangle.

        Raises
        ------
        ValueError
            If inputs are invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        return self._draw_filled_rectangle(width, height, symbol)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram (each row shifted right) with the given dimensions.

        Parameters
        ----------
        width : int
            The width of the parallelogram (number of symbols per row). Must be >= 1.
        height : int
            The height (number of rows). Must be >= 1.
        symbol : str
            Single, non-whitespace printable character.

        Returns
        -------
        str
            Multiline string representing the parallelogram.

        Raises
        ------
        ValueError
            If inputs are invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled, right-angled triangle (top-left at (0,0)).

        Grows diagonally to the right. The bottom row length will not exceed width.

        Parameters
        ----------
        width : int
            Base width (horizontal length of the bottom row). Must be >= 1.
        height : int
            Height (number of rows). Must be >= 1.
        symbol : str
            Single, non-whitespace printable character.

        Returns
        -------
        str
            Multiline string representing the right-angled triangle.

        Raises
        ------
        ValueError
            If inputs are invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Determine number of symbols for row i (from top 0 to bottom height-1)
            num_symbols = min(width, ((i + 1) * width) // height)
            if num_symbols < 1:
                num_symbols = 1
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled, symmetrical pyramid with given height and symbol.

        Parameters
        ----------
        height : int
            The number of rows. Must be >= 1.
        symbol : str
            Single, non-whitespace printable character.

        Returns
        -------
        str
            Multiline string representing the pyramid.

        Raises
        ------
        ValueError
            If inputs are invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Row i (0-indexed): has (2*i + 1) symbols and centered
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            line = " " * num_spaces + symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

    # --- Private utility methods ---

    def _draw_filled_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Helper to return filled rectangle as multi-line string."""
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    @staticmethod
    def _validate_dimension(value: Any, name: str) -> None:
        """
        Validate that a dimension (width/height) is an integer >= 1.

        Raises
        ------
        ValueError
            If not valid.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer")
        if value < 1:
            raise ValueError(f"{name.capitalize()} must be >= 1")

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Validates that symbol is a single, non-whitespace printable character.

        Raises
        ------
        ValueError
            If not valid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")


# --------- Example Usage and Simple Tests ---------
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:")
    print(art.draw_square(4, "#"))
    print("\nRectangle:")
    print(art.draw_rectangle(6, 3, "*"))
    print("\nParallelogram:")
    print(art.draw_parallelogram(5, 4, "+"))
    print("\nTriangle:")
    print(art.draw_triangle(6, 4, "o"))
    print("\nPyramid:")
    print(art.draw_pyramid(5, "@"))
