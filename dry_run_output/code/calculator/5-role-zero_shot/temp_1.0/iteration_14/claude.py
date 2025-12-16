
"""
Arithmetic Calculator Module

A high-quality console-based calculator that supports basic arithmetic operations
with proper error handling and expression parsing.
"""

import re
from typing import List, Union, Tuple
from enum import Enum


class TokenType(Enum):
    """Enumeration for different token types in mathematical expressions."""
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
        """String representation of the token."""
        return f"Token({self.type}, {self.value})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression is syntactically invalid."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""
    pass


class Calculator:
    """
    A robust arithmetic calculator that supports basic operations with proper
    operator precedence and parentheses handling.
    
    Supports operations: +, -, *, /
    Supports parentheses for grouping
    Handles both integers and floating-point numbers including negative values
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    # Valid operators
    OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing the mathematical expression
            
        Returns:
            The result of the calculation as a float
            
        Raises:
            InvalidExpressionError: If the expression is syntactically invalid
            DivisionByZeroError: If division by zero is attempted
            
        Example:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Empty expression")
        
        try:
            # Tokenize the expression
            tokens = self._tokenize(expression.strip())
            
            # Validate tokens
            self._validate_tokens(tokens)
            
            # Convert to postfix notation using Shunting Yard algorithm
            postfix = self._to_postfix(tokens)
            
            # Evaluate postfix expression
            result = self._evaluate_postfix(postfix)
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize the input expression into a list of tokens.
        
        Args:
            expression: The mathematical expression as a string
            
        Returns:
            A list of Token objects
            
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
                number_str, i = self._parse_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, float(number_str)))
            
            # Handle negative numbers at the beginning or after operators/opening parentheses
            elif char == '-' and self._is_unary_minus(tokens):
                number_str, i = self._parse_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, float(number_str)))
            
            # Handle operators
            elif char in self.OPERATORS:
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
                raise InvalidExpressionError(f"Invalid character: '{char}'")
        
        return tokens
    
    def _parse_number(self, expression: str, start_index: int) -> Tuple[str, int]:
        """
        Parse a number (including negative numbers and decimals) from the expression.
        
        Args:
            expression: The mathematical expression
            start_index: The starting index for parsing
            
        Returns:
            A tuple of (number_string, next_index)
        """
        i = start_index
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += '-'
            i += 1
        
        # Parse digits and decimal point
        decimal_found = False
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                number_str += char
            elif char == '.' and not decimal_found:
                decimal_found = True
                number_str += char
            else:
                break
            i += 1
        
        if not number_str or number_str == '-' or number_str == '.':
            raise InvalidExpressionError("Invalid number format")
        
        return number_str, i
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign should be treated as unary (negative number).
        
        Args:
            tokens: The list of tokens processed so far
            
        Returns:
            True if the minus should be treated as unary, False otherwise
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validate the token sequence for syntactic correctness.
        
        Args:
            tokens: The list of tokens to validate
            
        Raises:
            InvalidExpressionError: If the token sequence is invalid
        """
        if not tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise InvalidExpressionError("Unbalanced parentheses")
        
        # Check for proper token sequence
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError("Operator at invalid position")
                
                # Operators cannot be followed by operators (except unary minus)
                if i > 0 and tokens[i-1].type == TokenType.OPERATOR:
                    raise InvalidExpressionError("Consecutive operators")
                
                if i < len(tokens) - 1 and tokens[i+1].type == TokenType.OPERATOR:
                    # Allow unary minus after operators
                    if not (tokens[i+1].value == '-' and 
                           i + 2 < len(tokens) and 
                           tokens[i+2].type == TokenType.NUMBER):
                        raise InvalidExpressionError("Consecutive operators")
    
    def _to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix notation to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens: The list of tokens in infix notation
            
        Returns:
            The list of tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
            
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.PRECEDENCE[operator_stack[-1].value] >= self.PRECEDENCE[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output.append(operator_stack.pop())
                
                if not operator_stack:
                    raise InvalidExpressionError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise InvalidExpressionError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens: The list of tokens in postfix notation
            
        Returns:
            The result of the evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Invalid expression structure")
                
                b = stack.pop()
                a = stack.pop()
                
                if token.value == '+':
                    result = a + b
                elif token.value == '-':
                    result = a - b
                elif token.value == '*':
                    result = a * b
                elif token.value == '/':
                    if b == 0:
                        raise DivisionByZeroError("Division by zero")
                    result = a / b
                
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression structure")
        
        return stack[0]


def main():
    """
    Main function for the console-based calculator.
    Provides an interactive interface for the user.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
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
            
        except (InvalidExpressionError, DivisionByZeroError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
