
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
    """Represents a single token in a mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: str):
        """
        Initialize a token.
        
        Args:
            token_type (TokenType): The type of the token
            value (str): The string value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid syntax or characters."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence,
    parentheses, and both integer and floating-point numbers.
    """
    
    # Operator precedence mapping (higher value = higher precedence)
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for a new calculation."""
        self._tokens = []
        self._position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: The calculated result
            
        Raises:
            InvalidExpressionError: If the expression is invalid
            DivisionByZeroError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) * 2")
            10.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        self._reset_state()
        
        try:
            # Tokenize the expression
            self._tokens = self._tokenize(expression.strip())
            
            # Validate tokens
            self._validate_tokens()
            
            # Parse and evaluate using recursive descent parser
            self._position = 0
            result = self._parse_expression()
            
            # Ensure all tokens were consumed
            if self._position < len(self._tokens):
                raise InvalidExpressionError("Unexpected tokens at end of expression")
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert the input expression into a list of tokens.
        
        Args:
            expression (str): The mathematical expression to tokenize
            
        Returns:
            List[Token]: List of tokens representing the expression
            
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
            
            # Handle numbers (including negative numbers and decimals)
            if char.isdigit() or char == '.':
                number_str = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str))
                i += len(number_str)
            
            # Handle negative numbers at the beginning or after operators/left parenthesis
            elif char == '-' and self._is_unary_minus(tokens):
                number_str = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str))
                i += len(number_str)
            
            # Handle operators
            elif char in self.OPERATOR_PRECEDENCE:
                tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
            
            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
            
            # Invalid character
            else:
                raise InvalidExpressionError(f"Invalid character: '{char}'")
        
        return tokens
    
    def _extract_number(self, expression: str, start_pos: int) -> str:
        """
        Extract a complete number (including decimals and negative sign) from the expression.
        
        Args:
            expression (str): The full expression
            start_pos (int): Starting position of the number
            
        Returns:
            str: The complete number as a string
        """
        i = start_pos
        has_decimal = False
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            i += 1
        
        # Extract digits and decimal point
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                i += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                i += 1
            else:
                break
        
        number_str = expression[start_pos:i]
        
        # Validate the extracted number
        try:
            float(number_str)
        except ValueError:
            raise InvalidExpressionError(f"Invalid number format: '{number_str}'")
        
        return number_str
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign should be treated as unary (negative number).
        
        Args:
            tokens (List[Token]): Current list of tokens
            
        Returns:
            bool: True if the minus should be treated as unary
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self) -> None:
        """
        Validate the token sequence for common syntax errors.
        
        Raises:
            InvalidExpressionError: If validation fails
        """
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count > 0:
            raise InvalidExpressionError("Unbalanced parentheses: missing closing parentheses")
        
        # Check for invalid token sequences
        for i in range(len(self._tokens)):
            current = self._tokens[i]
            
            # First token validation
            if i == 0:
                if current.type == TokenType.OPERATOR:
                    raise InvalidExpressionError("Expression cannot start with an operator")
                elif current.type == TokenType.RIGHT_PAREN:
                    raise InvalidExpressionError("Expression cannot start with a closing parenthesis")
            
            # Last token validation
            elif i == len(self._tokens) - 1:
                if current.type == TokenType.OPERATOR:
                    raise InvalidExpressionError("Expression cannot end with an operator")
                elif current.type == TokenType.LEFT_PAREN:
                    raise InvalidExpressionError("Expression cannot end with an opening parenthesis")
            
            # Adjacent token validation
            if i > 0:
                previous = self._tokens[i - 1]
                
                # Two consecutive operators
                if (current.type == TokenType.OPERATOR and 
                    previous.type == TokenType.OPERATOR):
                    raise InvalidExpressionError("Cannot have consecutive operators")
                
                # Two consecutive numbers
                if (current.type == TokenType.NUMBER and 
                    previous.type == TokenType.NUMBER):
                    raise InvalidExpressionError("Cannot have consecutive numbers")
                
                # Operator after left parenthesis (except for handled unary minus)
                if (current.type == TokenType.OPERATOR and 
                    previous.type == TokenType.LEFT_PAREN):
                    raise InvalidExpressionError("Invalid operator after opening parenthesis")
                
                # Number before left parenthesis without operator
                if (current.type == TokenType.LEFT_PAREN and 
                    previous.type == TokenType.NUMBER):
                    raise InvalidExpressionError("Missing operator before opening parenthesis")
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate the expression using recursive descent parsing.
        
        Returns:
            float: The result of the expression
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """
        Parse addition and subtraction operations (lowest precedence).
        
        Returns:
            float: The result of the addition/subtraction operations
        """
        left = self._parse_multiplication_division()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['+', '-']):
            
            operator = self._tokens[self._position].value
            self._position += 1
            right = self._parse_multiplication_division()
            
            if operator == '+':
                left = left + right
            else:  # operator == '-'
                left = left - right
        
        return left
    
    def _parse_multiplication_division(self) -> float:
        """
        Parse multiplication and division operations (higher precedence).
        
        Returns:
            float: The result of the multiplication/division operations
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
        """
        left = self._parse_factor()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['*', '/']):
            
            operator = self._tokens[self._position].value
            self._position += 1
            right = self._parse_factor()
            
            if operator == '*':
                left = left * right
            else:  # operator == '/'
                if right == 0:
                    raise DivisionByZeroError("Division by zero is not allowed")
                left = left / right
        
        return left
    
    def _parse_factor(self) -> float:
        """
        Parse factors (numbers and parenthesized expressions).
        
        Returns:
            float: The value of the factor
            
        Raises:
            InvalidExpressionError: If the factor is invalid
        """
        if self._position >= len(self._tokens):
            raise InvalidExpressionError("Unexpected end of expression")
        
        token = self._tokens[self._position]
        
        if token.type == TokenType.NUMBER:
            self._position += 1
            return float(token.value)
        
        elif token.type == TokenType.LEFT_PAREN:
            self._position += 1  # consume '('
            result = self._parse_expression()
            
            # Expect closing parenthesis
            if (self._position >= len(self._tokens) or 
                self._tokens[self._position].type != TokenType.RIGHT_PAREN):
                raise InvalidExpressionError("Missing closing parenthesis")
            
            self._position += 1  # consume ')'
            return result
        
        else:
            raise InvalidExpressionError(f"Unexpected token: {token.value}")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    print("Console Arithmetic Calculator")
    print("Supports: +, -, *, /, parentheses ()")
    print("Enter 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
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
