
import math

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides a collection of methods to draw various geometric shapes
    using a specified character. It adheres to high-quality code standards,
    including robust input validation and clear documentation.
    """

    def _validate_inputs(
        self,
        symbol: str,
        dimensions: dict[str, int]
    ) -> None:
        """
        A private helper to validate common inputs for drawing methods.

        Args:
            symbol (str): The character to use for drawing.
            dimensions (dict): A dictionary mapping dimension names (e.g., 'width')
                               to their integer values.

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if a dimension is not positive.
        """
        # Validate symbol
        if not isinstance(symbol, str):
            raise TypeError("The drawing symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("The drawing symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("The drawing symbol cannot be a whitespace character.")

        # Validate dimensions
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"The dimension '{name}' must be an integer.")
            if value <= 0:
                raise ValueError(f"The dimension '{name}' must be positive.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width and height of the square.
            symbol (str): The character used to draw the square.

        Returns:
            str: A multi-line string representing the ASCII art square.
        
        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is not positive or symbol is invalid.
        """
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used to draw the rectangle.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        
        row = symbol * width
        rows = [row] * height
        
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, leaning to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width (int): The width of the parallelogram's top/bottom sides.
            height (int): The height of the parallelogram.
            symbol (str): The character used to draw the shape.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
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

        The triangle grows from the top-left corner, with the number of symbols
        per row scaling to meet the target width on the final row.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character used to draw the triangle.

        Returns:
            str: A multi-line string representing the ASCII art triangle.

        Raises:
            TypeError: If dimensions are not integers or symbol is not a string.
            ValueError: If dimensions are not positive or symbol is invalid.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})

        rows = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            # This ensures a smooth "slope" and that the last row has `width` symbols.
            # We use max(1, ...) to ensure the first row is never empty.
            current_width = max(1, round(((i + 1) / height) * width))
            rows.append(symbol * current_width)
            
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character used to draw the pyramid.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_inputs(symbol, {'height': height})

        rows = []
        # The total width of the pyramid's base is 2 * height - 1
        base_width = 2 * height - 1
        
        for i in range(height):
            # The number of symbols in the current row (0-indexed)
            num_symbols = 2 * i + 1
            # Calculate the padding on each side to center the symbols
            padding_size = (base_width - num_symbols) // 2
            padding = " " * padding_size
            content = symbol * num_symbols
            rows.append(f"{padding}{content}")

        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class.
    # It will only run when the script is executed directly.
    
    artist = AsciiArt()
    
    print("--- ASCII Art Demo ---")
    
    try:
        print("\n[+] Square (5x5, symbol '#')")
        print(artist.draw_square(width=5, symbol='#'))
        
        print("\n[+] Rectangle (10x4, symbol '*')")
        print(artist.draw_rectangle(width=10, height=4, symbol='*'))

        print("\n[+] Parallelogram (8x5, symbol '@')")
        print(artist.draw_parallelogram(width=8, height=5, symbol='@'))

        print("\n[+] Right-Angled Triangle (width=12, height=6, symbol 'T')")
        print(artist.draw_triangle(width=12, height=6, symbol='T'))
        
        print("\n[+] Pyramid (height=7, symbol '^')")
        print(artist.draw_pyramid(height=7, symbol='^'))
        
        # Example of error handling
        print("\n[!] Attempting to draw with an invalid symbol (should raise ValueError):")
        try:
            artist.draw_square(3, "&&")
        except ValueError as e:
            print(f"    Successfully caught expected error: {e}")

        print("\n[!] Attempting to draw with a negative dimension (should raise ValueError):")
        try:
            artist.draw_rectangle(5, -2, "$")
        except ValueError as e:
            print(f"    Successfully caught expected error: {e}")
            
    except (ValueError, TypeError) as e:
        print(f"\nAn unexpected error occurred during the demo: {e}")

