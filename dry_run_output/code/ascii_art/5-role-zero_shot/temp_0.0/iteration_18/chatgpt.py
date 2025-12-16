
"""
ascii_art.py

A console-based 2D ASCII Art application using OOP, adhering to ISO/IEC 25010 software quality standards.
Provides validated, maintainable API for drawing ASCII geometric shapes.

Author: (Your Name)
"""

from typing import Any


class AsciiArt:
    """
    A class for drawing 2D ASCII shapes on the console.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Draws a filled square with given width and symbol.
    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draws a filled rectangle.
    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draws a filled parallelogram, growing diagonally.
    draw_triangle(width: int, height: int, symbol: str) -> str
        Draws a filled right-angled triangle.
    draw_pyramid(height: int, symbol: str) -> str
        Draws a symmetrical pyramid.
    """

    def __validate_positive_int(self, value: Any, name: str) -> None:
        """
        Validates that 'value' is a positive (>=1) integer.

        Raises
        ------
        ValueError : if value is not a positive integer
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer (>=1); got {value!r}")

    def __validate_symbol(self, symbol: Any) -> None:
        """
        Validates that symbol is a single, non-whitespace, printable character.

        Raises
        ------
        ValueError : for invalid symbol
        """
        if (not isinstance(symbol, str) or 
            len(symbol) != 1 or 
            symbol.isspace() or 
            not symbol.isprintable()):
            raise ValueError(f"Symbol must be a single, printable, non-whitespace character; got {symbol!r}")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square.

        Parameters
        ----------
        width : int
            Width and height of the square (must be >=1).
        symbol : str
            Single character to use as fill.

        Returns
        -------
        str
            ASCII representation of the square.
        """
        self.__validate_positive_int(width, "width")
        self.__validate_symbol(symbol)

        row = symbol * width
        art = '\n'.join([row for _ in range(width)])
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle.

        Parameters
        ----------
        width : int
            Rectangle width (must be >=1).
        height : int
            Rectangle height (must be >=1).
        symbol : str
            Single character to use as fill.

        Returns
        -------
        str
            ASCII representation of the rectangle.
        """
        self.__validate_positive_int(width, "width")
        self.__validate_positive_int(height, "height")
        self.__validate_symbol(symbol)

        row = symbol * width
        art = '\n'.join([row for _ in range(height)])
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram (top-left starts, rows shift right).

        Parameters
        ----------
        width : int
            Width of the parallelogram (must be >=1).
        height : int
            Height of the parallelogram (must be >=1).
        symbol : str
            Fill symbol.

        Returns
        -------
        str
            ASCII parallelogram.
        """
        self.__validate_positive_int(width, "width")
        self.__validate_positive_int(height, "height")
        self.__validate_symbol(symbol)

        lines = []
        for i in range(height):
            line = (' ' * i) + (symbol * width)
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle (growing to the right and down).

        Parameters
        ----------
        width : int
            Maximum width at the base (must be >=1).
        height : int
            Number of rows (must be >=1).
        symbol : str
            Fill symbol.

        Returns
        -------
        str
            ASCII triangle.
        """
        self.__validate_positive_int(width, "width")
        self.__validate_positive_int(height, "height")
        self.__validate_symbol(symbol)

        lines = []
        for row in range(1, height + 1):
            num_symbols = max(1, (width * row) // height)
            # Clamp to max width (for exactness on boundary condition)
            num_symbols = min(num_symbols, width)
            lines.append(symbol * num_symbols)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical centered pyramid.

        Parameters
        ----------
        height : int
            Height of the pyramid (must be >=1).
        symbol : str
            Fill symbol.

        Returns
        -------
        str
            ASCII pyramid.
        """
        self.__validate_positive_int(height, "height")
        self.__validate_symbol(symbol)

        max_width = height * 2 - 1
        lines = []
        for i in range(1, height + 1):
            symbols = symbol * (2 * i - 1)
            spaces = ' ' * (height - i)
            line = f"{spaces}{symbols}{spaces}"
            lines.append(line)
        return '\n'.join(lines)


if __name__ == '__main__':
    # Example usage and simple test cases
    art = AsciiArt()

    print("Square 4x4 ('#'):")
    print(art.draw_square(4, "#"))
    print("\nRectangle 6x3 ('*'):")
    print(art.draw_rectangle(6, 3, "*"))
    print("\nParallelogram 5x4 ('+'):")
    print(art.draw_parallelogram(5, 4, "+"))
    print("\nTriangle width=7, height=5 ('$'):")
    print(art.draw_triangle(7, 5, "$"))
    print("\nPyramid height=5 ('@'):")
    print(art.draw_pyramid(5, "@"))

    # Input validation samples (uncomment to test exceptions)
    # art.draw_square(-1, '#')              # ValueError
    # art.draw_rectangle(5, 0, '$')         # ValueError
    # art.draw_pyramid(3, "ab")             # ValueError
    # art.draw_triangle(4, 3, " ")          # ValueError
