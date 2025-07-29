
import math

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    This class provides methods to draw simple geometric shapes using
    ASCII characters. It adheres to high-quality code standards, including
    input validation, efficiency, and clear documentation, aligning with
    the principles of ISO/IEC 25010.

    Attributes:
        None
    """

    def _validate_inputs(self, symbol: str, dimensions: dict[str, int]) -> None:
        """
        Validates the common inputs for drawing methods.

        This private helper method ensures that the symbol and dimensions
        meet the required criteria, promoting safety and fault tolerance.

        Args:
            symbol: The character to be used for drawing.
            dimensions: A dictionary mapping dimension names (e.g., 'width')
                        to their integer values.

        Raises:
            ValueError: If the symbol is not a single, printable, non-whitespace
                        character, or if any dimension is not a positive integer.
            TypeError: If any dimension is not an integer.
        """
        # Validate symbol
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        if not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a printable, non-whitespace character.")

        # Validate dimensions
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        This method leverages the draw_rectangle method for implementation,
        promoting code reusability.

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.
        """
        # A square is a rectangle with equal width and height.
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        The implementation is efficient, creating each row and joining them
        at the end, which is faster than repeated string concatenation.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the rectangle.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram.

        The shape grows diagonally to the right, with each subsequent row
        indented by one additional space.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.

        Returns:
            A multi-line string representing the parallelogram.
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

        The triangle grows to fit the bounding box defined by width and height.
        The width of each row is calculated proportionally to its vertical
        position, ensuring the base of the triangle has the specified width.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the triangle.

        Returns:
            A multi-line string representing the right-angled triangle.
        """
        self._validate_inputs(symbol, {'width': width, 'height': height})
        
        rows = []
        for i in range(height):
            # Calculate proportional width for the current row
            # Using math.ceil ensures the triangle grows steadily and the
            # final row has the correct width.
            current_width = math.ceil((i + 1) * width / height)
            rows.append(symbol * current_width)
            
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid.

        The pyramid has a base width of (2 * height - 1) characters.
        Each row is centered to create a symmetrical shape.

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the pyramid.

        Returns:
            A multi-line string representing the pyramid.
        """
        self._validate_inputs(symbol, {'height': height})
        
        rows = []
        # The total width of the pyramid's base
        base_width = 2 * height - 1
        
        for i in range(height):
            num_symbols = 2 * i + 1
            padding = " " * ((base_width - num_symbols) // 2)
            content = symbol * num_symbols
            rows.append(f"{padding}{content}")
            
        return "\n".join(rows)

# Example Usage (can be placed in a separate file, e.g., main.py)
if __name__ == "__main__":
    # This block demonstrates how to use the AsciiArt class and showcases
    # its functionality. It serves as a simple, informal test.
    
    artist = AsciiArt()
    
    print("--- 5x5 Square ---")
    print(artist.draw_square(width=5, symbol='*'))
    print("\n")

    print("--- 8x4 Rectangle ---")
    print(artist.draw_rectangle(width=8, height=4, symbol='#'))
    print("\n")

    print("--- 7x5 Parallelogram ---")
    print(artist.draw_parallelogram(width=7, height=5, symbol='+'))
    print("\n")

    print("--- 10x5 Right-Angled Triangle ---")
    print(artist.draw_triangle(width=10, height=5, symbol='@'))
    print("\n")

    print("--- 6-level Pyramid ---")
    print(artist.draw_pyramid(height=6, symbol='^'))
    print("\n")

    print("--- Input Validation Examples ---")
    try:
        artist.draw_square(width=-3, symbol='x')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        artist.draw_rectangle(width=5, height=5, symbol='$$')
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        artist.draw_pyramid(height=5, symbol=' ')
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        artist.draw_triangle(width=5.5, height=5, symbol='T')
    except TypeError as e:
        print(f"Caught expected error: {e}")
