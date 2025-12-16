
"""
ascii_art.py

A console-based 2D ASCII Art generator implemented in Python, applying OOP best practices and adhering to ISO/IEC 25010 quality guidelines.

Author: Senior Software Developer
Date: 2024-06
"""

import string

class AsciiArt:
    """
    A class for generating ASCII representations of common geometric shapes.
    
    Methods
    -------
    draw_square(width: int, symbol: str) -> str
        Draws and returns a square filled with the specified symbol.
        
    draw_rectangle(width: int, height: int, symbol: str) -> str
        Draws and returns a rectangle filled with the specified symbol.
        
    draw_parallelogram(width: int, height: int, symbol: str) -> str
        Draws and returns a parallelogram with each row indented one space more than the previous row.
        
    draw_triangle(width: int, height: int, symbol: str) -> str
        Draws and returns a right-angled triangle filled with the specified symbol.
        
    draw_pyramid(height: int, symbol: str) -> str
        Draws and returns a symmetrical pyramid filled with the specified symbol.
    """

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single printable, non-whitespace character.
        
        Raises
        ------
        ValueError
            If the symbol is not a single, non-whitespace, printable character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol in string.whitespace:
            raise ValueError("Symbol must not be a whitespace character.")
        if symbol not in string.printable or symbol in string.whitespace:
            raise ValueError("Symbol must be a single printable, non-whitespace character.")

    def _validate_positive_int(self, value: int, var_name: str) -> None:
        """
        Validates that a value is a positive integer (>0).
        
        Raises
        ------
        ValueError
            If the value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{var_name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{var_name} must be greater than 0.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square, of given width and symbol.

        Parameters
        ----------
        width : int
            The width (and height) of the square, must be > 0.
        symbol : str
            A single, non-whitespace, printable character.

        Returns
        -------
        str
            Multiline string representing the square.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Parameters
        ----------
        width : int
            The width of the rectangle, must be > 0.
        height : int
            The height of the rectangle, must be > 0.
        symbol : str
            A single, non-whitespace, printable character.
        
        Returns
        -------
        str
            Multiline string representing the rectangle.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join([line for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram (left-top aligned, each row shifts right by one space).

        Parameters
        ----------
        width : int
            The width of the parallelogram, must be > 0.
        height : int
            The height of the parallelogram, must be > 0.
        symbol : str
            A single, non-whitespace, printable character.

        Returns
        -------
        str
            Multiline string representing the parallelogram.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            spaces = ' ' * i
            line = spaces + (symbol * width)
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle (right-angle at top-left, grows to right).

        Parameters
        ----------
        width : int
            The width (horizontal size) of the triangle's base, must be > 0.
        height : int
            The height (vertical size) of the triangle, must be > 0.
        symbol : str
            A single, non-whitespace, printable character.

        Returns
        -------
        str
            Multiline string representing the triangle.

        Notes
        -----
        Triangle is right-angled at the top-left corner.
        Fills each row with min(width, current computed size).
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Calculate target width for current row (linear interpolation between 1 and width)
            # so that bottom row is width, top row is 1
            row_width = max(1, int(round((width - 1) * row / (height - 1))) + 1 if height > 1 else width)
            row_width = min(row_width, width)
            lines.append(symbol * row_width)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetric pyramid (centered, base width = 2*height-1).

        Parameters
        ----------
        height : int
            The height of the pyramid, must be > 0.
        symbol : str
            A single, non-whitespace, printable character.

        Returns
        -------
        str
            Multiline string representing the pyramid.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            spaces = ' ' * (height - i - 1)
            line = spaces + (symbol * num_symbols) + spaces
            lines.append(line)
        return "\n".join(lines)


# Example usage and minimal test cases
if __name__ == "__main__":
    art = AsciiArt()
    print("SQUARE:\n", art.draw_square(4, '#'))
    print("\nRECTANGLE:\n", art.draw_rectangle(6, 3, '*'))
    print("\nPARALLELOGRAM:\n", art.draw_parallelogram(5, 4, '@'))
    print("\nTRIANGLE:\n", art.draw_triangle(6, 4, '+'))
    print("\nPYRAMID:\n", art.draw_pyramid(5, '^'))
