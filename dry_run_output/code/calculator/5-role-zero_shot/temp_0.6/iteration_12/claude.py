
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
            position: The position of the token in the original expression
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
    """Raised when the expression contains invalid syntax or characters."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class Tokenizer:
    """Handles tokenization of mathematical expressions."""
    
    def __init__(self):
        # Pattern to match numbers (including negative numbers), operators, and parentheses
        self.token_pattern = re.compile(r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))')
        self.valid_chars = set('0123456789+-*/.() \t')
    
    def tokenize(self, expression: str) -> List[Token]:
        """
        Convert a mathematical expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List of tokens representing the expression
            
        Raises:
            InvalidExpressionError: If the expression contains invalid characters
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Empty expression")
        
        # Check for invalid characters
        for i, char in enumerate(expression):
            if char not in self.valid_chars:
                raise InvalidExpressionError(f"Invalid character '{char}' at position {i}")
        
        # Remove whitespace and find all tokens
        clean_expression = expression.replace(' ', '').replace('\t', '')
        tokens = []
        position = 0
        
        i = 0
        while i < len(clean_expression):
            char = clean_expression[i]
            
            if char.isdigit() or char == '.':
                # Handle numbers (including decimals)
                number_str = ''
                start_pos = i
                
                while i < len(clean_expression) and (clean_expression[i].isdigit() or clean_expression[i] == '.'):
                    number_str += clean_expression[i]
                    i += 1
                
                # Validate number format
                if number_str.count('.') > 1 or number_str == '.':
                    raise InvalidExpressionError(f"Invalid number format '{number_str}' at position {start_pos}")
                
                tokens.append(Token(TokenType.NUMBER, number_str, start_pos))
                
            elif char in '+-':
                # Handle operators and unary minus
                if (not tokens or 
                    tokens[-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    # This is a unary operator
                    if char == '-':
                        # Handle negative numbers
                        i += 1
                        if i >= len(clean_expression) or not (clean_expression[i].isdigit() or clean_expression[i] == '.'):
                            raise InvalidExpressionError(f"Invalid unary operator at position {i-1}")
                        
                        # Parse the number after the minus sign
                        number_str = '-'
                        start_pos = i - 1
                        
                        while i < len(clean_expression) and (clean_expression[i].isdigit() or clean_expression[i] == '.'):
                            number_str += clean_expression[i]
                            i += 1
                        
                        tokens.append(Token(TokenType.NUMBER, number_str, start_pos))
                    else:
                        # Unary plus is ignored
                        i += 1
                else:
                    # This is a binary operator
                    tokens.append(Token(TokenType.OPERATOR, char, i))
                    i += 1
                    
            elif char in '*/':
                tokens.append(Token(TokenType.OPERATOR, char, i))
                i += 1
                
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char, i))
                i += 1
                
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
                i += 1
                
            else:
                raise InvalidExpressionError(f"Unexpected character '{char}' at position {i}")
        
        return tokens


class ExpressionValidator:
    """Validates mathematical expressions for correctness."""
    
    @staticmethod
    def validate_tokens(tokens: List[Token]) -> None:
        """
        Validate a list of tokens for syntactic correctness.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            UnbalancedParenthesesError: If parentheses are not balanced
            InvalidExpressionError: If the expression has invalid syntax
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
                    raise UnbalancedParenthesesError(f"Unmatched closing parenthesis at position {token.position}")
        
        if paren_count > 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
        
        # Check for valid token sequences
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError(f"Invalid operator position at {token.position}")
                
                # Operators cannot be followed by other operators
                if i < len(tokens) - 1 and tokens[i + 1].type == TokenType.OPERATOR:
                    raise InvalidExpressionError(f"Consecutive operators at position {token.position}")
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Right parenthesis cannot be at the beginning
                if i == 0:
                    raise InvalidExpressionError(f"Invalid parenthesis at position {token.position}")
                
                # Right parenthesis cannot follow an operator
                if tokens[i - 1].type == TokenType.OPERATOR:
                    raise InvalidExpressionError(f"Invalid syntax before parenthesis at position {token.position}")


class ExpressionEvaluator:
    """Evaluates mathematical expressions using the Shunting Yard algorithm."""
    
    def __init__(self):
        # Operator precedence (higher number = higher precedence)
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        # All operators are left-associative
        self.left_associative = {'+', '-', '*', '/'}
    
    def evaluate(self, tokens: List[Token]) -> float:
        """
        Evaluate a list of tokens using the Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens representing the expression
            
        Returns:
            The result of the expression evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        # Convert infix to postfix using Shunting Yard algorithm
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate postfix expression
        return self._evaluate_postfix(postfix)
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """Convert infix notation to postfix notation."""
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
                
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and
                       operator_stack[-1].type == TokenType.OPERATOR and
                       ((token.value in self.left_associative and
                         self.precedence[token.value] <= self.precedence[operator_stack[-1].value]) or
                        (token.value not in self.left_associative and
                         self.precedence[token.value] < self.precedence[operator_stack[-1].value]))):
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
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """Evaluate a postfix expression."""
        stack = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
                
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Invalid expression: insufficient operands")
                
                right = stack.pop()
                left = stack.pop()
                
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
            raise InvalidExpressionError("Invalid expression: malformed")
        
        return stack[0]


class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations
    with proper operator precedence and parentheses.
    """
    
    def __init__(self):
        """Initialize the calculator with its components."""
        self.tokenizer = Tokenizer()
        self.validator = ExpressionValidator()
        self.evaluator = ExpressionEvaluator()
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing the mathematical expression to evaluate.
                       Supports +, -, *, /, parentheses, integers, and floating-point numbers.
        
        Returns:
            The result of the expression evaluation as a float.
        
        Raises:
            InvalidExpressionError: If the expression contains invalid syntax or characters
            UnbalancedParenthesesError: If parentheses are not properly balanced
            DivisionByZeroError: If division by zero is attempted
        
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("10 / 2.5")
            4.0
            >>> calc.calculate("-5 + 3")
            -2.0
        """
        try:
            # Tokenize the expression
            tokens = self.tokenizer.tokenize(expression)
            
            # Validate the tokens
            self.validator.validate_tokens(tokens)
            
            # Evaluate the expression
            result = self.evaluator.evaluate(tokens)
            
            return result
            
        except (InvalidExpressionError, UnbalancedParenthesesError, DivisionByZeroError):
            # Re-raise calculator-specific errors
            raise
        except Exception as e:
            # Wrap unexpected errors
            raise InvalidExpressionError(f"Unexpected error: {str(e)}")


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
            
        except (InvalidExpressionError, UnbalancedParenthesesError, DivisionByZeroError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
