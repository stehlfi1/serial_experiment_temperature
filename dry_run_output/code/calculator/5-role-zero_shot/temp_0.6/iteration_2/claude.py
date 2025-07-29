
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
    """Raised when the expression is syntactically invalid."""
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
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for a new calculation."""
        self._tokens: List[Token] = []
        self._current_position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing a mathematical expression
            
        Returns:
            The numerical result of the expression evaluation
            
        Raises:
            InvalidExpressionError: If the expression is syntactically invalid
            DivisionByZeroError: If division by zero is attempted
            
        Example:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) / 2.5")
            2.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        self._reset_state()
        
        try:
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate token sequence
            self._validate_tokens()
            
            # Convert to postfix notation using Shunting Yard algorithm
            postfix_tokens = self._to_postfix()
            
            # Evaluate the postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        # Regular expression to match numbers (including negative), operators, and parentheses
        pattern = r'(-?\d+\.?\d*|\+|\-|\*|\/|\(|\))'
        
        # Find all matches with their positions
        matches = []
        for match in re.finditer(pattern, expression):
            matches.append((match.group(), match.start()))
        
        # Check if the entire expression is covered by matches
        matched_length = sum(len(match[0]) for match in matches)
        # Remove spaces to get actual content length
        content_length = len(expression.replace(' ', ''))
        
        if matched_length != content_length:
            # Find the first invalid character
            valid_chars = set('0123456789+-*/.() ')
            for i, char in enumerate(expression):
                if char not in valid_chars:
                    raise InvalidExpressionError(f"Invalid character '{char}' at position {i}")
        
        # Convert matches to tokens
        for value, position in matches:
            if value in '+-*/':
                self._tokens.append(Token(TokenType.OPERATOR, value, position))
            elif value == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, value, position))
            elif value == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, value, position))
            else:
                # It's a number
                try:
                    float(value)  # Validate it's a valid number
                    self._tokens.append(Token(TokenType.NUMBER, value, position))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number '{value}' at position {position}")
    
    def _validate_tokens(self) -> None:
        """
        Validate the sequence of tokens for syntactic correctness.
        
        Raises:
            InvalidExpressionError: If the token sequence is invalid
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
                    raise InvalidExpressionError(f"Unmatched closing parenthesis at position {token.position}")
        
        if paren_count > 0:
            raise InvalidExpressionError("Unmatched opening parenthesis")
        
        # Validate token sequence
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus)
                if i == 0 and token.value != '-':
                    raise InvalidExpressionError(f"Expression cannot start with operator '{token.value}'")
                if i == len(self._tokens) - 1:
                    raise InvalidExpressionError(f"Expression cannot end with operator '{token.value}'")
                
                # Check for consecutive operators (except unary minus)
                if i > 0 and self._tokens[i-1].type == TokenType.OPERATOR:
                    if not (token.value == '-' and self._tokens[i-1].value in '(+-*/'):
                        raise InvalidExpressionError(f"Invalid consecutive operators at position {token.position}")
        
        # Handle unary minus by converting tokens
        self._handle_unary_minus()
    
    def _handle_unary_minus(self) -> None:
        """Convert unary minus operators to negative numbers."""
        new_tokens = []
        i = 0
        
        while i < len(self._tokens):
            token = self._tokens[i]
            
            # Check for unary minus
            if (token.type == TokenType.OPERATOR and token.value == '-' and
                (i == 0 or self._tokens[i-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])):
                
                # This is a unary minus, combine with the next number
                if i + 1 >= len(self._tokens) or self._tokens[i + 1].type != TokenType.NUMBER:
                    raise InvalidExpressionError(f"Invalid unary minus at position {token.position}")
                
                next_token = self._tokens[i + 1]
                # Create a new negative number token
                negative_value = '-' + next_token.value
                new_tokens.append(Token(TokenType.NUMBER, negative_value, token.position))
                i += 2  # Skip both the minus and the number
            else:
                new_tokens.append(token)
                i += 1
        
        self._tokens = new_tokens
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix order
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
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            elif token.type == TokenType.RIGHT_PAREN:
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
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
    
    def _evaluate_postfix(self, tokens: List[Token]) -> Union[int, float]:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix order
            
        Returns:
            The result of the evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
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
                    raise InvalidExpressionError("Insufficient operands for operator")
                
                right = stack.pop()
                left = stack.pop()
                
                result = self._apply_operator(token.value, left, right)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: too many operands")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: Union[int, float], right: Union[int, float]) -> Union[int, float]:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            left: The left operand
            right: The right operand
            
        Returns:
            The result of the operation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
        """
        if operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        elif operator == '*':
            result = left * right
        elif operator == '/':
            if right == 0:
                raise DivisionByZeroError("Division by zero is not allowed")
            result = left / right
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")
        
        # Return integer if result is a whole number
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result


def main():
    """
    Main function to run the calculator in interactive mode.
    """
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
            
        except CalculatorError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
