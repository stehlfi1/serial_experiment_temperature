
"""
ascii_art.py

A console-based 2D ASCII art application that allows you to generate various ASCII shapes with custom symbols.
This module adheres to ISO/IEC 25010 requirements focused on maintainability, reliability, and usability.

Author: [Your Name]
Date: 2024-06-19
"""

import string

class AsciiArt:
    """
    A class to generate ASCII art shapes using a specified single, printable, non-whitespace symbol.

    Public Methods
    --------------
    draw_square(width: int, symbol: str) -> str
        Draws and returns a square of given width filled with the specified symbol.

    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draws and returns a rectangle of given width and height filled with the specified symbol.

    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draws and returns a parallelogram of given width and height that grows diagonally to the right.

    draw_triangle(width: int, height: int, symbol: str) -> str
        Draws and returns a filled right-angled triangle that grows diagonally to the right.

    draw_pyramid(height: int, symbol: str) -> str
        Draws and returns a symmetrical pyramid of given height filled with the specified symbol.
    """

    def __init__(self):
        """Initializes a new AsciiArt generator."""
        pass

    # --- Validation Utilities ---
    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates symbol input.

        Args:
            symbol: The symbol to validate.

        Raises:
            ValueError: If symbol is not exactly one printable, non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if symbol not in string.printable or symbol in string.whitespace:
            raise ValueError("Symbol must be a printable, non-whitespace character.")

    @staticmethod
    def _validate_positive_integer(value: int, name: str = "value"):
        """
        Validates if value is a positive integer.

        Args:
            value: The integer value to validate.
            name: Optional; the parameter name for error messages.

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    # --- Shape Functions ---

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with each side equal to width.

        Args:
            width: The width and height of the square.
            symbol: The symbol to use to fill the square.

        Returns:
            Multi-line string representing the square.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of specified width and height.

        Args:
            width: Number of columns.
            height: Number of rows.
            symbol: Fill character.

        Returns:
            Multi-line string representing the rectangle.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram. Each subsequent row is shifted one space right.

        Args:
            width: Number of symbols per row.
            height: Number of rows.
            symbol: Fill character.

        Returns:
            Multi-line string representing the parallelogram.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        lines = [
            (" " * i) + (symbol * width)
            for i in range(height)
        ]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (right angle at top-left, grows to the right and downward).

        Args:
            width: Base (maximum width) of the triangle.
            height: Height of the triangle.
            symbol: Fill character.

        Returns:
            Multi-line string representing the triangle.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # For strictly right-angled triangle: distribute width over height
            # The last row fills up to width
            line_width = max(1, round((row + 1) * width / height))
            lines.append(symbol * line_width)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid of specified height.

        Args:
            height: Number of rows; the pyramid base will be width = 2*height - 1.
            symbol: Fill character.

        Returns:
            Multi-line string representing the pyramid.

        Raises:
            ValueError: For invalid arguments.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)

# --- Example Test Cases (for demonstration purposes, should be in a separate test module) ---

if __name__ == "__main__":
    art = AsciiArt()
    try:
        print("Square (width=4, symbol='#'):")
        print(art.draw_square(4, '#'), "\n")

        print("Rectangle (width=6, height=3, symbol='*'):")
        print(art.draw_rectangle(6, 3, '*'), "\n")

        print("Parallelogram (width=5, height=4, symbol='@'):")
        print(art.draw_parallelogram(5, 4, '@'), "\n")

        print("Triangle (width=7, height=5, symbol='%'):")
        print(art.draw_triangle(7, 5, '%'), "\n")

        print("Pyramid (height=5, symbol='^'):")
        print(art.draw_pyramid(5, '^'), "\n")

    except ValueError as ve:
        print("Validation error:", ve)
