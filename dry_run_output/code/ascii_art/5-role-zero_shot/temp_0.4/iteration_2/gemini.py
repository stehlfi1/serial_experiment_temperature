
import math
from typing import Dict, Optional

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various geometric shapes using a specified
    character. It adheres to ISO/IEC 25010 principles by ensuring correctness,
    performance, safety through input validation, and maintainability via a
    modular, well-documented structure.

    Attributes:
        None
    """

    def _validate_inputs(
        self,
        symbol: str,
        dimensions: Dict[str, Optional[int]]
    ) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper method centralizes input validation to ensure
        that the symbol and dimensions meet the required criteria, promoting
        code reusability and safety.

        Args:
            symbol: The character to be used for drawing.
            dimensions: A dictionary mapping dimension names (e.g., 'width')
                        to their integer values.

        Raises:
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if any dimension is a non-positive integer.
            TypeError: If any dimension is not an integer.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        for name, value in dimensions.items():
            if value is None:
                continue
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII square.
        """
        # A square is a rectangle with equal width and height.
        # We delegate to the more general draw_rectangle method.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII rectangle.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})

        row = symbol * width
        # Using a list comprehension and join is more memory-efficient
        # for building multi-line strings than repeated concatenation.
        rows = [row for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled parallelogram, slanted to the right.

        Each subsequent row is shifted one space to the right relative
        to the one above it.

        Args:
            width: The width of the parallelogram's top and bottom sides.
            height: The height of the parallelogram.
            symbol: The character to use for drawing the parallelogram.

        Returns:
            A multi-line string representing the ASCII parallelogram.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})

        rows = []
        for i in range(height):
            padding = " " * i
            content = symbol * width
            rows.append(f"{padding}{content}")
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left corner. The number of symbols
        in each row is scaled based on the overall width and height,
        creating a proportional shape.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing the triangle.

        Returns:
            A multi-line string representing the ASCII right-angled triangle.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})

        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row based on a
            # linear slope. math.ceil ensures the shape grows correctly.
            num_symbols = math.ceil((i + 1) * width / height)
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character to use for drawing the pyramid.

        Returns:
            A multi-line string representing the ASCII pyramid.
        """
        self._validate_inputs(symbol, {'height': height})

        rows = []
        # The width of the pyramid's base determines the canvas width.
        base_width = 2 * height - 1

        for i in range(height):
            # Number of symbols increases by 2 in each row (1, 3, 5, ...)
            num_symbols = 2 * i + 1
            # Calculate padding to center the symbols within the base width.
            padding = " " * ((base_width - num_symbols) // 2)
            content = symbol * num_symbols
            rows.append(f"{padding}{content}")
        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    # --- Testability & Correctness Demonstration ---
    # The code is easily testable by instantiating the class and calling
    # its methods. The pure-function nature of the drawing methods
    # (same input yields same output) simplifies testing.

    artist = AsciiArt()
    symbol = "*"

    print("--- ASCII Art Generator ---")

    try:
        print("\n[+] Square (5x5):")
        print(artist.draw_square(5, symbol))

        print("\n[+] Rectangle (8x4):")
        print(artist.draw_rectangle(8, 4, symbol))

        print("\n[+] Parallelogram (10x5):")
        print(artist.draw_parallelogram(10, 5, symbol))

        print("\n[+] Right-Angled Triangle (width=10, height=5):")
        print(artist.draw_triangle(10, 5, symbol))

        print("\n[+] Pyramid (height=6):")
        print(artist.draw_pyramid(6, symbol))

        # --- Safety Demonstration (Invalid Input) ---
        print("\n[+] Testing Error Handling...")
        try:
            artist.draw_square(5, "@@")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            artist.draw_rectangle(-3, 5, "$")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        try:
            artist.draw_pyramid(5, " ")
        except ValueError as e:
            print(f"Caught expected error: {e}")

    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred: {e}")

