
"""
Arithmetic Calculator Module

A console-based calculator that evaluates mathematical expressions with support for
basic arithmetic operations and parentheses while maintaining operator precedence.

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
    A mathematical expression calculator that supports basic arithmetic operations.
    
    This calculator uses the Shunting Yard algorithm for parsing expressions and
    maintains proper operator precedence while supporting parentheses.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    # Valid operators
    VALID_OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing the mathematical expression to evaluate
            
        Returns:
            The numerical result of the expression evaluation
            
        Raises:
            ValueError: If the expression contains invalid characters, unbalanced 
                       parentheses, or invalid syntax
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(1 + 2) * 3")
            9.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        # Remove whitespace for easier processing
        expression = expression.replace(" ", "")
        
        # Validate the expression
        self._validate_expression(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._to_postfix(tokens)
        
        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix_tokens)
        
        return result
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the mathematical expression for common errors.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If the expression contains invalid characters or 
                       unbalanced parentheses
        """
        # Check for valid characters
        valid_chars = set('0123456789+-*/().') 
        if not all(char in valid_chars for char in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Check for balanced parentheses
        paren_count = 0
        for char in expression:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: closing ')' without opening '('")
        
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: missing closing ')'")
        
        # Check for empty parentheses
        if '()' in expression:
            raise ValueError("Empty parentheses are not allowed")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            A list of Token objects representing the expression
            
        Raises:
            ValueError: If the expression has invalid syntax
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals)
                number_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                
                try:
                    number = float(number_str)
                    tokens.append(Token(TokenType.NUMBER, number))
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                
                continue
            
            elif char in self.VALID_OPERATORS:
                # Handle negative numbers
                if char == '-' and self._is_unary_minus(tokens):
                    # Parse negative number
                    i += 1
                    if i >= len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                        raise ValueError("Invalid syntax: '-' must be followed by a number")
                    
                    number_str = "-"
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        number_str += expression[i]
                        i += 1
                    
                    try:
                        number = float(number_str)
                        tokens.append(Token(TokenType.NUMBER, number))
                    except ValueError:
                        raise ValueError(f"Invalid number format: {number_str}")
                    
                    continue
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
            
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
            
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
            
            else:
                raise ValueError(f"Invalid character: {char}")
            
            i += 1
        
        self._validate_token_sequence(tokens)
        return tokens
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign should be treated as unary (negative number).
        
        Args:
            tokens: List of tokens processed so far
            
        Returns:
            True if the minus should be treated as unary, False otherwise
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.LEFT_PAREN or 
                last_token.type == TokenType.OPERATOR)
    
    def _validate_token_sequence(self, tokens: List[Token]) -> None:
        """
        Validate the sequence of tokens for proper syntax.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            ValueError: If the token sequence has invalid syntax
        """
        if not tokens:
            raise ValueError("Empty expression")
        
        # First token must be a number or left parenthesis
        if tokens[0].type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
            raise ValueError("Expression must start with a number or '('")
        
        # Last token must be a number or right parenthesis
        if tokens[-1].type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
            raise ValueError("Expression must end with a number or ')'")
        
        # Check for consecutive operators or numbers
        for i in range(len(tokens) - 1):
            current = tokens[i]
            next_token = tokens[i + 1]
            
            if (current.type == TokenType.OPERATOR and 
                next_token.type == TokenType.OPERATOR):
                raise ValueError("Consecutive operators are not allowed")
            
            if (current.type == TokenType.NUMBER and 
                next_token.type == TokenType.NUMBER):
                raise ValueError("Consecutive numbers are not allowed")
    
    def _to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix tokens to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens in infix notation
            
        Returns:
            List of tokens in postfix notation
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
                
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type == TokenType.LEFT_PAREN:
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression and return the result.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            The numerical result of the evaluation
            
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
                    raise ValueError("Invalid expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(token.value, left_operand, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: malformed")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply (+, -, *, /)
            left: The left operand
            right: The right operand
            
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
                raise ZeroDivisionError("Division by zero is not allowed")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
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
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
