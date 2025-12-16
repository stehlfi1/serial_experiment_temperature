
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
    """Raised when division by zero is attempted."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations
    with proper operator precedence and parentheses handling.
    
    Supports operations: +, -, *, /
    Supports parentheses for grouping
    Handles integers and floating-point numbers (including negative values)
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
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for new calculation."""
        self._tokens: List[Token] = []
        self._position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression: A string containing the mathematical expression
            
        Returns:
            The calculated result as a float
            
        Raises:
            InvalidExpressionError: If the expression is invalid
            DivisionByZeroError: If division by zero is attempted
            
        Example:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(1 + 2) * 3")
            9.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        self._reset_state()
        
        try:
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate tokens
            self._validate_tokens()
            
            # Convert to postfix notation and evaluate
            postfix_tokens = self._convert_to_postfix()
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert the expression string into tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        self._tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including decimals and negative numbers)
            if char.isdigit() or char == '.':
                number_str, i = self._extract_number(expression, i)
                self._tokens.append(Token(TokenType.NUMBER, number_str, i - len(number_str)))
            
            # Handle operators
            elif char in self.OPERATORS:
                # Handle negative numbers (unary minus)
                if char == '-' and self._is_unary_minus():
                    if i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        number_str, i = self._extract_number(expression, i)
                        self._tokens.append(Token(TokenType.NUMBER, number_str, i - len(number_str)))
                    else:
                        raise InvalidExpressionError(f"Invalid unary minus at position {i}")
                else:
                    self._tokens.append(Token(TokenType.OPERATOR, char, i))
                    i += 1
            
            # Handle parentheses
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
            
            # Invalid character
            else:
                raise InvalidExpressionError(f"Invalid character '{char}' at position {i}")
    
    def _extract_number(self, expression: str, start: int) -> tuple[str, int]:
        """
        Extract a complete number (including decimals and negative sign) from the expression.
        
        Args:
            expression: The expression string
            start: Starting position
            
        Returns:
            Tuple of (number_string, new_position)
            
        Raises:
            InvalidExpressionError: If the number format is invalid
        """
        i = start
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
        
        # Validate the number format
        if not self._is_valid_number(number_str):
            raise InvalidExpressionError(f"Invalid number format: '{number_str}'")
        
        return number_str, i
    
    def _is_valid_number(self, number_str: str) -> bool:
        """
        Validate if a string represents a valid number.
        
        Args:
            number_str: The string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            float(number_str)
            # Additional checks for edge cases
            if number_str in ['-', '.', '-.']:
                return False
            return True
        except ValueError:
            return False
    
    def _is_unary_minus(self) -> bool:
        """
        Determine if the current minus sign is a unary operator.
        
        Returns:
            True if it's a unary minus, False if it's a binary operator
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self) -> None:
        """
        Validate the token sequence for proper syntax.
        
        Raises:
            InvalidExpressionError: If syntax errors are found
        """
        if not self._tokens:
            raise InvalidExpressionError("No tokens found")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count != 0:
            raise InvalidExpressionError("Unbalanced parentheses: missing closing parentheses")
        
        # Validate token sequence
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus handled in tokenization)
                if i == len(self._tokens) - 1:
                    raise InvalidExpressionError(f"Expression cannot end with operator '{token.value}'")
                
                # Cannot have consecutive operators
                if i > 0 and self._tokens[i - 1].type == TokenType.OPERATOR:
                    raise InvalidExpressionError(f"Consecutive operators at position {token.position}")
            
            elif token.type == TokenType.LEFT_PAREN:
                # Cannot have number directly before opening parenthesis
                if i > 0 and self._tokens[i - 1].type == TokenType.NUMBER:
                    raise InvalidExpressionError(f"Missing operator before '(' at position {token.position}")
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Cannot have operator directly before closing parenthesis
                if i > 0 and self._tokens[i - 1].type == TokenType.OPERATOR:
                    raise InvalidExpressionError(f"Operator before ')' at position {token.position}")
                
                # Cannot have closing parenthesis directly before number
                if i < len(self._tokens) - 1 and self._tokens[i + 1].type == TokenType.NUMBER:
                    raise InvalidExpressionError(f"Missing operator after ')' at position {token.position}")
        
        # Check first and last tokens
        if self._tokens[0].type == TokenType.OPERATOR:
            raise InvalidExpressionError("Expression cannot start with an operator")
        
        if self._tokens[-1].type == TokenType.OPERATOR:
            raise InvalidExpressionError("Expression cannot end with an operator")
    
    def _convert_to_postfix(self) -> List[Token]:
        """
        Convert infix notation to postfix notation using Shunting Yard algorithm.
        
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
                
                if operator_stack and operator_stack[-1].type == TokenType.LEFT_PAREN:
                    operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise InvalidExpressionError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluate postfix expression.
        
        Args:
            tokens: List of tokens in postfix order
            
        Returns:
            The calculated result
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        stack: List[float] = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Invalid expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(left_operand, token.value, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: malformed postfix")
        
        return stack[0]
    
    def _perform_operation(self, left: float, operator: str, right: float) -> float:
        """
        Perform a single arithmetic operation.
        
        Args:
            left: Left operand
            operator: The operator (+, -, *, /)
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
            
        except CalculatorError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
