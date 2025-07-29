
"""
ascii_art.py

A console-based 2D ASCII art application for drawing various shapes,
implemented according to ISO/IEC 25010 quality requirements.

Author: [Your Name]
Date: [Today's Date]
"""

from typing import Any


class AsciiArt:
    """
    AsciiArt provides methods to generate ASCII representations of 2D shapes.
    All methods return a multi-line string with the requested shape filled with a given symbol.

    Shapes implemented:
    - Square
    - Rectangle
    - Parallelogram
    - Right-angled triangle
    - Pyramid

    Input validation is performed; ValueError is raised for invalid parameters.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square of a given width using the specified symbol.

        Args:
            width (int): Width (and height) of the square, must be > 0.
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: The ASCII art square as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)

        row = symbol * width
        return "\n".join([row for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle using the specified width, height, and symbol.

        Args:
            width (int): Width of the rectangle, must be > 0.
            height (int): Height of the rectangle, must be > 0.
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: The ASCII art rectangle as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        return "\n".join([row for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram (right-leaning) using the specified width, height, and symbol.

        Each row is shifted by one space to the right compared to the previous row.

        Args:
            width (int): Width of each row, must be > 0.
            height (int): Number of rows, must be > 0.
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: The ASCII art parallelogram as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Each row starts with i spaces
            rows.append(" " * i + symbol * width)
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle (right angle at top-left), 
        growing diagonally to the right with each row.

        Args:
            width (int): Base width of the triangle, must be > 0.
            height (int): Height of the triangle, must be > 0.
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: The ASCII art triangle as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Linear interpolation between 1 and width over height rows
            # Ensure last row will be width
            count = max(1, round(width * (i + 1) / height))
            rows.append(symbol * count)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetrical pyramid with a given height.

        Args:
            height (int): Height of the pyramid, must be > 0.
            symbol (str): A single printable, non-whitespace character.

        Returns:
            str: The ASCII art pyramid as a multi-line string.

        Raises:
            ValueError: If parameters are invalid.
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            symbols_in_row = 2 * i + 1
            spaces = height - i - 1
            rows.append(" " * spaces + symbol * symbols_in_row + " " * spaces)
        return "\n".join(rows)

    # --- Private helper methods ---

    @staticmethod
    def _validate_positive_integer(value: Any, name: str) -> None:
        """
        Validates that a value is a positive integer.

        Args:
            value (Any): Value to check.
            name (str): Name of the parameter for error messages.

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer, got {value!r}")

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Validates that the symbol is a single, printable, non-whitespace character.

        Args:
            symbol (Any): Symbol to check.

        Raises:
            ValueError: If the symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise ValueError("symbol must be a string")
        if len(symbol) != 1:
            raise ValueError("symbol must be a single character")
        if symbol.isspace():
            raise ValueError("symbol must not be a whitespace character")
        if not symbol.isprintable():
            raise ValueError("symbol must be printable")


# --- Example Usage & Testability ---

if __name__ == "__main__":
    # Example usage (can serve as basic test cases)
    art = AsciiArt()
    print("Square:\n" + art.draw_square(4, "#"))
    print("\nRectangle:\n" + art.draw_rectangle(6, 3, "*"))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, "@"))
    print("\nTriangle:\n" + art.draw_triangle(6, 5, "+"))
    print("\nPyramid:\n" + art.draw_pyramid(5, "$"))
