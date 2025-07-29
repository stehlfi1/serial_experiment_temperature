
"""
Arithmetic Calculator Module

A console-based calculator that supports basic arithmetic operations
with proper operator precedence and parentheses handling.
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
    A calculator class that evaluates arithmetic expressions using the Shunting Yard algorithm.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence
    and parentheses handling.
    """
    
    # Operator precedence mapping (higher value = higher precedence)
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
        self._tokens: List[Token] = []
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            float: The result of the calculation
            
        Raises:
            ValueError: If the expression is invalid
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        # Clean and validate the expression
        cleaned_expression = self._clean_expression(expression)
        
        # Tokenize the expression
        self._tokens = self._tokenize(cleaned_expression)
        
        # Validate tokens
        self._validate_tokens()
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._to_postfix()
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(postfix_tokens)
    
    def _clean_expression(self, expression: str) -> str:
        """
        Clean the expression by removing whitespace and validating characters.
        
        Args:
            expression: Raw input expression
            
        Returns:
            str: Cleaned expression
            
        Raises:
            ValueError: If expression contains invalid characters
        """
        # Remove all whitespace
        cleaned = re.sub(r'\s+', '', expression)
        
        # Check for invalid characters
        valid_chars = set('0123456789+-*/.()e')
        if not all(c in valid_chars for c in cleaned):
            invalid_chars = set(cleaned) - valid_chars
            raise ValueError(f"Invalid characters in expression: {invalid_chars}")
        
        return cleaned
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression: Cleaned expression string
            
        Returns:
            List[Token]: List of tokens representing the expression
            
        Raises:
            ValueError: If tokenization fails
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals and scientific notation)
                number_str, i = self._parse_number(expression, i)
                try:
                    number_value = float(number_str)
                    tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                    
            elif char in self.VALID_OPERATORS:
                # Handle unary minus
                if char == '-' and (not tokens or 
                                   tokens[-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    # This is a unary minus, parse the following number
                    if i + 1 >= len(expression):
                        raise ValueError("Invalid expression: operator at end")
                    
                    number_str, i = self._parse_number(expression, i + 1)
                    try:
                        number_value = -float(number_str)
                        tokens.append(Token(TokenType.NUMBER, number_value))
                    except ValueError:
                        raise ValueError(f"Invalid number format: -{number_str}")
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
                raise ValueError(f"Unexpected character: {char}")
        
        return tokens
    
    def _parse_number(self, expression: str, start_index: int) -> tuple[str, int]:
        """
        Parse a number from the expression starting at the given index.
        
        Args:
            expression: The expression string
            start_index: Starting index for parsing
            
        Returns:
            tuple: (number_string, next_index)
        """
        i = start_index
        number_str = ""
        decimal_count = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit():
                number_str += char
            elif char == '.' and decimal_count == 0:
                number_str += char
                decimal_count += 1
            elif char in 'eE' and number_str and number_str[-1].isdigit():
                # Handle scientific notation
                number_str += char
                i += 1
                if i < len(expression) and expression[i] in '+-':
                    number_str += expression[i]
                    i += 1
            else:
                break
            i += 1
        
        if not number_str or number_str in ['.', 'e', 'E']:
            raise ValueError(f"Invalid number at position {start_index}")
        
        return number_str, i
    
    def _validate_tokens(self) -> None:
        """
        Validate the token sequence for correctness.
        
        Raises:
            ValueError: If tokens form an invalid expression
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
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
        
        # Check for valid token sequences
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus, handled in tokenization)
                if i == 0 or i == len(self._tokens) - 1:
                    raise ValueError("Invalid operator position")
                
                # Operators cannot follow other operators or left parentheses
                prev_token = self._tokens[i - 1]
                if prev_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]:
                    raise ValueError("Invalid operator sequence")
                
                # Operators cannot be followed by right parentheses
                next_token = self._tokens[i + 1]
                if next_token.type == TokenType.RIGHT_PAREN:
                    raise ValueError("Invalid operator followed by closing parenthesis")
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix notation to postfix notation using the Shunting Yard algorithm.
        
        Returns:
            List[Token]: Tokens in postfix notation
        """
        output_queue = []
        operator_stack = []
        
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
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                
                # Remove the left parenthesis
                operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            float: Result of the evaluation
            
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
                
                result = self._perform_operation(left_operand, right_operand, token.value)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: incorrect number of operands")
        
        return stack[0]
    
    def _perform_operation(self, left: float, right: float, operator: str) -> float:
        """
        Perform a binary arithmetic operation.
        
        Args:
            left: Left operand
            right: Right operand
            operator: Operator string
            
        Returns:
            float: Result of the operation
            
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
                raise ZeroDivisionError("Division by zero")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")


def main():
    """Main function to run the calculator interactively."""
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and decimal numbers")
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
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
