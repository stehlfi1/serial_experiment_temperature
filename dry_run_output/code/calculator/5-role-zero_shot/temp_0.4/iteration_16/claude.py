
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
            position: Position in the original expression
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
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence,
    parentheses, and both integer and floating-point numbers.
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
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
            The result of the expression as a float
            
        Raises:
            InvalidExpressionError: If the expression is malformed
            DivisionByZeroError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5.5 + 2.3")
            -3.2
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        # Remove whitespace
        expression = expression.replace(" ", "")
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Validate tokens
        self._validate_tokens(tokens)
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._to_postfix(tokens)
        
        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix_tokens)
        
        return result
    
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
            
            # Handle numbers (including decimals and negative numbers)
            if char.isdigit() or char == '.':
                number_str, new_i = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, number_str, i))
                i = new_i
                
            # Handle operators
            elif char in self.OPERATORS:
                # Handle negative numbers (unary minus)
                if char == '-' and self._is_unary_minus(tokens):
                    number_str, new_i = self._extract_number(expression, i)
                    tokens.append(Token(TokenType.NUMBER, number_str, i))
                    i = new_i
                else:
                    tokens.append(Token(TokenType.OPERATOR, char, i))
                    i += 1
                    
            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
                
            # Invalid character
            else:
                raise InvalidExpressionError(f"Invalid character '{char}' at position {i}")
        
        return tokens
    
    def _extract_number(self, expression: str, start: int) -> tuple[str, int]:
        """
        Extracts a number (including negative numbers) from the expression.
        
        Args:
            expression: The full expression
            start: Starting position
            
        Returns:
            Tuple of (number_string, next_position)
            
        Raises:
            InvalidExpressionError: If the number format is invalid
        """
        i = start
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += '-'
            i += 1
        
        decimal_count = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.':
                decimal_count += 1
                if decimal_count > 1:
                    raise InvalidExpressionError(f"Invalid number format at position {start}")
                number_str += char
                i += 1
            else:
                break
        
        # Validate the number
        if not number_str or number_str in ['-', '.', '-.']:
            raise InvalidExpressionError(f"Invalid number format at position {start}")
        
        # Ensure the number is valid
        try:
            float(number_str)
        except ValueError:
            raise InvalidExpressionError(f"Invalid number format '{number_str}' at position {start}")
        
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
        
        # Check parentheses balance
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
        
        # Check for valid token sequences
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus which is handled in tokenization)
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError(f"Invalid operator placement at position {token.position}")
                
                # Two consecutive operators are not allowed
                if i > 0 and tokens[i-1].type == TokenType.OPERATOR:
                    raise InvalidExpressionError(f"Consecutive operators at position {token.position}")
                
                # Operator after opening parenthesis is not allowed
                if i > 0 and tokens[i-1].type == TokenType.LEFT_PAREN:
                    raise InvalidExpressionError(f"Operator after opening parenthesis at position {token.position}")
                
                # Operator before closing parenthesis is not allowed
                if i < len(tokens) - 1 and tokens[i+1].type == TokenType.RIGHT_PAREN:
                    raise InvalidExpressionError(f"Operator before closing parenthesis at position {token.position}")
    
    def _to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Converts infix notation to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens in infix notation
            
        Returns:
            List of tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
                
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.OPERATOR_PRECEDENCE[operator_stack[-1].value] >= 
                       self.OPERATOR_PRECEDENCE[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
                
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
                
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output.append(operator_stack.pop())
                
                # Remove the left parenthesis
                if operator_stack:
                    operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            The result of the evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
                
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Invalid expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(token.value, left_operand, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: malformed")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Applies an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            left: Left operand
            right: Right operand
            
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
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
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
            
        except (InvalidExpressionError, DivisionByZeroError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
