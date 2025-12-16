
"""
High-quality console-based arithmetic calculator implementation.

This module provides a Calculator class that can evaluate mathematical expressions
with support for basic arithmetic operations and parentheses while maintaining
proper operator precedence.
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
    """Represents a token in the mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: Union[float, str]):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class Calculator:
    """
    A high-quality arithmetic calculator that evaluates mathematical expressions.
    
    Supports addition, subtraction, multiplication, division, and parentheses
    with proper operator precedence. Handles both integers and floating-point
    numbers, including negative values.
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
        """Reset internal state for new calculation."""
        self._tokens: List[Token] = []
        self._position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: The mathematical expression to evaluate
            
        Returns:
            The result of the calculation as a float
            
        Raises:
            ValueError: If the expression is invalid
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5 + 3")
            -2.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        self._reset_state()
        
        try:
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate tokens
            self._validate_tokens()
            
            # Parse and evaluate using recursive descent parser
            self._position = 0
            result = self._parse_expression()
            
            # Ensure all tokens were consumed
            if self._position < len(self._tokens):
                raise ValueError("Unexpected tokens at end of expression")
            
            return float(result)
            
        except (ValueError, ZeroDivisionError):
            raise
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into a list of tokens.
        
        Args:
            expression: The expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Remove all whitespace
        expression = re.sub(r'\s+', '', expression)
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (integer or float)
                number_str, consumed = self._parse_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
                i += consumed
                
            elif char in self.VALID_OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
                
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
                
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
                
            else:
                raise ValueError(f"Invalid character: '{char}'")
    
    def _parse_number(self, expression: str, start: int) -> Tuple[str, int]:
        """
        Parse a number from the expression starting at the given position.
        
        Args:
            expression: The full expression
            start: Starting position
            
        Returns:
            Tuple of (number_string, characters_consumed)
            
        Raises:
            ValueError: If the number format is invalid
        """
        i = start
        has_decimal = False
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit():
                i += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                i += 1
            else:
                break
        
        number_str = expression[start:i]
        
        # Validate number format
        if not number_str or number_str == '.':
            raise ValueError("Invalid number format")
        
        # Check for multiple decimal points
        if number_str.count('.') > 1:
            raise ValueError("Invalid number format: multiple decimal points")
        
        return number_str, i - start
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for structural correctness.
        
        Raises:
            ValueError: If the token structure is invalid
        """
        if not self._tokens:
            raise ValueError("Empty expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses")
        
        # Validate token sequence
        self._validate_token_sequence()
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that tokens appear in a valid sequence.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            return
        
        # First token validation
        first_token = self._tokens[0]
        if first_token.type not in {TokenType.NUMBER, TokenType.LEFT_PAREN, TokenType.OPERATOR}:
            raise ValueError("Expression must start with number, '(', or unary operator")
        
        # If first token is operator, it must be unary + or -
        if first_token.type == TokenType.OPERATOR and first_token.value not in {'+', '-'}:
            raise ValueError("Expression cannot start with binary operator")
        
        # Last token validation
        last_token = self._tokens[-1]
        if last_token.type not in {TokenType.NUMBER, TokenType.RIGHT_PAREN}:
            raise ValueError("Expression must end with number or ')'")
        
        # Sequential validation
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if current.type == TokenType.NUMBER:
                if next_token.type not in {TokenType.OPERATOR, TokenType.RIGHT_PAREN}:
                    raise ValueError("Number must be followed by operator or ')'")
            
            elif current.type == TokenType.OPERATOR:
                if next_token.type not in {TokenType.NUMBER, TokenType.LEFT_PAREN, TokenType.OPERATOR}:
                    raise ValueError("Operator must be followed by number, '(', or unary operator")
                
                # Check for consecutive binary operators
                if (next_token.type == TokenType.OPERATOR and 
                    current.value not in {'+', '-'} and 
                    next_token.value not in {'+', '-'}):
                    raise ValueError("Invalid consecutive operators")
            
            elif current.type == TokenType.LEFT_PAREN:
                if next_token.type not in {TokenType.NUMBER, TokenType.LEFT_PAREN, TokenType.OPERATOR}:
                    raise ValueError("'(' must be followed by number, '(', or unary operator")
            
            elif current.type == TokenType.RIGHT_PAREN:
                if next_token.type not in {TokenType.OPERATOR, TokenType.RIGHT_PAREN}:
                    raise ValueError("')' must be followed by operator or ')'")
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate an expression using recursive descent parsing.
        
        Returns:
            The result of the expression evaluation
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """
        Parse addition and subtraction operations (lowest precedence).
        
        Returns:
            The result of the operation
        """
        result = self._parse_multiplication_division()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in {'+', '-'}):
            
            operator = self._tokens[self._position].value
            self._position += 1
            
            right = self._parse_multiplication_division()
            
            if operator == '+':
                result += right
            else:  # operator == '-'
                result -= right
        
        return result
    
    def _parse_multiplication_division(self) -> float:
        """
        Parse multiplication and division operations (higher precedence).
        
        Returns:
            The result of the operation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        result = self._parse_unary()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in {'*', '/'}):
            
            operator = self._tokens[self._position].value
            self._position += 1
            
            right = self._parse_unary()
            
            if operator == '*':
                result *= right
            else:  # operator == '/'
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= right
        
        return result
    
    def _parse_unary(self) -> float:
        """
        Parse unary operations (+ and -).
        
        Returns:
            The result after applying unary operations
        """
        if (self._position < len(self._tokens) and 
            self._tokens[self._position].type == TokenType.OPERATOR and
            self._tokens[self._position].value in {'+', '-'}):
            
            operator = self._tokens[self._position].value
            self._position += 1
            
            value = self._parse_factor()
            
            return -value if operator == '-' else value
        
        return self._parse_factor()
    
    def _parse_factor(self) -> float:
        """
        Parse factors (numbers and parenthesized expressions).
        
        Returns:
            The value of the factor
            
        Raises:
            ValueError: If unexpected token is encountered
        """
        if self._position >= len(self._tokens):
            raise ValueError("Unexpected end of expression")
        
        token = self._tokens[self._position]
        
        if token.type == TokenType.NUMBER:
            self._position += 1
            return token.value
        
        elif token.type == TokenType.LEFT_PAREN:
            self._position += 1  # consume '('
            result = self._parse_expression()
            
            # Expect closing parenthesis
            if (self._position >= len(self._tokens) or 
                self._tokens[self._position].type != TokenType.RIGHT_PAREN):
                raise ValueError("Missing closing parenthesis")
            
            self._position += 1  # consume ')'
            return result
        
        else:
            raise ValueError(f"Unexpected token: {token}")


def main():
    """
    Main function to demonstrate the calculator functionality.
    
    Provides an interactive console interface for the calculator.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Enter 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() == 'quit':
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
