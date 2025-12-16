
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes using object-oriented programming
and adheres to ISO/IEC 25010 quality standards.
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art representations of geometric shapes.
    
    This class provides methods to draw various shapes including squares,
    rectangles, parallelograms, triangles, and pyramids using ASCII characters.
    All methods include comprehensive input validation and return formatted
    multi-line strings.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single printable character.
        
        Args:
            symbol: The character to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one character or is whitespace
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")

    @staticmethod
    def _validate_positive_integer(value: Union[int, float], name: str) -> None:
        """
        Validate that a value is a positive integer.
        
        Args:
            value: The value to validate
            name: The name of the parameter for error messages
            
        Raises:
            TypeError: If value is not an integer
            ValueError: If value is not positive
        """
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{name} must be an integer")
        
        if value <= 0:
            raise ValueError(f"{name} must be positive")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width: The width and height of the square (must be positive)
            symbol: Single character to fill the square (must be printable)
            
        Returns:
            Multi-line string representing the ASCII square
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If width is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_positive_integer(width, "width")
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(width))

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width: The width of the rectangle (must be positive)
            height: The height of the rectangle (must be positive)
            symbol: Single character to fill the rectangle (must be printable)
            
        Returns:
            Multi-line string representing the ASCII rectangle
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If dimensions are not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 3, '#'))
            ####
            ####
            ####
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that grows diagonally to the right.
        
        Each row is shifted one space to the right from the previous row,
        starting from the top-left corner.
        
        Args:
            width: The width of each row (must be positive)
            height: The height of the parallelogram (must be positive)
            symbol: Single character to fill the parallelogram (must be printable)
            
        Returns:
            Multi-line string representing the ASCII parallelogram
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If dimensions are not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 4, '+'))
            +++
             +++
              +++
               +++
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Add leading spaces for the diagonal effect
            leading_spaces = ' ' * row
            line = leading_spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        
        The triangle starts from the top-left corner with one symbol
        and increases by one symbol per row until reaching the specified width.
        
        Args:
            width: The maximum width of the triangle base (must be positive)
            height: The height of the triangle (must be positive)
            symbol: Single character to fill the triangle (must be printable)
            
        Returns:
            Multi-line string representing the ASCII triangle
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If dimensions are not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(4, 4, 'o'))
            o
            oo
            ooo
            oooo
        """
        self._validate_positive_integer(width, "width")
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate symbols per row, ensuring we don't exceed width
            symbols_in_row = min(row + 1, width)
            line = symbol * symbols_in_row
            lines.append(line)
        
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid centered on each row.
        
        The pyramid starts with one symbol at the top and increases
        by two symbols per row (one on each side) to maintain symmetry.
        
        Args:
            height: The height of the pyramid (must be positive)
            symbol: Single character to fill the pyramid (must be printable)
            
        Returns:
            Multi-line string representing the ASCII pyramid
            
        Raises:
            TypeError: If parameters are of incorrect type
            ValueError: If height is not positive or symbol is invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(4, '^'))
               ^
              ^^^
             ^^^^^
            ^^^^^^^
        """
        self._validate_positive_integer(height, "height")
        self._validate_symbol(symbol)
        
        lines = []
        max_width = 2 * height - 1  # Maximum width at the base
        
        for row in range(height):
            # Calculate symbols for this row (increases by 2 each row)
            symbols_count = 2 * row + 1
            # Calculate leading spaces for centering
            leading_spaces = (max_width - symbols_count) // 2
            
            line = ' ' * leading_spaces + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """
    Demonstration of the AsciiArt class functionality.
    
    This function showcases all available shapes with sample parameters
    and includes basic error handling demonstration.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator Demo")
    print("=" * 40)
    
    # Demonstrate each shape
    shapes_demo = [
        ("Square (5x5)", lambda: art.draw_square(5, '*')),
        ("Rectangle (6x4)", lambda: art.draw_rectangle(6, 4, '#')),
        ("Parallelogram (4x5)", lambda: art.draw_parallelogram(4, 5, '+')),
        ("Triangle (6x6)", lambda: art.draw_triangle(6, 6, 'o')),
        ("Pyramid (height 6)", lambda: art.draw_pyramid(6, '^')),
    ]
    
    for description, shape_func in shapes_demo:
        print(f"\n{description}:")
        try:
            result = shape_func()
            print(result)
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
    
    # Demonstrate error handling
    print("\n" + "=" * 40)
    print("Error Handling Demonstration:")
    
    error_cases = [
        ("Invalid symbol (multiple chars)", lambda: art.draw_square(3, 'ab')),
        ("Invalid symbol (whitespace)", lambda: art.draw_square(3, ' ')),
        ("Negative width", lambda: art.draw_square(-1, '*')),
        ("Zero height", lambda: art.draw_rectangle(5, 0, '#')),
        ("Non-integer parameter", lambda: art.draw_triangle(3.5, 4, 'x')),
    ]
    
    for description, error_func in error_cases:
        print(f"\n{description}:")
        try:
            error_func()
            print("No error (unexpected)")
        except (TypeError, ValueError) as e:
            print(f"Caught expected error: {e}")


if __name__ == "__main__":
    main()
