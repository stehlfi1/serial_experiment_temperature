
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
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid characters or syntax."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence
    and parentheses. Handles both integers and floating-point numbers including
    negative values.
    """
    
    def __init__(self):
        """Initialize the calculator with operator precedence mapping."""
        self._operator_precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
        
        self._valid_operators = {'+', '-', '*', '/'}
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): The mathematical expression to evaluate
            
        Returns:
            float: The calculated result
            
        Raises:
            InvalidExpressionError: If the expression contains invalid characters
            UnbalancedParenthesesError: If parentheses are not balanced
            DivisionByZeroError: If division by zero is attempted
            
        Example:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * (4 - 1)")
            11.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        # Remove whitespace and validate characters
        expression = self._preprocess_expression(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Validate token sequence
        self._validate_tokens(tokens)
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._to_postfix(tokens)
        
        # Evaluate postfix expression
        result = self._evaluate_postfix(postfix_tokens)
        
        return result
    
    def _preprocess_expression(self, expression: str) -> str:
        """
        Preprocesses the expression by removing whitespace and validating characters.
        
        Args:
            expression (str): Raw expression string
            
        Returns:
            str: Cleaned expression
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        # Remove all whitespace
        clean_expr = re.sub(r'\s+', '', expression)
        
        # Validate characters (numbers, operators, parentheses, decimal points)
        valid_pattern = r'^[0-9+\-*/().]+$'
        if not re.match(valid_pattern, clean_expr):
            raise InvalidExpressionError("Expression contains invalid characters")
        
        return clean_expr
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Tokenizes the expression into a list of Token objects.
        
        Args:
            expression (str): The expression to tokenize
            
        Returns:
            List[Token]: List of tokens
            
        Raises:
            InvalidExpressionError: If tokenization fails
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimal numbers)
                number_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                
                try:
                    number = float(number_str)
                    tokens.append(Token(TokenType.NUMBER, number))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number format: {number_str}")
                
                continue
            
            elif char in self._valid_operators:
                # Handle unary minus
                if char == '-' and (not tokens or 
                                  tokens[-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]):
                    # This is a unary minus, parse the following number
                    i += 1
                    if i >= len(expression):
                        raise InvalidExpressionError("Invalid unary minus at end of expression")
                    
                    # Parse the number after unary minus
                    number_str = '-'
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        number_str += expression[i]
                        i += 1
                    
                    try:
                        number = float(number_str)
                        tokens.append(Token(TokenType.NUMBER, number))
                    except ValueError:
                        raise InvalidExpressionError(f"Invalid number format: {number_str}")
                    
                    continue
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
            
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
            
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
            
            else:
                raise InvalidExpressionError(f"Unexpected character: {char}")
            
            i += 1
        
        return tokens
    
    def _validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validates the sequence of tokens for syntax correctness.
        
        Args:
            tokens (List[Token]): List of tokens to validate
            
        Raises:
            InvalidExpressionError: If token sequence is invalid
            UnbalancedParenthesesError: If parentheses are unbalanced
        """
        if not tokens:
            raise InvalidExpressionError("No tokens found in expression")
        
        # Check balanced parentheses
        paren_count = 0
        for token in tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise UnbalancedParenthesesError("Unmatched closing parenthesis")
        
        if paren_count != 0:
            raise UnbalancedParenthesesError("Unmatched opening parenthesis")
        
        # Validate token sequence
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError("Operator cannot be at beginning or end")
                
                # Operators cannot be followed by another operator
                if tokens[i + 1].type == TokenType.OPERATOR:
                    raise InvalidExpressionError("Consecutive operators not allowed")
    
    def _to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Converts infix notation to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens (List[Token]): Tokens in infix notation
            
        Returns:
            List[Token]: Tokens in postfix notation
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
            
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self._operator_precedence[operator_stack[-1].value] >= 
                       self._operator_precedence[token.value]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output_queue.append(operator_stack.pop())
                
                # Remove the left parenthesis
                if operator_stack:
                    operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluates a postfix expression and returns the result.
        
        Args:
            tokens (List[Token]): Tokens in postfix notation
            
        Returns:
            float: The evaluated result
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operator")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(left_operand, token.value, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression structure")
        
        return stack[0]
    
    def _perform_operation(self, left: float, operator: str, right: float) -> float:
        """
        Performs a single arithmetic operation.
        
        Args:
            left (float): Left operand
            operator (str): Operator (+, -, *, /)
            right (float): Right operand
            
        Returns:
            float: Result of the operation
            
        Raises:
            DivisionByZeroError: If attempting to divide by zero
        """
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise DivisionByZeroError("Cannot divide by zero")
            return left / right
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")


def main():
    """
    Main function to demonstrate the calculator functionality.
    Provides a simple console interface for user interaction.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and decimal numbers")
    print("Enter 'quit' to exit\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() == 'quit':
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


calc = Calculator()
print(calc.calculate("2 + 3 * 4"))        # 14.0
print(calc.calculate("(2 + 3) * 4"))      # 20.0
print(calc.calculate("-5 + 3"))           # -2.0
print(calc.calculate("10 / (2 + 3)"))     # 2.0
