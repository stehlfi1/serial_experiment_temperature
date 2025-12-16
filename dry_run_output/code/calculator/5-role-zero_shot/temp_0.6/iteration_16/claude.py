
"""
High-Quality Arithmetic Calculator

This module implements a console-based arithmetic calculator that supports
basic operations with proper error handling and validation according to
ISO/IEC 25010 standards.

Author: Senior Software Developer
Version: 1.0.0
"""

import re
from typing import List, Union
from enum import Enum


class TokenType(Enum):
    """Enumeration for different types of tokens in mathematical expressions."""
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
            token_type (TokenType): The type of the token
            value (Union[float, str]): The value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        """String representation of the token for debugging."""
        return f"Token({self.type}, {self.value})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid syntax."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A high-quality arithmetic calculator that evaluates mathematical expressions.
    
    Supports:
    - Basic operations: +, -, *, /
    - Parentheses for grouping
    - Proper operator precedence
    - Integer and floating-point numbers
    - Negative numbers
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
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
            expression (str): The mathematical expression to evaluate
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            InvalidExpressionError: If the expression is invalid
            DivisionByZeroError: If division by zero is attempted
            
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
            raise InvalidExpressionError("Expression cannot be empty")
        
        try:
            self._reset_state()
            self._tokenize(expression)
            self._validate_tokens()
            result = self._evaluate_expression()
            return float(result)
        except ZeroDivisionError:
            raise DivisionByZeroError("Division by zero is not allowed")
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into a list of tokens.
        
        Args:
            expression (str): The expression to tokenize
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        # Remove whitespace and validate characters
        cleaned_expr = re.sub(r'\s+', '', expression)
        
        if not re.match(r'^[0-9+\-*/().]+$', cleaned_expr):
            raise InvalidExpressionError("Expression contains invalid characters")
        
        i = 0
        while i < len(cleaned_expr):
            char = cleaned_expr[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals)
                number_str, i = self._parse_number(cleaned_expr, i)
                self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
            
            elif char in '+-*/':
                # Handle operators and unary minus
                if char == '-' and self._is_unary_minus():
                    # Parse negative number
                    number_str, i = self._parse_number(cleaned_expr, i)
                    self._tokens.append(Token(TokenType.NUMBER, float(number_str)))
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
                raise InvalidExpressionError(f"Unexpected character: {char}")
    
    def _parse_number(self, expression: str, start_pos: int) -> tuple[str, int]:
        """
        Parse a number (including negative numbers and decimals) from the expression.
        
        Args:
            expression (str): The expression being parsed
            start_pos (int): Starting position in the expression
            
        Returns:
            tuple[str, int]: The number string and the new position
        """
        i = start_pos
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Parse digits and decimal point
        decimal_found = False
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.' and not decimal_found:
                decimal_found = True
                number_str += char
                i += 1
            else:
                break
        
        if not number_str or number_str in ['-', '.', '-.']:
            raise InvalidExpressionError("Invalid number format")
        
        return number_str, i
    
    def _is_unary_minus(self) -> bool:
        """
        Determine if the current minus sign is unary (negative number).
        
        Returns:
            bool: True if the minus is unary, False if it's binary subtraction
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return (last_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for common syntax errors.
        
        Raises:
            InvalidExpressionError: If validation fails
        """
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found")
        
        # Check balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise InvalidExpressionError("Unbalanced parentheses")
        
        # Check for consecutive operators
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if (current.type == TokenType.OPERATOR and 
                next_token.type == TokenType.OPERATOR):
                raise InvalidExpressionError("Consecutive operators not allowed")
        
        # Check that expression doesn't start/end with binary operators
        if (self._tokens[0].type == TokenType.OPERATOR and 
            self._tokens[0].value in ['*', '/', '+']):
            raise InvalidExpressionError("Expression cannot start with binary operator")
        
        if self._tokens[-1].type == TokenType.OPERATOR:
            raise InvalidExpressionError("Expression cannot end with operator")
    
    def _evaluate_expression(self) -> float:
        """
        Evaluate the tokenized expression using the shunting yard algorithm.
        
        Returns:
            float: The result of the evaluation
        """
        # Convert infix to postfix notation (Reverse Polish Notation)
        postfix = self._infix_to_postfix()
        
        # Evaluate postfix expression
        return self._evaluate_postfix(postfix)
    
    def _infix_to_postfix(self) -> List[Token]:
        """
        Convert infix notation to postfix notation using the Shunting Yard algorithm.
        
        Returns:
            List[Token]: Tokens in postfix notation
        """
        output_queue: List[Token] = []
        operator_stack: List[Token] = []
        
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
            
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.PRECEDENCE[operator_stack[-1].value] >= self.PRECEDENCE[token.value]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack:
                    raise InvalidExpressionError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise InvalidExpressionError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens (List[Token]): Tokens in postfix notation
            
        Returns:
            float: The result of the evaluation
        """
        stack: List[float] = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operator")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(token.value, left_operand, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression structure")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Apply a binary operator to two operands.
        
        Args:
            operator (str): The operator (+, -, *, /)
            left (float): Left operand
            right (float): Right operand
            
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
                raise DivisionByZeroError("Division by zero is not allowed")
            return left / right
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")


def main():
    """
    Main function to demonstrate the calculator functionality.
    Provides a simple console interface for user interaction.
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
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}\n")
            
        except (InvalidExpressionError, DivisionByZeroError) as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
