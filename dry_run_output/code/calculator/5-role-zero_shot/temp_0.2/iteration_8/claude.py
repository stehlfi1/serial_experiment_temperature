
"""
Console-based Arithmetic Calculator

A high-quality implementation of an arithmetic calculator that supports
basic operations (+, -, *, /) with parentheses and proper operator precedence.
Follows ISO/IEC 25010 quality standards.
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
    
    def __init__(self, token_type: TokenType, value: Union[str, float]):
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
    
    Supports:
    - Basic operations: +, -, *, /
    - Parentheses for grouping
    - Proper operator precedence
    - Integer and floating-point numbers (including negative values)
    """
    
    # Operator precedence mapping (higher value = higher precedence)
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
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
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: Result of the calculation
            
        Raises:
            InvalidExpressionError: If expression contains invalid syntax
            DivisionByZeroError: If division by zero is attempted
            UnbalancedParenthesesError: If parentheses are not balanced
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5 + 3.5")
            -1.5
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
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
                raise InvalidExpressionError("Unexpected tokens at end of expression")
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into a list of tokens.
        
        Args:
            expression (str): Expression to tokenize
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        # Remove whitespace and validate characters
        cleaned = re.sub(r'\s+', '', expression)
        
        if not re.match(r'^[0-9+\-*/().]+$', cleaned):
            raise InvalidExpressionError("Expression contains invalid characters")
        
        i = 0
        while i < len(cleaned):
            char = cleaned[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals)
                number_str = ''
                while i < len(cleaned) and (cleaned[i].isdigit() or cleaned[i] == '.'):
                    number_str += cleaned[i]
                    i += 1
                
                try:
                    number_value = float(number_str)
                    self._tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number format: {number_str}")
                
            elif char in self.OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
                
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
                
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
                
            else:
                raise InvalidExpressionError(f"Invalid character: {char}")
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for syntax errors.
        
        Raises:
            InvalidExpressionError: If syntax errors are found
            UnbalancedParenthesesError: If parentheses are not balanced
        """
        if not self._tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check parentheses balance
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise UnbalancedParenthesesError("Mismatched closing parenthesis")
        
        if paren_count != 0:
            raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        # Validate token sequence
        self._validate_token_sequence()
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that tokens appear in a valid sequence.
        
        Raises:
            InvalidExpressionError: If invalid token sequence is found
        """
        prev_token = None
        
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Handle unary minus
                if token.value == '-' and (prev_token is None or 
                                         prev_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    # Convert unary minus to -1 * 
                    self._tokens[i] = Token(TokenType.NUMBER, -1)
                    self._tokens.insert(i + 1, Token(TokenType.OPERATOR, '*'))
                    continue
                
                # Binary operators must follow numbers or closing parentheses
                if prev_token is None or prev_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
                    raise InvalidExpressionError(f"Invalid operator placement: {token.value}")
            
            elif token.type == TokenType.NUMBER:
                # Numbers cannot follow other numbers or closing parentheses directly
                if prev_token and prev_token.type in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
                    raise InvalidExpressionError("Invalid number placement")
            
            elif token.type == TokenType.LEFT_PAREN:
                # Opening parentheses cannot follow numbers or closing parentheses directly
                if prev_token and prev_token.type in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
                    raise InvalidExpressionError("Invalid opening parenthesis placement")
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Closing parentheses must follow numbers or other closing parentheses
                if prev_token is None or prev_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
                    raise InvalidExpressionError("Invalid closing parenthesis placement")
            
            prev_token = token
        
        # Expression cannot end with an operator or opening parenthesis
        last_token = self._tokens[-1]
        if last_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]:
            raise InvalidExpressionError("Expression cannot end with operator or opening parenthesis")
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate expression using recursive descent parsing.
        Handles addition and subtraction (lowest precedence).
        
        Returns:
            float: Result of the expression evaluation
        """
        result = self._parse_term()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['+', '-']):
            
            operator = self._tokens[self._position].value
            self._position += 1
            right = self._parse_term()
            
            if operator == '+':
                result += right
            else:  # operator == '-'
                result -= right
        
        return result
    
    def _parse_term(self) -> float:
        """
        Parse and evaluate term (multiplication and division).
        Higher precedence than addition/subtraction.
        
        Returns:
            float: Result of the term evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
        """
        result = self._parse_factor()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['*', '/']):
            
            operator = self._tokens[self._position].value
            self._position += 1
            right = self._parse_factor()
            
            if operator == '*':
                result *= right
            else:  # operator == '/'
                if right == 0:
                    raise DivisionByZeroError("Division by zero is not allowed")
                result /= right
        
        return result
    
    def _parse_factor(self) -> float:
        """
        Parse and evaluate factor (numbers and parenthesized expressions).
        Highest precedence.
        
        Returns:
            float: Result of the factor evaluation
            
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
            raise InvalidExpressionError(f"Unexpected token: {token.value}")


def main():
    """
    Main function to run the calculator in interactive mode.
    Demonstrates the calculator's functionality and error handling.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
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
