
"""
Console-based Arithmetic Calculator

A high-quality calculator implementation that supports basic arithmetic operations
with proper operator precedence, parentheses support, and comprehensive error handling.

Author: Senior Software Developer
Compliance: ISO/IEC 25010 Standard
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
    
    def __init__(self, token_type: TokenType, value: str, position: int):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The string value of the token
            position: The position in the original expression
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value}, {self.position})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid syntax or characters."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator supporting basic operations with proper precedence.
    
    Supports:
    - Addition (+), Subtraction (-), Multiplication (*), Division (/)
    - Parentheses for grouping operations
    - Both integers and floating-point numbers
    - Negative numbers
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
            expression: A string containing the mathematical expression
            
        Returns:
            float: The calculated result
            
        Raises:
            InvalidExpressionError: If the expression contains invalid syntax
            UnbalancedParenthesesError: If parentheses are not balanced
            DivisionByZeroError: If division by zero is attempted
            ValueError: If the expression is empty or contains invalid numbers
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        self._reset_state()
        
        # Tokenize the expression
        self._tokens = self._tokenize(expression.strip())
        
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found in expression")
        
        # Validate token sequence
        self._validate_token_sequence()
        
        # Check parentheses balance
        self._validate_parentheses_balance()
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._infix_to_postfix()
        
        # Evaluate postfix expression
        result = self._evaluate_postfix(postfix_tokens)
        
        return result
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize the input expression into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List[Token]: List of tokens representing the expression
            
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
            
            # Handle numbers (including decimals and negative numbers)
            if char.isdigit() or char == '.':
                number_str, new_i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
            
            # Handle negative numbers (unary minus)
            elif char == '-' and self._is_unary_minus(tokens):
                number_str, new_i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
            
            # Handle operators
            elif char in self.VALID_OPERATORS:
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
                raise InvalidExpressionError(
                    f"Invalid character '{char}' at position {i}"
                )
        
        return tokens
    
    def _extract_number(self, expression: str, start_pos: int) -> Tuple[str, int]:
        """
        Extract a complete number (including decimals and negative signs) from the expression.
        
        Args:
            expression: The full expression
            start_pos: Starting position in the expression
            
        Returns:
            Tuple[str, int]: The number string and the next position
            
        Raises:
            InvalidExpressionError: If the number format is invalid
        """
        i = start_pos
        number_str = ""
        has_decimal = False
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Extract digits and decimal point
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                number_str += char
                i += 1
            else:
                break
        
        # Validate the extracted number
        if not number_str or number_str in ['-', '.', '-.']:
            raise InvalidExpressionError(
                f"Invalid number format at position {start_pos}"
            )
        
        # Check if it's a valid number
        try:
            float(number_str)
        except ValueError:
            raise InvalidExpressionError(
                f"Invalid number '{number_str}' at position {start_pos}"
            )
        
        return number_str, i
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign should be treated as unary (negative number).
        
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
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that the sequence of tokens forms a valid mathematical expression.
        
        Raises:
            InvalidExpressionError: If the token sequence is invalid
        """
        if not self._tokens:
            raise InvalidExpressionError("Empty token sequence")
        
        # First token should be number or left parenthesis
        first_token = self._tokens[0]
        if first_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
            raise InvalidExpressionError(
                f"Expression cannot start with {first_token.value}"
            )
        
        # Last token should be number or right parenthesis
        last_token = self._tokens[-1]
        if last_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
            raise InvalidExpressionError(
                f"Expression cannot end with {last_token.value}"
            )
        
        # Check token sequence validity
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if current.type == TokenType.NUMBER:
                if next_token.type not in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]:
                    raise InvalidExpressionError(
                        f"Invalid token sequence: number followed by {next_token.value}"
                    )
            
            elif current.type == TokenType.OPERATOR:
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    raise InvalidExpressionError(
                        f"Invalid token sequence: operator followed by {next_token.value}"
                    )
            
            elif current.type == TokenType.LEFT_PAREN:
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    raise InvalidExpressionError(
                        f"Invalid token sequence: '(' followed by {next_token.value}"
                    )
            
            elif current.type == TokenType.RIGHT_PAREN:
                if next_token.type not in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]:
                    raise InvalidExpressionError(
                        f"Invalid token sequence: ')' followed by {next_token.value}"
                    )
    
    def _validate_parentheses_balance(self) -> None:
        """
        Validate that parentheses are properly balanced.
        
        Raises:
            UnbalancedParenthesesError: If parentheses are not balanced
        """
        balance = 0
        
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                balance += 1
            elif token.type == TokenType.RIGHT_PAREN:
                balance -= 1
                
                if balance < 0:
                    raise UnbalancedParenthesesError(
                        f"Unmatched closing parenthesis at position {token.position}"
                    )
        
        if balance > 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
    
    def _infix_to_postfix(self) -> List[Token]:
        """
        Convert infix notation to postfix notation using the Shunting Yard algorithm.
        
        Returns:
            List[Token]: Tokens in postfix order
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
                
                # Remove the left parenthesis
                if operator_stack:
                    operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression and return the result.
        
        Args:
            postfix_tokens: List of tokens in postfix order
            
        Returns:
            float: The calculated result
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Malformed expression")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(
                    token.value, left_operand, right_operand, token.position
                )
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Malformed expression")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float, 
                       position: int) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            left: Left operand
            right: Right operand
            position: Position in original expression for error reporting
            
        Returns:
            float: Result of the operation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
        """
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise DivisionByZeroError(f"Division by zero at position {position}")
            return left / right
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")


def main():
    """
    Main function to demonstrate the calculator usage.
    Provides a simple console interface for testing the calculator.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and decimal numbers")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() == 'quit':
                print("Goodbye!")
                break
            
            result = calculator.calculate(expression)
            print(f"Result: {result}\n")
            
        except (CalculatorError, ValueError) as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
