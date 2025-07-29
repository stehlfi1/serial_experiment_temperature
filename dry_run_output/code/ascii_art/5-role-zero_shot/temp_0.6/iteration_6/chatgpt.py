
"""
ascii_art.py

A console-based 2D ASCII Art application adhering to ISO/IEC 25010 quality attributes.
Implements square, rectangle, parallelogram, right-angled triangle, and pyramid drawing.

Author: [Your Name]
Date: [Current Date]
"""

from typing import Any


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    Provides methods to draw square, rectangle, parallelogram, right-angled triangle, and pyramid
    using a single printable symbol.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
    draw_rectangle(width: int, height: int, symbol: str) -> str
    draw_parallelogram(width: int, height: int, symbol: str) -> str
    draw_triangle(width: int, height: int, symbol: str) -> str
    draw_pyramid(height: int, symbol: str) -> str
    """

    def __init__(self) -> None:
        """Initialize the AsciiArt class."""
        pass  # No internal state required

    @staticmethod
    def _validate_positive_int(value: Any, name: str) -> None:
        """
        Validates that a value is a positive integer.

        Parameters
        ----------
        value : Any
            The value to validate.
        name : str
            The name of the parameter.

        Raises
        ------
        TypeError
            If value is not an integer.
        ValueError
            If value is not positive.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Validates that the symbol is a single, non-whitespace printable character.

        Parameters
        ----------
        symbol : Any
            The symbol to validate.

        Raises
        ------
        TypeError
            If symbol is not a string.
        ValueError
            If symbol is not a single, non-whitespace printable character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square using the specified symbol.

        Parameters
        ----------
        width : int
            The width and height of the square (must be positive).
        symbol : str
            The symbol used to draw the square (single printable character).

        Returns
        -------
        str
            The ASCII art representation of the square.

        Raises
        ------
        TypeError, ValueError
            For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified symbol.

        Parameters
        ----------
        width : int
            The width of the rectangle (must be positive).
        height : int
            The height of the rectangle (must be positive).
        symbol : str
            The symbol used to draw the rectangle (single printable character).

        Returns
        -------
        str
            The ASCII art representation of the rectangle.

        Raises
        ------
        TypeError, ValueError
            For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram using the specified symbol.

        The parallelogram grows diagonally to the right, starting from the top-left corner;
        each row is shifted by one space to the right.

        Parameters
        ----------
        width : int
            The width of the parallelogram (must be positive).
        height : int
            The height of the parallelogram (must be positive).
        symbol : str
            The symbol used to draw the parallelogram (single printable character).

        Returns
        -------
        str
            The ASCII art representation of the parallelogram.

        Raises
        ------
        TypeError, ValueError
            For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.

        The triangle grows diagonally to the right, starting from the top-left corner.
        The base is at the bottom; the right angle is at the top-left.

        Parameters
        ----------
        width : int
            The base width (maximum number of symbols in the bottom row, must be positive).
        height : int
            The height of the triangle (must be positive).
        symbol : str
            The symbol used to draw the triangle (single printable character).

        Returns
        -------
        str
            The ASCII art representation of the triangle.

        Raises
        ------
        TypeError, ValueError
            For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Compute line length proportional to height and width
            line_length = max(1, round((i + 1) * width / height))
            if line_length > width:
                line_length = width
            lines.append(symbol * line_length)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled, symmetrical pyramid using the specified symbol.

        Parameters
        ----------
        height : int
            The height of the pyramid (must be positive).
        symbol : str
            The symbol used to draw the pyramid (single printable character).

        Returns
        -------
        str
            The ASCII art representation of the pyramid.

        Raises
        ------
        TypeError, ValueError
            For invalid arguments.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


# Example usage and basic test cases
if __name__ == "__main__":
    art = AsciiArt()
    print("SQUARE:")
    print(art.draw_square(4, "#"))
    print("\nRECTANGLE:")
    print(art.draw_rectangle(6, 3, "*"))
    print("\nPARALLELOGRAM:")
    print(art.draw_parallelogram(5, 4, "@"))
    print("\nTRIANGLE:")
    print(art.draw_triangle(6, 4, "+"))
    print("\nPYRAMID:")
    print(art.draw_pyramid(5, "$"))
