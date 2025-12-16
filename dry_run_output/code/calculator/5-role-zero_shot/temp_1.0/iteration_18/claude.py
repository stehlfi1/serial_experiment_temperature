
"""
Arithmetic Calculator Module

A console-based calculator that evaluates arithmetic expressions with proper
operator precedence and parentheses support, following ISO/IEC 25010 standards.
"""

import re
from typing import List, Union
from enum import Enum


class TokenType(Enum):
    """Enumeration for different types of tokens in arithmetic expressions."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Represents a token in an arithmetic expression."""
    
    def __init__(self, token_type: TokenType, value: Union[float, str]):
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
    A calculator class for evaluating arithmetic expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper precedence
    and parentheses. Uses the Shunting Yard algorithm for parsing and
    evaluation without using eval().
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    # Valid operators
    OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for new calculation."""
        self._tokens: List[Token] = []
        self._output_queue: List[Token] = []
        self._operator_stack: List[Token] = []
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression: A string containing the arithmetic expression
            
        Returns:
            The result of the arithmetic expression as a float
            
        Raises:
            ValueError: If the expression is invalid or contains unsupported characters
            ZeroDivisionError: If division by zero is attempted
            
        Example:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        self._reset_state()
        
        # Step 1: Tokenize the expression
        self._tokenize(expression.strip())
        
        # Step 2: Validate tokens
        self._validate_tokens()
        
        # Step 3: Convert to postfix notation using Shunting Yard algorithm
        self._convert_to_postfix()
        
        # Step 4: Evaluate postfix expression
        result = self._evaluate_postfix()
        
        return result
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression: The expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Remove all whitespace
        expression = re.sub(r'\s+', '', expression)
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (integer or float)
                number_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                
                try:
                    number_value = float(number_str)
                    self._tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                continue
            
            elif char in self.OPERATORS:
                # Handle unary minus
                if char == '-' and self._is_unary_position():
                    # Parse negative number
                    i += 1
                    if i >= len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                        raise ValueError("Invalid unary minus usage")
                    
                    number_str = '-'
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        number_str += expression[i]
                        i += 1
                    
                    try:
                        number_value = float(number_str)
                        self._tokens.append(Token(TokenType.NUMBER, number_value))
                    except ValueError:
                        raise ValueError(f"Invalid number format: {number_str}")
                    continue
                else:
                    self._tokens.append(Token(TokenType.OPERATOR, char))
            
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char))
            
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char))
            
            else:
                raise ValueError(f"Invalid character in expression: {char}")
            
            i += 1
    
    def _is_unary_position(self) -> bool:
        """
        Check if the current position allows for a unary minus operator.
        
        Returns:
            True if unary minus is allowed at this position
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return (last_token.type == TokenType.LEFT_PAREN or 
                last_token.type == TokenType.OPERATOR)
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for common errors.
        
        Raises:
            ValueError: If the expression is invalid
        """
        if not self._tokens:
            raise ValueError("No valid tokens found in expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count > 0:
            raise ValueError("Unbalanced parentheses: too many opening parentheses")
        
        # Check for consecutive operators or invalid operator placement
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Check if operator is at the end
                if i == len(self._tokens) - 1:
                    raise ValueError("Expression cannot end with an operator")
                
                # Check for consecutive operators (except unary minus which is handled in tokenization)
                if i > 0:
                    prev_token = self._tokens[i - 1]
                    if prev_token.type == TokenType.OPERATOR:
                        raise ValueError("Consecutive operators are not allowed")
                    elif prev_token.type == TokenType.LEFT_PAREN and token.value != '-':
                        raise ValueError("Invalid operator placement after opening parenthesis")
        
        # Expression cannot start with binary operator (except minus which becomes unary)
        first_token = self._tokens[0]
        if first_token.type == TokenType.OPERATOR and first_token.value in {'+', '*', '/'}:
            raise ValueError(f"Expression cannot start with operator: {first_token.value}")
    
    def _convert_to_postfix(self) -> None:
        """
        Convert infix notation to postfix notation using the Shunting Yard algorithm.
        """
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                self._output_queue.append(token)
            
            elif token.type == TokenType.OPERATOR:
                while (self._operator_stack and 
                       self._operator_stack[-1].type == TokenType.OPERATOR and
                       self.PRECEDENCE[self._operator_stack[-1].value] >= self.PRECEDENCE[token.value]):
                    self._output_queue.append(self._operator_stack.pop())
                self._operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                self._operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (self._operator_stack and 
                       self._operator_stack[-1].type != TokenType.LEFT_PAREN):
                    self._output_queue.append(self._operator_stack.pop())
                
                if not self._operator_stack:
                    raise ValueError("Mismatched parentheses")
                
                # Remove the left parenthesis
                self._operator_stack.pop()
        
        # Pop remaining operators
        while self._operator_stack:
            if self._operator_stack[-1].type == TokenType.LEFT_PAREN:
                raise ValueError("Mismatched parentheses")
            self._output_queue.append(self._operator_stack.pop())
    
    def _evaluate_postfix(self) -> float:
        """
        Evaluate the postfix expression and return the result.
        
        Returns:
            The result of the evaluation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack: List[float] = []
        
        for token in self._output_queue:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(token.value, left_operand, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: invalid number of operands")
        
        return stack[0]
    
    def _perform_operation(self, operator: str, left: float, right: float) -> float:
        """
        Perform the specified arithmetic operation.
        
        Args:
            operator: The operator to apply
            left: Left operand
            right: Right operand
            
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
    print("Supports parentheses and negative numbers")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()


calc = Calculator()
print(calc.calculate("2 + 3 * 4"))        # Output: 14.0
print(calc.calculate("(2 + 3) * 4"))      # Output: 20.0
print(calc.calculate("-5 + 10"))          # Output: 5.0
print(calc.calculate("10 / (2 + 3)"))     # Output: 2.0
