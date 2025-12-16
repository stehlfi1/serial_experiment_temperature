
from typing import Any


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Draws a square of given width and symbol.
    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draws a rectangle of given width, height, and symbol.
    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draws a parallelogram with a given width, height, and symbol.
    draw_triangle(width: int, height: int, symbol: str) -> str
        Draws a right-angled triangle of given width, height, and symbol.
    draw_pyramid(height: int, symbol: str) -> str
        Draws a symmetrical pyramid of given height and symbol.
    """

    def __init__(self) -> None:
        """Initializes the AsciiArt object."""
        pass

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Validates the symbol: must be a single printable, non-whitespace character.

        Parameters
        ----------
        symbol : Any
            The symbol to validate.

        Raises
        ------
        TypeError
            If the symbol is not a string.
        ValueError
            If symbol is not a single printable non-whitespace character.
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
    def _validate_dimensions(*dimensions: Any) -> None:
        """
        Validates that all provided dimensions are positive integers.

        Parameters
        ----------
        *dimensions : Any
            The dimensions to validate.

        Raises
        ------
        TypeError
            If a dimension is not an integer.
        ValueError
            If a dimension is not positive.
        """
        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError("Dimensions must be integers.")
            if dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Parameters
        ----------
        width : int
            Length of one side of the square (must be > 0).
        symbol : str
            A single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art square as a multi-line string.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)

        row = symbol * width
        return '\n'.join([row for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Parameters
        ----------
        width : int
            Number of characters wide (must be > 0).
        height : int
            Number of rows (must be > 0).
        symbol : str
            A single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art rectangle as a multi-line string.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        row = symbol * width
        return '\n'.join([row for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram growing diagonally to the right.

        Each row starts with increasing spaces, then symbols.

        Parameters
        ----------
        width : int
            Number of symbols per row.
        height : int
            Number of rows.
        symbol : str
            A single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art parallelogram as a multi-line string.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            spaces = ' ' * row
            symbols = symbol * width
            lines.append(f"{spaces}{symbols}")
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle growing to the right and down.

        The triangle starts at the top-left corner. Maximum number of symbols
        on any row is 'width', and number of rows is 'height'.

        Parameters
        ----------
        width : int
            The maximum width of the triangle's base.
        height : int
            The height of the triangle.
        symbol : str
            A single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art triangle as a multi-line string.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # proportional width per row, min to avoid overflow on weird dimensions
            row_width = min(width, max(1, int(round((i+1) * width / height))))
            lines.append(symbol * row_width)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetric, filled pyramid.

        Parameters
        ----------
        height : int
            Number of rows in the pyramid.
        symbol : str
            A single, non-whitespace printable character.

        Returns
        -------
        str
            The ASCII art pyramid as a multi-line string.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        lines = []
        max_width = height * 2 - 1
        for i in range(height):
            num_symbols = 2 * i + 1
            spaces = (max_width - num_symbols) // 2
            line = ' ' * spaces + symbol * num_symbols + ' ' * spaces
            lines.append(line)
        return '\n'.join(lines)


if __name__ == "__main__":
    # Example usage and basic test cases
    art = AsciiArt()

    print("SQUARE:")
    print(art.draw_square(5, '#'))
    print("\nRECTANGLE:")
    print(art.draw_rectangle(8, 3, '*'))
    print("\nPARALLELOGRAM:")
    print(art.draw_parallelogram(6, 4, '@'))
    print("\nTRIANGLE:")
    print(art.draw_triangle(7, 5, '+'))
    print("\nPYRAMID:")
    print(art.draw_pyramid(4, '^'))
