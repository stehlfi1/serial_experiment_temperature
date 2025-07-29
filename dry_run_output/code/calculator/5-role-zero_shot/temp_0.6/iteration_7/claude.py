
import re
from typing import List, Union
from enum import Enum


class TokenType(Enum):
    """Enumeration for different token types in mathematical expressions."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Represents a token in a mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: str, position: int):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The string value of the token
            position: The position in the original expression
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value}, {self.position})"


class CalculatorError(Exception):
    """Base exception class for calculator errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid syntax."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations
    with proper operator precedence and parentheses handling.
    
    Supports: +, -, *, / operations with integers and floating-point numbers.
    Uses the Shunting Yard algorithm for expression parsing and evaluation.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    # Valid operators
    OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression: A string containing a mathematical expression
            
        Returns:
            The calculated result as a float
            
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
            # Tokenize the expression
            tokens = self._tokenize(expression.strip())
            
            # Validate tokens
            self._validate_tokens(tokens)
            
            # Convert to postfix notation using Shunting Yard algorithm
            postfix_tokens = self._infix_to_postfix(tokens)
            
            # Evaluate the postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Tokenizes the input expression into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            A list of Token objects
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including decimals and negative numbers)
            if char.isdigit() or char == '.':
                number_str, new_i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
                continue
            
            # Handle negative numbers at the beginning or after operators/left parentheses
            if char == '-' and self._is_unary_minus(tokens):
                number_str, new_i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
                continue
            
            # Handle operators
            if char in self.OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, char, i))
                i += 1
                continue
            
            # Handle parentheses
            if char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
                continue
            
            if char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
                continue
            
            # Invalid character
            raise InvalidExpressionError(f"Invalid character '{char}' at position {i}")
        
        return tokens
    
    def _extract_number(self, expression: str, start: int) -> tuple[str, int]:
        """
        Extracts a number (including negative numbers and decimals) from the expression.
        
        Args:
            expression: The full expression
            start: Starting position
            
        Returns:
            A tuple of (number_string, next_position)
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
                decimal_found = True
                number_str += char
                i += 1
            else:
                break
        
        if not number_str or number_str == '-' or number_str == '.':
            raise InvalidExpressionError(f"Invalid number format at position {start}")
        
        return number_str, i
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determines if a minus sign should be treated as unary (negative number).
        
        Args:
            tokens: List of tokens processed so far
            
        Returns:
            True if the minus should be treated as unary, False otherwise
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validates the token sequence for correct syntax.
        
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
                    raise InvalidExpressionError(f"Unmatched closing parenthesis at position {token.position}")
        
        if paren_count > 0:
            raise InvalidExpressionError("Unmatched opening parenthesis")
        
        # Validate token sequence
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus which is handled in tokenization)
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError(f"Operator '{token.value}' at invalid position {token.position}")
                
                # Operators cannot be followed by other operators (except after parentheses)
                if i < len(tokens) - 1:
                    next_token = tokens[i + 1]
                    if next_token.type == TokenType.OPERATOR:
                        raise InvalidExpressionError(f"Consecutive operators at position {token.position}")
        
        # First and last tokens validation
        first_token = tokens[0]
        last_token = tokens[-1]
        
        if first_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
            raise InvalidExpressionError("Expression must start with a number or opening parenthesis")
        
        if last_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
            raise InvalidExpressionError("Expression must end with a number or closing parenthesis")
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Converts infix notation to postfix notation using the Shunting Yard algorithm.
        
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
                    raise InvalidExpressionError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise InvalidExpressionError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluates a postfix expression.
        
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
                try:
                    stack.append(float(token.value))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number: {token.value}")
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Invalid expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(left_operand, right_operand, token.value)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: malformed")
        
        return stack[0]
    
    def _perform_operation(self, left: float, right: float, operator: str) -> float:
        """
        Performs a mathematical operation on two operands.
        
        Args:
            left: Left operand
            right: Right operand
            operator: The operator to apply
            
        Returns:
            The result of the operation
            
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
    Main function to run the calculator in console mode.
    Provides a simple interactive interface for the calculator.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supports: +, -, *, / with parentheses")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("\nEnter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except CalculatorError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
