
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
    
    def __init__(self, token_type: TokenType, value: Union[float, str]):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The value of the token (number or operator symbol)
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression is syntactically invalid."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations
    with proper operator precedence and parentheses handling.
    
    Supports: addition (+), subtraction (-), multiplication (*), division (/)
    Handles: integers, floating-point numbers, negative values, parentheses
    """
    
    # Operator precedence mapping (higher values = higher precedence)
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    # Valid operators
    OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression: A string containing the mathematical expression
            
        Returns:
            The result of the calculation as a float
            
        Raises:
            InvalidExpressionError: If the expression is syntactically invalid
            DivisionByZeroError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 2) / 4")
            2.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression cannot be empty")
        
        try:
            # Tokenize the expression
            tokens = self._tokenize(expression)
            
            # Validate tokens
            self._validate_tokens(tokens)
            
            # Convert to postfix notation using Shunting Yard algorithm
            postfix = self._to_postfix(tokens)
            
            # Evaluate the postfix expression
            result = self._evaluate_postfix(postfix)
            
            return float(result)
            
        except (ValueError, TypeError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
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
        expression = expression.replace(' ', '')  # Remove whitespace
        
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including negative numbers and decimals)
            if char.isdigit() or char == '.':
                number_str = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, float(number_str)))
                i += len(number_str)
            
            # Handle operators
            elif char in self.OPERATORS:
                # Handle negative numbers (unary minus)
                if char == '-' and self._is_unary_minus(tokens):
                    number_str = self._extract_number(expression, i)
                    tokens.append(Token(TokenType.NUMBER, float(number_str)))
                    i += len(number_str)
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
            
            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
            
            # Invalid character
            else:
                raise InvalidExpressionError(f"Invalid character: {char}")
        
        return tokens
    
    def _extract_number(self, expression: str, start_index: int) -> str:
        """
        Extracts a complete number (including decimals and negative sign) from the expression.
        
        Args:
            expression: The full expression
            start_index: Starting index of the number
            
        Returns:
            String representation of the number
        """
        i = start_index
        number_str = ""
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Extract digits and decimal point
        decimal_found = False
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                number_str += char
                i += 1
            elif char == '.' and not decimal_found:
                decimal_found = True
                number_str += char
                i += 1
            else:
                break
        
        if not number_str or number_str == '-' or number_str == '.':
            raise InvalidExpressionError("Invalid number format")
        
        return number_str
    
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
        Validates the token sequence for syntactic correctness.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            InvalidExpressionError: If the token sequence is invalid
        """
        if not tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise InvalidExpressionError("Unbalanced parentheses")
        
        # Check for valid token sequences
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError("Invalid operator placement")
                
                # Operators cannot be consecutive (except unary minus handled in tokenization)
                if (i > 0 and tokens[i-1].type == TokenType.OPERATOR):
                    raise InvalidExpressionError("Consecutive operators not allowed")
    
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
                       self.PRECEDENCE[operator_stack[-1].value] >= self.PRECEDENCE[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output.append(operator_stack.pop())
                
                if not operator_stack:
                    raise InvalidExpressionError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in (TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN):
                raise InvalidExpressionError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            postfix_tokens: List of tokens in postfix notation
            
        Returns:
            The result of the evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Invalid expression structure")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                result = self._apply_operator(token.value, operand1, operand2)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression structure")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, operand1: float, operand2: float) -> float:
        """
        Applies an arithmetic operator to two operands.
        
        Args:
            operator: The operator symbol
            operand1: First operand
            operand2: Second operand
            
        Returns:
            Result of the operation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
        """
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise DivisionByZeroError("Division by zero is not allowed")
            return operand1 / operand2
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")


def main():
    """
    Main function to run the calculator in console mode.
    Provides a simple REPL (Read-Eval-Print Loop) interface.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and decimal numbers")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ('quit', 'exit'):
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
result = calc.calculate("2 + 3 * (4 - 1)")  # Returns 11.0
