
"""
ascii_art.py

A console-based ASCII Art generator implementing:
- Square
- Rectangle
- Parallelogram
- Right-angled Triangle
- Pyramid

Meets ISO/IEC 25010 software quality requirements.
"""

from typing import Any


class AsciiArt:
    """
    AsciiArt provides methods to generate various ASCII geometric shapes as multi-line strings.

    Public Methods
    --------------
    draw_square(width: int, symbol: str) -> str
        Draw a filled square of given width using the specified symbol.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draw a filled rectangle of given width and height using the specified symbol.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draw a filled parallelogram (rows shifted) of given width and height.

    draw_triangle(width: int, height: int, symbol: str) -> str
        Draw a filled right-angled triangle with specified width and height.

    draw_pyramid(height: int, symbol: str) -> str
        Draw a filled symmetrical pyramid of specified height.
    """

    def _validate_positive_int(self, value: Any, name: str) -> None:
        """
        Validate that the given value is a positive integer (> 0).

        Raises
        ------
        ValueError
            If the value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate that the symbol is a single printable, non-whitespace character.

        Raises
        ------
        ValueError
            If the symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square as ASCII art.

        Parameters
        ----------
        width : int
            Width (and height) of the square. Must be > 0.
        symbol : str
            Fill character. Must be a single printable non-whitespace character.

        Returns
        -------
        str
            Multi-line string representing the filled square.

        Raises
        ------
        ValueError, TypeError
            For invalid argument values.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        # Each row is width symbols; there are width rows.
        row = symbol * width
        art_lines = [row for _ in range(width)]
        return "\n".join(art_lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle as ASCII art.

        Parameters
        ----------
        width : int
            Width of the rectangle. Must be > 0.
        height : int
            Height of the rectangle. Must be > 0.
        symbol : str
            Fill character. Must be a single printable non-whitespace character.

        Returns
        -------
        str
            Multi-line string representing the filled rectangle.

        Raises
        ------
        ValueError, TypeError
            For invalid argument values.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        art_lines = [row for _ in range(height)]
        return "\n".join(art_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram as ASCII art.

        Each row is shifted right by one space compared to the previous row, starting from no shift.

        Parameters
        ----------
        width : int
            Width of the parallelogram. Must be > 0.
        height : int
            Height of the parallelogram. Must be > 0.
        symbol : str
            Fill character. Must be a single printable non-whitespace character.

        Returns
        -------
        str
            Multi-line string representing the filled parallelogram.

        Raises
        ------
        ValueError, TypeError
            For invalid argument values.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        art_lines = []
        for row_idx in range(height):
            shift = row_idx
            art_lines.append(" " * shift + symbol * width)
        return "\n".join(art_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle as ASCII art.

        The right angle is at the top-left corner. The base and height are `width` and `height`.

        Each row i (0-based) has: num_symbols = 1 + (width - 1) * i // (height - 1)
        For height == 1, draws a single symbol.

        Parameters
        ----------
        width : int
            Width of the triangle's base. Must be > 0.
        height : int
            Height of the triangle. Must be > 0.
        symbol : str
            Fill character. Must be a single printable non-whitespace character.

        Returns
        -------
        str
            Multi-line string representing the filled right-angled triangle.

        Raises
        ------
        ValueError, TypeError
            For invalid argument values.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        art_lines = []
        if height == 1:
            # Special case: single row of width 1
            art_lines.append(symbol)
        else:
            for row_idx in range(height):
                # Calculate the filled width for this row, rounding up as the last row should have 'width' symbols
                if height == 1:
                    row_width = width
                else:
                    row_width = 1 + (width - 1) * row_idx // (height - 1)
                art_lines.append(symbol * row_width)
        return "\n".join(art_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid as ASCII art.

        The base is at the bottom, centered horizontally. The number of symbols in each row increases from
        1 at the top to (2*height - 1) at the bottom.

        Parameters
        ----------
        height : int
            Number of rows in the pyramid. Must be > 0.
        symbol : str
            Fill character. Must be a single printable non-whitespace character.

        Returns
        -------
        str
            Multi-line string representing the filled pyramid.

        Raises
        ------
        ValueError, TypeError
            For invalid argument values.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        art_lines = []
        base_width = 2 * height - 1
        for row_idx in range(height):
            num_symbols = 2 * row_idx + 1
            num_spaces = height - row_idx - 1
            line = (" " * num_spaces) + (symbol * num_symbols) + (" " * num_spaces)
            art_lines.append(line)
        return "\n".join(art_lines)


# Example test cases (remove or adjust for actual production/test use)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square (width=5, '*'):")
    print(art.draw_square(5, '*'))
    print("\nRectangle (width=7, height=3, '#'):")
    print(art.draw_rectangle(7, 3, '#'))
    print("\nParallelogram (width=6, height=4, 'A'):")
    print(art.draw_parallelogram(6, 4, 'A'))
    print("\nRight-angled Triangle (width=5, height=4, '+'):")
    print(art.draw_triangle(5, 4, '+'))
    print("\nPyramid (height=4, 'O'):")
    print(art.draw_pyramid(4, 'O'))
