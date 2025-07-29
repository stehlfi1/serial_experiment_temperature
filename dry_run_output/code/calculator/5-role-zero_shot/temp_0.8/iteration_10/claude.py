
"""
High-quality console-based arithmetic calculator implementation.

This module provides a Calculator class that can evaluate mathematical expressions
with proper operator precedence, parentheses support, and comprehensive error handling.
Adheres to ISO/IEC 25010 quality standards.
"""

import re
from typing import List, Union, Tuple
from enum import Enum


class TokenType(Enum):
    """Enumeration of token types for expression parsing."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Represents a token in the mathematical expression."""
    
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
        """String representation of the token."""
        return f"Token({self.type}, {self.value})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid syntax or characters."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class Calculator:
    """
    A high-quality arithmetic calculator supporting basic operations with parentheses.
    
    This calculator uses the Shunting Yard algorithm for parsing expressions and
    evaluates them using a stack-based approach for optimal performance and correctness.
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
        """Reset internal state for a fresh calculation."""
        self._tokens: List[Token] = []
        self._postfix_tokens: List[Token] = []
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            The calculated result as a float
            
        Raises:
            InvalidExpressionError: For invalid syntax or characters
            DivisionByZeroError: When attempting to divide by zero
            UnbalancedParenthesesError: When parentheses are not balanced
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5 + 3.5")
            -1.5
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        try:
            self._reset_state()
            self._tokenize(expression.strip())
            self._validate_tokens()
            self._convert_to_postfix()
            return self._evaluate_postfix()
            
        except CalculatorError:
            # Re-raise calculator-specific errors
            raise
        except Exception as e:
            # Wrap unexpected errors
            raise InvalidExpressionError(f"Unexpected error: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert the input expression into tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        # Remove all whitespace
        expression = re.sub(r'\s+', '', expression)
        
        if not expression:
            raise InvalidExpressionError("Expression cannot be empty")
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including floating point)
                number_str, i = self._parse_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
                
            elif char in self.VALID_OPERATORS:
                # Handle unary minus
                if char == '-' and self._is_unary_minus_context():
                    # Parse negative number
                    if i + 1 >= len(expression):
                        raise InvalidExpressionError("Invalid unary minus at end of expression")
                    
                    number_str, i = self._parse_number(expression, i + 1)
                    self._tokens.append(Token(TokenType.NUMBER, -float(number_str)))
                else:
                    self._tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
                    
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
                
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
                
            else:
                raise InvalidExpressionError(f"Invalid character: '{char}'")
    
    def _parse_number(self, expression: str, start_index: int) -> Tuple[str, int]:
        """
        Parse a number from the expression starting at the given index.
        
        Args:
            expression: The full expression
            start_index: Starting index for parsing
            
        Returns:
            Tuple of (number_string, next_index)
            
        Raises:
            InvalidExpressionError: If the number format is invalid
        """
        i = start_index
        number_str = ""
        decimal_count = 0
        
        while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
            if expression[i] == '.':
                decimal_count += 1
                if decimal_count > 1:
                    raise InvalidExpressionError("Invalid number format: multiple decimal points")
            number_str += expression[i]
            i += 1
        
        if not number_str or number_str == '.':
            raise InvalidExpressionError("Invalid number format")
        
        # Validate that the number can be converted to float
        try:
            float(number_str)
        except ValueError:
            raise InvalidExpressionError(f"Invalid number format: '{number_str}'")
        
        return number_str, i
    
    def _is_unary_minus_context(self) -> bool:
        """
        Determine if a minus sign should be treated as unary.
        
        Returns:
            True if the minus should be treated as unary, False otherwise
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for correctness.
        
        Raises:
            InvalidExpressionError: If the token sequence is invalid
            UnbalancedParenthesesError: If parentheses are not balanced
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
                    raise UnbalancedParenthesesError("Mismatched closing parenthesis")
        
        if paren_count != 0:
            raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        # Validate token sequence
        self._validate_token_sequence()
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that the sequence of tokens follows proper mathematical syntax.
        
        Raises:
            InvalidExpressionError: If the token sequence is invalid
        """
        if not self._tokens:
            return
        
        # First token must be number or left parenthesis
        first_token = self._tokens[0]
        if first_token.type not in (TokenType.NUMBER, TokenType.LEFT_PAREN):
            raise InvalidExpressionError("Expression must start with a number or opening parenthesis")
        
        # Last token must be number or right parenthesis
        last_token = self._tokens[-1]
        if last_token.type not in (TokenType.NUMBER, TokenType.RIGHT_PAREN):
            raise InvalidExpressionError("Expression must end with a number or closing parenthesis")
        
        # Check adjacent token validity
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if not self._are_valid_adjacent_tokens(current, next_token):
                raise InvalidExpressionError(
                    f"Invalid token sequence: {current.value} followed by {next_token.value}"
                )
    
    def _are_valid_adjacent_tokens(self, current: Token, next_token: Token) -> bool:
        """
        Check if two adjacent tokens form a valid sequence.
        
        Args:
            current: The current token
            next_token: The next token
            
        Returns:
            True if the sequence is valid, False otherwise
        """
        # Define valid transitions
        valid_transitions = {
            TokenType.NUMBER: {TokenType.OPERATOR, TokenType.RIGHT_PAREN},
            TokenType.OPERATOR: {TokenType.NUMBER, TokenType.LEFT_PAREN},
            TokenType.LEFT_PAREN: {TokenType.NUMBER, TokenType.LEFT_PAREN},
            TokenType.RIGHT_PAREN: {TokenType.OPERATOR, TokenType.RIGHT_PAREN}
        }
        
        return next_token.type in valid_transitions.get(current.type, set())
    
    def _convert_to_postfix(self) -> None:
        """
        Convert infix tokens to postfix notation using the Shunting Yard algorithm.
        
        This method provides O(n) time complexity for conversion.
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
                       self._has_higher_or_equal_precedence(operator_stack[-1].value, token.value)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
                
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
                
            elif token.type == TokenType.RIGHT_PAREN:
                # Pop until left parenthesis
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                # Remove the left parenthesis
                if operator_stack:
                    operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        self._postfix_tokens = output_queue
    
    def _has_higher_or_equal_precedence(self, op1: str, op2: str) -> bool:
        """
        Check if operator op1 has higher or equal precedence than op2.
        
        Args:
            op1: First operator
            op2: Second operator
            
        Returns:
            True if op1 has higher or equal precedence
        """
        return self.OPERATOR_PRECEDENCE[op1] >= self.OPERATOR_PRECEDENCE[op2]
    
    def _evaluate_postfix(self) -> float:
        """
        Evaluate the postfix expression using a stack.
        
        Returns:
            The calculated result
            
        Raises:
            DivisionByZeroError: When attempting to divide by zero
            InvalidExpressionError: If the expression is malformed
        """
        if not self._postfix_tokens:
            raise InvalidExpressionError("No expression to evaluate")
        
        stack: List[float] = []
        
        for token in self._postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
                
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operator")
                
                # Pop operands (note the order)
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                # Perform operation
                result = self._perform_operation(left_operand, token.value, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Malformed expression: incorrect number of operands")
        
        return stack[0]
    
    def _perform_operation(self, left: float, operator: str, right: float) -> float:
        """
        Perform a binary arithmetic operation.
        
        Args:
            left: Left operand
            operator: Arithmetic operator
            right: Right operand
            
        Returns:
            Result of the operation
            
        Raises:
            DivisionByZeroError: When attempting to divide by zero
        """
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise DivisionByZeroError("Division by zero is not allowed")
            return left / right
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")


def main():
    """
    Main function to demonstrate calculator usage.
    Provides a simple console interface for testing.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ('quit', 'exit', 'q'):
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}\n")
            
        except CalculatorError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
