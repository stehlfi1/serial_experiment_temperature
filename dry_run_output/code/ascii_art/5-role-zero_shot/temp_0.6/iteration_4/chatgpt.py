
from typing import Any

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Returns a string representing a filled square.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Returns a string representing a filled rectangle.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Returns a string representing a filled parallelogram.

    draw_triangle(width: int, height: int, symbol: str) -> str
        Returns a string representing a filled right-angled triangle.

    draw_pyramid(height: int, symbol: str) -> str
        Returns a string representing a filled symmetrical pyramid.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def _validate_positive_int(value: Any, name: str) -> None:
        """
        Validates that the value is a positive integer.

        Parameters
        ----------
        value : Any
            The value to check.
        name : str
            The name of the parameter for error messages.

        Raises
        ------
        TypeError
            If value is not an integer.
        ValueError
            If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Validates that the symbol is a single, printable, non-whitespace character.

        Parameters
        ----------
        symbol : Any
            The symbol to check.

        Raises
        ------
        TypeError
            If symbol is not a string.
        ValueError
            If symbol is not a single, printable, non-whitespace character.
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
        Draws a filled square using the specified symbol.

        Parameters
        ----------
        width : int
            The width and height of the square. Must be positive.
        symbol : str
            The symbol to use. Must be a single, printable, non-whitespace character.

        Returns
        -------
        str
            The ASCII art square as a multi-line string.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)
        # Generate square
        row = symbol * width
        return '\n'.join([row for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle using the specified symbol.

        Parameters
        ----------
        width : int
            The width of the rectangle. Must be positive.
        height : int
            The height of the rectangle. Must be positive.
        symbol : str
            The symbol to use. Must be a single, printable, non-whitespace character.

        Returns
        -------
        str
            The ASCII art rectangle as a multi-line string.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        # Generate rectangle
        row = symbol * width
        return '\n'.join([row for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram (each line shifted right by one space).

        Parameters
        ----------
        width : int
            The width of the parallelogram. Must be positive.
        height : int
            The height of the parallelogram. Must be positive.
        symbol : str
            The symbol to use. Must be a single, printable, non-whitespace character.

        Returns
        -------
        str
            The ASCII art parallelogram as a multi-line string.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        # Generate parallelogram
        lines = []
        for i in range(height):
            line = ' ' * i + symbol * width
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left right angle).

        The triangle's bottom-most row will have 'width' symbols.
        The height is the number of rows.

        Parameters
        ----------
        width : int
            The width (base) of the triangle. Must be positive.
        height : int
            The height of the triangle. Must be positive.
        symbol : str
            The symbol to use. Must be a single, printable, non-whitespace character.

        Returns
        -------
        str
            The ASCII art triangle as a multi-line string.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Calculate number of symbols for this row (proportional to height/width)
            # Last row should have exactly 'width' symbols
            if height == 1:
                num_symbols = width
            else:
                num_symbols = max(1, int(round((row + 1) * width / height)))
            lines.append(symbol * num_symbols)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid.

        The base of the pyramid will have (2 * height - 1) symbols.

        Parameters
        ----------
        height : int
            The height of the pyramid. Must be positive.
        symbol : str
            The symbol to use. Must be a single, printable, non-whitespace character.

        Returns
        -------
        str
            The ASCII art pyramid as a multi-line string.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            lines.append(line)
        return '\n'.join(lines)


if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n" + art.draw_square(5, '#'))
    print("\nRectangle:\n" + art.draw_rectangle(7, 3, '*'))
    print("\nParallelogram:\n" + art.draw_parallelogram(6, 4, '@'))
    print("\nTriangle:\n" + art.draw_triangle(7, 5, '$'))
    print("\nPyramid:\n" + art.draw_pyramid(4, 'X'))
