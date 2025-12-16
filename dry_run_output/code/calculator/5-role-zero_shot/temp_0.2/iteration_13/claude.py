
"""
A high-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

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
    A robust arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator
    precedence and parentheses. Handles both integers and floating-point numbers.
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
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Regular expression to match numbers (including negative), operators, and parentheses
        pattern = r'(-?\d+\.?\d*)|([+\-*/()])'
        matches = re.finditer(pattern, expression)
        
        position = 0
        prev_token_type = None
        
        for match in matches:
            if match.start() != position:
                # There are invalid characters between tokens
                invalid_char = expression[position:match.start()].strip()
                if invalid_char:
                    raise ValueError(f"Invalid character(s) '{invalid_char}' at position {position}")
            
            token_value = match.group(0)
            token_start = match.start()
            
            if match.group(1):  # Number
                # Handle negative numbers vs subtraction operator
                if (token_value.startswith('-') and 
                    prev_token_type in [TokenType.NUMBER, TokenType.RIGHT_PAREN]):
                    # This is a subtraction operator followed by a positive number
                    self._tokens.append(Token(TokenType.OPERATOR, '-', token_start))
                    if len(token_value) > 1:  # There's a number after the minus
                        number_value = token_value[1:]
                        self._validate_number(number_value, token_start + 1)
                        self._tokens.append(Token(TokenType.NUMBER, number_value, token_start + 1))
                        prev_token_type = TokenType.NUMBER
                    else:
                        prev_token_type = TokenType.OPERATOR
                else:
                    # Regular number (positive or negative)
                    self._validate_number(token_value, token_start)
                    self._tokens.append(Token(TokenType.NUMBER, token_value, token_start))
                    prev_token_type = TokenType.NUMBER
                    
            elif token_value in self.VALID_OPERATORS:  # Operator
                self._tokens.append(Token(TokenType.OPERATOR, token_value, token_start))
                prev_token_type = TokenType.OPERATOR
                
            elif token_value == '(':  # Left parenthesis
                self._tokens.append(Token(TokenType.LEFT_PAREN, token_value, token_start))
                prev_token_type = TokenType.LEFT_PAREN
                
            elif token_value == ')':  # Right parenthesis
                self._tokens.append(Token(TokenType.RIGHT_PAREN, token_value, token_start))
                prev_token_type = TokenType.RIGHT_PAREN
                
            position = match.end()
        
        # Check if there are remaining invalid characters
        if position < len(expression):
            invalid_char = expression[position:].strip()
            if invalid_char:
                raise ValueError(f"Invalid character(s) '{invalid_char}' at position {position}")
    
    def _validate_number(self, number_str: str, position: int) -> None:
        """
        Validate that a string represents a valid number.
        
        Args:
            number_str: String representation of the number
            position: Position in the original expression
            
        Raises:
            ValueError: If the number format is invalid
        """
        try:
            float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number format '{number_str}' at position {position}")
    
    def _validate_tokens(self) -> None:
        """
        Validate the sequence of tokens for syntactic correctness.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            raise ValueError("No valid tokens found in expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError(f"Unmatched closing parenthesis at position {token.position}")
        
        if paren_count > 0:
            raise ValueError("Unmatched opening parenthesis")
        
        # Validate token sequence
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus)
                if i == 0 and token.value != '-':
                    raise ValueError(f"Expression cannot start with operator '{token.value}'")
                if i == len(self._tokens) - 1:
                    raise ValueError(f"Expression cannot end with operator '{token.value}'")
                
                # Check for consecutive operators
                if i > 0 and self._tokens[i-1].type == TokenType.OPERATOR:
                    raise ValueError(f"Consecutive operators at position {token.position}")
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Right parenthesis cannot be at the beginning
                if i == 0:
                    raise ValueError("Expression cannot start with closing parenthesis")
                
                # Right parenthesis cannot follow an operator
                if self._tokens[i-1].type == TokenType.OPERATOR:
                    raise ValueError(f"Operator cannot be followed by closing parenthesis at position {token.position}")
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix order
        """
        output_queue: List[Token] = []
        operator_stack: List[Token] = []
        
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
                
            elif token.type == TokenType.OPERATOR:
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
                
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> Union[int, float]:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix order
            
        Returns:
            The calculated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack: List[Union[int, float]] = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                # Convert to appropriate numeric type
                value = token.value
                if '.' in value:
                    stack.append(float(value))
                else:
                    stack.append(int(value))
                    
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError(f"Insufficient operands for operator '{token.value}'")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(left_operand, right_operand, token.value)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: incorrect number of operands")
        
        return stack[0]
    
    def _apply_operator(self, left: Union[int, float], right: Union[int, float], 
                       operator: str) -> Union[int, float]:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            left: Left operand
            right: Right operand
            operator: Arithmetic operator
            
        Returns:
            Result of the operation
            
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
