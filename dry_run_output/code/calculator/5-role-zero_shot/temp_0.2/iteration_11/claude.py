
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
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Regular expression pattern for tokenization
        pattern = r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))'
        
        # Remove all whitespace
        clean_expression = re.sub(r'\s+', '', expression)
        
        # Find all tokens
        matches = re.finditer(pattern, clean_expression)
        position = 0
        
        for match in matches:
            token_value = match.group(1)
            token_start = match.start()
            
            # Check for invalid characters between tokens
            if token_start > position:
                invalid_chars = clean_expression[position:token_start]
                if invalid_chars:
                    raise ValueError(f"Invalid character(s) '{invalid_chars}' at position {position}")
            
            # Determine token type and create token
            if re.match(r'\d+\.?\d*', token_value):
                self._tokens.append(Token(TokenType.NUMBER, token_value, token_start))
            elif token_value in self.VALID_OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, token_value, token_start))
            elif token_value == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, token_value, token_start))
            elif token_value == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, token_value, token_start))
            
            position = match.end()
        
        # Check for remaining invalid characters
        if position < len(clean_expression):
            invalid_chars = clean_expression[position:]
            raise ValueError(f"Invalid character(s) '{invalid_chars}' at position {position}")
        
        if not self._tokens:
            raise ValueError("No valid tokens found in expression")
    
    def _validate_tokens(self) -> None:
        """
        Validate the sequence of tokens for syntactic correctness.
        
        Raises:
            ValueError: If token sequence is invalid
        """
        if not self._tokens:
            raise ValueError("Empty token sequence")
        
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
        self._validate_token_sequence()
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that tokens form a valid mathematical expression.
        
        Raises:
            ValueError: If token sequence is syntactically invalid
        """
        if not self._tokens:
            return
        
        # First token validation
        first_token = self._tokens[0]
        if first_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN, TokenType.OPERATOR]:
            raise ValueError(f"Expression cannot start with {first_token.value}")
        
        # If first token is operator, it must be unary minus
        if first_token.type == TokenType.OPERATOR and first_token.value != '-':
            raise ValueError(f"Expression cannot start with operator '{first_token.value}'")
        
        # Last token validation
        last_token = self._tokens[-1]
        if last_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
            raise ValueError(f"Expression cannot end with {last_token.value}")
        
        # Sequential token validation
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if current.type == TokenType.NUMBER:
                if next_token.type not in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]:
                    raise ValueError(f"Invalid token sequence: number followed by {next_token.value}")
            
            elif current.type == TokenType.OPERATOR:
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    # Allow unary minus after operators and left parentheses
                    if not (next_token.type == TokenType.OPERATOR and next_token.value == '-'):
                        raise ValueError(f"Invalid token sequence: operator followed by {next_token.value}")
            
            elif current.type == TokenType.LEFT_PAREN:
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN, TokenType.OPERATOR]:
                    raise ValueError(f"Invalid token sequence: '(' followed by {next_token.value}")
                # If operator after '(', it must be unary minus
                if next_token.type == TokenType.OPERATOR and next_token.value != '-':
                    raise ValueError(f"Invalid operator '{next_token.value}' after '('")
            
            elif current.type == TokenType.RIGHT_PAREN:
                if next_token.type not in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]:
                    raise ValueError(f"Invalid token sequence: ')' followed by {next_token.value}")
    
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
                    (i == 0 or 
                     self._tokens[i-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])):
                    # Convert unary minus to binary subtraction from zero
                    zero_token = Token(TokenType.NUMBER, '0', token.position)
                    output_queue.append(zero_token)
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
                # Pop operators until left parenthesis
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                # Remove left parenthesis
                if operator_stack:
                    operator_stack.pop()
            
            i += 1
        
        # Pop remaining operators
        while operator_stack:
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
            ValueError: If expression is malformed
        """
        stack: List[Union[int, float]] = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                # Convert to appropriate numeric type
                if '.' in token.value:
                    stack.append(float(token.value))
                else:
                    stack.append(int(token.value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                # Pop operands (note: order matters for subtraction and division)
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                # Perform operation
                if token.value == '+':
                    result = left_operand + right_operand
                elif token.value == '-':
                    result = left_operand - right_operand
                elif token.value == '*':
                    result = left_operand * right_operand
                elif token.value == '/':
                    if right_operand == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = left_operand / right_operand
                
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: invalid number of operands")
        
        return stack[0]


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
