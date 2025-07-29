
"""
Console-based Arithmetic Calculator

A high-quality calculator implementation that evaluates mathematical expressions
with proper operator precedence, parentheses support, and comprehensive error handling.
Complies with ISO/IEC 25010 quality standards.
"""

import re
from typing import List, Union
from enum import Enum


class TokenType(Enum):
    """Enumeration of token types for expression parsing."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Represents a token in the mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: Union[float, str]):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The value of the token (number or operator symbol)
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


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
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence,
    parentheses, and both integer and floating-point numbers (including negative values).
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
        self._position = 0
    
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
        
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found in expression")
        
        # Validate parentheses balance
        self._validate_parentheses()
        
        # Parse and evaluate using recursive descent parser
        self._position = 0
        result = self._parse_expression()
        
        # Ensure all tokens were consumed
        if self._position < len(self._tokens):
            raise InvalidExpressionError("Unexpected tokens at end of expression")
        
        return result
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List of Token objects
            
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
            
            # Handle numbers (including negative numbers and decimals)
            if char.isdigit() or char == '.':
                number_str, i = self._extract_number(expression, i)
                try:
                    number_value = float(number_str)
                    tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number format: {number_str}")
            
            # Handle operators
            elif char in self.OPERATORS:
                # Handle negative numbers (unary minus)
                if char == '-' and self._is_unary_minus_context(tokens):
                    # This is a unary minus, treat as part of the next number
                    if i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        number_str, i = self._extract_number(expression, i)
                        try:
                            number_value = float(number_str)
                            tokens.append(Token(TokenType.NUMBER, number_value))
                        except ValueError:
                            raise InvalidExpressionError(f"Invalid number format: {number_str}")
                    else:
                        raise InvalidExpressionError("Invalid use of unary minus")
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
            
            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
            
            # Invalid character
            else:
                raise InvalidExpressionError(f"Invalid character: {char}")
        
        return tokens
    
    def _extract_number(self, expression: str, start_pos: int) -> tuple[str, int]:
        """
        Extract a complete number (including decimals and negative sign) from the expression.
        
        Args:
            expression: The full expression string
            start_pos: Starting position in the expression
            
        Returns:
            Tuple of (number_string, next_position)
        """
        i = start_pos
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Extract digits and decimal point
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
        
        return number_str, i
    
    def _is_unary_minus_context(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign should be treated as unary (negative number).
        
        Args:
            tokens: List of tokens processed so far
            
        Returns:
            True if the minus should be treated as unary
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_parentheses(self) -> None:
        """
        Validate that parentheses are properly balanced.
        
        Raises:
            UnbalancedParenthesesError: If parentheses are not balanced
        """
        balance = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                balance += 1
            elif token.type == TokenType.RIGHT_PAREN:
                balance -= 1
                if balance < 0:
                    raise UnbalancedParenthesesError("Unmatched closing parenthesis")
        
        if balance != 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate an expression using recursive descent parsing.
        Handles addition and subtraction (lowest precedence).
        
        Returns:
            The evaluated result
        """
        result = self._parse_term()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['+', '-']):
            
            operator = self._tokens[self._position].value
            self._position += 1
            right_operand = self._parse_term()
            
            if operator == '+':
                result += right_operand
            else:  # operator == '-'
                result -= right_operand
        
        return result
    
    def _parse_term(self) -> float:
        """
        Parse and evaluate a term (handles multiplication and division).
        
        Returns:
            The evaluated result
        """
        result = self._parse_factor()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['*', '/']):
            
            operator = self._tokens[self._position].value
            self._position += 1
            right_operand = self._parse_factor()
            
            if operator == '*':
                result *= right_operand
            else:  # operator == '/'
                if right_operand == 0:
                    raise DivisionByZeroError("Division by zero is not allowed")
                result /= right_operand
        
        return result
    
    def _parse_factor(self) -> float:
        """
        Parse and evaluate a factor (numbers and parenthesized expressions).
        
        Returns:
            The evaluated result
            
        Raises:
            InvalidExpressionError: If unexpected token is encountered
        """
        if self._position >= len(self._tokens):
            raise InvalidExpressionError("Unexpected end of expression")
        
        token = self._tokens[self._position]
        
        if token.type == TokenType.NUMBER:
            self._position += 1
            return token.value
        
        elif token.type == TokenType.LEFT_PAREN:
            self._position += 1  # consume '('
            result = self._parse_expression()
            
            if (self._position >= len(self._tokens) or 
                self._tokens[self._position].type != TokenType.RIGHT_PAREN):
                raise InvalidExpressionError("Missing closing parenthesis")
            
            self._position += 1  # consume ')'
            return result
        
        else:
            raise InvalidExpressionError(f"Unexpected token: {token}")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and decimal numbers")
    print("Type 'quit' or 'exit' to stop")
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
            
        except CalculatorError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
