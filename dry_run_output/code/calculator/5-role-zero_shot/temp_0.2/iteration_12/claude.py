
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
            expression: Mathematical expression string to evaluate
            
        Returns:
            The calculated result as a float
            
        Raises:
            ValueError: If the expression is invalid (syntax errors, unbalanced parentheses)
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) / 2.5")
            2.0
            >>> calc.calculate("-3 + 4")
            1.0
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
            expression: The expression string to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Regular expression to match numbers (including negative), operators, and parentheses
        token_pattern = r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))'
        
        # Remove whitespace and find all tokens
        clean_expression = re.sub(r'\s+', '', expression)
        matches = re.finditer(token_pattern, clean_expression)
        
        position = 0
        for match in matches:
            token_value = match.group(1)
            token_start = match.start()
            
            # Check for gaps in tokenization (invalid characters)
            if token_start > position:
                invalid_char = clean_expression[position]
                raise ValueError(f"Invalid character '{invalid_char}' at position {position}")
            
            # Determine token type and create token
            if self._is_number(token_value):
                self._tokens.append(Token(TokenType.NUMBER, token_value, token_start))
            elif token_value in self.VALID_OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, token_value, token_start))
            elif token_value == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, token_value, token_start))
            elif token_value == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, token_value, token_start))
            
            position = match.end()
        
        # Check if entire expression was tokenized
        if position < len(clean_expression):
            invalid_char = clean_expression[position]
            raise ValueError(f"Invalid character '{invalid_char}' at position {position}")
    
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
        Validate the tokenized expression for syntax errors.
        
        Raises:
            ValueError: If syntax errors are found
        """
        if not self._tokens:
            raise ValueError("Empty expression")
        
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
        Validate the sequence of tokens for proper syntax.
        
        Raises:
            ValueError: If invalid token sequences are found
        """
        if not self._tokens:
            return
        
        # Handle unary minus by converting to binary operation with zero
        self._handle_unary_operators()
        
        # Check for valid token sequences
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators must have operands on both sides (after unary handling)
                if i == 0 or i == len(self._tokens) - 1:
                    raise ValueError(f"Operator '{token.value}' at position {token.position} missing operand")
                
                prev_token = self._tokens[i - 1]
                next_token = self._tokens[i + 1]
                
                # Previous token should be number or closing parenthesis
                if prev_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
                    raise ValueError(f"Invalid token before operator '{token.value}' at position {token.position}")
                
                # Next token should be number or opening parenthesis
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    raise ValueError(f"Invalid token after operator '{token.value}' at position {token.position}")
    
    def _handle_unary_operators(self) -> None:
        """
        Handle unary minus operators by converting them to binary operations with zero.
        """
        new_tokens = []
        
        for i, token in enumerate(self._tokens):
            if (token.type == TokenType.OPERATOR and token.value == '-' and
                (i == 0 or self._tokens[i - 1].type in [TokenType.LEFT_PAREN, TokenType.OPERATOR])):
                # This is a unary minus, convert to "0 - "
                new_tokens.append(Token(TokenType.NUMBER, '0', token.position))
                new_tokens.append(token)
            else:
                new_tokens.append(token)
        
        self._tokens = new_tokens
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix order
        """
        output_queue = []
        operator_stack = []
        
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
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                # Convert to appropriate numeric type
                value = float(token.value)
                if value.is_integer():
                    value = int(value)
                stack.append(value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError(f"Insufficient operands for operator '{token.value}'")
                
                # Pop two operands (note the order)
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                # Perform operation
                result = self._perform_operation(left_operand, right_operand, token.value)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression")
        
        return stack[0]
    
    def _perform_operation(self, left: Union[int, float], right: Union[int, float], 
                          operator: str) -> Union[int, float]:
        """
        Perform a binary arithmetic operation.
        
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
            result = left + right
        elif operator == '-':
            result = left - right
        elif operator == '*':
            result = left * right
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            result = left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")
        
        # Return integer if result is a whole number
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result


def main():
    """
    Main function to demonstrate calculator usage.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and negative numbers")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() == 'quit':
                break
            
            result = calculator.calculate(expression)
            print(f"Result: {result}\n")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
