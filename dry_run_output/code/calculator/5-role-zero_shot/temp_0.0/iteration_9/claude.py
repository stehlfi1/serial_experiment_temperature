
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
            expression: String containing the mathematical expression to evaluate
            
        Returns:
            The numerical result of the expression evaluation
            
        Raises:
            InvalidExpressionError: If the expression contains invalid syntax or characters
            DivisionByZeroError: If division by zero is attempted
            UnbalancedParenthesesError: If parentheses are not properly balanced
            
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
            raise InvalidExpressionError("Expression cannot be empty")
        
        self._reset_state()
        
        try:
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate parentheses balance
            self._validate_parentheses()
            
            # Validate token sequence
            self._validate_token_sequence()
            
            # Parse and evaluate using recursive descent parser
            self._position = 0
            result = self._parse_expression()
            
            # Ensure all tokens were consumed
            if self._position < len(self._tokens):
                raise InvalidExpressionError("Unexpected tokens at end of expression")
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression format: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        # Remove all whitespace
        expression = re.sub(r'\s+', '', expression)
        
        if not expression:
            raise InvalidExpressionError("Expression cannot be empty")
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals)
                number_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                
                # Validate number format
                if number_str.count('.') > 1:
                    raise InvalidExpressionError(f"Invalid number format: {number_str}")
                
                try:
                    number_value = float(number_str)
                    self._tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number format: {number_str}")
                
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
                raise InvalidExpressionError(f"Invalid character: '{char}'")
    
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
        
        if balance > 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
    
    def _validate_token_sequence(self) -> None:
        """
        Validate the sequence of tokens for proper syntax.
        
        Raises:
            InvalidExpressionError: If token sequence is invalid
        """
        if not self._tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check for valid token sequences
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Handle unary minus
                if token.value == '-' and (i == 0 or 
                    self._tokens[i-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    # Convert unary minus to negative number
                    if i + 1 >= len(self._tokens) or self._tokens[i + 1].type != TokenType.NUMBER:
                        raise InvalidExpressionError("Invalid unary minus usage")
                    # Merge unary minus with following number
                    next_token = self._tokens[i + 1]
                    self._tokens[i] = Token(TokenType.NUMBER, -next_token.value)
                    self._tokens.pop(i + 1)
                    continue
                
                # Binary operators must have operands on both sides
                if i == 0 or i == len(self._tokens) - 1:
                    raise InvalidExpressionError(f"Operator '{token.value}' missing operand")
                
                prev_token = self._tokens[i - 1]
                next_token = self._tokens[i + 1]
                
                if prev_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
                    raise InvalidExpressionError(f"Invalid token before operator '{token.value}'")
                
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    # Check for unary minus after operator
                    if (next_token.type == TokenType.OPERATOR and next_token.value == '-' and
                        i + 2 < len(self._tokens) and self._tokens[i + 2].type == TokenType.NUMBER):
                        continue
                    raise InvalidExpressionError(f"Invalid token after operator '{token.value}'")
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate the expression using recursive descent parsing.
        
        Returns:
            The result of the expression evaluation
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """Parse addition and subtraction (lowest precedence)."""
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
        """Parse multiplication and division (higher precedence)."""
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
        """Parse factors (numbers and parenthesized expressions)."""
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
                raise UnbalancedParenthesesError("Missing closing parenthesis")
            
            self._position += 1  # consume ')'
            return result
        
        else:
            raise InvalidExpressionError(f"Unexpected token: {token}")


def main():
    """
    Main function to run the calculator in interactive mode.
    Demonstrates the calculator's functionality with a simple console interface.
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
            
        except CalculatorError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
