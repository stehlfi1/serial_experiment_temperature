
from typing import Any

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes for console display.
    Adheres to ISO/IEC 25010:2011 standards on maintainability, correctness, and safety.
    """

    def __init__(self):
        pass

    def _validate_dimensions(self, **kwargs: int) -> None:
        """
        Validates that all provided dimension keyword arguments are positive integers (> 0).
        """
        for dim, value in kwargs.items():
            if not isinstance(value, int):
                raise TypeError(f"{dim.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{dim.capitalize()} must be positive (got {value})")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the input symbol is a single non-whitespace printable character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.
        
        :param width: The width and height of the square (must be > 0)
        :param symbol: The character used to draw the shape (must be single, non-whitespace)
        :return: A multiline string representing the square
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        square = [symbol * width for _ in range(width)]
        return '\n'.join(square)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height using the given symbol.
        
        :param width: The width of the rectangle (must be > 0)
        :param height: The height of the rectangle (must be > 0)
        :param symbol: The character used to draw the shape (must be single, non-whitespace)
        :return: A multiline string representing the rectangle
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        rectangle = [symbol * width for _ in range(height)]
        return '\n'.join(rectangle)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram of the specified width and height using the symbol.

        Each row is shifted one space to the right relative to the one above.
        
        :param width: The width of the parallelogram base (must be > 0)
        :param height: The height of the parallelogram (must be > 0)
        :param symbol: The character used to draw the shape (must be single, non-whitespace)
        :return: A multiline string representing the parallelogram
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        parallelogram = [
            ' ' * i + symbol * width
            for i in range(height)
        ]
        return '\n'.join(parallelogram)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle with the right angle at the top-left corner.

        The base has the specified width; height is the number of rows.
        In each row, the number of symbols increases until reaching the base width.
        If height > width, the triangle will still stop growing after width is reached.
        
        :param width: The width of the triangle's base (must be > 0)
        :param height: The number of rows (must be > 0)
        :param symbol: The character used to draw the shape (must be single, non-whitespace)
        :return: A multiline string representing the right-angled triangle
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        triangle = [
            symbol * min(width, i + 1)
            for i in range(height)
        ]
        return '\n'.join(triangle)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid of the specified height using the given symbol.

        Each row is centered, with the number of symbols increasing by 2 each time (for symmetry).
        
        :param height: The height of the pyramid (must be > 0)
        :param symbol: The character used to draw the shape (must be single, non-whitespace)
        :return: A multiline string representing the pyramid
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            line = ' ' * num_spaces + symbol * num_symbols + ' ' * num_spaces
            lines.append(line)
        return '\n'.join(lines)

# Example usage and basic demonstration/testing
if __name__ == "__main__":
    art = AsciiArt()
    print("Square:")
    print(art.draw_square(5, "#"))
    print("\nRectangle:")
    print(art.draw_rectangle(7, 3, "*"))
    print("\nParallelogram:")
    print(art.draw_parallelogram(5, 4, "@"))
    print("\nRight-Angled Triangle:")
    print(art.draw_triangle(5, 5, "+"))
    print("\nPyramid:")
    print(art.draw_pyramid(5, "^"))
