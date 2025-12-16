
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements an interface to draw
various geometric shapes using ASCII characters. The implementation prioritizes
code quality, adhering to principles of the ISO/IEC 25010 standard, including
correctness, performance, safety, and maintainability.
"""

import math

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a collection of methods for drawing filled, geometric
    shapes as multi-line strings. It enforces strict input validation to ensure
    functional correctness and safety.

    Methods:
        draw_square(width, symbol): Draws a filled square.
        draw_rectangle(width, height, symbol): Draws a filled rectangle.
        draw_parallelogram(width, height, symbol): Draws a filled parallelogram.
        draw_triangle(width, height, symbol): Draws a filled right-angled triangle.
        draw_pyramid(height, symbol): Draws a filled symmetrical pyramid.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the symbol used for drawing.

        This is a static helper method ensuring the symbol is a single,
        printable, non-whitespace character.

        Args:
            symbol: The character to validate.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single character, is whitespace,
                        or is not printable.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

    @staticmethod
    def _validate_positive_integers(*dimensions: int) -> None:
        """
        Validates that all provided dimensions are positive integers.

        This is a static helper method for validating dimensional arguments
        like width and height.

        Args:
            *dimensions: A variable number of integer dimensions to validate.

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive number (<= 0).
        """
        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError(f"Dimension must be an integer, but got {type(dim).__name__}.")
            if dim <= 0:
                raise ValueError(f"Dimension must be a positive integer, but got {dim}.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the ASCII square.
        
        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_positive_integers(width)
        self._validate_symbol(symbol)
        # A square is a rectangle with equal width and height.
        # This promotes code reuse and reduces maintenance.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.
            
        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
        """
        self._validate_positive_integers(width, height)
        self._validate_symbol(symbol)
        
        row = symbol * width
        # Creating a list of rows and joining is more memory-efficient
        # for large strings than repeated string concatenation.
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right relative
        to the row above it.

        Args:
            width: The width of the parallelogram's parallel sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the ASCII parallelogram.
            
        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
        """
        self._validate_positive_integers(width, height)
        self._validate_symbol(symbol)

        # Using a list comprehension for a concise and performant implementation.
        rows = [" " * i + symbol * width for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle's width grows proportionally with its height, fitting
        within the specified width x height bounding box.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the ASCII triangle.
            
        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
        """
        self._validate_positive_integers(width, height)
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row (i).
            # The slope is (width / height). For row i, the width is
            # (i + 1) * slope. We use math.ceil to ensure the shape is filled.
            num_symbols = math.ceil((i + 1) * width / height)
            
            # Ensure we don't exceed the maximum width on the final rows.
            num_symbols = min(width, num_symbols)
            
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.
            
        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_positive_integers(height)
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # For row i (0-indexed), there are (2*i + 1) symbols.
            num_symbols = 2 * i + 1
            # The total width of the pyramid is determined by its base.
            # Base width = 2 * (height - 1) + 1 = 2 * height - 1.
            # Padding on each side = (total_width - num_symbols) / 2
            # which simplifies to (height - 1 - i).
            padding = " " * (height - 1 - i)
            rows.append(padding + symbol * num_symbols)
        return "\n".join(rows)


if __name__ == "__main__":
    # This block serves as a simple demonstration of the AsciiArt class.
    # It allows for easy visual testing and showcases usage.
    
    # Create an instance of the AsciiArt class
    artist = AsciiArt()
    
    print("--- Demonstrating AsciiArt Shapes ---")

    try:
        print("\n[ Square (5x5, '#') ]")
        print(artist.draw_square(5, "#"))

        print("\n[ Rectangle (8x4, '*') ]")
        print(artist.draw_rectangle(8, 4, "*"))

        print("\n[ Parallelogram (10x5, '=') ]")
        print(artist.draw_parallelogram(10, 5, "="))

        print("\n[ Triangle (width=10, height=5, '+') ]")
        print(artist.draw_triangle(10, 5, "+"))
        
        print("\n[ Triangle (width=7, height=7, 'T') ]")
        print(artist.draw_triangle(7, 7, "T"))

        print("\n[ Pyramid (height=6, '^') ]")
        print(artist.draw_pyramid(6, "^"))

        print("\n--- Demonstrating Input Validation ---")
        print("Attempting to draw with invalid input (negative width)...")
        artist.draw_square(-3, "X")

    except (ValueError, TypeError) as e:
        print(f"Successfully caught expected error: {e}")

