
"""
ASCII Art Generator

A console-based application for generating 2D ASCII art shapes.
Implements various geometric shapes using object-oriented programming
and adheres to ISO/IEC 25010 quality standards.
"""

from typing import Union


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various geometric shapes
    using ASCII characters, including squares, rectangles, parallelograms,
    triangles, and pyramids.
    """
    
    def __init__(self) -> None:
        """Initialize the AsciiArt instance."""
        pass
    
    def _validate_dimensions(self, width: int, height: int = None) -> None:
        """
        Validate width and height parameters.
        
        Args:
            width (int): The width dimension to validate
            height (int, optional): The height dimension to validate
            
        Raises:
            TypeError: If width or height is not an integer
            ValueError: If width or height is not positive
        """
        if not isinstance(width, int):
            raise TypeError("Width must be an integer")
        if width <= 0:
            raise ValueError("Width must be positive")
            
        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer")
            if height <= 0:
                raise ValueError("Height must be positive")
    
    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate the symbol parameter.
        
        Args:
            symbol (str): The symbol to validate
            
        Raises:
            TypeError: If symbol is not a string
            ValueError: If symbol is not exactly one printable character
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square
            symbol (str): The character to fill the square with
            
        Returns:
            str: Multi-line string representing the ASCII square
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_square(3, '*'))
            ***
            ***
            ***
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(width))
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle
            height (int): The height of the rectangle
            symbol (str): The character to fill the rectangle with
            
        Returns:
            str: Multi-line string representing the ASCII rectangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_rectangle(4, 2, '#'))
            ####
            ####
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        return '\n'.join(symbol * width for _ in range(height))
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from
        the top-left corner. Each row is shifted by one space to the right.
        
        Args:
            width (int): The width of the parallelogram base
            height (int): The height of the parallelogram
            symbol (str): The character to fill the parallelogram with
            
        Returns:
            str: Multi-line string representing the ASCII parallelogram
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_parallelogram(3, 3, '+'))
            +++
             +++
              +++
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            spaces = ' ' * row
            line = spaces + symbol * width
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from
        the top-left corner with one symbol and expanding by one
        symbol per row.
        
        Args:
            width (int): The maximum width of the triangle base
            height (int): The height of the triangle
            symbol (str): The character to fill the triangle with
            
        Returns:
            str: Multi-line string representing the ASCII triangle
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_triangle(3, 3, 'o'))
            o
            oo
            ooo
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate the number of symbols for this row
            symbols_count = min(row + 1, width)
            line = symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows symmetrically from top to bottom.
        Each row has an odd number of symbols, starting with 1 at the top.
        
        Args:
            height (int): The height of the pyramid
            symbol (str): The character to fill the pyramid with
            
        Returns:
            str: Multi-line string representing the ASCII pyramid
            
        Raises:
            TypeError: If parameters are not of correct type
            ValueError: If parameters are invalid
            
        Example:
            >>> art = AsciiArt()
            >>> print(art.draw_pyramid(3, '^'))
              ^
             ^^^
            ^^^^^
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate number of symbols (odd numbers: 1, 3, 5, ...)
            symbols_count = 2 * row + 1
            # Calculate leading spaces for centering
            spaces_count = height - row - 1
            line = ' ' * spaces_count + symbol * symbols_count
            lines.append(line)
        
        return '\n'.join(lines)


def main() -> None:
    """
    Main function to demonstrate the AsciiArt class functionality.
    
    Provides an interactive console interface for users to generate
    various ASCII art shapes.
    """
    art = AsciiArt()
    
    print("ASCII Art Generator")
    print("==================")
    print("Available shapes:")
    print("1. Square")
    print("2. Rectangle") 
    print("3. Parallelogram")
    print("4. Triangle")
    print("5. Pyramid")
    print("6. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '6':
                print("Goodbye!")
                break
            
            if choice not in ['1', '2', '3', '4', '5']:
                print("Invalid choice. Please enter 1-6.")
                continue
            
            # Get symbol input
            symbol = input("Enter a symbol (single printable character): ").strip()
            
            if choice == '1':  # Square
                width = int(input("Enter width: "))
                result = art.draw_square(width, symbol)
                
            elif choice == '2':  # Rectangle
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = art.draw_rectangle(width, height, symbol)
                
            elif choice == '3':  # Parallelogram
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = art.draw_parallelogram(width, height, symbol)
                
            elif choice == '4':  # Triangle
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = art.draw_triangle(width, height, symbol)
                
            elif choice == '5':  # Pyramid
                height = int(input("Enter height: "))
                result = art.draw_pyramid(height, symbol)
            
            print("\nGenerated ASCII Art:")
            print(result)
            
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
