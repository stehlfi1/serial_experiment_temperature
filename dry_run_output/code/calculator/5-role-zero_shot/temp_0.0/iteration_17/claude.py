
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
        
        # Remove all whitespace
        clean_expression = re.sub(r'\s+', '', expression)
        
        # Find all tokens
        matches = re.finditer(token_pattern, clean_expression)
        position = 0
        
        for match in matches:
            if match.start() != position:
                # There are invalid characters between tokens
                invalid_char = clean_expression[position:match.start()]
                raise ValueError(f"Invalid character(s) '{invalid_char}' at position {position}")
            
            token_value = match.group(1)
            token_type = self._determine_token_type(token_value, position)
            
            self._tokens.append(Token(token_type, token_value, position))
            position = match.end()
        
        # Check if there are remaining characters
        if position < len(clean_expression):
            invalid_char = clean_expression[position:]
            raise ValueError(f"Invalid character(s) '{invalid_char}' at position {position}")
    
    def _determine_token_type(self, value: str, position: int) -> TokenType:
        """
        Determine the type of a token based on its value and context.
        
        Args:
            value: The token value
            position: Position in the token list
            
        Returns:
            The appropriate TokenType
        """
        if value == '(':
            return TokenType.LEFT_PAREN
        elif value == ')':
            return TokenType.RIGHT_PAREN
        elif value in self.VALID_OPERATORS:
            return TokenType.OPERATOR
        elif self._is_number(value):
            return TokenType.NUMBER
        else:
            raise ValueError(f"Invalid token '{value}' at position {position}")
    
    def _is_number(self, value: str) -> bool:
        """
        Check if a string represents a valid number.
        
        Args:
            value: String to check
            
        Returns:
            True if the string is a valid number, False otherwise
        """
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for correctness.
        
        Raises:
            ValueError: If the expression is invalid
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
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            return
        
        # Handle unary minus at the beginning or after opening parenthesis
        processed_tokens = self._handle_unary_operators()
        self._tokens = processed_tokens
        
        # Check for valid alternating pattern
        expecting_operand = True
        
        for i, token in enumerate(self._tokens):
            if expecting_operand:
                if token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    raise ValueError(f"Expected number or opening parenthesis at position {token.position}")
                expecting_operand = (token.type == TokenType.LEFT_PAREN)
            else:
                if token.type == TokenType.OPERATOR:
                    expecting_operand = True
                elif token.type == TokenType.RIGHT_PAREN:
                    expecting_operand = False
                else:
                    raise ValueError(f"Expected operator or closing parenthesis at position {token.position}")
        
        if expecting_operand:
            raise ValueError("Expression ends with operator")
    
    def _handle_unary_operators(self) -> List[Token]:
        """
        Handle unary minus operators by converting them to binary operations with zero.
        
        Returns:
            List of tokens with unary operators handled
        """
        if not self._tokens:
            return []
        
        processed_tokens = []
        
        for i, token in enumerate(self._tokens):
            if (token.type == TokenType.OPERATOR and token.value == '-' and
                (i == 0 or self._tokens[i-1].type in [TokenType.LEFT_PAREN, TokenType.OPERATOR])):
                # This is a unary minus
                processed_tokens.extend([
                    Token(TokenType.NUMBER, "0", token.position),
                    Token(TokenType.OPERATOR, "-", token.position)
                ])
            else:
                processed_tokens.append(token)
        
        return processed_tokens
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix notation
        """
        output_queue = []
        operator_stack = []
        
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
                if operator_stack:
                    operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            The calculated result
            
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
                
                result = self._apply_operator(token.value, left_operand, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: incorrect number of operands")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            left: Left operand
            right: Right operand
            
        Returns:
            The result of the operation
            
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
    Main function to demonstrate the calculator functionality.
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
