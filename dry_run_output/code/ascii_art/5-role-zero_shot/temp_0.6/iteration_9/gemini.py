
"""
A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which offers a suite of methods to
draw various geometric shapes using ASCII characters. The implementation focuses
on code quality, maintainability, and robustness, adhering to principles
outlined in the ISO/IEC 25010 standard.

Key Quality Attributes Addressed (ISO/IEC 25010):
- Functional Suitability: Correctly implements all required shape-drawing functions.
- Performance Efficiency: Uses efficient string-building techniques (list comprehensions
  and str.join) to minimize resource usage.
- Reliability: Incorporates robust input validation to handle errors gracefully
  and prevent crashes (Maturity, Fault Tolerance).
- Usability: Provides a clear, well-documented, and intuitive API.
- Maintainability: Employs an object-oriented structure, modular helper methods,
  and clear documentation to make the code easy to understand, modify, and test
  (Modularity, Reusability, Analyzability, Testability).
- Security: Basic input validation protects against malformed inputs that could
  cause unexpected behavior.
"""

import sys
from typing import List


class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    Each method returns a multi-line string representing the desired shape,
    filled with a specified symbol. The class ensures that all inputs are
    validated for correctness before any drawing operation proceeds.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates the symbol used for drawing.

        Args:
            symbol: The character to use for drawing the shape.

        Raises:
            ValueError: If the symbol is not a single character or is whitespace.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("The 'symbol' must be a single character string.")
        if symbol.isspace():
            raise ValueError("The 'symbol' cannot be a whitespace character.")

    @staticmethod
    def _validate_dimensions(*dims: int) -> None:
        """
        Validates the dimensions (width, height) for drawing.

        Args:
            *dims: A variable number of integer dimensions.

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive integer (must be > 0).
        """
        for dim in dims:
            if not isinstance(dim, int):
                raise TypeError(f"All dimensions must be integers, but received {type(dim)}.")
            if dim <= 0:
                raise ValueError(f"All dimensions must be positive, but received {dim}.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII square.
        """
        # A square is a rectangle with equal width and height.
        # Validation is implicitly handled by the draw_rectangle call.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width, height)

        row = symbol * width
        # Efficiently create the multi-line string using a list and join
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram.

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII parallelogram.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width, height)

        lines: List[str] = []
        base_row = symbol * width
        for i in range(height):
            padding = " " * i
            lines.append(f"{padding}{base_row}")
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle's width grows linearly from 1 to the specified `width`
        over `height` rows.

        Args:
            width: The final width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII triangle.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(width, height)

        lines: List[str] = []
        # Handle the edge case of height=1 to avoid division by zero
        if height == 1:
            return symbol * width

        for i in range(height):
            # Linearly interpolate the number of symbols for the current row
            # The formula ensures the width grows from 1 to `width` over `height` rows.
            # The final row (i = height - 1) will have exactly `width` symbols.
            current_width = 1 + int(i * (width - 1) / (height - 1))
            lines.append(symbol * current_width)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII pyramid.
        """
        self._validate_symbol(symbol)
        self._validate_dimensions(height)

        lines: List[str] = []
        for i in range(height):
            # Calculate padding and number of symbols for the current level
            num_symbols = 2 * i + 1
            padding = " " * (height - 1 - i)
            lines.append(f"{padding}{symbol * num_symbols}")
        return "\n".join(lines)


def main() -> int:
    """
    Main function to demonstrate the AsciiArt class functionality.
    Instantiates the AsciiArt class and prints various shapes to the console.
    """
    print("--- ASCII Art Generator ---")
    artist = AsciiArt()
    symbol = "*"

    try:
        # --- Demonstrate successful drawing ---
        print("\n[+] Drawing a 5x5 Square:")
        print(artist.draw_square(width=5, symbol=symbol))

        print("\n[+] Drawing a 7x4 Rectangle:")
        print(artist.draw_rectangle(width=7, height=4, symbol="$"))

        print("\n[+] Drawing a 6x4 Parallelogram:")
        print(artist.draw_parallelogram(width=6, height=4, symbol="#"))

        print("\n[+] Drawing a Right-Angled Triangle (Width=7, Height=4):")
        print(artist.draw_triangle(width=7, height=4, symbol="@"))
        
        print("\n[+] Drawing a Right-Angled Triangle (Width=4, Height=7):")
        print(artist.draw_triangle(width=4, height=7, symbol="@"))

        print("\n[+] Drawing a Pyramid (Height=5):")
        print(artist.draw_pyramid(height=5, symbol="^"))

        # --- Demonstrate input validation ---
        print("\n--- Testing Error Handling ---")
        try:
            print("\n[-] Attempting to draw with an invalid symbol (multi-char)...")
            artist.draw_square(3, "&&")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            print("\n[-] Attempting to draw with an invalid symbol (whitespace)...")
            artist.draw_square(3, " ")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            print("\n[-] Attempting to draw with a negative dimension...")
            artist.draw_rectangle(5, -3, "%")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        try:
            print("\n[-] Attempting to draw with a non-integer dimension...")
            artist.draw_rectangle(5, 3.5, "%")
        except TypeError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
