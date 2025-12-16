
import math
from typing import Dict, Any

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various geometric shapes using
    ASCII characters. It adheres to high-quality code standards, including
    input validation, efficiency, and clear documentation, aligning with
    the principles of the ISO/IEC 25010 standard.

    Attributes:
        None

    Methods:
        draw_square(width, symbol): Draws a filled square.
        draw_rectangle(width, height, symbol): Draws a filled rectangle.
        draw_parallelogram(width, height, symbol): Draws a filled parallelogram.
        draw_triangle(width, height, symbol): Draws a filled right-angled triangle.
        draw_pyramid(height, symbol): Draws a filled symmetrical pyramid.
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates the symbol for drawing. (Safety, Reliability)

        Args:
            symbol: The character to be used for drawing.

        Raises:
            TypeError: If the symbol is not a string.
            ValueError: If the symbol is not a single, non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError(f"Symbol must be a string, but got {type(symbol).__name__}.")
        if len(symbol) != 1:
            raise ValueError(f"Symbol must be a single character, but got a string of length {len(symbol)}.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def _validate_dimensions(self, **dims: Any) -> None:
        """
        Validates shape dimensions. (Safety, Reliability)

        Args:
            **dims: Keyword arguments representing dimensions (e.g., width=5).

        Raises:
            TypeError: If any dimension is not an integer.
            ValueError: If any dimension is not a positive integer.
        """
        for name, value in dims.items():
            if not isinstance(value, int):
                raise TypeError(f"Dimension '{name}' must be an integer, but got {type(value).__name__}.")
            if value <= 0:
                raise ValueError(f"Dimension '{name}' must be a positive integer, but got {value}.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square. (Correctness, Reusability)

        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.

        Returns:
            A multi-line string representing the square.
        
        Raises:
            ValueError, TypeError: Propagated from validation helpers.
        """
        # This method promotes reusability by leveraging the draw_rectangle method.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_rectangle(self, width: int, height: int, symbol:str) -> str:
        """
        Draws a filled rectangle. (Correctness, Performance)

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.

        Returns:
            A multi-line string representing the rectangle.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        # Performance: Creating a single row and multiplying the list is more
        # efficient than building the string row by row in a loop.
        row = symbol * width
        rows = [row] * height
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, slanted to the right. (Correctness, Performance)

        Each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram's top/bottom sides.
            height: The height of the parallelogram.
            symbol: The character used to draw the shape.

        Returns:
            A multi-line string representing the parallelogram.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        # Performance & Readability: A list comprehension is both efficient and
        # clearly expresses the logic of generating each shifted row.
        rows = [" " * i + symbol * width for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle. (Correctness, Performance)

        The triangle grows from the top-left corner. The number of symbols
        per row is calculated to create a slope defined by width and height.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character used to draw the shape.

        Returns:
            A multi-line string representing the triangle.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)

        # Correctness: The formula using math.ceil ensures a smooth-looking
        # slope and that the final row has the correct width.
        rows = [
            symbol * int(math.ceil(i * width / height))
            for i in range(1, height + 1)
        ]
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid. (Correctness, Performance)

        Args:
            height: The height of the pyramid in rows.
            symbol: The character used to draw the shape.

        Returns:
            A multi-line string representing the pyramid.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)

        # Readability: The logic for calculating spaces and symbols for each
        # level of the pyramid is clearly laid out in the list comprehension.
        rows = [
            " " * (height - i) + symbol * (2 * i - 1)
            for i in range(1, height + 1)
        ]
        return "\n".join(rows)


if __name__ == '__main__':
    # This block demonstrates the usage of the AsciiArt class and serves
    # as a simple, informal test case. (Testability)
    
    # Instantiate the artist
    artist = AsciiArt()
    
    print("--- ASCII Art Shape Generator ---")
    
    try:
        print("\nSquare (5x5, symbol '#'):")
        print(artist.draw_square(5, '#'))

        print("\nRectangle (8x4, symbol '*'):")
        print(artist.draw_rectangle(8, 4, '*'))

        print("\nParallelogram (10x5, symbol '@'):")
        print(artist.draw_parallelogram(10, 5, '@'))

        print("\nRight-Angled Triangle (width=10, height=5, symbol '+'):")
        print(artist.draw_triangle(10, 5, '+'))

        print("\nPyramid (height=6, symbol '^'):")
        print(artist.draw_pyramid(6, '^'))

        # Example of error handling
        print("\n--- Testing Error Handling ---")
        print("Attempting to draw with an invalid symbol...")
        artist.draw_square(3, '@@')

    except (ValueError, TypeError) as e:
        print(f"Caught expected error: {e}")

