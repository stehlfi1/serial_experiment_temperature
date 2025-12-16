
"""
High-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

This module provides a Calculator class that can evaluate mathematical expressions
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
    """Represents a token in a mathematical expression."""
    
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
    parentheses, and both integer and floating-point numbers including negative values.
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
            >>> calc.calculate("(10 - 5) * 2")
            10.0
            >>> calc.calculate("-3.5 + 2.1")
            -1.4
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
            postfix_tokens = self._to_postfix()
            
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
            expression: The mathematical expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Regular expression to match numbers (including negative), operators, and parentheses
        pattern = r'(-?\d+\.?\d*|\+|\-|\*|\/|\(|\))'
        
        # Remove all whitespace
        clean_expression = re.sub(r'\s+', '', expression)
        
        # Find all tokens
        matches = re.finditer(pattern, clean_expression)
        position = 0
        
        for match in matches:
            token_value = match.group(1)
            token_start = match.start()
            
            # Check for gaps in matching (invalid characters)
            if token_start > position:
                invalid_char = clean_expression[position:token_start]
                raise ValueError(f"Invalid character(s) '{invalid_char}' at position {position}")
            
            # Determine token type and create token
            if token_value == '(':
                token = Token(TokenType.LEFT_PAREN, token_value, token_start)
            elif token_value == ')':
                token = Token(TokenType.RIGHT_PAREN, token_value, token_start)
            elif token_value in self.VALID_OPERATORS:
                token = Token(TokenType.OPERATOR, token_value, token_start)
            else:
                # Must be a number
                try:
                    float(token_value)  # Validate it's a valid number
                    token = Token(TokenType.NUMBER, token_value, token_start)
                except ValueError:
                    raise ValueError(f"Invalid number '{token_value}' at position {token_start}")
            
            self._tokens.append(token)
            position = match.end()
        
        # Check if entire expression was matched
        if position < len(clean_expression):
            invalid_char = clean_expression[position:]
            raise ValueError(f"Invalid character(s) '{invalid_char}' at position {position}")
        
        # Handle negative numbers vs subtraction operator
        self._process_negative_numbers()
    
    def _process_negative_numbers(self) -> None:
        """
        Process tokens to distinguish between negative numbers and subtraction operators.
        
        A minus sign is part of a negative number if it appears:
        - At the beginning of the expression
        - After an opening parenthesis
        - After another operator
        """
        processed_tokens = []
        
        for i, token in enumerate(self._tokens):
            if (token.type == TokenType.OPERATOR and token.value == '-' and
                self._is_negative_sign_context(i)):
                
                # This is a negative sign, combine with next number
                if i + 1 < len(self._tokens) and self._tokens[i + 1].type == TokenType.NUMBER:
                    next_token = self._tokens[i + 1]
                    # Create a new negative number token
                    negative_value = '-' + next_token.value
                    negative_token = Token(TokenType.NUMBER, negative_value, token.position)
                    processed_tokens.append(negative_token)
                    # Skip the next token as it's now part of the negative number
                    self._tokens[i + 1] = None
                else:
                    raise ValueError(f"Invalid negative sign at position {token.position}")
            elif token is not None:
                processed_tokens.append(token)
        
        self._tokens = processed_tokens
    
    def _is_negative_sign_context(self, index: int) -> bool:
        """
        Determine if a minus sign at the given index should be treated as a negative sign.
        
        Args:
            index: Index of the minus token
            
        Returns:
            True if it should be treated as a negative sign, False otherwise
        """
        if index == 0:
            return True
        
        prev_token = self._tokens[index - 1]
        return (prev_token.type == TokenType.LEFT_PAREN or
                prev_token.type == TokenType.OPERATOR)
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for structural correctness.
        
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
        
        # First token must be a number or opening parenthesis
        first_token = self._tokens[0]
        if first_token.type not in (TokenType.NUMBER, TokenType.LEFT_PAREN):
            raise ValueError(f"Expression cannot start with '{first_token.value}'")
        
        # Last token must be a number or closing parenthesis
        last_token = self._tokens[-1]
        if last_token.type not in (TokenType.NUMBER, TokenType.RIGHT_PAREN):
            raise ValueError(f"Expression cannot end with '{last_token.value}'")
        
        # Validate adjacent token pairs
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if not self._is_valid_token_pair(current, next_token):
                raise ValueError(
                    f"Invalid token sequence: '{current.value}' followed by '{next_token.value}' "
                    f"at position {next_token.position}"
                )
    
    def _is_valid_token_pair(self, current: Token, next_token: Token) -> bool:
        """
        Check if two adjacent tokens form a valid sequence.
        
        Args:
            current: The current token
            next_token: The next token
            
        Returns:
            True if the pair is valid, False otherwise
        """
        valid_pairs = {
            TokenType.NUMBER: {TokenType.OPERATOR, TokenType.RIGHT_PAREN},
            TokenType.OPERATOR: {TokenType.NUMBER, TokenType.LEFT_PAREN},
            TokenType.LEFT_PAREN: {TokenType.NUMBER, TokenType.LEFT_PAREN},
            TokenType.RIGHT_PAREN: {TokenType.OPERATOR, TokenType.RIGHT_PAREN}
        }
        
        return next_token.type in valid_pairs.get(current.type, set())
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using the Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix order
        """
        output_queue = []
        operator_stack = []
        
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
            elif token.type == TokenType.OPERATOR:
                # Pop operators with higher or equal precedence
                while (operator_stack and
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.OPERATOR_PRECEDENCE[operator_stack[-1].value] >= 
                       self.OPERATOR_PRECEDENCE[token.value]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            elif token.type == TokenType.RIGHT_PAREN:
                # Pop until we find the matching left parenthesis
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                # Remove the left parenthesis
                if operator_stack:
                    operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> Union[int, float]:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix order
            
        Returns:
            The calculated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                # Convert to appropriate numeric type
                value = float(token.value)
                if value.is_integer():
                    value = int(value)
                stack.append(value)
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError(f"Insufficient operands for operator '{token.value}'")
                
                # Pop two operands (note the order)
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                # Perform the operation
                result = self._perform_operation(left_operand, right_operand, token.value)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression")
        
        return stack[0]
    
    def _perform_operation(self, left: Union[int, float], right: Union[int, float], 
                          operator: str) -> Union[int, float]:
        """
        Perform a binary arithmetic operation.
        
        Args:
            left: Left operand
            right: Right operand
            operator: The operator to apply
            
        Returns:
            The result of the operation
            
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
                raise ZeroDivisionError("Division by zero")
            result = left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")
        
        # Return integer if result is a whole number
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result


def main():
    """
    Main function to demonstrate the calculator with interactive console interface.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
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
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
