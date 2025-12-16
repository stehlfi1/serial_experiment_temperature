
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which implements methods to draw
various geometric shapes using ASCII characters. The implementation focuses on
correctness, efficiency, safety, and maintainability, aligning with the
ISO/IEC 25010 standard for software quality.
"""

import math

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides a clean interface for creating filled, console-based
    shapes like squares, rectangles, and pyramids. It includes robust input
    validation to ensure functional safety and prevent unexpected behavior.

    Attributes:
        None
    """

    def _validate(self, symbol: str, **dimensions: int) -> None:
        """
        Private helper method to validate input parameters.

        This method centralizes input validation to ensure that all drawing
        functions operate on safe and valid data, enhancing the reliability
        and security of the class.

        Args:
            symbol (str): The character to be used for drawing.
            **dimensions (int): Keyword arguments for shape dimensions (e.g.,
                                width, height).

        Raises:
            TypeError: If a dimension is not an integer or the symbol is not a
                       string.
            ValueError: If a dimension is non-positive, the symbol is not a
                        single character, or the symbol is a whitespace character.
        """
        # --- Symbol Validation ---
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        # --- Dimension Validation ---
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"Dimension '{name}' must be an integer, not {type(value).__name__}.")
            if value <= 0:
                raise ValueError(f"Dimension '{name}' must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method provides a simplified interface for drawing a square, which
        is a special case of a rectangle.

        Args:
            width (int): The width and height of the square. Must be a positive
                         integer.
            symbol (str): The single, non-whitespace character to draw the
                          square with.

        Returns:
            str: A multi-line string representing the ASCII square.
        
        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate(symbol, width=width)
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle.

        The implementation is performance-oriented, using string multiplication
        and list joining for efficient string construction.

        Args:
            width (int): The width of the rectangle. Must be a positive integer.
            height (int): The height of the rectangle. Must be a positive integer.
            symbol (str): The single, non-whitespace character to draw the
                          rectangle with.

        Returns:
            str: A multi-line string representing the ASCII rectangle.

        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
        """
        self._validate(symbol, width=width, height=height)
        row = symbol * width
        # Efficiently create the multi-line string by joining a list of rows
        return "\n".join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is indented by one additional space to create the
        slanted effect, demonstrating clear algorithmic logic.

        Args:
            width (int): The width of the parallelogram. Must be a positive
                         integer.
            height (int): The height of the parallelogram. Must be a positive
                          integer.
            symbol (str): The single, non-whitespace character to draw the
                          parallelogram with.

        Returns:
            str: A multi-line string representing the ASCII parallelogram.

        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
        """
        self._validate(symbol, width=width, height=height)
        shape_rows = []
        for i in range(height):
            indentation = " " * i
            content = symbol * width
            shape_rows.append(f"{indentation}{content}")
        return "\n".join(shape_rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows to fit within the specified width and height,
        starting from the top-left. The number of symbols per row is
        calculated to ensure the final row has the specified width.

        Args:
            width (int): The width of the triangle's base. Must be a positive
                         integer.
            height (int): The height of the triangle. Must be a positive
                          integer.
            symbol (str): The single, non-whitespace character to draw the
                          triangle with.

        Returns:
            str: A multi-line string representing the ASCII triangle.
        
        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
        """
        self._validate(symbol, width=width, height=height)
        shape_rows = []
        for i in range(height):
            # Calculate symbols for the current row to scale correctly
            # to the final width and height.
            num_symbols = math.ceil((i + 1) * width / height)
            shape_rows.append(symbol * num_symbols)
        return "\n".join(shape_rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        The algorithm correctly calculates the necessary padding and number of
        symbols for each level of the pyramid to ensure symmetry.

        Args:
            height (int): The height of the pyramid. Must be a positive
                          integer.
            symbol (str): The single, non-whitespace character to draw the
                          pyramid with.

        Returns:
            str: A multi-line string representing the ASCII pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate(symbol, height=height)
        shape_rows = []
        for i in range(height):
            # Number of symbols for the current row (1, 3, 5, ...)
            num_symbols = 2 * i + 1
            # Indentation to center the row
            indentation = " " * (height - 1 - i)
            shape_rows.append(f"{indentation}{symbol * num_symbols}")
        return "\n".join(shape_rows)

# --- Example Usage ---
# This block demonstrates the functionality of the AsciiArt class and allows
# for easy, informal testing. It will only run when the script is executed
# directly.
if __name__ == "__main__":
    # Instantiate the drawing class
    artist = AsciiArt()

    print("--- ASCII Art Generator ---")

    try:
        print("\n[+] Square (5x5, #):")
        print(artist.draw_square(width=5, symbol="#"))

        print("\n[+] Rectangle (8x4, *):")
        print(artist.draw_rectangle(width=8, height=4, symbol="*"))

        print("\n[+] Parallelogram (10x5, @):")
        print(artist.draw_parallelogram(width=10, height=5, symbol="@"))
        
        print("\n[+] Right-angled Triangle (width=7, height=4, +):")
        print(artist.draw_triangle(width=7, height=4, symbol="+"))

        print("\n[+] Pyramid (height=6, ^):")
        print(artist.draw_pyramid(height=6, symbol="^"))

        # Example of error handling
        print("\n[!] Testing Error Handling: draw_square(-3, 'X')")
        try:
            artist.draw_square(width=-3, symbol="X")
        except ValueError as e:
            print(f"    Successfully caught expected error: {e}")

        print("\n[!] Testing Error Handling: draw_rectangle(5, 3, 'AB')")
        try:
            artist.draw_rectangle(width=5, height=3, symbol="AB")
        except ValueError as e:
            print(f"    Successfully caught expected error: {e}")
            
        print("\n[!] Testing Error Handling: draw_pyramid('a', '$')")
        try:
            # Mypy would catch this, but for runtime demonstration:
            artist.draw_pyramid(height='a', symbol="$") # type: ignore
        except TypeError as e:
            print(f"    Successfully caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during demonstration: {e}")
