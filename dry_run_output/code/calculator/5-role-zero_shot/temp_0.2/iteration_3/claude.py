
"""
Console-based Arithmetic Calculator

A high-quality implementation of an arithmetic calculator that supports
basic operations (+, -, *, /) with parentheses and proper operator precedence.
Follows ISO/IEC 25010 quality standards.
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
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports:
    - Basic operations: +, -, *, /
    - Parentheses for grouping
    - Proper operator precedence
    - Integer and floating-point numbers (including negative values)
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
        self._position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: Mathematical expression as a string
            
        Returns:
            The calculated result as a float
            
        Raises:
            ValueError: If the expression is invalid
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
        
        self._reset_state()
        
        try:
            # Step 1: Tokenize the expression
            self._tokenize(expression)
            
            # Step 2: Validate tokens
            self._validate_tokens()
            
            # Step 3: Convert to postfix notation using Shunting Yard algorithm
            postfix = self._to_postfix()
            
            # Step 4: Evaluate postfix expression
            result = self._evaluate_postfix(postfix)
            
            return float(result)
            
        except (ValueError, ZeroDivisionError):
            raise
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert the expression string into tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Remove whitespace
        expression = re.sub(r'\s+', '', expression)
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals)
                number_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                
                # Validate number format
                if number_str.count('.') > 1:
                    raise ValueError(f"Invalid number format: {number_str}")
                
                try:
                    value = float(number_str)
                    self._tokens.append(Token(TokenType.NUMBER, value))
                except ValueError:
                    raise ValueError(f"Invalid number: {number_str}")
                
                continue
            
            elif char in self.OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
            
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
            
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
            
            else:
                raise ValueError(f"Invalid character: {char}")
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for correctness.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            raise ValueError("Empty expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses")
        
        # Validate token sequence
        self._validate_token_sequence()
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that tokens appear in a valid sequence.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        prev_token = None
        
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.NUMBER:
                # Numbers can't follow other numbers or right parentheses
                if prev_token and prev_token.type in (TokenType.NUMBER, TokenType.RIGHT_PAREN):
                    raise ValueError("Invalid token sequence: unexpected number")
            
            elif token.type == TokenType.OPERATOR:
                # Handle unary minus
                if token.value == '-' and (prev_token is None or 
                                         prev_token.type in (TokenType.OPERATOR, TokenType.LEFT_PAREN)):
                    # Convert unary minus to (0 - ...)
                    self._tokens.insert(i, Token(TokenType.NUMBER, 0))
                    continue
                
                # Operators must follow numbers or right parentheses
                if not prev_token or prev_token.type not in (TokenType.NUMBER, TokenType.RIGHT_PAREN):
                    raise ValueError("Invalid token sequence: unexpected operator")
            
            elif token.type == TokenType.LEFT_PAREN:
                # Left parentheses can't follow numbers or right parentheses
                if prev_token and prev_token.type in (TokenType.NUMBER, TokenType.RIGHT_PAREN):
                    raise ValueError("Invalid token sequence: unexpected left parenthesis")
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Right parentheses must follow numbers or other right parentheses
                if not prev_token or prev_token.type not in (TokenType.NUMBER, TokenType.RIGHT_PAREN):
                    raise ValueError("Invalid token sequence: unexpected right parenthesis")
            
            prev_token = token
        
        # Expression can't end with an operator or left parenthesis
        last_token = self._tokens[-1]
        if last_token.type in (TokenType.OPERATOR, TokenType.LEFT_PAREN):
            raise ValueError("Expression cannot end with operator or left parenthesis")
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix order
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
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in (TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN):
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens: List of tokens in postfix order
            
        Returns:
            The calculated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack: List[float] = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                result = self._apply_operator(token.value, operand1, operand2)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, operand1: float, operand2: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            operand1: First operand
            operand2: Second operand
            
        Returns:
            The result of the operation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise ZeroDivisionError("Division by zero")
            return operand1 / operand2
        else:
            raise ValueError(f"Unknown operator: {operator}")


def main():
    """
    Main function to run the calculator in console mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and negative numbers")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ('quit', 'exit'):
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}\n")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
