
"""
Arithmetic Calculator Module

A robust console-based calculator implementing basic arithmetic operations
with proper error handling and validation according to ISO/IEC 25010 standards.
"""

import re
from typing import List, Union, Tuple
from enum import Enum


class TokenType(Enum):
    """Enumeration for different types of tokens in mathematical expressions."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PARENTHESIS = "LEFT_PARENTHESIS"
    RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"


class Token:
    """Represents a token in a mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: str, position: int = 0):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The string value of the token
            position: Position in the original expression
        """
        self.type = token_type
        self.value = value
        self.position = position
    
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
    A mathematical expression calculator supporting basic arithmetic operations.
    
    Supports addition (+), subtraction (-), multiplication (*), division (/),
    and parentheses with proper operator precedence.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    # Valid operators
    OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for a new calculation."""
        self._tokens: List[Token] = []
        self._current_position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            The result of the calculation as a float
            
        Raises:
            InvalidExpressionError: If the expression is syntactically invalid
            DivisionByZeroError: If division by zero is attempted
            CalculatorError: For other calculation errors
        """
        if not isinstance(expression, str):
            raise InvalidExpressionError("Expression must be a string")
        
        if not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        try:
            self._reset_state()
            self._tokens = self._tokenize(expression)
            self._validate_tokens()
            postfix_tokens = self._convert_to_postfix()
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (InvalidExpressionError, DivisionByZeroError):
            raise
        except Exception as e:
            raise CalculatorError(f"Unexpected error during calculation: {str(e)}")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List of tokens representing the expression
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        tokens = []
        i = 0
        expression = expression.replace(' ', '')  # Remove whitespace
        
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including decimals and negative numbers)
            if char.isdigit() or char == '.':
                number_str, i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
            
            # Handle operators
            elif char in self.OPERATORS:
                # Handle unary minus
                if (char == '-' and 
                    (not tokens or 
                     tokens[-1].type in [TokenType.OPERATOR, TokenType.LEFT_PARENTHESIS])):
                    # This is a unary minus, treat as part of the next number
                    if i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        number_str, i = self._extract_number(expression, i)
                        tokens.append(Token(TokenType.NUMBER, number_str, i))
                    else:
                        tokens.append(Token(TokenType.NUMBER, "0", i))
                        tokens.append(Token(TokenType.OPERATOR, char, i))
                        i += 1
                else:
                    tokens.append(Token(TokenType.OPERATOR, char, i))
                    i += 1
            
            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PARENTHESIS, char, i))
                i += 1
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PARENTHESIS, char, i))
                i += 1
            
            # Invalid character
            else:
                raise InvalidExpressionError(f"Invalid character '{char}' at position {i}")
        
        return tokens
    
    def _extract_number(self, expression: str, start_pos: int) -> Tuple[str, int]:
        """
        Extract a complete number from the expression starting at given position.
        
        Args:
            expression: The expression string
            start_pos: Starting position in the expression
            
        Returns:
            Tuple of (number_string, next_position)
            
        Raises:
            InvalidExpressionError: If the number format is invalid
        """
        i = start_pos
        number_str = ""
        decimal_count = 0
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Extract digits and decimal point
        while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
            if expression[i] == '.':
                decimal_count += 1
                if decimal_count > 1:
                    raise InvalidExpressionError(f"Invalid number format at position {start_pos}")
            number_str += expression[i]
            i += 1
        
        # Validate number format
        if number_str in ['-', '.', '-.'] or number_str == '':
            raise InvalidExpressionError(f"Invalid number format at position {start_pos}")
        
        return number_str, i
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for syntax errors.
        
        Raises:
            InvalidExpressionError: If syntax errors are found
        """
        if not self._tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PARENTHESIS:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PARENTHESIS:
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count > 0:
            raise InvalidExpressionError("Unbalanced parentheses: missing closing parentheses")
        
        # Check for valid token sequences
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus handled in tokenization)
                if i == len(self._tokens) - 1:
                    raise InvalidExpressionError("Expression cannot end with an operator")
                
                # Check for consecutive operators
                if (i > 0 and 
                    self._tokens[i - 1].type == TokenType.OPERATOR):
                    raise InvalidExpressionError("Consecutive operators are not allowed")
            
            elif token.type == TokenType.RIGHT_PARENTHESIS:
                # Right parenthesis cannot follow left parenthesis or operator
                if (i > 0 and 
                    self._tokens[i - 1].type in [TokenType.LEFT_PARENTHESIS, TokenType.OPERATOR]):
                    raise InvalidExpressionError("Empty parentheses or operator before closing parenthesis")
    
    def _convert_to_postfix(self) -> List[Token]:
        """
        Convert infix tokens to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix notation
        """
        output_queue = []
        operator_stack = []
        
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
            
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.PRECEDENCE[operator_stack[-1].value] >= self.PRECEDENCE[token.value]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PARENTHESIS:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PARENTHESIS:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PARENTHESIS):
                    output_queue.append(operator_stack.pop())
                
                if operator_stack:
                    operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate postfix expression tokens.
        
        Args:
            postfix_tokens: List of tokens in postfix notation
            
        Returns:
            The result of the evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                try:
                    stack.append(float(token.value))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number: {token.value}")
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operator")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                result = self._apply_operator(token.value, operand1, operand2)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: incorrect number of operands")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, operand1: float, operand2: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            operand1: The first operand
            operand2: The second operand
            
        Returns:
            The result of the operation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
        """
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise DivisionByZeroError("Division by zero is not allowed")
            return operand1 / operand2
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")


def main():
    """
    Main function to run the calculator in console mode.
    Provides a simple REPL interface for user interaction.
    """
    calculator = Calculator()
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
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
            
        except (InvalidExpressionError, DivisionByZeroError, CalculatorError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


calc = Calculator()
print(calc.calculate("2 + 3 * 4"))        # 14.0
print(calc.calculate("(2 + 3) * 4"))      # 20.0
print(calc.calculate("-5 + 3"))           # -2.0
print(calc.calculate("10 / (2 + 3)"))     # 2.0
