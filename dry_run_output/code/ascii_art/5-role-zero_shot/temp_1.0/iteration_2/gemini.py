
# -*- coding: utf-8 -*-
"""
ascii_art.py

A module for generating 2D ASCII art shapes.

This module provides the AsciiArt class, which contains methods for drawing
various geometric shapes using a specified character. The implementation follows
best practices for quality, maintainability, and robustness in line with
ISO/IEC 25010 principles.
"""

from typing import Dict, Any

class AsciiArt:
    """
    A class to generate various 2D ASCII art shapes.

    Each method validates its inputs and returns a multi-line string
    representing the requested shape.
    """

    @staticmethod
    def _validate_inputs(symbol: str, **dimensions: int) -> None:
        """
        Validates the symbol and dimension inputs for drawing methods.

        This private helper ensures that inputs meet the required criteria,
        promoting reliability and fault tolerance.

        Args:
            symbol (str): The character to use for drawing.
            **dimensions (int): A dictionary of named dimensions (e.g., width, height).

        Raises:
            TypeError: If the symbol is not a string or a dimension is not an integer.
            ValueError: If the symbol is not a single, non-whitespace character,
                        or if a dimension is not a positive integer.
        """
        # Validate symbol
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

        # Validate dimensions
        for name, value in dimensions.items():
            if not isinstance(value, int):
                raise TypeError(f"{name.capitalize()} must be an integer.")
            if value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            TypeError: For invalid input types.
            ValueError: For invalid input values.
        """
        self._validate_inputs(symbol, width=width, height=height)
        
        row = symbol * width
        # Use list multiplication and join for efficient string building
        return "\n".join([row] * height)

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square. This is a convenience method that reuses
        the draw_rectangle logic, promoting code reusability.

        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing the square.

        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            TypeError: For invalid input types.
            ValueError: For invalid input values.
        """
        # A square is a rectangle with equal width and height.
        # No need to re-validate here as draw_rectangle will do it.
        return self.draw_rectangle(width=width, height=width, symbol=symbol)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram, skewed to the right.

        Each subsequent row is shifted one space to the right relative to the
        previous one.

        Args:
            width (int): The width of the parallelogram's top/bottom edge.
            height (int): The perpendicular height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            TypeError: For invalid input types.
            ValueError: For invalid input values.
        """
        self._validate_inputs(symbol, width=width, height=height)
        
        rows = [
            " " * i + symbol * width
            for i in range(height)
        ]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled, right-angled triangle.

        The triangle grows from the top-left, filling a bounding box
        defined by the specified width and height. The number of symbols
        in each row is scaled linearly.

        Args:
            width (int): The maximum width of the triangle at its base.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            TypeError: For invalid input types.
            ValueError: For invalid input values.
        """
        self._validate_inputs(symbol, width=width, height=height)

        rows = []
        for i in range(height):
            # Calculate the width for the current row based on scaling
            # The ratio (i + 1) / height determines the progress down the triangle
            current_width = round((i + 1) * width / height)
            
            # Ensure at least one symbol is drawn for thin triangles
            current_width = max(1, current_width)
            
            rows.append(symbol * current_width)
            
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid.

        Args:
            height (int): The height of the pyramid in rows.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            TypeError: For invalid input types.
            ValueError: For invalid input values.
        """
        self._validate_inputs(symbol, height=height)
        
        rows = []
        for i in range(height):
            # Number of symbols in the current row (1, 3, 5, ...)
            num_symbols = 2 * i + 1
            # Amount of padding on each side to keep it centered
            padding = " " * (height - 1 - i)
            rows.append(f"{padding}{symbol * num_symbols}")

        return "\n".join(rows)


if __name__ == "__main__":
    """
    Demonstration of the AsciiArt class.
    
    This block showcases the usage of each drawing function and provides
    an example of how exceptions are handled for invalid inputs. This makes
    the module runnable and easy to understand.
    """
    
    drawer = AsciiArt()

    print("--- High-Quality ASCII Art Generator ---")

    # Define shapes and their drawing functions for easy demonstration
    shapes_to_draw = {
        "Square (5x5, '#')": lambda: drawer.draw_square(5, "#"),
        "Rectangle (10x4, '*')": lambda: drawer.draw_rectangle(10, 4, "*"),
        "Parallelogram (8x5, '=')": lambda: drawer.draw_parallelogram(8, 5, "="),
        "Right Triangle (width=10, height=5, '+')": lambda: drawer.draw_triangle(10, 5, "+"),
        "Right Triangle (width=6, height=12, 'T')": lambda: drawer.draw_triangle(6, 12, "T"),
        "Pyramid (height=6, '^')": lambda: drawer.draw_pyramid(6, "^"),
    }

    for title, draw_func in shapes_to_draw.items():
        print(f"\n--- {title} ---")
        print(draw_func())

    # --- Demonstrate Error Handling ---
    print("\n\n--- Demonstrating Error Handling ---")
    
    error_cases = {
        "Negative width": lambda: drawer.draw_square(-3, "X"),
        "Zero height": lambda: drawer.draw_rectangle(5, 0, "X"),
        "Multi-character symbol": lambda: drawer.draw_pyramid(4, "^^"),
        "Whitespace symbol": lambda: drawer.draw_square(4, " "),
        "Non-integer height": lambda: drawer.draw_pyramid(4.5, "$"),
    }

    for description, error_func in error_cases.items():
        try:
            error_func()
        except (ValueError, TypeError) as e:
            print(f"OK: Caught expected error for '{description}': {e}")

