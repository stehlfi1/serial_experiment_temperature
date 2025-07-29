
"""
Console-based Arithmetic Calculator

A high-quality calculator implementation that evaluates mathematical expressions
with proper operator precedence, parentheses support, and comprehensive error handling.
Complies with ISO/IEC 25010 quality standards.
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
            value: The value of the token (number or operator symbol)
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence,
    parentheses, and both integer and floating-point numbers including negative values.
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
            expression: Mathematical expression as a string
            
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
            >>> calc.calculate("-3.5 + 2.1")
            -1.4
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
        # Remove whitespace and validate characters
        cleaned_expr = re.sub(r'\s+', '', expression)
        
        if not re.match(r'^[0-9+\-*/().]+$', cleaned_expr):
            raise ValueError("Expression contains invalid characters")
        
        i = 0
        while i < len(cleaned_expr):
            char = cleaned_expr[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals)
                number_str, i = self._parse_number(cleaned_expr, i)
                self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
                
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
                raise ValueError(f"Invalid character: {char}")
    
    def _parse_number(self, expression: str, start: int) -> Tuple[str, int]:
        """
        Parse a number from the expression starting at the given position.
        
        Args:
            expression: The expression string
            start: Starting position
            
        Returns:
            Tuple of (number_string, next_position)
            
        Raises:
            ValueError: If the number format is invalid
        """
        i = start
        number_str = ""
        decimal_count = 0
        
        while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
            if expression[i] == '.':
                decimal_count += 1
                if decimal_count > 1:
                    raise ValueError("Invalid number format: multiple decimal points")
            number_str += expression[i]
            i += 1
        
        if not number_str or number_str == '.':
            raise ValueError("Invalid number format")
        
        # Validate the number can be converted to float
        try:
            float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number: {number_str}")
        
        return number_str, i
    
    def _validate_tokens(self) -> None:
        """
        Validate the token sequence for correctness.
        
        Raises:
            ValueError: If token sequence is invalid
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
        prev_token = None
        
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Handle unary minus
                if token.value == '-' and (prev_token is None or 
                                         prev_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    # Convert unary minus to -1 * next_expression
                    self._tokens[i] = Token(TokenType.NUMBER, -1.0)
                    self._tokens.insert(i + 1, Token(TokenType.OPERATOR, '*'))
                    continue
                
                # Binary operators must have operands on both sides
                if (prev_token is None or 
                    prev_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    raise ValueError(f"Invalid operator placement: {token.value}")
                
                if (i == len(self._tokens) - 1 or 
                    self._tokens[i + 1].type in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]):
                    raise ValueError(f"Invalid operator placement: {token.value}")
            
            elif token.type == TokenType.RIGHT_PAREN:
                if (prev_token is None or 
                    prev_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    raise ValueError("Empty parentheses or invalid content")
            
            prev_token = token
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate the expression using recursive descent parsing.
        
        Returns:
            The result of the expression evaluation
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """
        Parse addition and subtraction operations (lowest precedence).
        
        Returns:
            The result of the addition/subtraction operations
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
            The result of the multiplication/division operations
            
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
            
            if (self._position >= len(self._tokens) or 
                self._tokens[self._position].type != TokenType.RIGHT_PAREN):
                raise ValueError("Missing closing parenthesis")
            
            self._position += 1  # consume ')'
            return result
        
        else:
            raise ValueError(f"Unexpected token: {token.value}")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and decimal numbers")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}\n")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
