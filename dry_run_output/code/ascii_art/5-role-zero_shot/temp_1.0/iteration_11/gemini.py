
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains methods for drawing
various geometric shapes using a specified printable character. The implementation
adheres to high-quality coding standards, focusing on correctness, efficiency,
and maintainability.
"""

from typing import final


@final
class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a collection of static methods for creating string
    representations of common geometric shapes. It is marked as @final as
    it is designed as a utility class and is not intended for inheritance.
    """

    def __init__(self):
        """
        AsciiArt is a utility class and is not meant to be instantiated.
        """
        raise NotImplementedError("This class is not meant to be instantiated.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the symbol used for drawing.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single character or is whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    @staticmethod
    def _validate_dimension(*dimensions: int) -> None:
        """
        Validates that all provided dimensions are positive integers.

        Args:
            *dimensions (int): A variable number of dimension values to validate.

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive number (> 0).
        """
        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError(f"Dimension must be an integer, but got {type(dim).__name__}.")
            if dim <= 0:
                raise ValueError(f"Dimension must be positive, but got {dim}.")

    @staticmethod
    def draw_square(width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width (int): The width and height of the square.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        
        Raises:
            TypeError: If inputs are of the wrong type.
            ValueError: If inputs have invalid values.
        """
        AsciiArt._validate_dimension(width)
        AsciiArt._validate_symbol(symbol)

        row = symbol * width
        rows = [row] * width
        return "\n".join(rows)

    @staticmethod
    def draw_rectangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            TypeError: If inputs are of the wrong type.
            ValueError: If inputs have invalid values.
        """
        AsciiArt._validate_dimension(width, height)
        AsciiArt._validate_symbol(symbol)

        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    @staticmethod
    def draw_parallelogram(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram leaning to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width (int): The width of the parallelogram's top/bottom edge.
            height (int): The height of the parallelogram.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            TypeError: If inputs are of the wrong type.
            ValueError: If inputs have invalid values.
        """
        AsciiArt._validate_dimension(width, height)
        AsciiArt._validate_symbol(symbol)

        rows = [
            " " * i + symbol * width
            for i in range(height)
        ]
        return "\n".join(rows)

    @staticmethod
    def draw_triangle(width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner, and its base has the
        specified width.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            TypeError: If inputs are of the wrong type.
            ValueError: If inputs have invalid values.
        """
        AsciiArt._validate_dimension(width, height)
        AsciiArt._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Calculate num_symbols for the current row based on its proportion of total height
            # Use max(1, ...) to ensure at least one symbol is drawn per row
            num_symbols = max(1, round((i + 1) * width / height))
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    @staticmethod
    def draw_pyramid(height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            TypeError: If inputs are of the wrong type.
            ValueError: If inputs have invalid values.
        """
        AsciiArt._validate_dimension(height)
        AsciiArt._validate_symbol(symbol)

        rows = [
            " " * (height - 1 - i) + symbol * (2 * i + 1)
            for i in range(height)
        ]
        return "\n".join(rows)


# Example Usage:
if __name__ == '__main__':
    try:
        print("--- Square (5x5, #) ---")
        print(AsciiArt.draw_square(5, '#'))
        print("\n--- Rectangle (8x4, *) ---")
        print(AsciiArt.draw_rectangle(8, 4, '*'))
        print("\n--- Parallelogram (10x5, @) ---")
        print(AsciiArt.draw_parallelogram(10, 5, '@'))
        print("\n--- Right-angled Triangle (width=10, height=5, +) ---")
        print(AsciiArt.draw_triangle(10, 5, '+'))
        print("\n--- Symmetrical Pyramid (height=6, ^) ---")
        print(AsciiArt.draw_pyramid(6, '^'))

        # Example of invalid input handling
        print("\n--- Testing Invalid Input ---")
        AsciiArt.draw_square(-3, 'X')

    except (ValueError, TypeError, NotImplementedError) as e:
        print(f"An error occurred: {e}")
