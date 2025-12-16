
"""
ascii_art.py - Console-based 2D ASCII ART app

Implements ASCII shape drawing according to ISO/IEC 25010 requirements.
Author: [Your Name]
"""

import string


class AsciiArt:
    """
    AsciiArt provides static methods to draw various filled ASCII shapes.

    All methods validate inputs and raise built-in errors for invalid values.

    Shapes:
        - Square
        - Rectangle
        - Parallelogram
        - Right-angled Triangle
        - Symmetrical Pyramid
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates if the given symbol is a single, non-whitespace printable character.

        Raises:
            ValueError: If the symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol in string.whitespace:
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be printable.")

    @staticmethod
    def _validate_positive_integer(value: int, name: str) -> None:
        """
        Validates if a value is a positive integer.

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def draw_square(width: int, symbol: str) -> str:
        """
        Draws a filled square of size width x width.

        Args:
            width (int): The width and height of the square.
            symbol (str): The fill symbol.

        Returns:
            str: String representing the square.

        Raises:
            ValueError, TypeError: On invalid input.
        """
        AsciiArt._validate_positive_integer(width, "width")
        AsciiArt._validate_symbol(symbol)
        rows = [symbol * width for _ in range(width)]
        return '\n'.join(rows)

    @staticmethod
    def draw_rectangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): Width of the rectangle.
            height (int): Height of the rectangle.
            symbol (str): The fill symbol.

        Returns:
            str: String representing the rectangle.

        Raises:
            ValueError, TypeError: On invalid input.
        """
        AsciiArt._validate_positive_integer(width, "width")
        AsciiArt._validate_positive_integer(height, "height")
        AsciiArt._validate_symbol(symbol)
        rows = [symbol * width for _ in range(height)]
        return '\n'.join(rows)

    @staticmethod
    def draw_parallelogram(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, growing diagonally to the right.

        Each row is shifted right by one space relative to the previous row.

        Args:
            width (int): Width of the parallelogram.
            height (int): Height of the parallelogram.
            symbol (str): The fill symbol.

        Returns:
            str: String representing the parallelogram.

        Raises:
            ValueError, TypeError: On invalid input.
        """
        AsciiArt._validate_positive_integer(width, "width")
        AsciiArt._validate_positive_integer(height, "height")
        AsciiArt._validate_symbol(symbol)
        rows = [(' ' * i) + (symbol * width) for i in range(height)]
        return '\n'.join(rows)

    @staticmethod
    def draw_triangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (growing down and right from top-left), clipped by width and height.

        Args:
            width (int): The maximum width (base length) of the triangle.
            height (int): The height of the triangle.
            symbol (str): The fill symbol.

        Returns:
            str: String representing the triangle.

        Raises:
            ValueError, TypeError: On invalid input.
        """
        AsciiArt._validate_positive_integer(width, "width")
        AsciiArt._validate_positive_integer(height, "height")
        AsciiArt._validate_symbol(symbol)

        # Linear growth: row i has max 1, ..., width symbols, evenly spread over height rows.
        rows = []
        for i in range(height):
            # Ensure base matches width in last row
            current_row_symbols = max(1, round(width * (i + 1) / height))
            # Don't exceed width
            current_row_symbols = min(current_row_symbols, width)
            rows.append(symbol * current_row_symbols)
        return '\n'.join(rows)

    @staticmethod
    def draw_pyramid(height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid with the given height.

        Args:
            height (int): Height of the pyramid (number of rows).
            symbol (str): The fill symbol.

        Returns:
            str: String representing the pyramid.

        Raises:
            ValueError, TypeError: On invalid input.
        """
        AsciiArt._validate_positive_integer(height, "height")
        AsciiArt._validate_symbol(symbol)

        rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            row = (' ' * num_spaces) + (symbol * num_symbols) + (' ' * num_spaces)
            rows.append(row)
        return '\n'.join(rows)


# Example usage (for testability)
if __name__ == "__main__":
    shapes = AsciiArt()

    print("SQUARE:\n", shapes.draw_square(4, '#'))
    print("\nRECTANGLE:\n", shapes.draw_rectangle(6, 3, '*'))
    print("\nPARALLELOGRAM:\n", shapes.draw_parallelogram(5, 4, '@'))
    print("\nTRIANGLE:\n", shapes.draw_triangle(6, 4, '+'))
    print("\nPYRAMID:\n", shapes.draw_pyramid(5, '$'))
