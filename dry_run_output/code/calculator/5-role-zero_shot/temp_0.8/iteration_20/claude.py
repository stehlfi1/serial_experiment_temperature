
"""
Console-based Arithmetic Calculator

A high-quality calculator implementation that supports basic arithmetic operations
with proper operator precedence and parentheses handling.

Author: Senior Software Developer
Standard: ISO/IEC 25010 compliant
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
    
    def __init__(self, token_type: TokenType, value: str, position: int = 0):
        """
        Initialize a token.
        
        Args:
            token_type (TokenType): The type of the token
            value (str): The string value of the token
            position (int): Position in the original expression
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        return f"Token({self.type.value}, '{self.value}', {self.position})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
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
    A console-based arithmetic calculator that supports basic operations
    with proper operator precedence and parentheses handling.
    
    Supported operations:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (*)
    - Division (/)
    - Parentheses for grouping
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
        self._current_position = 0
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: The calculated result
            
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
            >>> calc.calculate("-5.5 + 3.2")
            -2.3
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Empty expression")
        
        self._reset_state()
        
        try:
            # Tokenize the expression
            self._tokenize(expression.strip())
            
            # Validate tokens
            self._validate_tokens()
            
            # Convert to postfix notation (Reverse Polish Notation)
            postfix_tokens = self._infix_to_postfix()
            
            # Evaluate postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert expression string into tokens.
        
        Args:
            expression (str): The expression to tokenize
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        # Remove whitespace
        expression = re.sub(r'\s+', '', expression)
        
        # Pattern to match numbers (including negative), operators, and parentheses
        pattern = r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))'
        matches = re.finditer(pattern, expression)
        
        position = 0
        prev_token = None
        
        for match in matches:
            token_value = match.group(1)
            token_start = match.start()
            
            # Check for gaps in matching (invalid characters)
            if token_start > position:
                invalid_char = expression[position]
                raise InvalidExpressionError(
                    f"Invalid character '{invalid_char}' at position {position}"
                )
            
            # Determine token type
            if re.match(r'\d+\.?\d*', token_value):
                self._tokens.append(Token(TokenType.NUMBER, token_value, token_start))
            elif token_value in self.OPERATORS:
                # Handle unary minus
                if (token_value == '-' and 
                    (prev_token is None or 
                     prev_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])):
                    # This is a unary minus, combine with next number
                    self._tokens.append(Token(TokenType.OPERATOR, token_value, token_start))
                else:
                    self._tokens.append(Token(TokenType.OPERATOR, token_value, token_start))
            elif token_value == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, token_value, token_start))
            elif token_value == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, token_value, token_start))
            
            prev_token = self._tokens[-1] if self._tokens else None
            position = match.end()
        
        # Check if entire expression was matched
        if position < len(expression):
            invalid_char = expression[position]
            raise InvalidExpressionError(
                f"Invalid character '{invalid_char}' at position {position}"
            )
        
        # Handle unary minus by merging with following number
        self._process_unary_operators()
    
    def _process_unary_operators(self) -> None:
        """Process unary minus operators by merging them with following numbers."""
        processed_tokens = []
        i = 0
        
        while i < len(self._tokens):
            current_token = self._tokens[i]
            
            if (current_token.type == TokenType.OPERATOR and 
                current_token.value == '-' and
                i + 1 < len(self._tokens) and
                self._tokens[i + 1].type == TokenType.NUMBER):
                
                # Check if this is a unary minus
                prev_token = processed_tokens[-1] if processed_tokens else None
                if (prev_token is None or 
                    prev_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    
                    # Merge unary minus with number
                    next_token = self._tokens[i + 1]
                    merged_value = '-' + next_token.value
                    processed_tokens.append(
                        Token(TokenType.NUMBER, merged_value, current_token.position)
                    )
                    i += 2  # Skip the number token
                    continue
            
            processed_tokens.append(current_token)
            i += 1
        
        self._tokens = processed_tokens
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for correct syntax.
        
        Raises:
            InvalidExpressionError: If syntax errors are found
            UnbalancedParenthesesError: If parentheses are unbalanced
        """
        if not self._tokens:
            raise InvalidExpressionError("No valid tokens found")
        
        # Check parentheses balance
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise UnbalancedParenthesesError(
                        f"Unmatched closing parenthesis at position {token.position}"
                    )
        
        if paren_count > 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
        
        # Validate token sequence
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators must have operands on both sides (except handled unary)
                if i == 0 or i == len(self._tokens) - 1:
                    raise InvalidExpressionError(
                        f"Operator '{token.value}' at position {token.position} "
                        "requires operands on both sides"
                    )
                
                prev_token = self._tokens[i - 1]
                next_token = self._tokens[i + 1]
                
                if prev_token.type not in [TokenType.NUMBER, TokenType.RIGHT_PAREN]:
                    raise InvalidExpressionError(
                        f"Invalid token before operator '{token.value}' "
                        f"at position {token.position}"
                    )
                
                if next_token.type not in [TokenType.NUMBER, TokenType.LEFT_PAREN]:
                    raise InvalidExpressionError(
                        f"Invalid token after operator '{token.value}' "
                        f"at position {token.position}"
                    )
    
    def _infix_to_postfix(self) -> List[Token]:
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
                       self.PRECEDENCE[operator_stack[-1].value] >= 
                       self.PRECEDENCE[token.value]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack:
                    raise UnbalancedParenthesesError(
                        f"Unmatched closing parenthesis at position {token.position}"
                    )
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            token = operator_stack.pop()
            if token.type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise UnbalancedParenthesesError("Unmatched parenthesis")
            output_queue.append(token)
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> Union[int, float]:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens (List[Token]): Tokens in postfix notation
            
        Returns:
            Union[int, float]: The calculated result
            
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
                    raise InvalidExpressionError(
                        f"Insufficient operands for operator '{token.value}'"
                    )
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(
                    token.value, left_operand, right_operand, token.position
                )
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Malformed expression")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: Union[int, float], 
                       right: Union[int, float], position: int) -> Union[int, float]:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator (str): The operator to apply
            left (Union[int, float]): Left operand
            right (Union[int, float]): Right operand
            position (int): Position of operator in original expression
            
        Returns:
            Union[int, float]: The result of the operation
            
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
                raise DivisionByZeroError(
                    f"Division by zero at position {position}"
                )
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
    print("Enter 'quit' or 'exit' to stop")
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
            
        except CalculatorError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        print()  # Empty line for readability


if __name__ == "__main__":
    main()
