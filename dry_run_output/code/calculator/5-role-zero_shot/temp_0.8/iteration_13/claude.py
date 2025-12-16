
"""
High-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

This module provides a Calculator class that can evaluate mathematical expressions
with proper operator precedence and parentheses support.
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
    A high-quality arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator
    precedence and parentheses. Implements the Shunting Yard algorithm for
    expression parsing and evaluation.
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
        self._output_queue: List[Token] = []
        self._operator_stack: List[Token] = []
    
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
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        self._reset_state()
        
        # Step 1: Tokenize the expression
        self._tokenize(expression.strip())
        
        # Step 2: Validate tokens
        self._validate_tokens()
        
        # Step 3: Convert to postfix notation using Shunting Yard algorithm
        self._convert_to_postfix()
        
        # Step 4: Evaluate postfix expression
        return self._evaluate_postfix()
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression: The expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Regular expression to match numbers (including negative), operators, and parentheses
        pattern = r'(-?\d*\.?\d+|[+\-*/()])'
        matches = re.findall(pattern, expression)
        
        # Check if the entire expression was matched
        reconstructed = ''.join(matches)
        if reconstructed.replace(' ', '') != expression.replace(' ', ''):
            raise ValueError("Invalid characters in expression")
        
        i = 0
        while i < len(matches):
            token_str = matches[i].strip()
            
            if not token_str:
                i += 1
                continue
            
            if token_str == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, token_str))
            elif token_str == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, token_str))
            elif token_str in self.VALID_OPERATORS:
                # Handle unary minus
                if token_str == '-' and self._is_unary_minus_position(len(self._tokens)):
                    # Look ahead to get the number
                    if i + 1 < len(matches) and self._is_number(matches[i + 1]):
                        number_value = -float(matches[i + 1])
                        self._tokens.append(Token(TokenType.NUMBER, number_value))
                        i += 1  # Skip the next token as we've processed it
                    else:
                        raise ValueError("Invalid unary minus usage")
                else:
                    self._tokens.append(Token(TokenType.OPERATOR, token_str))
            elif self._is_number(token_str):
                self._tokens.append(Token(TokenType.NUMBER, float(token_str)))
            else:
                raise ValueError(f"Invalid token: {token_str}")
            
            i += 1
    
    def _is_number(self, token_str: str) -> bool:
        """Check if a string represents a valid number."""
        try:
            float(token_str)
            return True
        except ValueError:
            return False
    
    def _is_unary_minus_position(self, position: int) -> bool:
        """
        Check if a minus sign at the given position should be treated as unary.
        
        Args:
            position: Current position in the token list
            
        Returns:
            True if the minus should be treated as unary
        """
        if position == 0:
            return True
        
        prev_token = self._tokens[position - 1]
        return (prev_token.type == TokenType.LEFT_PAREN or 
                prev_token.type == TokenType.OPERATOR)
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for common errors.
        
        Raises:
            ValueError: If validation fails
        """
        if not self._tokens:
            raise ValueError("No valid tokens found")
        
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
        
        # Check for valid token sequences
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the end or followed by another operator
                if i == len(self._tokens) - 1:
                    raise ValueError("Expression cannot end with an operator")
                
                next_token = self._tokens[i + 1]
                if next_token.type == TokenType.OPERATOR:
                    raise ValueError("Two consecutive operators are not allowed")
                elif next_token.type == TokenType.RIGHT_PAREN:
                    raise ValueError("Operator cannot be followed by closing parenthesis")
            
            elif token.type == TokenType.LEFT_PAREN:
                # Left parenthesis cannot be followed by an operator (except unary minus, handled in tokenization)
                if i < len(self._tokens) - 1:
                    next_token = self._tokens[i + 1]
                    if next_token.type == TokenType.OPERATOR and next_token.value != '-':
                        raise ValueError("Opening parenthesis cannot be followed by operator")
    
    def _convert_to_postfix(self) -> None:
        """
        Convert infix expression to postfix notation using the Shunting Yard algorithm.
        """
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                self._output_queue.append(token)
            
            elif token.type == TokenType.OPERATOR:
                while (self._operator_stack and 
                       self._operator_stack[-1].type == TokenType.OPERATOR and
                       self.OPERATOR_PRECEDENCE[self._operator_stack[-1].value] >= 
                       self.OPERATOR_PRECEDENCE[token.value]):
                    self._output_queue.append(self._operator_stack.pop())
                self._operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                self._operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (self._operator_stack and 
                       self._operator_stack[-1].type != TokenType.LEFT_PAREN):
                    self._output_queue.append(self._operator_stack.pop())
                
                if not self._operator_stack:
                    raise ValueError("Mismatched parentheses")
                
                # Remove the left parenthesis
                self._operator_stack.pop()
        
        # Pop remaining operators
        while self._operator_stack:
            if self._operator_stack[-1].type == TokenType.LEFT_PAREN:
                raise ValueError("Mismatched parentheses")
            self._output_queue.append(self._operator_stack.pop())
    
    def _evaluate_postfix(self) -> float:
        """
        Evaluate the postfix expression and return the result.
        
        Returns:
            The calculated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack: List[float] = []
        
        for token in self._output_queue:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
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
            operator: Operation to perform
            
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
    print("Supports parentheses and negative numbers")
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


calc = Calculator()
print(calc.calculate("2 + 3 * 4"))        # 14.0
print(calc.calculate("(2 + 3) * 4"))      # 20.0
print(calc.calculate("-5 + 3"))           # -2.0
print(calc.calculate("10 / 2 - 3"))       # 2.0
