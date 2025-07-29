
import math
from typing import List

class AsciiArt:
    """
    A class for generating various 2D ASCII art shapes.

    This class provides methods to draw simple geometric shapes like squares,
    rectangles, and pyramids using user-specified symbols. It adheres to
    high-quality code standards, including input validation, clear documentation,
    and efficient implementation, aligning with the principles of ISO/IEC 25010.

    Attributes:
        None
    """

    def _validate_dimension(self, value: int, name: str = "dimension") -> None:
        """
        Validates that a dimension (e.g., width, height) is a positive integer.

        Args:
            value: The dimension value to validate.
            name: The name of the dimension for the error message.

        Raises:
            TypeError: If the value is not an integer.
            ValueError: If the value is not a positive integer (<= 0).
        """
        if not isinstance(value, int):
            raise TypeError(f"Error: The {name} must be an integer.")
        if value <= 0:
            raise ValueError(f"Error: The {name} must be a positive integer greater than 0.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace character.

        Args:
            symbol: The symbol string to validate.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single character or is a whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Error: The symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Error: The symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Error: The symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        # A square is a rectangle with equal width and height.
        # We can delegate the drawing logic to the draw_rectangle method.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle of a given width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        # More efficient to build a list of rows and join them at the end
        # than to use repeated string concatenation.
        row: str = symbol * width
        rows: List[str] = [row] * height
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
            A multi-line string representing the parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows: List[str] = []
        line: str = symbol * width
        for i in range(height):
            # Prepend spaces for the shift. Row 'i' gets 'i' spaces.
            padding = " " * i
            rows.append(f"{padding}{line}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner, scaling proportionally
        to fit the specified width and height.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string.
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows: List[str] = []
        for i in range(height):
            # Calculate the number of symbols for the current row (i).
            # The formula scales the number of symbols proportionally.
            # We use (i + 1) because rows are 0-indexed.
            # math.ceil ensures the shape grows and the final row has `width` symbols.
            num_symbols = math.ceil((i + 1) * width / height)
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows: List[str] = []
        # The base of the pyramid determines its maximum width
        max_width: int = 2 * height - 1

        for i in range(height):
            # Number of symbols in the current row
            num_symbols: int = 2 * i + 1
            # Calculate the necessary padding on the left to center the symbols
            padding: str = " " * ((max_width - num_symbols) // 2)
            # Construct the row
            rows.append(f"{padding}{symbol * num_symbols}")
        return "\n".join(rows)


if __name__ == "__main__":
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    artist = AsciiArt()

    print("--- ASCII Art Shape Generator ---")

    try:
        print("\n[+] Drawing a 5x5 Square with '#':")
        print(artist.draw_square(5, "#"))

        print("\n[+] Drawing a 10x4 Rectangle with '@':")
        print(artist.draw_rectangle(10, 4, "@"))

        print("\n[+] Drawing a 8x5 Parallelogram with '=':")
        print(artist.draw_parallelogram(8, 5, "="))

        print("\n[+] Drawing a 10x5 Right-Angled Triangle with '+':")
        print(artist.draw_triangle(10, 5, "+"))

        print("\n[+] Drawing a Pyramid of height 6 with '^':")
        print(artist.draw_pyramid(6, "^"))

        # --- Demonstration of Error Handling ---
        print("\n--- Testing Error Handling ---")

        print("\n[!] Testing invalid dimension (negative value):")
        try:
            artist.draw_square(-3, "X")
        except ValueError as e:
            print(e)

        print("\n[!] Testing invalid symbol (multiple characters):")
        try:
            artist.draw_rectangle(5, 5, "XX")
        except ValueError as e:
            print(e)

        print("\n[!] Testing invalid symbol (whitespace):")
        try:
            artist.draw_pyramid(4, " ")
        except ValueError as e:
            print(e)

        print("\n[!] Testing invalid type for height:")
        try:
            artist.draw_triangle(5, "five", "*")
        except TypeError as e:
            print(e)

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}")

