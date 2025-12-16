
"""
ascii_art.py

A console-based 2D ASCII art app for drawing shapes, implemented according to
the ISO/IEC 25010 quality model. The AsciiArt class supports squares, rectangles,
parallelograms, right-angled triangles, and pyramids using an OOP approach.

Author: Senior Software Developer
Date: 2024
"""

class AsciiArt:
    """
    A class for generating ASCII representations of geometric shapes.

    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def __init__(self) -> None:
        """Initialize the ASCII Art generator."""
        pass

    def _validate_positive_int(self, name: str, value: int) -> None:
        """Validate that a parameter is a positive integer."""
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be positive (got {value}).")

    def _validate_symbol(self, symbol: str) -> None:
        """Ensure symbol is a single, non-whitespace, printable character."""
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square.

        Args:
            width: The width and height of the square (must be positive).
            symbol: The single printable character to fill the square.

        Returns:
            Multi-line string representing the square.
        """
        self._validate_positive_int("width", width)
        self._validate_symbol(symbol)
        square_lines = [symbol * width for _ in range(width)]
        return '\n'.join(square_lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle.

        Args:
            width: The width of the rectangle (must be positive).
            height: The height of the rectangle (must be positive).
            symbol: The character to fill the rectangle.

        Returns:
            Multi-line string representing the rectangle.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        rectangle_lines = [symbol * width for _ in range(height)]
        return '\n'.join(rectangle_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram (right-leaning).

        Args:
            width: The width of the parallelogram (must be positive).
            height: The height of the parallelogram (must be positive).
            symbol: The character to fill the parallelogram.

        Returns:
            Multi-line string representing the parallelogram.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        parallelogram_lines = [
            ' ' * i + symbol * width for i in range(height)
        ]
        return '\n'.join(parallelogram_lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle (right angle at top-left).

        Args:
            width: The base width of the triangle (must be positive).
            height: The height of the triangle (must be positive).
            symbol: The character to fill the triangle.

        Returns:
            Multi-line string representing the triangle.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)

        triangle_lines = []
        for row in range(height):
            # The number of symbols per row increases from 1 to width in height steps
            # Ensure the last row is always 'width' symbols
            num_symbols = max(1, round(width * (height - row) / height))
            triangle_lines.append(symbol * num_symbols)
        return '\n'.join(triangle_lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a filled symmetric pyramid.

        Args:
            height: The height of the pyramid (must be positive).
            symbol: The character to fill the pyramid.

        Returns:
            Multi-line string representing the pyramid.
        """
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        pyramid_lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            pyramid_lines.append(line)
        return '\n'.join(pyramid_lines)

# ----------------------------------- #
# Example/Test usage of the AsciiArt class
# ----------------------------------- #

if __name__ == "__main__":
    art = AsciiArt()

    print("Square:\n" + art.draw_square(4, '#'))
    print("\nRectangle:\n" + art.draw_rectangle(6, 3, '*'))
    print("\nParallelogram:\n" + art.draw_parallelogram(5, 4, '$'))
    print("\nTriangle:\n" + art.draw_triangle(5, 4, '@'))
    print("\nPyramid:\n" + art.draw_pyramid(4, '+'))

    # Uncomment below lines to see the error handling in action:
    # art.draw_square(-3, '#')    # Should raise ValueError
    # art.draw_rectangle(3, 2, 'ab')  # Should raise ValueError
    # art.draw_parallelogram(4, 2, ' ')  # Should raise ValueError
