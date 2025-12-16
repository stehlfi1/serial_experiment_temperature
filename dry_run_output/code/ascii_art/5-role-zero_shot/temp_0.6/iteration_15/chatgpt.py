
# ascii_art.py
from typing import Any

class AsciiArt:
    """
    A class to generate 2D ASCII art shapes.

    Each method returns a string containing the ASCII art representation of the requested shape.
    Only one printable, non-whitespace character can be used for drawing shapes.
    All methods validate input parameters and raise appropriate exceptions on invalid input.
    """

    def __init__(self) -> None:
        """
        Initialize the AsciiArt class.
        Currently stateless, but allows for future expansion.
        """
        pass

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single, non-whitespace, printable character.

        Args:
            symbol (str): The character to use for drawing.

        Raises:
            ValueError: If the symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")

    @staticmethod
    def _validate_positive_int(value: Any, name: str) -> None:
        """
        Validate that `value` is a positive integer (>= 1).

        Args:
            value (Any): Value to check.
            name (str): Name of the argument for error messages.

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 1:
            raise ValueError(f"{name} must be >= 1.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square.

        Args:
            width (int): Width and height of the square (must be >= 1).
            symbol (str): Symbol to use (single, printable, non-whitespace char).

        Returns:
            str: ASCII art of the square.
        """
        self._validate_positive_int(width, "Width")
        self._validate_symbol(symbol)
        row = symbol * width
        art = "\n".join([row for _ in range(width)])
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle.

        Args:
            width (int): Width of the rectangle (must be >= 1).
            height (int): Height of the rectangle (must be >= 1).
            symbol (str): Symbol to use (single, printable, non-whitespace char).

        Returns:
            str: ASCII art of the rectangle.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        row = symbol * width
        art = "\n".join([row for _ in range(height)])
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-oriented parallelogram.

        Each line is shifted by one additional space to the right.

        Args:
            width (int): Width of the parallelogram (must be >= 1).
            height (int): Height of the parallelogram (must be >= 1).
            symbol (str): Symbol to use (single, printable, non-whitespace char).

        Returns:
            str: ASCII art of the parallelogram.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)

        art_lines = []
        for row in range(height):
            line = ' ' * row + symbol * width
            art_lines.append(line)
        return "\n".join(art_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle (top-left right angle).

        The triangle's base is at least of height length, width is the maximum per row.

        Args:
            width (int): Width of the triangle's base (must be >= 1).
            height (int): Height of the triangle (must be >= 1).
            symbol (str): Symbol to use (single, printable, non-whitespace char).

        Returns:
            str: ASCII art of the triangle.
        """

        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)

        if height == 1:
            # special case: single row, show width at the top
            return symbol * min(width, 1)

        art_lines = []
        for row in range(height):
            # Compute the width of the current row 
            # Linearly interpolate from width for row=0 to min(width, height) on the base row
            line_len = min(width, max(1, (width * (height - row)) // height))
            # Right-angled triangle: for top-left, each subsequent row has fewer symbols
            line = symbol * line_len
            art_lines.append(line)
        return "\n".join(art_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled, centered pyramid.

        The widest row is (2*height-1). Each upper row is 2 symbols narrower.

        Args:
            height (int): Height of the pyramid (must be >= 1).
            symbol (str): Symbol to use (single, printable, non-whitespace char).

        Returns:
            str: ASCII art of the pyramid.
        """
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        art_lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            pad = height - row - 1
            line = ' ' * pad + symbol * num_symbols + ' ' * pad
            art_lines.append(line)
        return '\n'.join(art_lines)


# --- Example usage & quick tests (can be stripped out for deployment) ---
if __name__ == "__main__":
    art = AsciiArt()

    print("SQUARE (width=4):")
    print(art.draw_square(4, '#'))

    print("\nRECTANGLE (width=6, height=3):")
    print(art.draw_rectangle(6, 3, '*'))

    print("\nPARALLELOGRAM (width=5, height=4):")
    print(art.draw_parallelogram(5, 4, '$'))

    print("\nTRIANGLE (width=5, height=4):")
    print(art.draw_triangle(5, 4, '@'))

    print("\nPYRAMID (height=4):")
    print(art.draw_pyramid(4, '+'))
