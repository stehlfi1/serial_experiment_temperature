
"""
ascii_art.py

A modular, maintainable ASCII art drawing application, adhering to ISO/IEC 25010 core attributes such as
correctness, safety, and testability. Implements OOP, input validation, and rich docstrings.
"""

import string

class AsciiArt:
    """
    ASCII Art drawing class for generating various filled shapes as multi-line strings.
    Methods follow strict input validation and are designed for testability and maintainability.
    """

    def __init__(self):
        """Initialize an AsciiArt instance. (No internal state required.)"""
        pass

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates that the symbol is a single, visible (printable non-whitespace) character.

        Raises:
            ValueError: If symbol is not a single, printable, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if symbol not in string.printable.strip():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_positive_int(value: int, name='value'):
        """
        Validates that value is a positive integer (greater than zero).

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using the specified symbol.

        Args:
            width (int): Width (and height) of the square (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The square as a multi-line string.

        Raises:
            ValueError: On invalid width or symbol.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle using the specified symbol.

        Args:
            width (int): Rectangle width (must be positive).
            height (int): Rectangle height (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The rectangle as a multi-line string.

        Raises:
            ValueError: On invalid width/height or symbol.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram (each row is shifted by one space to the right).

        Args:
            width (int): Width of parallelogram (must be positive).
            height (int): Height of parallelogram (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The parallelogram as a multi-line string.

        Raises:
            ValueError: On invalid width/height or symbol.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            line = ' ' * row + symbol * width
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left at [0,0], grows to the right and down).

        Args:
            width (int): Maximum width (base, must be positive).
            height (int): Height of the triangle (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The right-angled triangle as a multi-line string.

        Raises:
            ValueError: On invalid width/height or symbol.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Calculate proportional width for the row: at least 1 symbol per row, at most width.
            row_width = max(1, round(width * (row + 1) / height))
            if row == height - 1:  # Ensure last row is exactly width
                row_width = width
            line = symbol * row_width
            lines.append(line)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetric filled pyramid with the specified height.

        Args:
            height (int): Height of the pyramid (must be positive).
            symbol (str): Single printable character.

        Returns:
            str: The pyramid as a multi-line string.

        Raises:
            ValueError: On invalid height or symbol.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            spaces = height - row - 1
            line = ' ' * spaces + symbol * num_symbols + ' ' * spaces
            lines.append(line)
        return '\n'.join(lines)

# Example usage (in main or via tests, not run at module import)
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:")
    print(art.draw_square(5, '*'))
    print("\nRectangle:")
    print(art.draw_rectangle(6, 3, '#'))
    print("\nParallelogram:")
    print(art.draw_parallelogram(5, 4, '@'))
    print("\nTriangle:")
    print(art.draw_triangle(7, 5, '$'))
    print("\nPyramid:")
    print(art.draw_pyramid(4, '+'))
