
"""
Arithmetic Calculator Module

A robust calculator implementation that evaluates mathematical expressions
with support for basic arithmetic operations and parentheses.

Author: Senior Software Developer
Version: 1.0
"""

import re
from typing import List, Union, Tuple
from enum import Enum


class TokenType(Enum):
    """Enumeration of token types for expression parsing."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Represents a token in a mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: Union[float, str]):
        """
        Initialize a token.
        
        Args:
            token_type (TokenType): The type of the token
            value (Union[float, str]): The value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class CalculatorError(Exception):
    """Base exception class for calculator errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when an expression is syntactically invalid."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A mathematical expression calculator supporting basic arithmetic operations.
    
    Supports:
    - Addition (+), Subtraction (-), Multiplication (*), Division (/)
    - Parentheses for grouping
    - Positive and negative numbers (integers and floats)
    - Proper operator precedence
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    # Valid operators
    VALID_OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal calculator state."""
        self._tokens: List[Token] = []
        self._position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: The calculated result
            
        Raises:
            InvalidExpressionError: If the expression is invalid
            DivisionByZeroError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) / 2")
            2.5
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Empty expression provided")
        
        self._reset_state()
        
        try:
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate token sequence
            self._validate_tokens()
            
            # Parse and evaluate using recursive descent parser
            self._position = 0
            result = self._parse_expression()
            
            # Ensure all tokens were consumed
            if self._position < len(self._tokens):
                raise InvalidExpressionError("Unexpected tokens at end of expression")
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert expression string into tokens.
        
        Args:
            expression (str): The expression to tokenize
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        # Remove all whitespace
        expression = re.sub(r'\s+', '', expression)
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including negative numbers and decimals)
            if char.isdigit() or char == '.':
                number_str, i = self._extract_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
            
            # Handle operators
            elif char in self.VALID_OPERATORS:
                # Handle unary minus (negative numbers)
                if char == '-' and self._is_unary_minus():
                    number_str, i = self._extract_number(expression, i)
                    self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
                else:
                    self._tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
            
            # Handle parentheses
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
            
            # Invalid character
            else:
                raise InvalidExpressionError(f"Invalid character: '{char}'")
    
    def _extract_number(self, expression: str, start: int) -> Tuple[str, int]:
        """
        Extract a number (including negative and decimal) from expression.
        
        Args:
            expression (str): The full expression
            start (int): Starting position
            
        Returns:
            Tuple[str, int]: The number string and new position
        """
        i = start
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Extract digits and decimal point
        decimal_count = 0
        while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
            if expression[i] == '.':
                decimal_count += 1
                if decimal_count > 1:
                    raise InvalidExpressionError("Multiple decimal points in number")
            number_str += expression[i]
            i += 1
        
        if not number_str or number_str == '-' or number_str == '.':
            raise InvalidExpressionError("Invalid number format")
        
        return number_str, i
    
    def _is_unary_minus(self) -> bool:
        """
        Determine if the current minus sign is unary (negative number).
        
        Returns:
            bool: True if it's a unary minus, False if binary
        """
        return (len(self._tokens) == 0 or 
                self._tokens[-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])
    
    def _validate_tokens(self) -> None:
        """
        Validate the sequence of tokens for basic syntax errors.
        
        Raises:
            InvalidExpressionError: If token sequence is invalid
        """
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found")
        
        # Check parentheses balance
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unmatched closing parenthesis")
        
        if paren_count != 0:
            raise InvalidExpressionError("Unmatched opening parenthesis")
        
        # Check for consecutive operators
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if (current.type == TokenType.OPERATOR and 
                next_token.type == TokenType.OPERATOR):
                raise InvalidExpressionError("Consecutive operators not allowed")
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate expression using recursive descent parsing.
        
        Returns:
            float: The result of the expression
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """Parse addition and subtraction (lowest precedence)."""
        result = self._parse_multiplication_division()
        
        while (self._position < len(self._tokens) and 
               self._current_token().type == TokenType.OPERATOR and
               self._current_token().value in ['+', '-']):
            
            operator = self._current_token().value
            self._position += 1
            right = self._parse_multiplication_division()
            
            if operator == '+':
                result += right
            else:  # operator == '-'
                result -= right
        
        return result
    
    def _parse_multiplication_division(self) -> float:
        """Parse multiplication and division (higher precedence)."""
        result = self._parse_factor()
        
        while (self._position < len(self._tokens) and 
               self._current_token().type == TokenType.OPERATOR and
               self._current_token().value in ['*', '/']):
            
            operator = self._current_token().value
            self._position += 1
            right = self._parse_factor()
            
            if operator == '*':
                result *= right
            else:  # operator == '/'
                if right == 0:
                    raise DivisionByZeroError("Division by zero")
                result /= right
        
        return result
    
    def _parse_factor(self) -> float:
        """Parse factors (numbers and parenthesized expressions)."""
        if self._position >= len(self._tokens):
            raise InvalidExpressionError("Unexpected end of expression")
        
        token = self._current_token()
        
        if token.type == TokenType.NUMBER:
            self._position += 1
            return token.value
        
        elif token.type == TokenType.LEFT_PAREN:
            self._position += 1  # consume '('
            result = self._parse_expression()
            
            if (self._position >= len(self._tokens) or 
                self._current_token().type != TokenType.RIGHT_PAREN):
                raise InvalidExpressionError("Missing closing parenthesis")
            
            self._position += 1  # consume ')'
            return result
        
        else:
            raise InvalidExpressionError(f"Unexpected token: {token.value}")
    
    def _current_token(self) -> Token:
        """
        Get the current token being processed.
        
        Returns:
            Token: The current token
        """
        if self._position >= len(self._tokens):
            raise InvalidExpressionError("Unexpected end of expression")
        return self._tokens[self._position]


def main():
    """
    Main function for console-based calculator interface.
    Provides interactive calculator functionality.
    """
    calculator = Calculator()
    
    print("=== Arithmetic Calculator ===")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and decimal numbers")
    print("Type 'quit' or 'exit' to end the program")
    print("-" * 35)
    
    while True:
        try:
            expression = input("\nEnter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except CalculatorError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
