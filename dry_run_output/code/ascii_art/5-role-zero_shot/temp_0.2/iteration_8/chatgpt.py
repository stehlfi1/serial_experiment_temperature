
from typing import Any


class AsciiArt:
    """
    Class for generating various ASCII art shapes for the console.

    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def _validate_symbol(self, symbol: Any) -> None:
        """
        Validates the symbol used for drawing shapes.
        Raises:
            ValueError: If the symbol is not a single, printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Whitespace is not allowed as a drawing symbol.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    def _validate_positive_int(self, name: str, value: Any) -> None:
        """
        Validates that a value is a positive integer.
        Args:
            name: Name of the parameter (for error messages).
            value: Value to be checked.
        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer (got {value}).")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square (must be > 0)
            symbol (str): The symbol to use for filling the square (single printable character)

        Returns:
            str: Multiline string representation of the square.
        """
        self._validate_positive_int("width", width)
        self._validate_symbol(symbol)

        line = symbol * width
        square = [line for _ in range(width)]
        return "\n".join(square)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle (must be > 0)
            height (int): The height of the rectangle (must be > 0)
            symbol (str): The symbol to use for filling the rectangle (single printable character)

        Returns:
            str: Multiline string representation of the rectangle.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)

        line = symbol * width
        rectangle = [line for _ in range(height)]
        return "\n".join(rectangle)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram (rows shift right by one space with each next line).

        Args:
            width (int): The width of each row (must be > 0)
            height (int): The number of rows (must be > 0)
            symbol (str): The symbol to use for filling the parallelogram (single printable character)

        Returns:
            str: Multiline string representation of the parallelogram.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            spaces = " " * row
            symbols = symbol * width
            lines.append(f"{spaces}{symbols}")
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (corner at top-left, grows to right and down).

        Args:
            width (int): The base width of the triangle (must be > 0)
            height (int): The height of the triangle (must be > 0)
            symbol (str): The symbol to use for filling the triangle (single printable character)

        Returns:
            str: Multiline string representation of the triangle.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)

        lines = []
        # Determine the number of symbols for each row (max at bottom = width)
        for row in range(height):
            # Linear interpolation: row 0 -> 1 symbol, row (height - 1) -> width symbols
            symbols = symbol * ((width * (row + 1)) // height)
            # Ensure at least 1 symbol per row, but not to exceed width
            count = max(1, min(width, len(symbols)))
            lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid.

        Args:
            height (int): The height of the pyramid (must be > 0)
            symbol (str): The symbol to use for filling the pyramid (single printable character)

        Returns:
            str: Multiline string representation of the pyramid.
        """
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)

        lines = []
        # The base width is always (2*height - 1)
        base_width = 2 * height - 1
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage and simple test cases
    art = AsciiArt()

    print("Square (4, '#'):")
    print(art.draw_square(4, '#'))
    print()

    print("Rectangle (5x3, '*'):")
    print(art.draw_rectangle(5, 3, '*'))
    print()

    print("Parallelogram (5x4, '%'):")
    print(art.draw_parallelogram(5, 4, '%'))
    print()

    print("Right-angled Triangle (5x4, '@'):")
    print(art.draw_triangle(5, 4, '@'))
    print()

    print("Pyramid (5, '+'):")
    print(art.draw_pyramid(5, '+'))
    print()
