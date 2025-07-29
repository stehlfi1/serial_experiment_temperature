
"""
Console-based Arithmetic Calculator

A high-quality calculator implementation that evaluates mathematical expressions
with support for basic arithmetic operations and parentheses, following ISO/IEC 25010 standards.
"""

import re
from typing import List, Union
from enum import Enum


class TokenType(Enum):
    """Enumeration for different types of tokens in mathematical expressions."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Represents a token in a mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: str, position: int):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The string value of the token
            position: Position in the original expression
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value}, {self.position})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid syntax or characters."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports:
    - Basic arithmetic operations: +, -, *, /
    - Parentheses for grouping
    - Integer and floating-point numbers (including negative values)
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
    OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for new calculation."""
        self._tokens: List[Token] = []
        self._current_position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: Mathematical expression as a string
            
        Returns:
            The calculated result as a float
            
        Raises:
            InvalidExpressionError: If the expression contains invalid syntax
            DivisionByZeroError: If division by zero is attempted
            UnbalancedParenthesesError: If parentheses are not balanced
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        self._reset_state()
        
        # Tokenize the expression
        self._tokens = self._tokenize(expression.strip())
        
        # Validate tokens
        self._validate_tokens()
        
        # Parse and evaluate using recursive descent parser
        self._current_position = 0
        result = self._parse_expression()
        
        # Ensure all tokens were consumed
        if self._current_position < len(self._tokens):
            raise InvalidExpressionError(
                f"Unexpected token at position {self._tokens[self._current_position].position}"
            )
        
        return result
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize the input expression into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List of tokens representing the expression
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including decimals and negative numbers)
            if char.isdigit() or char == '.':
                number_str, new_i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
                continue
            
            # Handle negative numbers (when '-' appears at start or after operator/left paren)
            if char == '-' and self._is_negative_number_context(tokens):
                number_str, new_i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
                continue
            
            # Handle operators
            if char in self.OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, char, i))
                i += 1
                continue
            
            # Handle parentheses
            if char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
                continue
            
            if char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
                continue
            
            # Invalid character
            raise InvalidExpressionError(f"Invalid character '{char}' at position {i}")
        
        return tokens
    
    def _extract_number(self, expression: str, start: int) -> tuple[str, int]:
        """
        Extract a number (including negative numbers and decimals) from the expression.
        
        Args:
            expression: The full expression
            start: Starting position
            
        Returns:
            Tuple of (number_string, next_position)
        """
        i = start
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        decimal_found = False
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.' and not decimal_found:
                decimal_found = True
                number_str += char
                i += 1
            else:
                break
        
        # Validate the number format
        if number_str in ['-', '.', '-.'] or number_str.count('.') > 1:
            raise InvalidExpressionError(f"Invalid number format at position {start}")
        
        return number_str, i
    
    def _is_negative_number_context(self, tokens: List[Token]) -> bool:
        """
        Determine if a '-' character should be treated as part of a negative number.
        
        Args:
            tokens: List of tokens processed so far
            
        Returns:
            True if the '-' should be part of a negative number
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for syntax errors.
        
        Raises:
            InvalidExpressionError: If syntax errors are found
            UnbalancedParenthesesError: If parentheses are not balanced
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
                    raise UnbalancedParenthesesError(
                        f"Unmatched closing parenthesis at position {token.position}"
                    )
        
        if paren_count > 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
        
        # Validate token sequence
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the start or end
                if i == 0 or i == len(self._tokens) - 1:
                    raise InvalidExpressionError(
                        f"Operator '{token.value}' cannot be at position {token.position}"
                    )
                
                # Operators cannot be followed by other operators
                if (i + 1 < len(self._tokens) and 
                    self._tokens[i + 1].type == TokenType.OPERATOR):
                    raise InvalidExpressionError(
                        f"Consecutive operators at position {token.position}"
                    )
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate an expression using recursive descent parsing.
        
        Returns:
            The evaluated result
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """Parse addition and subtraction (lowest precedence)."""
        left = self._parse_multiplication_division()
        
        while (self._current_position < len(self._tokens) and
               self._tokens[self._current_position].type == TokenType.OPERATOR and
               self._tokens[self._current_position].value in ['+', '-']):
            
            operator = self._tokens[self._current_position].value
            self._current_position += 1
            right = self._parse_multiplication_division()
            
            if operator == '+':
                left = left + right
            else:  # operator == '-'
                left = left - right
        
        return left
    
    def _parse_multiplication_division(self) -> float:
        """Parse multiplication and division (higher precedence)."""
        left = self._parse_factor()
        
        while (self._current_position < len(self._tokens) and
               self._tokens[self._current_position].type == TokenType.OPERATOR and
               self._tokens[self._current_position].value in ['*', '/']):
            
            operator = self._tokens[self._current_position].value
            operator_position = self._tokens[self._current_position].position
            self._current_position += 1
            right = self._parse_factor()
            
            if operator == '*':
                left = left * right
            else:  # operator == '/'
                if right == 0:
                    raise DivisionByZeroError(
                        f"Division by zero at position {operator_position}"
                    )
                left = left / right
        
        return left
    
    def _parse_factor(self) -> float:
        """Parse factors (numbers and parenthesized expressions)."""
        if self._current_position >= len(self._tokens):
            raise InvalidExpressionError("Unexpected end of expression")
        
        token = self._tokens[self._current_position]
        
        if token.type == TokenType.NUMBER:
            self._current_position += 1
            try:
                return float(token.value)
            except ValueError:
                raise InvalidExpressionError(
                    f"Invalid number format '{token.value}' at position {token.position}"
                )
        
        elif token.type == TokenType.LEFT_PAREN:
            self._current_position += 1  # consume '('
            result = self._parse_expression()
            
            # Expect closing parenthesis
            if (self._current_position >= len(self._tokens) or
                self._tokens[self._current_position].type != TokenType.RIGHT_PAREN):
                raise UnbalancedParenthesesError("Missing closing parenthesis")
            
            self._current_position += 1  # consume ')'
            return result
        
        else:
            raise InvalidExpressionError(
                f"Unexpected token '{token.value}' at position {token.position}"
            )


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Enter 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (CalculatorError, KeyboardInterrupt) as e:
            if isinstance(e, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
