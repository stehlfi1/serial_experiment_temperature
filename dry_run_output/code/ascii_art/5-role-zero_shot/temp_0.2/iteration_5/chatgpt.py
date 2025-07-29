
"""
ASCII Art Console Application

This module defines the AsciiArt class, which provides functions to generate various ASCII art shapes.
The implementation follows OOP principles, includes input validation, and adheres to ISO/IEC 25010 guidelines
for software quality, focusing on correctness, performance, maintainability, safety, and testability.

Author: AI Assistant
"""

import string


class AsciiArt:
    """
    AsciiArt provides methods for generating different ASCII art shapes.
    All methods validate input and return the shape as a multi-line string.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Generates a filled square as a multi-line string.

        Parameters:
            width (int): The width (and height) of the square. Must be >= 1.
            symbol (str): A single, printable, non-whitespace character.

        Returns:
            str: The ASCII art square.

        Raises:
            ValueError: If invalid width or symbol is provided.
        """
        self._validate_dimension(width, 'width')
        self._validate_symbol(symbol)

        row = symbol * width
        art = '\n'.join([row for _ in range(width)])
        return art

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a filled rectangle as a multi-line string.

        Parameters:
            width (int): The width of the rectangle. Must be >= 1.
            height (int): The height of the rectangle. Must be >= 1.
            symbol (str): A single, printable, non-whitespace character.

        Returns:
            str: The ASCII art rectangle.

        Raises:
            ValueError: If invalid width, height, or symbol is provided.
        """
        self._validate_dimension(width, 'width')
        self._validate_dimension(height, 'height')
        self._validate_symbol(symbol)

        row = symbol * width
        art = '\n'.join([row for _ in range(height)])
        return art

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a filled parallelogram as a multi-line string.
        Each line is shifted one space to the right from the line above.

        Parameters:
            width (int): The width of the parallelogram. Must be >= 1.
            height (int): The height of the parallelogram. Must be >= 1.
            symbol (str): A single, printable, non-whitespace character.

        Returns:
            str: The ASCII art parallelogram.

        Raises:
            ValueError: If invalid width, height, or symbol is provided.
        """
        self._validate_dimension(width, 'width')
        self._validate_dimension(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            line = ' ' * i + symbol * width
            lines.append(line)
        art = '\n'.join(lines)
        return art

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Generates a filled right-angled triangle (grows rightwards from top-left).

        The triangle's hypotenuse grows from top-left to bottom-right:
        - Each row width increases up to (and including) 'width' across at most 'height' rows.

        Parameters:
            width (int): The width of the triangle's base. Must be >= 1.
            height (int): The triangle's height. Must be >= 1.
            symbol (str): A single, printable, non-whitespace character.

        Returns:
            str: The ASCII art triangle.

        Raises:
            ValueError: If invalid width, height, or symbol is provided.
        """
        self._validate_dimension(width, 'width')
        self._validate_dimension(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Row's length increases linearly, at most to 'width'
            row_length = min(width, (i + 1) * width // height) if height > 1 else width
            if row_length == 0:
                row_length = 1  # Ensure at least one symbol per row
            line = symbol * row_length
            lines.append(line)
        art = '\n'.join(lines)
        return art

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Generates a symmetrical pyramid as a multi-line string.

        Parameters:
            height (int): The height (number of rows) of the pyramid. Must be >= 1.
            symbol (str): A single, printable, non-whitespace character.

        Returns:
            str: The ASCII art pyramid.

        Raises:
            ValueError: If invalid height or symbol is provided.
        """
        self._validate_dimension(height, 'height')
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            lines.append(line)
        art = '\n'.join(lines)
        return art

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates that a dimension value is an integer greater than zero.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.title()} must be an integer, got {type(value).__name__}")
        if value < 1:
            raise ValueError(f"{name.title()} must be >= 1; got {value}.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that a symbol is a single, printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")


# Sample usage and demonstration
if __name__ == "__main__":
    art = AsciiArt()
    print("SQUARE:\n", art.draw_square(4, "#"))
    print("\nRECTANGLE:\n", art.draw_rectangle(8, 3, "*"))
    print("\nPARALLELOGRAM:\n", art.draw_parallelogram(5, 4, "+"))
    print("\nTRIANGLE:\n", art.draw_triangle(6, 4, "@"))
    print("\nPYRAMID:\n", art.draw_pyramid(5, "$"))
