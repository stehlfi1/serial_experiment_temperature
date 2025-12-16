
"""
Arithmetic Calculator Module

A high-quality, maintainable calculator implementation that supports
basic arithmetic operations with proper error handling and validation.

Author: Senior Software Developer
Standards: ISO/IEC 25010 compliant
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
            token_type: Type of the token
            value: String value of the token
            position: Position in the original expression
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value}, {self.position})"


class CalculatorError(Exception):
    """Base exception class for calculator errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression is syntactically invalid."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class Calculator:
    """
    A robust arithmetic calculator supporting basic operations with parentheses.
    
    This calculator implements the Shunting Yard algorithm for expression parsing
    and evaluation, ensuring correct operator precedence and associativity.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    # Valid operators set for quick lookup
    VALID_OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for fresh calculation."""
        self._tokens: List[Token] = []
        self._current_position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            The calculated result as a float
            
        Raises:
            InvalidExpressionError: When expression syntax is invalid
            DivisionByZeroError: When division by zero is attempted
            UnbalancedParenthesesError: When parentheses don't match
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Empty expression")
        
        self._reset_state()
        
        try:
            # Step 1: Tokenize the expression
            self._tokenize(expression.strip())
            
            # Step 2: Validate tokens
            self._validate_tokens()
            
            # Step 3: Convert to postfix notation using Shunting Yard
            postfix_tokens = self._to_postfix()
            
            # Step 4: Evaluate postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression format: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression: The input expression string
            
        Raises:
            InvalidExpressionError: When invalid characters are found
        """
        self._tokens.clear()
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including negative numbers and decimals)
            if char.isdigit() or char == '.':
                number_str, new_i = self._parse_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
            
            # Handle negative numbers at the beginning or after operators/opening parentheses
            elif char == '-' and self._is_unary_minus_position():
                number_str, new_i = self._parse_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
            
            # Handle operators
            elif char in self.VALID_OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, char, i))
                i += 1
            
            # Handle parentheses
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
            
            # Invalid character
            else:
                raise InvalidExpressionError(
                    f"Invalid character '{char}' at position {i}"
                )
    
    def _parse_number(self, expression: str, start_pos: int) -> tuple[str, int]:
        """
        Parse a number (integer or float) from the expression.
        
        Args:
            expression: The full expression string
            start_pos: Starting position to parse from
            
        Returns:
            Tuple of (number_string, next_position)
        """
        i = start_pos
        number_str = ""
        decimal_count = 0
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Parse digits and decimal point
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.' and decimal_count == 0:
                number_str += char
                decimal_count += 1
                i += 1
            else:
                break
        
        # Validate the number format
        if not number_str or number_str in ['-', '.', '-.']:
            raise InvalidExpressionError(
                f"Invalid number format at position {start_pos}"
            )
        
        # Ensure the number is valid
        try:
            float(number_str)
        except ValueError:
            raise InvalidExpressionError(
                f"Invalid number '{number_str}' at position {start_pos}"
            )
        
        return number_str, i
    
    def _is_unary_minus_position(self) -> bool:
        """
        Determine if the current position could be a unary minus.
        
        Returns:
            True if this could be a unary minus, False otherwise
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return last_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for syntax correctness.
        
        Raises:
            InvalidExpressionError: When syntax errors are found
            UnbalancedParenthesesError: When parentheses don't match
        """
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found")
        
        # Check parentheses balance
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise UnbalancedParenthesesError(
                        f"Unmatched closing parenthesis at position {token.position}"
                    )
        
        if paren_count != 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
        
        # Validate token sequence
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end
                if i == 0 or i == len(self._tokens) - 1:
                    raise InvalidExpressionError(
                        f"Operator '{token.value}' cannot be at position {token.position}"
                    )
                
                # Operators cannot be followed by other operators
                next_token = self._tokens[i + 1]
                if next_token.type == TokenType.OPERATOR:
                    raise InvalidExpressionError(
                        f"Consecutive operators at positions {token.position} and {next_token.position}"
                    )
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Right parenthesis cannot be at the beginning
                if i == 0:
                    raise InvalidExpressionError(
                        f"Unexpected ')' at position {token.position}"
                    )
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix notation
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
                # Pop until matching left parenthesis
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
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            The calculated result
            
        Raises:
            DivisionByZeroError: When division by zero is attempted
            InvalidExpressionError: When the expression is malformed
        """
        stack: List[float] = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError(
                        f"Insufficient operands for operator '{token.value}'"
                    )
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(
                    token.value, left_operand, right_operand, token.position
                )
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression structure")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float, 
                       position: int) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator symbol
            left: Left operand
            right: Right operand
            position: Position in original expression for error reporting
            
        Returns:
            Result of the operation
            
        Raises:
            DivisionByZeroError: When division by zero is attempted
        """
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise DivisionByZeroError(
                    f"Division by zero at position {position}"
                )
            return left / right
        else:
            # This should never happen due to earlier validation
            raise InvalidExpressionError(f"Unknown operator: {operator}")


def main():
    """
    Main function to demonstrate calculator usage.
    Provides a simple console interface for testing.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() == 'quit':
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except CalculatorError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
