
"""
ascii_art.py

A console-based 2D ASCII Art application implementing shape drawing functions
according to ISO/IEC 25010 standards for high-quality, maintainable code.

Author: [Your Name]
Date: [Date]
"""

import string


class AsciiArt:
    """
    AsciiArt provides methods to generate ASCII representations of various 2D shapes.
    Each method returns a multi-line string with the shape filled by a user-specified symbol.

    Shape methods:
        - draw_square(width, symbol)
        - draw_rectangle(width, height, symbol)
        - draw_parallelogram(width, height, symbol)
        - draw_triangle(width, height, symbol)
        - draw_pyramid(height, symbol)
    """

    def __init__(self):
        """
        Initializes the AsciiArt class.
        """
        pass

    @staticmethod
    def _validate_positive_int(value: int, name: str):
        """
        Validates that a value is a positive integer.

        Args:
            value (int): The value to validate.
            name (str): The name of the parameter.

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer, got {value}.")

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates that the symbol is a single, printable, non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if symbol not in string.printable or symbol in string.whitespace:
            raise ValueError("Symbol must be a printable, non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of given width using the specified symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): The symbol to use.

        Returns:
            str: The ASCII art square.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        # Each row is 'width' symbols; repeat for 'width' rows
        lines = [symbol * width for _ in range(width)]
        return '\n'.join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of given width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use.

        Returns:
            str: The ASCII art rectangle.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return '\n'.join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right, starting from the top-left corner.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use.

        Returns:
            str: The ASCII art parallelogram.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Each row is shifted right by one space from the previous
            line = ' ' * row + symbol * width
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle (right angle at top-left, grows right and down).

        Args:
            width (int): The maximum width of the base of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use.

        Returns:
            str: The ASCII art triangle.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Calculate number of symbols for this row (at least 1, at most width)
            # Distribute symbols as evenly as possible over the height
            num_symbols = max(1, min(width, (width * (row + 1)) // height))
            lines.append(symbol * num_symbols)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use.

        Returns:
            str: The ASCII art pyramid.

        Raises:
            ValueError: For invalid arguments.
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


# Example usage & quick tests (can be removed/commented for production or moved to unit tests)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:\n" + art.draw_square(4, '#'))
    print("\nRectangle:\n" + art.draw_rectangle(6, 3, '*'))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, '@'))
    print("\nTriangle:\n" + art.draw_triangle(7, 5, '$'))
    print("\nPyramid:\n" + art.draw_pyramid(4, '%'))
