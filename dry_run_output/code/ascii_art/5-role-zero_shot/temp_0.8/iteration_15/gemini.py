
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods for drawing
various geometric shapes using ASCII characters. The implementation follows
best practices for quality, maintainability, and reliability, adhering to the
principles outlined in the ISO/IEC 25010 standard.
"""

from typing import Dict, Any


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a clean interface for creating filled geometric shapes
    as multi-line strings. It emphasizes code quality through robust input
    validation, efficiency, and clear documentation, making it reliable and
    easy to maintain.
    """

    @staticmethod
    def _validate_inputs(symbol: str, **dimensions: Dict[str, Any]) -> None:
        """
        Validate the symbol and dimension inputs for drawing methods.

        This private helper method ensures that the symbol is a single,
        printable character and that all provided dimensions (e.g., width,
        height) are positive integers.

        Args:
            symbol (str): The character to use for drawing.
            **dimensions: A dictionary of dimension names and their values.

        Raises:
            ValueError: If the symbol is not a single character, is a
                        whitespace character, or if any dimension is not a
                        positive integer.
            TypeError: If any dimension is not an integer.
        """
        # Validate the symbol
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

        # Validate the dimensions (width, height, etc.)
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"The '{name}' must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If width is not an integer.
        """
        self._validate_inputs(symbol=symbol, width=width)
        row = symbol * width
        rows = [row] * width
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If width or height are not integers.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous row.

        Args:
            width (int): The width of the parallelogram's top/bottom edge.
            height (int): The height of the parallelogram.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If width or height are not integers.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        rows = [' ' * i + symbol * width for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner. The width of the triangle
        base is determined by the 'width' parameter, and it reaches that width
        over 'height' rows.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If width or height are not integers.
        """
        self._validate_inputs(symbol=symbol, width=width, height=height)
        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row based on a
            # linear growth rate to reach the final width at the given height.
            # We ensure at least one symbol is always printed.
            num_symbols = max(1, round((i + 1) * (width / height)))
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The single character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If inputs are invalid.
            TypeError: If height is not an integer.
        """
        self._validate_inputs(symbol=symbol, height=height)
        rows = []
        for i in range(height):
            # Calculate padding and number of symbols for each row
            padding = ' ' * (height - 1 - i)
            num_symbols = 1 + (2 * i)
            rows.append(padding + symbol * num_symbols)
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.

    artist = AsciiArt()
    print("--- ASCII Art Shape Generator ---")

    try:
        print("\n[+] Drawing a 5x5 Square with '#':")
        print(artist.draw_square(width=5, symbol='#'))

        print("\n[+] Drawing a 10x4 Rectangle with '*':")
        print(artist.draw_rectangle(width=10, height=4, symbol='*'))
        
        print("\n[+] Drawing a 12x5 Parallelogram with '=':")
        print(artist.draw_parallelogram(width=12, height=5, symbol='='))

        print("\n[+] Drawing a 10x5 Right-Angled Triangle with '+':")
        print(artist.draw_triangle(width=10, height=5, symbol='+'))

        print("\n[+] Drawing a Pyramid of height 6 with '^':")
        print(artist.draw_pyramid(height=6, symbol='^'))
        
        # Example of error handling
        print("\n[!] Testing invalid input (negative height):")
        try:
            artist.draw_square(width=-3, symbol='X')
        except ValueError as e:
            print(f"    Caught expected error: {e}")
            
        print("\n[!] Testing invalid input (multi-character symbol):")
        try:
            artist.draw_pyramid(height=3, symbol='&&')
        except ValueError as e:
            print(f"    Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")

