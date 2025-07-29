
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
    parentheses, and both integer and floating-point numbers.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    # Valid operators
    VALID_OPERATORS = {'+', '-', '*', '/'}
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression: A string containing the mathematical expression
            
        Returns:
            float: The result of the evaluated expression
            
        Raises:
            ValueError: If the expression is invalid (syntax errors, unbalanced parentheses)
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5.5 + 2.3")
            -3.2
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        # Tokenize the expression
        tokens = self._tokenize(expression.strip())
        
        # Validate tokens
        self._validate_tokens(tokens)
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(postfix_tokens)
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Tokenizes the input expression into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List[Token]: List of tokens representing the expression
            
        Raises:
            ValueError: If invalid characters are found
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
                number_str, new_i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
            
            # Handle operators
            elif char in self.VALID_OPERATORS:
                # Check if this is a unary minus
                if char == '-' and self._is_unary_minus(tokens):
                    # Handle unary minus by extracting the negative number
                    if i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        number_str, new_i = self._extract_number(expression, i)
                        tokens.append(Token(TokenType.NUMBER, number_str, i))
                        i = new_i
                    else:
                        # Unary minus followed by parentheses or another operator
                        tokens.append(Token(TokenType.NUMBER, "0", i))
                        tokens.append(Token(TokenType.OPERATOR, "-", i))
                        i += 1
                else:
                    tokens.append(Token(TokenType.OPERATOR, char, i))
                    i += 1
            
            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
            
            # Invalid character
            else:
                raise ValueError(f"Invalid character '{char}' at position {i}")
        
        return tokens
    
    def _extract_number(self, expression: str, start: int) -> tuple[str, int]:
        """
        Extracts a number (including negative numbers and decimals) from the expression.
        
        Args:
            expression: The full expression
            start: Starting position
            
        Returns:
            tuple: (number_string, next_position)
            
        Raises:
            ValueError: If the number format is invalid
        """
        i = start
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        decimal_count = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.':
                decimal_count += 1
                if decimal_count > 1:
                    raise ValueError(f"Invalid number format: multiple decimal points at position {start}")
                number_str += char
                i += 1
            else:
                break
        
        # Validate the extracted number
        if not number_str or number_str == '-' or number_str == '.':
            raise ValueError(f"Invalid number format at position {start}")
        
        # Check for valid number format
        try:
            float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number format '{number_str}' at position {start}")
        
        return number_str, i
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determines if a minus sign should be treated as unary.
        
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
        Validates the token sequence for syntax errors.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            ValueError: If syntax errors are found
        """
        if not tokens:
            raise ValueError("Empty expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError(f"Unmatched closing parenthesis at position {token.position}")
        
        if paren_count > 0:
            raise ValueError("Unmatched opening parenthesis")
        
        # Check for valid token sequences
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the end
                if i == len(tokens) - 1:
                    raise ValueError(f"Expression cannot end with operator '{token.value}'")
                
                # Operators cannot be followed by operators (except unary minus)
                if i < len(tokens) - 1:
                    next_token = tokens[i + 1]
                    if (next_token.type == TokenType.OPERATOR and 
                        not (next_token.value == '-' and self._is_unary_minus(tokens[:i+1]))):
                        raise ValueError(f"Invalid operator sequence at position {token.position}")
        
        # First token must be number or left parenthesis
        if tokens[0].type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
            raise ValueError("Expression must start with a number or opening parenthesis")
        
        # Last token must be number or right parenthesis
        if tokens[-1].type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
            raise ValueError("Expression must end with a number or closing parenthesis")
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Converts infix notation to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens in infix notation
            
        Returns:
            List[Token]: List of tokens in postfix notation
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
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
                
                # Remove the left parenthesis
                if operator_stack:
                    operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(
                    left_operand, token.value, right_operand, token.position
                )
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: incorrect number of operands")
        
        return stack[0]
    
    def _perform_operation(self, left: float, operator: str, right: float, position: int) -> float:
        """
        Performs a single arithmetic operation.
        
        Args:
            left: Left operand
            operator: The operator (+, -, *, /)
            right: Right operand
            position: Position in original expression for error reporting
            
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
                raise ZeroDivisionError(f"Division by zero at position {position}")
            return left / right
        else:
            raise ValueError(f"Unknown operator '{operator}'")


def main():
    """
    Main function to demonstrate the calculator functionality.
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
            
            if expression.lower() == 'quit':
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
