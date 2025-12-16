
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
    
    def __init__(self, token_type: TokenType, value: str, position: int = 0):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The string value of the token
            position: Position in the original expression (for error reporting)
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        return f"Token({self.type}, '{self.value}', {self.position})"


class CalculatorError(Exception):
    """Base exception class for calculator errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid syntax or characters."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports addition (+), subtraction (-), multiplication (*), division (/),
    parentheses for grouping, and proper operator precedence.
    """
    
    # Operator precedence (higher number = higher precedence)
    PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    # Valid operators
    OPERATORS = set(PRECEDENCE.keys())
    
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
            InvalidExpressionError: If the expression contains invalid syntax
            UnbalancedParenthesesError: If parentheses are not balanced
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
            raise InvalidExpressionError("Empty expression provided")
        
        self._reset_state()
        
        try:
            # Step 1: Tokenize the expression
            self._tokens = self._tokenize(expression.strip())
            
            # Step 2: Validate tokens and parentheses
            self._validate_tokens()
            self._validate_parentheses()
            
            # Step 3: Convert to postfix notation using Shunting Yard algorithm
            postfix_tokens = self._to_postfix()
            
            # Step 4: Evaluate postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List of Token objects
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        tokens = []
        i = 0
        
        # Regular expression for matching numbers (including negative and decimal)
        number_pattern = re.compile(r'-?\d+\.?\d*')
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including negative numbers)
            if char.isdigit() or (char == '-' and self._is_negative_number(expression, i)):
                match = number_pattern.match(expression[i:])
                if match:
                    number_str = match.group()
                    tokens.append(Token(TokenType.NUMBER, number_str, i))
                    i += len(number_str)
                else:
                    raise InvalidExpressionError(f"Invalid number format at position {i}")
            
            # Handle operators
            elif char in self.OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, char, i))
                i += 1
            
            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
            
            # Handle decimal point (part of number)
            elif char == '.':
                # This should be handled as part of number tokenization
                raise InvalidExpressionError(f"Unexpected decimal point at position {i}")
            
            # Invalid character
            else:
                raise InvalidExpressionError(f"Invalid character '{char}' at position {i}")
        
        return tokens
    
    def _is_negative_number(self, expression: str, position: int) -> bool:
        """
        Determine if a minus sign represents a negative number or subtraction.
        
        Args:
            expression: The full expression
            position: Position of the minus sign
            
        Returns:
            True if it's a negative number, False if it's subtraction
        """
        if position == 0:
            return True
        
        # Look at the previous non-whitespace character
        prev_pos = position - 1
        while prev_pos >= 0 and expression[prev_pos].isspace():
            prev_pos -= 1
        
        if prev_pos < 0:
            return True
        
        prev_char = expression[prev_pos]
        # Negative number if preceded by operator or opening parenthesis
        return prev_char in self.OPERATORS or prev_char == '('
    
    def _validate_tokens(self) -> None:
        """
        Validate the sequence of tokens for basic syntax errors.
        
        Raises:
            InvalidExpressionError: If token sequence is invalid
        """
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found")
        
        # Check for consecutive operators or invalid sequences
        for i in range(len(self._tokens)):
            current = self._tokens[i]
            
            if i > 0:
                prev = self._tokens[i - 1]
                
                # Two consecutive operators (except for negative numbers)
                if (current.type == TokenType.OPERATOR and 
                    prev.type == TokenType.OPERATOR):
                    raise InvalidExpressionError(
                        f"Consecutive operators at positions {prev.position} and {current.position}")
                
                # Operator after opening parenthesis (except negative)
                if (current.type == TokenType.OPERATOR and 
                    prev.type == TokenType.LEFT_PAREN and 
                    current.value != '-'):
                    raise InvalidExpressionError(
                        f"Invalid operator '{current.value}' after opening parenthesis at position {current.position}")
            
            # Check for operator at the end
            if (i == len(self._tokens) - 1 and 
                current.type == TokenType.OPERATOR):
                raise InvalidExpressionError(
                    f"Expression cannot end with operator '{current.value}' at position {current.position}")
    
    def _validate_parentheses(self) -> None:
        """
        Validate that parentheses are properly balanced.
        
        Raises:
            UnbalancedParenthesesError: If parentheses are not balanced
        """
        balance = 0
        
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                balance += 1
            elif token.type == TokenType.RIGHT_PAREN:
                balance -= 1
                
                if balance < 0:
                    raise UnbalancedParenthesesError(
                        f"Unmatched closing parenthesis at position {token.position}")
        
        if balance > 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List of tokens in postfix order
        """
        output = []
        operator_stack = []
        
        for token in self._tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
            
            elif token.type == TokenType.OPERATOR:
                # Pop operators with higher or equal precedence
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.PRECEDENCE[operator_stack[-1].value] >= self.PRECEDENCE[token.value]):
                    output.append(operator_stack.pop())
                
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Pop until we find the matching left parenthesis
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output.append(operator_stack.pop())
                
                # Remove the left parenthesis
                if operator_stack:
                    operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, tokens: List[Token]) -> Union[int, float]:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens: List of tokens in postfix order
            
        Returns:
            The numerical result
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If evaluation fails
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                # Convert to appropriate numeric type
                value = token.value
                if '.' in value:
                    stack.append(float(value))
                else:
                    stack.append(int(value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError(
                        f"Insufficient operands for operator '{token.value}' at position {token.position}")
                
                # Pop two operands (note: order matters for non-commutative operations)
                right = stack.pop()
                left = stack.pop()
                
                # Perform the operation
                if token.value == '+':
                    result = left + right
                elif token.value == '-':
                    result = left - right
                elif token.value == '*':
                    result = left * right
                elif token.value == '/':
                    if right == 0:
                        raise DivisionByZeroError("Division by zero")
                    result = left / right
                else:
                    raise InvalidExpressionError(f"Unknown operator: {token.value}")
                
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: incorrect number of operands")
        
        return stack[0]


def main():
    """
    Main function for interactive calculator usage.
    Provides a console interface for the calculator.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supports: +, -, *, /, parentheses ()")
    print("Enter 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
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
