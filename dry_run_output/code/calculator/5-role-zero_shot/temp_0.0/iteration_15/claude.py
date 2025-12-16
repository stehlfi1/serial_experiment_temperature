
"""
High-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

This module provides a Calculator class that can evaluate mathematical expressions
with proper operator precedence, parentheses support, and comprehensive error handling.
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


class Calculator:
    """
    A high-quality arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence,
    parentheses, and both integer and floating-point numbers including negative values.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    # Valid operators
    VALID_OPERATORS = {'+', '-', '*', '/'}
    
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
            
            # Convert to postfix notation using Shunting Yard algorithm
            postfix_tokens = self._to_postfix()
            
            # Evaluate postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, ZeroDivisionError):
            raise
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Regular expression to match numbers, operators, and parentheses
        token_pattern = r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))'
        
        position = 0
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                position += 1
                continue
            
            # Handle numbers (including decimals)
            if char.isdigit() or char == '.':
                number_str = ''
                start_pos = position
                
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                    position += 1
                
                # Validate number format
                if not self._is_valid_number(number_str):
                    raise ValueError(f"Invalid number format: '{number_str}' at position {start_pos}")
                
                self._tokens.append(Token(TokenType.NUMBER, number_str, start_pos))
                continue
            
            # Handle operators and parentheses
            if char in self.VALID_OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, char, position))
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char, position))
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char, position))
            else:
                raise ValueError(f"Invalid character '{char}' at position {position}")
            
            i += 1
            position += 1
    
    def _is_valid_number(self, number_str: str) -> bool:
        """
        Validate if a string represents a valid number.
        
        Args:
            number_str: String to validate
            
        Returns:
            True if valid number, False otherwise
        """
        if not number_str or number_str == '.':
            return False
        
        # Count decimal points
        decimal_count = number_str.count('.')
        if decimal_count > 1:
            return False
        
        # Check if it's a valid float
        try:
            float(number_str)
            return True
        except ValueError:
            return False
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for correctness.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            raise ValueError("Empty expression")
        
        # Check for balanced parentheses
        self._check_balanced_parentheses()
        
        # Check for valid token sequence
        self._check_token_sequence()
    
    def _check_balanced_parentheses(self) -> None:
        """
        Check if parentheses are balanced in the expression.
        
        Raises:
            ValueError: If parentheses are unbalanced
        """
        balance = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                balance += 1
            elif token.type == TokenType.RIGHT_PAREN:
                balance -= 1
                if balance < 0:
                    raise ValueError(f"Unmatched closing parenthesis at position {token.position}")
        
        if balance > 0:
            raise ValueError("Unmatched opening parenthesis")
    
    def _check_token_sequence(self) -> None:
        """
        Validate the sequence of tokens for proper syntax.
        
        Raises:
            ValueError: If token sequence is invalid
        """
        if not self._tokens:
            return
        
        prev_token = None
        
        for i, token in enumerate(self._tokens):
            # First token validation
            if i == 0:
                if token.type == TokenType.OPERATOR and token.value not in ['+', '-']:
                    raise ValueError(f"Expression cannot start with operator '{token.value}'")
                if token.type == TokenType.RIGHT_PAREN:
                    raise ValueError("Expression cannot start with closing parenthesis")
            
            # Last token validation
            if i == len(self._tokens) - 1:
                if token.type == TokenType.OPERATOR:
                    raise ValueError("Expression cannot end with an operator")
                if token.type == TokenType.LEFT_PAREN:
                    raise ValueError("Expression cannot end with opening parenthesis")
            
            # Sequential token validation
            if prev_token:
                if (prev_token.type == TokenType.OPERATOR and 
                    token.type == TokenType.OPERATOR and 
                    not (prev_token.value in ['+', '-'] and token.value in ['+', '-'])):
                    raise ValueError(f"Invalid operator sequence at position {token.position}")
                
                if (prev_token.type == TokenType.NUMBER and 
                    token.type == TokenType.LEFT_PAREN):
                    raise ValueError(f"Missing operator before parenthesis at position {token.position}")
                
                if (prev_token.type == TokenType.RIGHT_PAREN and 
                    token.type == TokenType.NUMBER):
                    raise ValueError(f"Missing operator after parenthesis at position {prev_token.position}")
            
            prev_token = token
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix order
        """
        output_queue: List[Token] = []
        operator_stack: List[Token] = []
        
        i = 0
        while i < len(self._tokens):
            token = self._tokens[i]
            
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
            
            elif token.type == TokenType.OPERATOR:
                # Handle unary minus
                if (token.value == '-' and 
                    (i == 0 or self._tokens[i-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])):
                    # Convert unary minus to binary operation: 0 - operand
                    output_queue.append(Token(TokenType.NUMBER, '0', token.position))
                    operator_stack.append(token)
                else:
                    # Handle binary operators
                    while (operator_stack and 
                           operator_stack[-1].type == TokenType.OPERATOR and
                           self.OPERATOR_PRECEDENCE[operator_stack[-1].value] >= 
                           self.OPERATOR_PRECEDENCE[token.value]):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output_queue.append(operator_stack.pop())
                
                if operator_stack:
                    operator_stack.pop()  # Remove the left parenthesis
            
            i += 1
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens: List of tokens in postfix order
            
        Returns:
            The calculated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack: List[float] = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(left_operand, right_operand, token.value)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: invalid number of operands")
        
        return stack[0]
    
    def _perform_operation(self, left: float, right: float, operator: str) -> float:
        """
        Perform a single arithmetic operation.
        
        Args:
            left: Left operand
            right: Right operand
            operator: Arithmetic operator
            
        Returns:
            Result of the operation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If operator is invalid
        """
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")


def main():
    """
    Main function to demonstrate calculator usage.
    Provides an interactive console interface for the calculator.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and decimal numbers")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
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
