
"""
High-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

This module provides a Calculator class that can evaluate mathematical expressions
with support for basic arithmetic operations and parentheses.
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
    
    Supports addition (+), subtraction (-), multiplication (*), division (/),
    and parentheses with correct operator precedence.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    SUPPORTED_OPERATORS = {'+', '-', '*', '/'}
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing the mathematical expression
            
        Returns:
            float: The result of the calculation
            
        Raises:
            ValueError: If the expression is invalid
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) * 2")
            10.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        # Remove whitespace and validate basic format
        expression = expression.replace(" ", "")
        self._validate_expression_format(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Validate tokens and parentheses
        self._validate_tokens(tokens)
        self._validate_parentheses_balance(tokens)
        
        # Convert to postfix notation and evaluate
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        
        return result
    
    def _validate_expression_format(self, expression: str) -> None:
        """
        Validate the basic format of the expression.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        # Check for invalid characters
        valid_pattern = re.compile(r'^[0-9+\-*/.()]+$')
        if not valid_pattern.match(expression):
            raise ValueError("Expression contains invalid characters")
        
        # Check for empty parentheses
        if "()" in expression:
            raise ValueError("Empty parentheses are not allowed")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression: The expression to tokenize
            
        Returns:
            List[Token]: List of tokens representing the expression
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimal numbers)
                number_str, i = self._parse_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, float(number_str)))
                
            elif char in self.SUPPORTED_OPERATORS:
                # Handle unary minus
                if char == '-' and self._is_unary_minus(tokens):
                    number_str, i = self._parse_number(expression, i)
                    tokens.append(Token(TokenType.NUMBER, float(number_str)))
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
                    
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
                
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
                
            else:
                i += 1
        
        return tokens
    
    def _parse_number(self, expression: str, start_index: int) -> tuple[str, int]:
        """
        Parse a number (including negative numbers) from the expression.
        
        Args:
            expression: The full expression
            start_index: Starting index for parsing
            
        Returns:
            tuple: (number_string, next_index)
        """
        i = start_index
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += '-'
            i += 1
        
        # Parse digits and decimal point
        decimal_found = False
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                number_str += char
            elif char == '.' and not decimal_found:
                number_str += char
                decimal_found = True
            else:
                break
            i += 1
        
        if not number_str or number_str == '-' or number_str == '.':
            raise ValueError("Invalid number format")
        
        return number_str, i
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign is unary (negative number) or binary (subtraction).
        
        Args:
            tokens: Current list of tokens
            
        Returns:
            bool: True if the minus is unary, False if binary
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validate the sequence of tokens for logical correctness.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not tokens:
            raise ValueError("No valid tokens found")
        
        # Check for consecutive operators
        for i in range(len(tokens) - 1):
            current = tokens[i]
            next_token = tokens[i + 1]
            
            if (current.type == TokenType.OPERATOR and 
                next_token.type == TokenType.OPERATOR):
                raise ValueError("Consecutive operators are not allowed")
        
        # Expression cannot start or end with binary operators
        if tokens[0].type == TokenType.OPERATOR:
            raise ValueError("Expression cannot start with an operator")
        
        if tokens[-1].type == TokenType.OPERATOR:
            raise ValueError("Expression cannot end with an operator")
    
    def _validate_parentheses_balance(self, tokens: List[Token]) -> None:
        """
        Validate that parentheses are properly balanced.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            ValueError: If parentheses are not balanced
        """
        balance = 0
        for token in tokens:
            if token.type == TokenType.LEFT_PAREN:
                balance += 1
            elif token.type == TokenType.RIGHT_PAREN:
                balance -= 1
                if balance < 0:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
        
        if balance != 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix notation to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens in infix notation
            
        Returns:
            List[Token]: List of tokens in postfix notation
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
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
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
                
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(
                    left_operand, token.value, right_operand
                )
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: invalid number of operands")
        
        return stack[0]
    
    def _perform_operation(self, left: float, operator: str, right: float) -> float:
        """
        Perform a single arithmetic operation.
        
        Args:
            left: Left operand
            operator: The operator (+, -, *, /)
            right: Right operand
            
        Returns:
            float: The result of the operation
            
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
                raise ZeroDivisionError("Division by zero is not allowed")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")


def main():
    """
    Main function to demonstrate the calculator functionality.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() == 'quit':
                print("Goodbye!")
                break
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        print()  # Empty line for readability


if __name__ == "__main__":
    main()
