
"""
Console-based Arithmetic Calculator

A high-quality implementation of an arithmetic calculator that supports
basic operations (+, -, *, /) with parentheses and proper operator precedence.
Adheres to ISO/IEC 25010 quality standards.

Author: Senior Software Developer
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
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression is syntactically invalid."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class InvalidCharacterError(CalculatorError):
    """Raised when invalid characters are found in the expression."""
    pass


class Lexer:
    """Tokenizes mathematical expressions into a list of tokens."""
    
    # Regular expressions for token recognition
    TOKEN_PATTERNS = [
        (TokenType.NUMBER, r'\d+\.?\d*'),
        (TokenType.OPERATOR, r'[+\-*/]'),
        (TokenType.LEFT_PAREN, r'\('),
        (TokenType.RIGHT_PAREN, r'\)'),
    ]
    
    def __init__(self, expression: str):
        """
        Initialize the lexer with an expression.
        
        Args:
            expression: Mathematical expression to tokenize
        """
        self.expression = expression.replace(' ', '')  # Remove whitespace
        self.position = 0
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the expression into a list of tokens.
        
        Returns:
            List of tokens representing the expression
            
        Raises:
            InvalidCharacterError: If invalid characters are found
        """
        self.position = 0
        self.tokens = []
        
        while self.position < len(self.expression):
            self._match_next_token()
        
        return self.tokens
    
    def _match_next_token(self) -> None:
        """Match and consume the next token in the expression."""
        if self.position >= len(self.expression):
            return
        
        current_char = self.expression[self.position]
        
        # Handle negative numbers
        if (current_char == '-' and 
            (len(self.tokens) == 0 or 
             self.tokens[-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])):
            self._handle_negative_number()
            return
        
        # Try to match token patterns
        for token_type, pattern in self.TOKEN_PATTERNS:
            regex = re.compile(pattern)
            match = regex.match(self.expression, self.position)
            
            if match:
                value = match.group(0)
                token = Token(token_type, value, self.position)
                self.tokens.append(token)
                self.position = match.end()
                return
        
        # If no pattern matches, raise an error
        raise InvalidCharacterError(
            f"Invalid character '{current_char}' at position {self.position}"
        )
    
    def _handle_negative_number(self) -> None:
        """Handle negative numbers by combining minus sign with the following number."""
        start_pos = self.position
        self.position += 1  # Skip the minus sign
        
        # Look for a number after the minus sign
        if self.position < len(self.expression):
            number_pattern = re.compile(r'\d+\.?\d*')
            match = number_pattern.match(self.expression, self.position)
            
            if match:
                # Create a negative number token
                value = '-' + match.group(0)
                token = Token(TokenType.NUMBER, value, start_pos)
                self.tokens.append(token)
                self.position = match.end()
                return
        
        # If no number follows, treat as operator
        token = Token(TokenType.OPERATOR, '-', start_pos)
        self.tokens.append(token)


class Parser:
    """Parses tokens using the Shunting Yard algorithm and evaluates expressions."""
    
    # Operator precedence and associativity
    OPERATORS = {
        '+': {'precedence': 1, 'left_associative': True},
        '-': {'precedence': 1, 'left_associative': True},
        '*': {'precedence': 2, 'left_associative': True},
        '/': {'precedence': 2, 'left_associative': True},
    }
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize the parser with tokens.
        
        Args:
            tokens: List of tokens to parse
        """
        self.tokens = tokens
        self.output_queue: List[Token] = []
        self.operator_stack: List[Token] = []
    
    def parse_and_evaluate(self) -> float:
        """
        Parse tokens using Shunting Yard algorithm and evaluate the result.
        
        Returns:
            The evaluated result as a float
            
        Raises:
            UnbalancedParenthesesError: If parentheses are unbalanced
            InvalidExpressionError: If expression is invalid
        """
        self._validate_expression()
        self._convert_to_postfix()
        return self._evaluate_postfix()
    
    def _validate_expression(self) -> None:
        """
        Validate the expression for basic syntax errors.
        
        Raises:
            InvalidExpressionError: If expression is empty or has invalid syntax
            UnbalancedParenthesesError: If parentheses are unbalanced
        """
        if not self.tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in self.tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        # Check for consecutive operators or invalid sequences
        for i in range(len(self.tokens) - 1):
            current = self.tokens[i]
            next_token = self.tokens[i + 1]
            
            if (current.type == TokenType.OPERATOR and 
                next_token.type == TokenType.OPERATOR):
                raise InvalidExpressionError("Consecutive operators found")
    
    def _convert_to_postfix(self) -> None:
        """Convert infix notation to postfix using Shunting Yard algorithm."""
        self.output_queue = []
        self.operator_stack = []
        
        for token in self.tokens:
            if token.type == TokenType.NUMBER:
                self.output_queue.append(token)
            
            elif token.type == TokenType.OPERATOR:
                self._handle_operator(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                self.operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                self._handle_right_parenthesis()
        
        # Pop remaining operators
        while self.operator_stack:
            operator = self.operator_stack.pop()
            if operator.type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise UnbalancedParenthesesError("Unbalanced parentheses")
            self.output_queue.append(operator)
    
    def _handle_operator(self, token: Token) -> None:
        """Handle operator tokens during postfix conversion."""
        while (self.operator_stack and
               self.operator_stack[-1].type == TokenType.OPERATOR and
               self._should_pop_operator(token, self.operator_stack[-1])):
            self.output_queue.append(self.operator_stack.pop())
        
        self.operator_stack.append(token)
    
    def _should_pop_operator(self, current: Token, stack_top: Token) -> bool:
        """Determine if the stack operator should be popped."""
        current_prec = self.OPERATORS[current.value]['precedence']
        stack_prec = self.OPERATORS[stack_top.value]['precedence']
        current_left_assoc = self.OPERATORS[current.value]['left_associative']
        
        return (stack_prec > current_prec or
                (stack_prec == current_prec and current_left_assoc))
    
    def _handle_right_parenthesis(self) -> None:
        """Handle right parenthesis during postfix conversion."""
        while self.operator_stack and self.operator_stack[-1].type != TokenType.LEFT_PAREN:
            self.output_queue.append(self.operator_stack.pop())
        
        if not self.operator_stack:
            raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        # Remove the left parenthesis
        self.operator_stack.pop()
    
    def _evaluate_postfix(self) -> float:
        """
        Evaluate the postfix expression.
        
        Returns:
            The evaluated result as a float
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If expression is malformed
        """
        stack: List[float] = []
        
        for token in self.output_queue:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands")
                
                right = stack.pop()
                left = stack.pop()
                result = self._apply_operator(token.value, left, right)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            left: Left operand
            right: Right operand
            
        Returns:
            Result of the operation
            
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
                raise DivisionByZeroError("Division by zero")
            return left / right
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")


class Calculator:
    """
    High-quality arithmetic calculator supporting basic operations with parentheses.
    
    This calculator implements a complete mathematical expression evaluator that:
    - Supports addition, subtraction, multiplication, and division
    - Handles parentheses with proper precedence
    - Accepts integers and floating-point numbers (including negative values)
    - Provides comprehensive error handling
    - Uses efficient algorithms (Shunting Yard for parsing)
    """
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: Mathematical expression string to evaluate
                       Supports: +, -, *, /, (), integers, floats, negative numbers
                       
        Returns:
            The evaluated result as a float
            
        Raises:
            InvalidExpressionError: If the expression is syntactically invalid
            DivisionByZeroError: If division by zero is attempted
            UnbalancedParenthesesError: If parentheses are not properly balanced
            InvalidCharacterError: If invalid characters are found
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) * 2")
            10.0
            >>> calc.calculate("-3 + 5")
            2.0
        """
        try:
            # Input validation
            if not isinstance(expression, str):
                raise InvalidExpressionError("Expression must be a string")
            
            if not expression or not expression.strip():
                raise InvalidExpressionError("Empty expression")
            
            # Tokenize the expression
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            
            # Parse and evaluate
            parser = Parser(tokens)
            result = parser.parse_and_evaluate()
            
            return result
            
        except (InvalidExpressionError, DivisionByZeroError, 
                UnbalancedParenthesesError, InvalidCharacterError):
            # Re-raise calculator-specific errors
            raise
        except Exception as e:
            # Wrap unexpected errors
            raise InvalidExpressionError(f"Unexpected error: {str(e)}")


def main():
    """
    Main function to run the calculator in interactive mode.
    
    Provides a user-friendly console interface for the calculator.
    """
    calculator = Calculator()
    
    print("=== Arithmetic Calculator ===")
    print("Supports: +, -, *, /, () with integers and floats")
    print("Type 'quit' or 'exit' to stop")
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
            
        except (InvalidExpressionError, DivisionByZeroError,
                UnbalancedParenthesesError, InvalidCharacterError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        
        print()  # Empty line for readability


if __name__ == "__main__":
    main()
