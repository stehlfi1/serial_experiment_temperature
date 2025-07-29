
from typing import Any

class AsciiArt:
    """
    Class for generating 2D ASCII art for various geometric shapes.
    
    Provides methods to draw a square, rectangle, parallelogram, right-angled triangle, and a pyramid.
    All shapes are filled with the user-specified symbol.
    """

    def __init__(self) -> None:
        """
        Initialize the AsciiArt class.
        """
        pass

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using the specified symbol.
        
        Args:
            width (int): The width and height of the square (must be >= 1).
            symbol (str): A single, non-whitespace printable character.

        Returns:
            str: The ASCII art representation of the square.

        Raises:
            ValueError: If width < 1 or symbol is invalid.
        """
        self._validate_size(width, 'width')
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height using the specified symbol.
        
        Args:
            width (int): The width of the rectangle (must be >= 1).
            height (int): The height of the rectangle (must be >= 1).
            symbol (str): A single, non-whitespace printable character.

        Returns:
            str: The ASCII art representation of the rectangle.

        Raises:
            ValueError: If width/height < 1 or symbol is invalid.
        """
        self._validate_size(width, 'width')
        self._validate_size(height, 'height')
        self._validate_symbol(symbol)
        line = symbol * width
        return '\n'.join([line] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram where each subsequent row is shifted right by one space.
        
        Args:
            width (int): The width of each parallelogram row (must be >= 1).
            height (int): Number of rows in the parallelogram (must be >= 1).
            symbol (str): A single, non-whitespace printable character.

        Returns:
            str: The ASCII art representation of the parallelogram.

        Raises:
            ValueError: If width/height < 1 or symbol is invalid.
        """
        self._validate_size(width, 'width')
        self._validate_size(height, 'height')
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            line = ' ' * row + symbol * width
            lines.append(line)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (top-left right angle).
        The base is at the bottom and the right side slopes downward.
        Each row i has min(width, ceil((i + 1) * width / height)) symbols.
        
        Args:
            width (int): The base width of the triangle (must be >= 1).
            height (int): The height of the triangle (must be >= 1).
            symbol (str): A single, non-whitespace printable character.
        
        Returns:
            str: The ASCII art representation of the triangle.
        
        Raises:
            ValueError: If width/height < 1 or symbol is invalid.
        """
        self._validate_size(width, 'width')
        self._validate_size(height, 'height')
        self._validate_symbol(symbol)
        from math import ceil

        lines = []
        for row in range(height):
            # Linear interpolation: distribute width over height rows
            symbols_in_row = min(width, ceil((row + 1) * width / height))
            line = symbol * symbols_in_row
            lines.append(line)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, centered pyramid of given height.

        Args:
            height (int): Number of rows in the pyramid (must be >= 1).
            symbol (str): A single, non-whitespace printable character.

        Returns:
            str: The ASCII art representation of the pyramid.

        Raises:
            ValueError: If height < 1 or symbol is invalid.
        """
        self._validate_size(height, 'height')
        self._validate_symbol(symbol)
        lines = []
        # The base width is always (2*height - 1)
        for row in range(height):
            num_symbols = 2 * row + 1
            spaces = height - row - 1
            line = ' ' * spaces + symbol * num_symbols + ' ' * spaces
            lines.append(line)
        return '\n'.join(lines)

    @staticmethod
    def _validate_symbol(symbol: Any) -> None:
        """
        Validates that the symbol is exactly one printable, non-whitespace character.
        
        Args:
            symbol (Any): The symbol to check.

        Raises:
            TypeError: If symbol is not a string.
            ValueError: If symbol is not a single character, is whitespace, or not printable.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be whitespace.")
        # Exclude non-printable chars
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_size(value: Any, name: str = 'value') -> None:
        """
        Validates that a size (width/height) is a positive integer.
        
        Args:
            value (Any): The value to check.
            name (str): The parameter name for error message.

        Raises:
            TypeError: If value is not integer.
            ValueError: If value is less than 1.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value < 1:
            raise ValueError(f"{name.capitalize()} must be at least 1.")
