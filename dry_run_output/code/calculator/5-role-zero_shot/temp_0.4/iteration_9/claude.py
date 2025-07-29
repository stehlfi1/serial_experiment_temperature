
"""
High-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

This module provides a Calculator class that can evaluate mathematical expressions
with support for basic arithmetic operations and parentheses.
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
    """Represents a token in a mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: Union[str, float]):
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
    
    Supports addition (+), subtraction (-), multiplication (*), division (/),
    and parentheses with proper operator precedence.
    """
    
    # Operator precedence mapping (higher values = higher precedence)
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
        """Reset internal state for a new calculation."""
        self._tokens: List[Token] = []
        self._position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing the mathematical expression
            
        Returns:
            The calculated result as a float
            
        Raises:
            ValueError: If the expression is invalid
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) * 2")
            10.0
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
        Convert the expression string into tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
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
                number_str, i = self._parse_number(expression, i)
                try:
                    number_value = float(number_str)
                    self._tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                    
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
    
    def _parse_number(self, expression: str, start: int) -> tuple[str, int]:
        """
        Parse a number from the expression starting at the given position.
        
        Args:
            expression: The expression string
            start: Starting position
            
        Returns:
            Tuple of (number_string, next_position)
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
        if number_str == '.' or number_str == '':
            raise ValueError("Invalid number format")
        
        return number_str, i
    
    def _validate_tokens(self) -> None:
        """
        Validate the token sequence for correctness.
        
        Raises:
            ValueError: If tokens are invalid or unbalanced
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
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count > 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
        
        # Validate token sequence
        self._validate_token_sequence()
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that tokens appear in a valid sequence.
        
        Raises:
            ValueError: If token sequence is invalid
        """
        if len(self._tokens) == 0:
            return
        
        # First token validation
        first_token = self._tokens[0]
        if first_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN, TokenType.OPERATOR]:
            raise ValueError("Expression must start with a number, opening parenthesis, or unary operator")
        
        # If first token is operator, it must be unary + or -
        if first_token.type == TokenType.OPERATOR and first_token.value not in ['+', '-']:
            raise ValueError("Expression cannot start with binary operator")
        
        # Last token validation
        last_token = self._tokens[-1]
        if last_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
            raise ValueError("Expression must end with a number or closing parenthesis")
        
        # Sequential validation
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if current.type == TokenType.NUMBER:
                if next_token.type not in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]:
                    raise ValueError("Number must be followed by operator or closing parenthesis")
            
            elif current.type == TokenType.OPERATOR:
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN, TokenType.OPERATOR]:
                    raise ValueError("Operator must be followed by number, opening parenthesis, or unary operator")
                
                # Check for unary operators
                if next_token.type == TokenType.OPERATOR and next_token.value not in ['+', '-']:
                    raise ValueError("Only + and - can be unary operators")
            
            elif current.type == TokenType.LEFT_PAREN:
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN, TokenType.OPERATOR]:
                    raise ValueError("Opening parenthesis must be followed by number, opening parenthesis, or unary operator")
            
            elif current.type == TokenType.RIGHT_PAREN:
                if next_token.type not in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]:
                    raise ValueError("Closing parenthesis must be followed by operator or closing parenthesis")
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate an expression using recursive descent parsing.
        
        Returns:
            The evaluated result
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """
        Parse addition and subtraction operations (lowest precedence).
        
        Returns:
            The evaluated result
        """
        result = self._parse_multiplication_division()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['+', '-']):
            
            operator = self._tokens[self._position].value
            self._position += 1
            
            right_operand = self._parse_multiplication_division()
            
            if operator == '+':
                result += right_operand
            else:  # operator == '-'
                result -= right_operand
        
        return result
    
    def _parse_multiplication_division(self) -> float:
        """
        Parse multiplication and division operations (higher precedence).
        
        Returns:
            The evaluated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
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
                    raise ZeroDivisionError("Division by zero")
                result /= right_operand
        
        return result
    
    def _parse_factor(self) -> float:
        """
        Parse factors (numbers, parentheses, and unary operators).
        
        Returns:
            The evaluated result
            
        Raises:
            ValueError: If unexpected token is encountered
        """
        if self._position >= len(self._tokens):
            raise ValueError("Unexpected end of expression")
        
        token = self._tokens[self._position]
        
        # Handle unary operators
        if token.type == TokenType.OPERATOR and token.value in ['+', '-']:
            self._position += 1
            factor_value = self._parse_factor()
            return factor_value if token.value == '+' else -factor_value
        
        # Handle numbers
        elif token.type == TokenType.NUMBER:
            self._position += 1
            return token.value
        
        # Handle parentheses
        elif token.type == TokenType.LEFT_PAREN:
            self._position += 1  # consume '('
            result = self._parse_expression()
            
            if (self._position >= len(self._tokens) or 
                self._tokens[self._position].type != TokenType.RIGHT_PAREN):
                raise ValueError("Missing closing parenthesis")
            
            self._position += 1  # consume ')'
            return result
        
        else:
            raise ValueError(f"Unexpected token: {token}")


def main():
    """
    Main function demonstrating the calculator usage.
    """
    calculator = Calculator()
    
    # Example expressions for testing
    test_expressions = [
        "2 + 3",
        "10 - 5",
        "4 * 6",
        "15 / 3",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "10 / (5 - 3)",
        "-5 + 3",
        "2.5 * 4",
        "((1 + 2) * 3) - 4"
    ]
    
    print("Calculator Demo:")
    print("=" * 40)
    
    for expression in test_expressions:
        try:
            result = calculator.calculate(expression)
            print(f"{expression} = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"{expression} = Error: {e}")
    
    # Interactive mode
    print("\n" + "=" * 40)
    print("Interactive Calculator (type 'quit' to exit):")
    
    while True:
        try:
            expression = input("\nEnter expression: ").strip()
            if expression.lower() == 'quit':
                break
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
