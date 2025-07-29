
"""
Arithmetic Calculator Module

A robust console-based calculator that supports basic arithmetic operations
with proper operator precedence and parentheses handling.
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
    
    def __init__(self, token_type: TokenType, value: Union[str, float]):
        """
        Initialize a token.
        
        Args:
            token_type (TokenType): The type of the token
            value (Union[str, float]): The value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class Calculator:
    """
    A mathematical expression calculator that supports basic arithmetic operations.
    
    Supports:
    - Addition (+), Subtraction (-), Multiplication (*), Division (/)
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
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: The calculated result
            
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
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate tokens
            self._validate_tokens()
            
            # Convert to postfix notation and evaluate
            postfix = self._to_postfix()
            result = self._evaluate_postfix(postfix)
            
            return float(result)
            
        except (ValueError, ZeroDivisionError) as e:
            raise e
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert expression string into tokens.
        
        Args:
            expression (str): The expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Remove whitespace and validate characters
        clean_expr = re.sub(r'\s+', '', expression)
        
        # Check for invalid characters
        valid_chars = set('0123456789+-*/().') 
        if not all(c in valid_chars for c in clean_expr):
            invalid_chars = set(clean_expr) - valid_chars
            raise ValueError(f"Invalid characters found: {', '.join(invalid_chars)}")
        
        i = 0
        while i < len(clean_expr):
            char = clean_expr[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals)
                number_str = ''
                while i < len(clean_expr) and (clean_expr[i].isdigit() or clean_expr[i] == '.'):
                    number_str += clean_expr[i]
                    i += 1
                
                # Validate number format
                if number_str.count('.') > 1:
                    raise ValueError(f"Invalid number format: {number_str}")
                
                try:
                    value = float(number_str)
                    self._tokens.append(Token(TokenType.NUMBER, value))
                except ValueError:
                    raise ValueError(f"Invalid number: {number_str}")
                
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
                raise ValueError(f"Unexpected character: {char}")
    
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
        
        if paren_count > 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
        
        # Handle unary minus by converting to (0 - number)
        self._handle_unary_operators()
        
        # Validate token sequence
        self._validate_token_sequence()
    
    def _handle_unary_operators(self) -> None:
        """Convert unary minus operators to binary operations."""
        new_tokens = []
        
        for i, token in enumerate(self._tokens):
            if (token.type == TokenType.OPERATOR and token.value == '-' and
                (i == 0 or self._tokens[i-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])):
                # This is a unary minus
                new_tokens.extend([
                    Token(TokenType.NUMBER, 0),
                    Token(TokenType.OPERATOR, '-')
                ])
            else:
                new_tokens.append(token)
        
        self._tokens = new_tokens
    
    def _validate_token_sequence(self) -> None:
        """
        Validate that tokens form a proper mathematical expression.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            raise ValueError("Empty expression after processing")
        
        # First token must be number or left parenthesis
        if self._tokens[0].type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
            raise ValueError("Expression must start with a number or opening parenthesis")
        
        # Last token must be number or right parenthesis
        if self._tokens[-1].type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
            raise ValueError("Expression must end with a number or closing parenthesis")
        
        # Check token sequence validity
        for i in range(len(self._tokens) - 1):
            current = self._tokens[i]
            next_token = self._tokens[i + 1]
            
            if current.type == TokenType.NUMBER:
                if next_token.type not in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]:
                    raise ValueError("Number must be followed by operator or closing parenthesis")
            
            elif current.type == TokenType.OPERATOR:
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    raise ValueError("Operator must be followed by number or opening parenthesis")
            
            elif current.type == TokenType.LEFT_PAREN:
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    raise ValueError("Opening parenthesis must be followed by number or another opening parenthesis")
            
            elif current.type == TokenType.RIGHT_PAREN:
                if next_token.type not in [TokenType.OPERATOR, TokenType.RIGHT_PAREN]:
                    raise ValueError("Closing parenthesis must be followed by operator or another closing parenthesis")
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix notation to postfix using Shunting Yard algorithm.
        
        Returns:
            List[Token]: Tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
                
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.PRECEDENCE[operator_stack[-1].value] >= self.PRECEDENCE[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
                
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
                
            elif token.type == TokenType.RIGHT_PAREN:
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate postfix expression.
        
        Args:
            postfix_tokens (List[Token]): Tokens in postfix notation
            
        Returns:
            float: The calculated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
                
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                right = stack.pop()
                left = stack.pop()
                
                result = self._perform_operation(left, right, token.value)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression: invalid number of operands")
        
        return stack[0]
    
    def _perform_operation(self, left: float, right: float, operator: str) -> float:
        """
        Perform arithmetic operation.
        
        Args:
            left (float): Left operand
            right (float): Right operand  
            operator (str): Operator (+, -, *, /)
            
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
print(calc.calculate("-5 + 3"))           # -2.0
print(calc.calculate("10 / (2 + 3)"))     # 2.0
