
"""
High-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

This module provides a Calculator class that can evaluate arithmetic expressions
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
    EOF = "EOF"


class Token:
    """Represents a token in the arithmetic expression."""
    
    def __init__(self, token_type: TokenType, value: Union[str, float]):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class Calculator:
    """
    A high-quality arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence,
    parentheses, and both integer and floating-point numbers including negative values.
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
        self._tokens: List[Token] = []
        self._current_token_index: int = 0
        self._current_token: Token = None
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression: A string containing the arithmetic expression to evaluate
            
        Returns:
            The result of the expression as a float
            
        Raises:
            ValueError: If the expression is invalid (empty, malformed, etc.)
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5 + 3")
            -2.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        try:
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate parentheses balance
            self._validate_parentheses_balance()
            
            # Parse and evaluate the expression
            self._current_token_index = 0
            self._current_token = self._tokens[0] if self._tokens else None
            
            result = self._parse_expression()
            
            # Ensure we've consumed all tokens
            if self._current_token.type != TokenType.EOF:
                raise ValueError("Invalid expression: unexpected tokens after evaluation")
            
            return float(result)
            
        except (IndexError, AttributeError) as e:
            raise ValueError(f"Invalid expression format: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into a list of tokens.
        
        Args:
            expression: The expression string to tokenize
            
        Raises:
            ValueError: If invalid characters are found in the expression
        """
        self._tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including negative numbers)
            if char.isdigit() or char == '.':
                number_str, i = self._extract_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
                continue
            
            # Handle negative numbers at the beginning or after operators/opening parentheses
            if char == '-' and self._is_negative_number_context():
                number_str, i = self._extract_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
                continue
            
            # Handle operators
            if char in self.VALID_OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
                continue
            
            # Handle parentheses
            if char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
                continue
            
            if char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
                continue
            
            # Invalid character
            raise ValueError(f"Invalid character in expression: '{char}'")
        
        # Add EOF token
        self._tokens.append(Token(TokenType.EOF, None))
    
    def _extract_number(self, expression: str, start_index: int) -> tuple[str, int]:
        """
        Extract a number (including negative numbers) from the expression.
        
        Args:
            expression: The expression string
            start_index: The starting index for extraction
            
        Returns:
            A tuple containing the number string and the next index
            
        Raises:
            ValueError: If the number format is invalid
        """
        i = start_index
        number_str = ""
        has_decimal = False
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Extract digits and decimal point
        while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
            if expression[i] == '.':
                if has_decimal:
                    raise ValueError(f"Invalid number format: multiple decimal points in '{number_str + expression[i]}'")
                has_decimal = True
            number_str += expression[i]
            i += 1
        
        # Validate the extracted number
        if not number_str or number_str == '-' or number_str == '.':
            raise ValueError(f"Invalid number format: '{number_str}'")
        
        # Check for valid number format
        if number_str.count('.') > 1 or number_str.endswith('.'):
            if not (number_str.endswith('.') and number_str.count('.') == 1 and len(number_str) > 1):
                raise ValueError(f"Invalid number format: '{number_str}'")
        
        return number_str, i
    
    def _is_negative_number_context(self) -> bool:
        """
        Determine if a minus sign represents a negative number rather than subtraction.
        
        Returns:
            True if the minus sign should be treated as part of a negative number
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return (last_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN] or
                len(self._tokens) == 0)
    
    def _validate_parentheses_balance(self) -> None:
        """
        Validate that parentheses are properly balanced in the expression.
        
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
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
        
        if balance > 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
    
    def _advance_token(self) -> None:
        """Move to the next token in the token list."""
        if self._current_token_index < len(self._tokens) - 1:
            self._current_token_index += 1
            self._current_token = self._tokens[self._current_token_index]
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate the expression using recursive descent parsing.
        
        Returns:
            The result of the expression evaluation
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """
        Parse addition and subtraction operations (lowest precedence).
        
        Returns:
            The result of the addition/subtraction operations
        """
        result = self._parse_multiplication_division()
        
        while (self._current_token.type == TokenType.OPERATOR and 
               self._current_token.value in ['+', '-']):
            operator = self._current_token.value
            self._advance_token()
            right_operand = self._parse_multiplication_division()
            
            if operator == '+':
                result += right_operand
            else:  # operator == '-'
                result -= right_operand
        
        return result
    
    def _parse_multiplication_division(self) -> float:
        """
        Parse multiplication and division operations (higher precedence).
        
        Returns:
            The result of the multiplication/division operations
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        result = self._parse_factor()
        
        while (self._current_token.type == TokenType.OPERATOR and 
               self._current_token.value in ['*', '/']):
            operator = self._current_token.value
            self._advance_token()
            right_operand = self._parse_factor()
            
            if operator == '*':
                result *= right_operand
            else:  # operator == '/'
                if right_operand == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                result /= right_operand
        
        return result
    
    def _parse_factor(self) -> float:
        """
        Parse factors (numbers and parenthesized expressions).
        
        Returns:
            The value of the factor
            
        Raises:
            ValueError: If the factor is malformed
        """
        if self._current_token.type == TokenType.NUMBER:
            value = self._current_token.value
            self._advance_token()
            return value
        
        elif self._current_token.type == TokenType.LEFT_PAREN:
            self._advance_token()  # consume '('
            result = self._parse_expression()
            
            if self._current_token.type != TokenType.RIGHT_PAREN:
                raise ValueError("Missing closing parenthesis")
            
            self._advance_token()  # consume ')'
            return result
        
        else:
            raise ValueError(f"Unexpected token: {self._current_token}")


# Example usage and testing
if __name__ == "__main__":
    def test_calculator():
        """Test function to demonstrate calculator functionality."""
        calc = Calculator()
        
        test_cases = [
            ("2 + 3", 5.0),
            ("10 - 4", 6.0),
            ("3 * 4", 12.0),
            ("15 / 3", 5.0),
            ("2 + 3 * 4", 14.0),
            ("(2 + 3) * 4", 20.0),
            ("-5 + 3", -2.0),
            ("10 / (2 + 3)", 2.0),
            ("3.14 * 2", 6.28),
            ("(-2 + 3) * 4", 4.0),
            ("2 * (3 + 4) / 7", 2.0),
        ]
        
        print("Calculator Test Results:")
        print("-" * 40)
        
        for expression, expected in test_cases:
            try:
                result = calc.calculate(expression)
                status = "✓" if abs(result - expected) < 1e-10 else "✗"
                print(f"{status} {expression} = {result} (expected: {expected})")
            except Exception as e:
                print(f"✗ {expression} -> Error: {e}")
        
        # Test error cases
        error_cases = [
            "2 / 0",  # Division by zero
            "2 + ",   # Incomplete expression
            "((2 + 3)",  # Unbalanced parentheses
            "2 + 3)",     # Extra closing parenthesis
            "2 @ 3",      # Invalid operator
            "",           # Empty expression
        ]
        
        print("\nError Handling Tests:")
        print("-" * 40)
        
        for expression in error_cases:
            try:
                result = calc.calculate(expression)
                print(f"✗ '{expression}' should have raised an error but got: {result}")
            except Exception as e:
                print(f"✓ '{expression}' -> {type(e).__name__}: {e}")
    
    test_calculator()
