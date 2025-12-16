
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
    """Represents a token in the mathematical expression."""
    
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
        # Regular expression to match numbers (including negative), operators, and parentheses
        pattern = r'(-?\d+\.?\d*)|([+\-*/()])'
        matches = re.finditer(pattern, expression)
        
        position = 0
        previous_token_type = None
        
        for match in matches:
            if match.start() != position:
                # There are invalid characters between tokens
                invalid_char = expression[position:match.start()].strip()
                if invalid_char:
                    raise ValueError(f"Invalid character(s) '{invalid_char}' at position {position}")
            
            token_value = match.group(0)
            token_start = match.start()
            
            # Determine token type
            if token_value == '(':
                token_type = TokenType.LEFT_PAREN
            elif token_value == ')':
                token_type = TokenType.RIGHT_PAREN
            elif token_value in self.VALID_OPERATORS:
                token_type = TokenType.OPERATOR
                # Handle unary minus
                if (token_value == '-' and 
                    (previous_token_type is None or 
                     previous_token_type in [TokenType.LEFT_PAREN, TokenType.OPERATOR])):
                    # This is a unary minus, combine with next number
                    continue
            else:
                # Must be a number
                try:
                    float(token_value)
                    token_type = TokenType.NUMBER
                except ValueError:
                    raise ValueError(f"Invalid number '{token_value}' at position {token_start}")
            
            self._tokens.append(Token(token_type, token_value, token_start))
            previous_token_type = token_type
            position = match.end()
        
        # Check if there are remaining characters
        if position < len(expression):
            remaining = expression[position:].strip()
            if remaining:
                raise ValueError(f"Invalid character(s) '{remaining}' at position {position}")
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for correctness.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            raise ValueError("Empty expression")
        
        paren_count = 0
        previous_token = None
        
        for i, token in enumerate(self._tokens):
            # Check parentheses balance
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError(f"Unmatched closing parenthesis at position {token.position}")
            
            # Validate token sequences
            if previous_token:
                self._validate_token_sequence(previous_token, token)
            
            previous_token = token
        
        # Check final parentheses balance
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses")
        
        # Expression cannot start with binary operator or end with operator
        if self._tokens[0].type == TokenType.OPERATOR:
            raise ValueError("Expression cannot start with an operator")
        
        if self._tokens[-1].type == TokenType.OPERATOR:
            raise ValueError("Expression cannot end with an operator")
    
    def _validate_token_sequence(self, prev_token: Token, curr_token: Token) -> None:
        """
        Validate that two consecutive tokens form a valid sequence.
        
        Args:
            prev_token: The previous token
            curr_token: The current token
            
        Raises:
            ValueError: If the token sequence is invalid
        """
        # Define valid token transitions
        valid_transitions = {
            TokenType.NUMBER: {TokenType.OPERATOR, TokenType.RIGHT_PAREN},
            TokenType.OPERATOR: {TokenType.NUMBER, TokenType.LEFT_PAREN},
            TokenType.LEFT_PAREN: {TokenType.NUMBER, TokenType.LEFT_PAREN},
            TokenType.RIGHT_PAREN: {TokenType.OPERATOR, TokenType.RIGHT_PAREN}
        }
        
        if curr_token.type not in valid_transitions.get(prev_token.type, set()):
            raise ValueError(
                f"Invalid token sequence: {prev_token.value} followed by {curr_token.value} "
                f"at position {curr_token.position}"
            )
    
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
                # Pop operators with higher or equal precedence
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.OPERATOR_PRECEDENCE[operator_stack[-1].value] >= 
                       self.OPERATOR_PRECEDENCE[token.value]):
                    output_queue.append(operator_stack.pop())
                
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Pop until left parenthesis
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                # Remove left parenthesis
                if operator_stack:
                    operator_stack.pop()
        
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
                    raise ValueError("Malformed expression: insufficient operands")
                
                # Pop two operands (note the order)
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                # Perform operation
                result = self._perform_operation(left_operand, token.value, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: incorrect number of operands")
        
        return stack[0]
    
    def _perform_operation(self, left: Union[int, float], operator: str, 
                          right: Union[int, float]) -> Union[int, float]:
        """
        Perform a single arithmetic operation.
        
        Args:
            left: Left operand
            operator: Arithmetic operator
            right: Right operand
            
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
                raise ZeroDivisionError("Division by zero")
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
