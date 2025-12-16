
"""
ascii_art.py

A console-based 2D ASCII Art application implementing OOP best practices and following ISO/IEC 25010 quality standards.
Provides a class for drawing various filled shapes using a user-selected, single printable symbol.

Author: [Your Name]
"""

from typing import Optional


class AsciiArt:
    """
    Class for generating ASCII representations of basic filled 2D shapes.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Draws a filled square shape.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draws a filled rectangle shape.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draws a filled parallelogram shape.

    draw_triangle(width: int, height: int, symbol: str) -> str
        Draws a filled right-angled triangle.

    draw_pyramid(height: int, symbol: str) -> str
        Draws a filled symmetrical pyramid.
    """

    def _validate_positive_int(self, value: int, name: str) -> None:
        """
        Validates that the given value is a positive integer.

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
        Validates that the given symbol is a single, printable, non-whitespace character.

        Raises
        ------
        ValueError
            If the symbol does not meet the criteria.
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a single printable, non-whitespace character.")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("symbol must be a printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square shape.

        Parameters
        ----------
        width : int
            The width (and height) of the square; must be a positive integer.
        symbol : str
            The symbol to fill the square with; must be a single printable non-whitespace character.

        Returns
        -------
        str
            A string representation of the square.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        row = symbol * width
        return "\n".join([row for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle shape.

        Parameters
        ----------
        width : int
            The width of the rectangle; must be a positive integer.
        height : int
            The height of the rectangle; must be a positive integer.
        symbol : str
            The symbol to fill the rectangle with; must be a single printable non-whitespace character.

        Returns
        -------
        str
            A string representation of the rectangle.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        return "\n".join([row for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram shape (each row shifted by one space to the right).

        Parameters
        ----------
        width : int
            The width of the parallelogram; must be a positive integer.
        height : int
            The height of the parallelogram; must be a positive integer.
        symbol : str
            The symbol to fill the parallelogram with; must be a single printable non-whitespace character.

        Returns
        -------
        str
            A string representation of the parallelogram.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            spaces = " " * row
            shape = symbol * width
            lines.append(f"{spaces}{shape}")
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle (grows to the right, starts at top left corner).

        Parameters
        ----------
        width : int
            The width (base) of the triangle; must be a positive integer.
        height : int
            The height of the triangle; must be a positive integer.
        symbol : str
            The symbol to fill the triangle with; must be a single printable non-whitespace character.

        Returns
        -------
        str
            A string representation of the triangle.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        # To make sure the right angle is on the top-left and grows diagonally to the right,
        # we linearly interpolate row length from width (top) to min(width, height) (bottom).
        for row in range(height):
            chars_in_row = min(width, (width * (row + 1)) // height)
            # Ensure at least 1 character in each row for valid shapes
            chars_in_row = max(1, chars_in_row)
            lines.append(symbol * chars_in_row)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid.

        Parameters
        ----------
        height : int
            The pyramid's height; must be a positive integer.
        symbol : str
            The symbol to fill the pyramid with; must be a single printable non-whitespace character.

        Returns
        -------
        str
            A string representation of the pyramid.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        max_width = 2 * height - 1
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = (max_width - num_symbols) // 2
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


# Example usage for manual/test runs (for testability and demonstration purposes)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n" + art.draw_square(5, "#"))
    print("\nRectangle:\n" + art.draw_rectangle(7, 3, "*"))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, "@"))
    print("\nRight-angled Triangle:\n" + art.draw_triangle(6, 4, "+"))
    print("\nPyramid:\n" + art.draw_pyramid(5, "$"))
