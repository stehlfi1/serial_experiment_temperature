
"""
Console-based Arithmetic Calculator

A high-quality implementation of an arithmetic calculator that supports
basic operations (+, -, *, /) with proper operator precedence and parentheses.
Follows ISO/IEC 25010 quality standards.
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
        return f"Token({self.type}, {self.value})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression is syntactically invalid."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports:
    - Basic operations: +, -, *, /
    - Parentheses for grouping
    - Proper operator precedence
    - Integer and floating-point numbers (including negative values)
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    def __init__(self):
        """Initialize the calculator."""
        self._operators = {'+', '-', '*', '/'}
        self._number_pattern = re.compile(r'^-?\d+\.?\d*$')
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            The calculated result as a float
            
        Raises:
            InvalidExpressionError: If the expression is syntactically invalid
            DivisionByZeroError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 2) / 4")
            2.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        try:
            # Tokenize the expression
            tokens = self._tokenize(expression)
            
            # Validate token sequence
            self._validate_tokens(tokens)
            
            # Convert to postfix notation using Shunting Yard algorithm
            postfix_tokens = self._to_postfix(tokens)
            
            # Evaluate the postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression string
            
        Returns:
            List of Token objects
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        tokens = []
        i = 0
        expression = expression.replace(' ', '')  # Remove whitespace
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Handle numbers (including decimals)
                number_str, i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, float(number_str)))
                
            elif char == '-':
                # Handle negative numbers vs subtraction
                if self._is_negative_number_context(tokens):
                    number_str, i = self._extract_number(expression, i)
                    tokens.append(Token(TokenType.NUMBER, float(number_str)))
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
                    
            elif char in self._operators:
                tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
                
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
                
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
                
            else:
                raise InvalidExpressionError(f"Invalid character: '{char}'")
        
        return tokens
    
    def _extract_number(self, expression: str, start: int) -> Tuple[str, int]:
        """
        Extract a number (including negative numbers) from the expression.
        
        Args:
            expression: The expression string
            start: Starting index
            
        Returns:
            Tuple of (number_string, next_index)
        """
        i = start
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Extract digits and decimal point
        decimal_found = False
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.' and not decimal_found:
                number_str += char
                decimal_found = True
                i += 1
            else:
                break
        
        if not number_str or number_str == '-' or number_str == '.':
            raise InvalidExpressionError(f"Invalid number format at position {start}")
        
        return number_str, i
    
    def _is_negative_number_context(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign represents a negative number or subtraction.
        
        Args:
            tokens: List of tokens processed so far
            
        Returns:
            True if the minus sign should be treated as part of a negative number
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validate the sequence of tokens for syntactic correctness.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            InvalidExpressionError: If the token sequence is invalid
        """
        if not tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise InvalidExpressionError("Unbalanced parentheses")
        
        # Validate token sequence
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError("Operator cannot be at beginning or end")
                
                # Operators cannot be followed by other operators
                if (i < len(tokens) - 1 and 
                    tokens[i + 1].type == TokenType.OPERATOR):
                    raise InvalidExpressionError("Consecutive operators not allowed")
    
    def _to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix notation to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens in infix notation
            
        Returns:
            List of tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
                
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.OPERATOR_PRECEDENCE[operator_stack[-1].value] >= 
                       self.OPERATOR_PRECEDENCE[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
                
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
                
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output.append(operator_stack.pop())
                
                if not operator_stack:
                    raise InvalidExpressionError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in (TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN):
                raise InvalidExpressionError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            The calculated result
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
                
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Invalid expression structure")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(
                    left_operand, token.value, right_operand
                )
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression structure")
        
        return stack[0]
    
    def _perform_operation(self, left: float, operator: str, right: float) -> float:
        """
        Perform a single arithmetic operation.
        
        Args:
            left: Left operand
            operator: Operator symbol
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
    Demonstrates the calculator's functionality and error handling.
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
                print("Goodbye!")
                break
            
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
