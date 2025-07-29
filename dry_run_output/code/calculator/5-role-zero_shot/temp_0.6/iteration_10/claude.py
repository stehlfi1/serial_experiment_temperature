
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
    """Raised when division by zero is attempted."""
    pass


class Lexer:
    """Tokenizes mathematical expressions into a list of tokens."""
    
    def __init__(self):
        """Initialize the lexer with token patterns."""
        self.token_patterns = [
            (r'\d+\.?\d*', TokenType.NUMBER),
            (r'[+\-*/]', TokenType.OPERATOR),
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN),
        ]
    
    def tokenize(self, expression: str) -> List[Token]:
        """
        Convert a mathematical expression into tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List of tokens representing the expression
            
        Raises:
            InvalidExpressionError: If the expression contains invalid characters
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Empty expression")
        
        # Remove whitespace
        expression = re.sub(r'\s+', '', expression)
        tokens = []
        position = 0
        
        while position < len(expression):
            matched = False
            
            for pattern, token_type in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(expression, position)
                
                if match:
                    value = match.group(0)
                    tokens.append(Token(token_type, value, position))
                    position = match.end()
                    matched = True
                    break
            
            if not matched:
                raise InvalidExpressionError(
                    f"Invalid character '{expression[position]}' at position {position}"
                )
        
        return self._handle_unary_operators(tokens)
    
    def _handle_unary_operators(self, tokens: List[Token]) -> List[Token]:
        """
        Handle unary plus and minus operators by converting them to appropriate tokens.
        
        Args:
            tokens: List of tokens to process
            
        Returns:
            List of tokens with unary operators handled
        """
        if not tokens:
            return tokens
        
        processed_tokens = []
        
        for i, token in enumerate(tokens):
            if (token.type == TokenType.OPERATOR and token.value in ['+', '-'] and
                (i == 0 or tokens[i-1].type in [TokenType.LEFT_PAREN, TokenType.OPERATOR])):
                
                # This is a unary operator
                if token.value == '-':
                    # Convert unary minus to multiplication by -1
                    processed_tokens.extend([
                        Token(TokenType.LEFT_PAREN, '(', token.position),
                        Token(TokenType.NUMBER, '-1', token.position),
                        Token(TokenType.OPERATOR, '*', token.position),
                    ])
                # Unary plus is ignored (no-op)
            else:
                processed_tokens.append(token)
        
        return processed_tokens


class Parser:
    """Parses tokens into an Abstract Syntax Tree and evaluates the expression."""
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize the parser with tokens.
        
        Args:
            tokens: List of tokens to parse
        """
        self.tokens = tokens
        self.position = 0
    
    def parse_and_evaluate(self) -> float:
        """
        Parse and evaluate the expression.
        
        Returns:
            The result of the mathematical expression
            
        Raises:
            InvalidExpressionError: If the expression has invalid syntax
        """
        if not self.tokens:
            raise InvalidExpressionError("No tokens to parse")
        
        result = self._parse_expression()
        
        if self.position < len(self.tokens):
            raise InvalidExpressionError(
                f"Unexpected token '{self.tokens[self.position].value}' "
                f"at position {self.tokens[self.position].position}"
            )
        
        return result
    
    def _current_token(self) -> Union[Token, None]:
        """Get the current token without advancing the position."""
        return self.tokens[self.position] if self.position < len(self.tokens) else None
    
    def _consume_token(self, expected_type: TokenType = None) -> Token:
        """
        Consume and return the current token.
        
        Args:
            expected_type: Expected token type (optional)
            
        Returns:
            The consumed token
            
        Raises:
            InvalidExpressionError: If no more tokens or unexpected token type
        """
        if self.position >= len(self.tokens):
            raise InvalidExpressionError("Unexpected end of expression")
        
        token = self.tokens[self.position]
        
        if expected_type and token.type != expected_type:
            raise InvalidExpressionError(
                f"Expected {expected_type.value}, got {token.type.value} "
                f"at position {token.position}"
            )
        
        self.position += 1
        return token
    
    def _parse_expression(self) -> float:
        """Parse addition and subtraction (lowest precedence)."""
        result = self._parse_term()
        
        while (self._current_token() and 
               self._current_token().type == TokenType.OPERATOR and
               self._current_token().value in ['+', '-']):
            
            operator = self._consume_token().value
            right = self._parse_term()
            
            if operator == '+':
                result += right
            else:  # operator == '-'
                result -= right
        
        return result
    
    def _parse_term(self) -> float:
        """Parse multiplication and division (higher precedence)."""
        result = self._parse_factor()
        
        while (self._current_token() and 
               self._current_token().type == TokenType.OPERATOR and
               self._current_token().value in ['*', '/']):
            
            operator = self._consume_token().value
            right = self._parse_factor()
            
            if operator == '*':
                result *= right
            else:  # operator == '/'
                if right == 0:
                    raise DivisionByZeroError("Division by zero")
                result /= right
        
        return result
    
    def _parse_factor(self) -> float:
        """Parse numbers and parenthesized expressions (highest precedence)."""
        token = self._current_token()
        
        if not token:
            raise InvalidExpressionError("Unexpected end of expression")
        
        if token.type == TokenType.NUMBER:
            self._consume_token()
            try:
                return float(token.value)
            except ValueError:
                raise InvalidExpressionError(f"Invalid number: {token.value}")
        
        elif token.type == TokenType.LEFT_PAREN:
            self._consume_token()  # consume '('
            result = self._parse_expression()
            
            if not self._current_token() or self._current_token().type != TokenType.RIGHT_PAREN:
                raise InvalidExpressionError("Missing closing parenthesis")
            
            self._consume_token()  # consume ')'
            return result
        
        else:
            raise InvalidExpressionError(
                f"Unexpected token '{token.value}' at position {token.position}"
            )


class Calculator:
    """
    A console-based arithmetic calculator that supports basic mathematical operations.
    
    Supports:
    - Basic arithmetic operations: +, -, *, /
    - Parentheses for grouping
    - Integer and floating-point numbers
    - Negative numbers
    - Proper operator precedence
    """
    
    def __init__(self):
        """Initialize the calculator."""
        self.lexer = Lexer()
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing a mathematical expression
            
        Returns:
            The numerical result of the expression as a float
            
        Raises:
            InvalidExpressionError: If the expression contains invalid syntax
            DivisionByZeroError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5 + 3")
            -2.0
        """
        if not isinstance(expression, str):
            raise InvalidExpressionError("Expression must be a string")
        
        # Validate parentheses balance
        self._validate_parentheses(expression)
        
        # Tokenize the expression
        tokens = self.lexer.tokenize(expression)
        
        # Parse and evaluate
        parser = Parser(tokens)
        result = parser.parse_and_evaluate()
        
        return result
    
    def _validate_parentheses(self, expression: str) -> None:
        """
        Validate that parentheses are balanced in the expression.
        
        Args:
            expression: The expression to validate
            
        Raises:
            InvalidExpressionError: If parentheses are unbalanced
        """
        balance = 0
        for i, char in enumerate(expression):
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    raise InvalidExpressionError(
                        f"Unmatched closing parenthesis at position {i}"
                    )
        
        if balance > 0:
            raise InvalidExpressionError("Unmatched opening parenthesis")


def main():
    """
    Main function to run the calculator in interactive mode.
    Demonstrates the calculator functionality with a simple REPL.
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


calc = Calculator()
print(calc.calculate("2 + 3 * 4"))        # 14.0
print(calc.calculate("(2 + 3) * 4"))      # 20.0
print(calc.calculate("-5 + 3"))           # -2.0
print(calc.calculate("10 / (2 + 3)"))     # 2.0
