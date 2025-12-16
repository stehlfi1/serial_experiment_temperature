
"""
High-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

This module provides a Calculator class that can evaluate arithmetic expressions
with proper operator precedence, parentheses support, and comprehensive error handling.
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
    """Represents a token in the arithmetic expression."""
    
    def __init__(self, token_type: TokenType, value: str, position: int):
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
        return f"Token({self.type}, {self.value}, {self.position})"


class Calculator:
    """
    A high-quality arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence,
    parentheses, and both integer and floating-point numbers.
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
        self._current_position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
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
            >>> calc.calculate("(10 - 5) * 2")
            10.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        self._reset_state()
        
        try:
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate tokens
            self._validate_tokens()
            
            # Convert to postfix notation using Shunting Yard algorithm
            postfix_tokens = self._convert_to_postfix()
            
            # Evaluate postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, ZeroDivisionError):
            raise
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression: The expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including negative numbers and decimals)
            if char.isdigit() or char == '.':
                number_str, new_i = self._extract_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
                continue
            
            # Handle negative numbers at the beginning or after operators/left parentheses
            if char == '-' and self._is_unary_minus_position():
                number_str, new_i = self._extract_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
                continue
            
            # Handle operators
            if char in self.VALID_OPERATORS:
                self._tokens.append(Token(TokenType.OPERATOR, char, i))
                i += 1
                continue
            
            # Handle parentheses
            if char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
                continue
            
            if char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
                continue
            
            # Invalid character
            raise ValueError(f"Invalid character '{char}' at position {i}")
    
    def _extract_number(self, expression: str, start_pos: int) -> tuple[str, int]:
        """
        Extract a complete number from the expression starting at the given position.
        
        Args:
            expression: The full expression
            start_pos: Starting position to extract from
            
        Returns:
            Tuple of (number_string, next_position)
            
        Raises:
            ValueError: If the number format is invalid
        """
        i = start_pos
        number_str = ""
        has_decimal = False
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Extract digits and decimal point
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                number_str += char
                i += 1
            else:
                break
        
        # Validate the extracted number
        if not number_str or number_str == '-' or number_str == '.':
            raise ValueError(f"Invalid number format at position {start_pos}")
        
        # Check for valid number format
        try:
            float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number format '{number_str}' at position {start_pos}")
        
        return number_str, i
    
    def _is_unary_minus_position(self) -> bool:
        """
        Check if the current position is valid for a unary minus operator.
        
        Returns:
            True if unary minus is valid at current position
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
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
                    raise ValueError(f"Unmatched closing parenthesis at position {token.position}")
        
        if paren_count > 0:
            raise ValueError("Unmatched opening parenthesis")
        
        # Validate token sequence
        self._validate_token_sequence()
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that the sequence of tokens follows proper mathematical syntax.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            return
        
        # First token must be number or left parenthesis
        first_token = self._tokens[0]
        if first_token.type not in (TokenType.NUMBER, TokenType.LEFT_PAREN):
            raise ValueError(f"Expression cannot start with {first_token.value}")
        
        # Last token must be number or right parenthesis
        last_token = self._tokens[-1]
        if last_token.type not in (TokenType.NUMBER, TokenType.RIGHT_PAREN):
            raise ValueError(f"Expression cannot end with {last_token.value}")
        
        # Check adjacent token validity
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if not self._are_adjacent_tokens_valid(current, next_token):
                raise ValueError(
                    f"Invalid token sequence: '{current.value}' followed by '{next_token.value}' "
                    f"at position {next_token.position}"
                )
    
    def _are_adjacent_tokens_valid(self, current: Token, next_token: Token) -> bool:
        """
        Check if two adjacent tokens form a valid sequence.
        
        Args:
            current: Current token
            next_token: Next token
            
        Returns:
            True if the sequence is valid
        """
        valid_sequences = {
            TokenType.NUMBER: {TokenType.OPERATOR, TokenType.RIGHT_PAREN},
            TokenType.OPERATOR: {TokenType.NUMBER, TokenType.LEFT_PAREN},
            TokenType.LEFT_PAREN: {TokenType.NUMBER, TokenType.LEFT_PAREN},
            TokenType.RIGHT_PAREN: {TokenType.OPERATOR, TokenType.RIGHT_PAREN}
        }
        
        return next_token.type in valid_sequences.get(current.type, set())
    
    def _convert_to_postfix(self) -> List[Token]:
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
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> Union[int, float]:
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
        stack: List[Union[int, float]] = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                # Convert to appropriate numeric type
                value = float(token.value)
                if value.is_integer():
                    value = int(value)
                stack.append(value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(
                    left_operand, token.value, right_operand, token.position
                )
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: incorrect number of operands")
        
        return stack[0]
    
    def _perform_operation(self, left: Union[int, float], operator: str, 
                          right: Union[int, float], position: int) -> Union[int, float]:
        """
        Perform a single arithmetic operation.
        
        Args:
            left: Left operand
            operator: Operator symbol
            right: Right operand
            position: Position in original expression (for error reporting)
            
        Returns:
            Result of the operation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        if operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        elif operator == '*':
            result = left * right
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError(f"Division by zero at position {position}")
            result = left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")
        
        # Return integer if result is a whole number
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result


def main():
    """
    Main function to demonstrate calculator usage.
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
