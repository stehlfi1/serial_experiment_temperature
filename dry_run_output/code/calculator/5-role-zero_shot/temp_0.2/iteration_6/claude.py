
"""
Console-based Arithmetic Calculator

A high-quality, maintainable calculator implementation that supports basic arithmetic
operations with proper error handling and validation according to ISO/IEC 25010 standards.
"""

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
    A console-based arithmetic calculator that supports basic operations
    with proper operator precedence and parentheses handling.
    
    Supports: addition (+), subtraction (-), multiplication (*), division (/)
    Features: parentheses, operator precedence, integer and floating-point numbers
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
            ValueError: For invalid expressions, unbalanced parentheses, or invalid characters
            ZeroDivisionError: For division by zero
            
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
        
        # Tokenize the expression
        self._tokenize(expression)
        
        # Validate tokens
        self._validate_tokens()
        
        # Parse and evaluate using recursive descent parser
        self._position = 0
        result = self._parse_expression()
        
        # Ensure all tokens were consumed
        if self._position < len(self._tokens):
            raise ValueError("Invalid expression: unexpected tokens at end")
        
        return float(result)
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert the input expression into tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            ValueError: For invalid characters in the expression
        """
        # Remove whitespace and validate characters
        cleaned_expr = re.sub(r'\s+', '', expression)
        
        # Check for invalid characters
        valid_chars = set('0123456789+-*/.()e')
        if not all(char in valid_chars for char in cleaned_expr):
            invalid_chars = set(cleaned_expr) - valid_chars
            raise ValueError(f"Invalid characters in expression: {invalid_chars}")
        
        i = 0
        while i < len(cleaned_expr):
            char = cleaned_expr[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including floating point and scientific notation)
                number_str, i = self._parse_number(cleaned_expr, i)
                try:
                    number_value = float(number_str)
                    self._tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
            
            elif char in self.VALID_OPERATORS:
                # Handle unary minus
                if char == '-' and self._is_unary_minus():
                    # Parse negative number
                    if i + 1 < len(cleaned_expr) and (cleaned_expr[i + 1].isdigit() or cleaned_expr[i + 1] == '.'):
                        number_str, i = self._parse_number(cleaned_expr, i)
                        try:
                            number_value = float(number_str)
                            self._tokens.append(Token(TokenType.NUMBER, number_value))
                        except ValueError:
                            raise ValueError(f"Invalid number format: {number_str}")
                    else:
                        # Unary minus before parentheses or another expression
                        self._tokens.append(Token(TokenType.NUMBER, 0))
                        self._tokens.append(Token(TokenType.OPERATOR, '-'))
                        i += 1
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
                raise ValueError(f"Unexpected character: {char}")
    
    def _parse_number(self, expression: str, start_pos: int) -> tuple[str, int]:
        """
        Parse a number from the expression starting at the given position.
        
        Args:
            expression: The expression string
            start_pos: Starting position for parsing
            
        Returns:
            Tuple of (number_string, next_position)
        """
        i = start_pos
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Parse digits and decimal point
        has_decimal = False
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                number_str += char
                i += 1
            elif char.lower() == 'e' and len(number_str) > 0:
                # Scientific notation
                number_str += char
                i += 1
                if i < len(expression) and expression[i] in '+-':
                    number_str += expression[i]
                    i += 1
            else:
                break
        
        return number_str, i
    
    def _is_unary_minus(self) -> bool:
        """
        Determine if the current minus sign is unary (negative) or binary (subtraction).
        
        Returns:
            True if the minus is unary, False if binary
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for structural correctness.
        
        Raises:
            ValueError: For unbalanced parentheses or invalid token sequences
        """
        if not self._tokens:
            raise ValueError("Empty expression")
        
        # Check balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count > 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
        
        # Validate token sequence
        self._validate_token_sequence()
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that tokens appear in a valid sequence.
        
        Raises:
            ValueError: For invalid token sequences
        """
        if not self._tokens:
            return
        
        # First token should be number or left parenthesis
        first_token = self._tokens[0]
        if first_token.type not in (TokenType.NUMBER, TokenType.LEFT_PAREN):
            raise ValueError("Expression must start with a number or opening parenthesis")
        
        # Last token should be number or right parenthesis
        last_token = self._tokens[-1]
        if last_token.type not in (TokenType.NUMBER, TokenType.RIGHT_PAREN):
            raise ValueError("Expression must end with a number or closing parenthesis")
        
        # Check consecutive tokens
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if current.type == TokenType.OPERATOR:
                if next_token.type not in (TokenType.NUMBER, TokenType.LEFT_PAREN):
                    raise ValueError("Operator must be followed by number or opening parenthesis")
            
            elif current.type == TokenType.NUMBER:
                if next_token.type not in (TokenType.OPERATOR, TokenType.RIGHT_PAREN):
                    raise ValueError("Number must be followed by operator or closing parenthesis")
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate an expression using recursive descent parsing.
        
        Returns:
            The evaluated result
        """
        return self._parse_addition_subtraction()
    
    def _parse_addition_subtraction(self) -> float:
        """
        Parse addition and subtraction operations (lowest precedence).
        
        Returns:
            The evaluated result
        """
        result = self._parse_multiplication_division()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['+', '-']):
            
            operator = self._tokens[self._position].value
            self._position += 1
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
            The evaluated result
            
        Raises:
            ZeroDivisionError: For division by zero
        """
        result = self._parse_factor()
        
        while (self._position < len(self._tokens) and 
               self._tokens[self._position].type == TokenType.OPERATOR and
               self._tokens[self._position].value in ['*', '/']):
            
            operator = self._tokens[self._position].value
            self._position += 1
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
            The evaluated result
            
        Raises:
            ValueError: For unexpected tokens
        """
        if self._position >= len(self._tokens):
            raise ValueError("Unexpected end of expression")
        
        token = self._tokens[self._position]
        
        if token.type == TokenType.NUMBER:
            self._position += 1
            return token.value
        
        elif token.type == TokenType.LEFT_PAREN:
            self._position += 1  # consume '('
            result = self._parse_expression()
            
            if (self._position >= len(self._tokens) or 
                self._tokens[self._position].type != TokenType.RIGHT_PAREN):
                raise ValueError("Missing closing parenthesis")
            
            self._position += 1  # consume ')'
            return result
        
        else:
            raise ValueError(f"Unexpected token: {token}")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and floating-point numbers")
    print("Type 'quit' or 'exit' to stop\n")
    
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
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()


calc = Calculator()
print(calc.calculate("2 + 3 * 4"))        # 14.0
print(calc.calculate("(2 + 3) * 4"))      # 20.0
print(calc.calculate("-5 + 3.14"))        # -1.86
print(calc.calculate("10 / (2 + 3)"))     # 2.0
