
"""
Console-based arithmetic calculator implementation.

This module provides a Calculator class that can evaluate mathematical expressions
containing basic arithmetic operations (+, -, *, /) with support for parentheses
and proper operator precedence.

Author: Senior Software Developer
Standard: ISO/IEC 25010 compliant
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
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with parentheses and
    proper operator precedence. Uses the Shunting Yard algorithm for parsing
    and evaluation.
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
            expression: String containing the mathematical expression
            
        Returns:
            float: The result of the calculation
            
        Raises:
            ValueError: If the expression is invalid or contains unsupported characters
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Validate tokens
        self._validate_tokens(tokens)
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix = self._to_postfix(tokens)
        
        # Evaluate postfix expression
        return self._evaluate_postfix(postfix)
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression string
            
        Returns:
            List[Token]: List of tokens representing the expression
            
        Raises:
            ValueError: If invalid characters are found
        """
        tokens = []
        i = 0
        expression = expression.replace(' ', '')  # Remove whitespace
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (integer or float)
                number_str, i = self._parse_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, float(number_str)))
            
            elif char in self.OPERATORS:
                # Handle unary minus
                if char == '-' and self._is_unary_minus(tokens):
                    # Parse negative number
                    i += 1
                    if i >= len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                        raise ValueError("Invalid unary minus: no number follows")
                    number_str, i = self._parse_number(expression, i)
                    tokens.append(Token(TokenType.NUMBER, -float(number_str)))
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
            
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
            
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
            
            else:
                raise ValueError(f"Invalid character: '{char}'")
        
        return tokens
    
    def _parse_number(self, expression: str, start: int) -> Tuple[str, int]:
        """
        Parse a number from the expression starting at the given position.
        
        Args:
            expression: The expression string
            start: Starting position
            
        Returns:
            Tuple[str, int]: The number string and the new position
            
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
        
        return number_str, i
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign should be treated as unary.
        
        Args:
            tokens: List of tokens processed so far
            
        Returns:
            bool: True if the minus should be treated as unary
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validate the token sequence for correctness.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not tokens:
            raise ValueError("Empty expression")
        
        # Check balanced parentheses
        paren_count = 0
        for token in tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: extra closing parenthesis")
        
        if paren_count > 0:
            raise ValueError("Unbalanced parentheses: unclosed opening parenthesis")
        
        # Validate token sequence
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus, handled in tokenization)
                if i == 0 or i == len(tokens) - 1:
                    raise ValueError("Invalid operator placement")
                
                # Operators cannot be adjacent
                if (i > 0 and tokens[i-1].type == TokenType.OPERATOR or
                    i < len(tokens) - 1 and tokens[i+1].type == TokenType.OPERATOR):
                    raise ValueError("Adjacent operators not allowed")
    
    def _to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix tokens to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens in infix notation
            
        Returns:
            List[Token]: Tokens in postfix notation
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
                    raise ValueError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in (TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN):
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens: Tokens in postfix notation
            
        Returns:
            float: Result of the evaluation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                right = stack.pop()
                left = stack.pop()
                
                result = self._apply_operator(token.value, left, right)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: invalid number of operands")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            left: Left operand
            right: Right operand
            
        Returns:
            float: Result of the operation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ('quit', 'exit'):
                print("Goodbye!")
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
