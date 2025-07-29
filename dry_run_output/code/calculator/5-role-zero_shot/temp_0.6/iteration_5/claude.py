
"""
A robust console-based arithmetic calculator implementing the Shunting Yard algorithm
for expression evaluation with comprehensive error handling and validation.

This module adheres to ISO/IEC 25010 quality standards for software systems.
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
    
    def __init__(self, type_: TokenType, value: str, position: int):
        """
        Initialize a token.
        
        Args:
            type_: The type of the token
            value: The string value of the token
            position: The position of the token in the original expression
        """
        self.type = type_
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


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class Calculator:
    """
    A robust arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator
    precedence and parentheses handling using the Shunting Yard algorithm.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    # Left-associative operators
    LEFT_ASSOCIATIVE = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        self._expression = ""
        self._tokens = []
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing the mathematical expression to evaluate
            
        Returns:
            The numerical result of the expression evaluation
            
        Raises:
            InvalidExpressionError: If the expression contains invalid syntax
            DivisionByZeroError: If division by zero is attempted
            UnbalancedParenthesesError: If parentheses are not balanced
            
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
        
        self._expression = expression.strip()
        self._validate_expression()
        self._tokens = self._tokenize()
        self._validate_tokens()
        
        postfix_tokens = self._convert_to_postfix()
        result = self._evaluate_postfix(postfix_tokens)
        
        return result
    
    def _validate_expression(self) -> None:
        """
        Validate the expression for basic syntax rules.
        
        Raises:
            InvalidExpressionError: If invalid characters are found
            UnbalancedParenthesesError: If parentheses are not balanced
        """
        # Check for valid characters only
        valid_chars = set('0123456789+-*/().eE ')
        if not all(char in valid_chars for char in self._expression):
            invalid_chars = set(self._expression) - valid_chars
            raise InvalidExpressionError(
                f"Invalid characters found: {', '.join(sorted(invalid_chars))}"
            )
        
        # Check balanced parentheses
        paren_count = 0
        for char in self._expression:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise UnbalancedParenthesesError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count > 0:
            raise UnbalancedParenthesesError("Unbalanced parentheses: too many opening parentheses")
    
    def _tokenize(self) -> List[Token]:
        """
        Convert the expression string into a list of tokens.
        
        Returns:
            A list of Token objects representing the expression
            
        Raises:
            InvalidExpressionError: If tokenization fails
        """
        tokens = []
        i = 0
        
        while i < len(self._expression):
            char = self._expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including negative numbers and decimals)
            if char.isdigit() or char == '.':
                number, new_i = self._parse_number(i)
                tokens.append(Token(TokenType.NUMBER, number, i))
                i = new_i
            
            # Handle operators
            elif char in self.OPERATOR_PRECEDENCE:
                # Check if this is a unary minus
                if char == '-' and self._is_unary_minus(tokens):
                    number, new_i = self._parse_number(i)
                    tokens.append(Token(TokenType.NUMBER, number, i))
                    i = new_i
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
            
            else:
                raise InvalidExpressionError(f"Unexpected character '{char}' at position {i}")
        
        return tokens
    
    def _parse_number(self, start_index: int) -> Tuple[str, int]:
        """
        Parse a number (including negative numbers and decimals) from the expression.
        
        Args:
            start_index: Starting position in the expression
            
        Returns:
            Tuple of (number_string, next_index)
            
        Raises:
            InvalidExpressionError: If number format is invalid
        """
        i = start_index
        number_str = ""
        
        # Handle negative sign
        if i < len(self._expression) and self._expression[i] == '-':
            number_str += '-'
            i += 1
        
        # Handle digits and decimal point
        has_decimal = False
        has_digits = False
        
        while i < len(self._expression):
            char = self._expression[i]
            
            if char.isdigit():
                number_str += char
                has_digits = True
                i += 1
            elif char == '.' and not has_decimal:
                number_str += char
                has_decimal = True
                i += 1
            elif char.lower() == 'e' and has_digits:
                # Handle scientific notation
                number_str += char
                i += 1
                if i < len(self._expression) and self._expression[i] in '+-':
                    number_str += self._expression[i]
                    i += 1
                # Continue parsing digits after 'e'
                while i < len(self._expression) and self._expression[i].isdigit():
                    number_str += self._expression[i]
                    i += 1
                break
            else:
                break
        
        if not has_digits:
            raise InvalidExpressionError(f"Invalid number format at position {start_index}")
        
        # Validate the number format
        try:
            float(number_str)
        except ValueError:
            raise InvalidExpressionError(f"Invalid number format '{number_str}' at position {start_index}")
        
        return number_str, i
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign should be treated as unary.
        
        Args:
            tokens: List of tokens parsed so far
            
        Returns:
            True if the minus should be treated as unary, False otherwise
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self) -> None:
        """
        Validate the sequence of tokens for proper syntax.
        
        Raises:
            InvalidExpressionError: If token sequence is invalid
        """
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found")
        
        # Check for consecutive operators
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if (current.type == TokenType.OPERATOR and 
                next_token.type == TokenType.OPERATOR):
                raise InvalidExpressionError(
                    f"Consecutive operators at positions {current.position} and {next_token.position}"
                )
        
        # Check first and last tokens
        first_token = self._tokens[0]
        last_token = self._tokens[-1]
        
        if first_token.type == TokenType.OPERATOR and first_token.value != '-':
            raise InvalidExpressionError("Expression cannot start with an operator (except minus)")
        
        if last_token.type == TokenType.OPERATOR:
            raise InvalidExpressionError("Expression cannot end with an operator")
    
    def _convert_to_postfix(self) -> List[Token]:
        """
        Convert infix tokens to postfix notation using the Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
            
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self._should_pop_operator(token.value, operator_stack[-1].value)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output.append(operator_stack.pop())
                
                if operator_stack:
                    operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def _should_pop_operator(self, current_op: str, stack_op: str) -> bool:
        """
        Determine if an operator should be popped from the stack.
        
        Args:
            current_op: Current operator being processed
            stack_op: Operator on top of the stack
            
        Returns:
            True if the stack operator should be popped, False otherwise
        """
        current_precedence = self.OPERATOR_PRECEDENCE[current_op]
        stack_precedence = self.OPERATOR_PRECEDENCE[stack_op]
        
        if current_op in self.LEFT_ASSOCIATIVE:
            return stack_precedence >= current_precedence
        else:
            return stack_precedence > current_precedence
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluate postfix notation tokens to get the final result.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            The numerical result of the expression
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If evaluation fails
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                try:
                    stack.append(float(token.value))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number: {token.value}")
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operator")
                
                right = stack.pop()
                left = stack.pop()
                
                result = self._apply_operator(token.value, left, right)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: incorrect number of operands")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            left: Left operand
            right: Right operand
            
        Returns:
            Result of the operation
            
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
                raise DivisionByZeroError("Division by zero is not allowed")
            return left / right
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ('quit', 'exit'):
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (InvalidExpressionError, DivisionByZeroError, 
                UnbalancedParenthesesError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
