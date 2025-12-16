
from typing import Optional


class AsciiArt:
    """
    Class providing methods to generate various 2D ASCII art shapes.

    All methods return a multi-line string representing the ASCII art.
    Input validation is performed to conform to ISO/IEC 25010 standards.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace printable character.
        Raises:
            ValueError: If the symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    @staticmethod
    def _validate_positive_int(value: int, name: str, min_value: int = 1) -> None:
        """
        Validates that the value is an integer >= min_value.
        Raises:
            ValueError: If the value is invalid.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < min_value:
            raise ValueError(f"{name} must be at least {min_value}.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square with the specified width and symbol.

        Args:
            width (int): The width (and height) of the square; must be >= 1.
            symbol (str): A single, non-whitespace character.

        Returns:
            str: Multi-line ASCII art square.
        """
        self._validate_positive_int(width, "Width", min_value=1)
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width (int): Number of columns; must be >= 1.
            height (int): Number of rows; must be >= 1.
            symbol (str): A single, non-whitespace character.

        Returns:
            str: Multi-line ASCII art rectangle.
        """
        self._validate_positive_int(width, "Width", min_value=1)
        self._validate_positive_int(height, "Height", min_value=1)
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, shifted to the right on each row.

        Args:
            width (int): Number of symbols per row; must be >= 1.
            height (int): Number of rows; must be >= 1.
            symbol (str): A single, non-whitespace character.

        Returns:
            str: Multi-line ASCII art parallelogram.
        """
        self._validate_positive_int(width, "Width", min_value=1)
        self._validate_positive_int(height, "Height", min_value=1)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            spaces = " " * row
            line = spaces + (symbol * width)
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle.
        The right angle is at top-left; the bottom-most line is the longest.

        Args:
            width (int): Maximum width of triangle base (must be >= 1).
            height (int): Height of triangle (must be >= 1).
            symbol (str): A single, non-whitespace character.

        Returns:
            str: Multi-line ASCII art triangle.
        """
        self._validate_positive_int(width, "Width", min_value=1)
        self._validate_positive_int(height, "Height", min_value=1)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # For proportional triangle, fill up to a fraction of width
            num_symbols = max(1, int(round((row + 1) * width / height)))
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a centered, filled pyramid with the given height.

        Args:
            height (int): Height of the pyramid (must be >= 1).
            symbol (str): A single, non-whitespace character.

        Returns:
            str: Multi-line ASCII art pyramid.
        """
        self._validate_positive_int(height, "Height", min_value=1)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            spaces = height - row - 1
            line = " " * spaces + symbol * num_symbols + " " * spaces
            lines.append(line)
        return "\n".join(lines)


# Example of usage and easy unit testing
if __name__ == "__main__":
    art = AsciiArt()
    try:
        print("Square\n")
        print(art.draw_square(4, "#"))
        print("\nRectangle\n")
        print(art.draw_rectangle(6, 3, "*"))
        print("\nParallelogram\n")
        print(art.draw_parallelogram(5, 4, "@"))
        print("\nTriangle\n")
        print(art.draw_triangle(6, 4, "+"))
        print("\nPyramid\n")
        print(art.draw_pyramid(5, "#"))
    except Exception as e:
        print("Error:", e)
