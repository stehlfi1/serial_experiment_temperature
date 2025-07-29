
"""
ascii_art.py

A console-based 2D ASCII Art application adhering to ISO/IEC 25010 quality standards.
Implements an AsciiArt class with methods to draw various filled ASCII shapes.
"""

import string

class AsciiArt:
    """
    Provides methods to generate ASCII art for various 2D shapes.
    All methods validate input and return the ASCII art as a multi-line string.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using the specified symbol.

        :param width: Width (and height) of the square (must be positive integer)
        :param symbol: A single printable, non-whitespace character
        :return: Multiline string representing the square
        :raises ValueError: If invalid input is provided
        """
        self._validate_positive_int(width, 'width')
        self._validate_symbol(symbol)

        line = symbol * width
        return '\n'.join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height using the specified symbol.

        :param width: Width of the rectangle (must be positive integer)
        :param height: Height of the rectangle (must be positive integer)
        :param symbol: A single printable, non-whitespace character
        :return: Multiline string representing the rectangle
        :raises ValueError: If invalid input is provided
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)

        line = symbol * width
        return '\n'.join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram (each row is shifted one space right) of given width and height.

        :param width: Width of the parallelogram (must be positive integer)
        :param height: Height of the parallelogram (must be positive integer)
        :param symbol: A single printable, non-whitespace character
        :return: Multiline string representing the parallelogram
        :raises ValueError: If invalid input is provided
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = spaces + (symbol * width)
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left right angle) of given width and height.

        :param width: Base width of the triangle (must be positive integer)
        :param height: Height of the triangle (must be positive integer)
        :param symbol: A single printable, non-whitespace character
        :return: Multiline string representing the triangle
        :raises ValueError: If invalid input is provided
        """
        self._validate_positive_int(width, 'width')
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Calculate the number of symbols for this row (from 1 up to width)
            # Linear interpolation: symbols = ceil(width * (row + 1) / height)
            num_symbols = max(1, (width * (row + 1) + height - 1) // height)
            line = symbol * num_symbols
            lines.append(line)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, centered pyramid of given height.

        :param height: Height of the pyramid (must be positive integer)
        :param symbol: A single printable, non-whitespace character
        :return: Multiline string representing the pyramid
        :raises ValueError: If invalid input is provided
        """
        self._validate_positive_int(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        max_width = 2 * height - 1
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = (max_width - num_symbols) // 2
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            lines.append(line)
        return '\n'.join(lines)

    @staticmethod
    def _validate_positive_int(value: int, name: str):
        """
        Validates that a value is a positive integer.

        :param value: The value to validate
        :param name: The name of the parameter (for error messages)
        :raises ValueError: If the value is not a positive integer
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer (got {value!r})")

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates that the symbol is a single printable, non-whitespace character.

        :param symbol: The symbol to validate
        :raises ValueError: If the symbol is invalid
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string")
        if len(symbol) != 1:
            raise ValueError(f"symbol must be a single character (got {symbol!r})")
        if symbol.isspace():
            raise ValueError("symbol must not be a whitespace character")
        if symbol not in string.printable or symbol in string.whitespace:
            raise ValueError("symbol must be a printable, non-whitespace character")

# Example usage and simple tests (can be removed or replaced with unit tests)
if __name__ == "__main__":
    art = AsciiArt()
    print("SQUARE:")
    print(art.draw_square(4, '#'))
    print("\nRECTANGLE:")
    print(art.draw_rectangle(6, 3, '*'))
    print("\nPARALLELOGRAM:")
    print(art.draw_parallelogram(5, 4, '@'))
    print("\nTRIANGLE:")
    print(art.draw_triangle(6, 4, '+'))
    print("\nPYRAMID:")
    print(art.draw_pyramid(5, '$'))
