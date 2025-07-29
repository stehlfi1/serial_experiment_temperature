
import re
from typing import List, Union
from enum import Enum


class Token:
    """Represents a token in the mathematical expression."""
    
    def __init__(self, type_: str, value: Union[float, str]):
        self.type = type_
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class TokenType:
    """Constants for token types."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class OperatorPrecedence:
    """Defines operator precedence levels."""
    PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression is syntactically invalid."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""
    pass


class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations
    with proper operator precedence and parentheses handling.
    
    Features:
    - Addition (+), subtraction (-), multiplication (*), division (/)
    - Parentheses support with proper nesting
    - Correct operator precedence
    - Support for integers and floating-point numbers
    - Support for negative numbers
    - Comprehensive error handling
    """
    
    def __init__(self):
        """Initialize the calculator."""
        self._operators = {'+', '-', '*', '/'}
        self._token_pattern = re.compile(
            r'(\d+\.?\d*)|([+\-*/])|(\()|(\))|(\s+)'
        )
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: Result of the calculation
            
        Raises:
            InvalidExpressionError: If the expression is syntactically invalid
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
        if not expression or not expression.strip():
            raise InvalidExpressionError("Empty expression")
        
        try:
            tokens = self._tokenize(expression)
            tokens = self._handle_unary_operators(tokens)
            self._validate_tokens(tokens)
            postfix = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix)
            return result
        except (ValueError, IndexError) as e:
            raise InvalidExpressionError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Tokenizes the input expression into a list of tokens.
        
        Args:
            expression (str): The expression to tokenize
            
        Returns:
            List[Token]: List of tokens
            
        Raises:
            InvalidExpressionError: If invalid characters are found
        """
        tokens = []
        
        for match in self._token_pattern.finditer(expression):
            number, operator, left_paren, right_paren, whitespace = match.groups()
            
            if whitespace:
                continue  # Skip whitespace
            elif number:
                tokens.append(Token(TokenType.NUMBER, float(number)))
            elif operator:
                tokens.append(Token(TokenType.OPERATOR, operator))
            elif left_paren:
                tokens.append(Token(TokenType.LEFT_PAREN, left_paren))
            elif right_paren:
                tokens.append(Token(TokenType.RIGHT_PAREN, right_paren))
        
        # Check for invalid characters
        tokenized_length = sum(len(str(token.value)) for token in tokens)
        clean_expression = re.sub(r'\s+', '', expression)
        
        if tokenized_length != len(clean_expression):
            raise InvalidExpressionError("Invalid characters in expression")
        
        return tokens
    
    def _handle_unary_operators(self, tokens: List[Token]) -> List[Token]:
        """
        Handles unary operators (negative numbers) by converting them to binary operations.
        
        Args:
            tokens (List[Token]): Original token list
            
        Returns:
            List[Token]: Modified token list with unary operators handled
        """
        if not tokens:
            return tokens
        
        result = []
        
        for i, token in enumerate(tokens):
            # Check if this minus sign is unary
            if (token.type == TokenType.OPERATOR and token.value == '-' and
                (i == 0 or tokens[i-1].type in [TokenType.LEFT_PAREN, TokenType.OPERATOR])):
                # Insert 0 before the unary minus to make it binary
                result.append(Token(TokenType.NUMBER, 0.0))
            
            result.append(token)
        
        return result
    
    def _validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validates the token sequence for syntactic correctness.
        
        Args:
            tokens (List[Token]): Tokens to validate
            
        Raises:
            InvalidExpressionError: If tokens are invalid
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
                    raise InvalidExpressionError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise InvalidExpressionError("Unbalanced parentheses")
        
        # Validate token sequence
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the end or followed by another operator
                if i == len(tokens) - 1:
                    raise InvalidExpressionError("Expression cannot end with operator")
                if (i < len(tokens) - 1 and 
                    tokens[i + 1].type == TokenType.OPERATOR):
                    raise InvalidExpressionError("Consecutive operators not allowed")
            elif token.type == TokenType.NUMBER:
                # Numbers cannot be followed by left parentheses or other numbers
                if (i < len(tokens) - 1 and 
                    tokens[i + 1].type in [TokenType.LEFT_PAREN, TokenType.NUMBER]):
                    raise InvalidExpressionError("Invalid number sequence")
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Converts infix notation to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens (List[Token]): Infix tokens
            
        Returns:
            List[Token]: Postfix tokens
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       OperatorPrecedence.PRECEDENCE[operator_stack[-1].value] >= 
                       OperatorPrecedence.PRECEDENCE[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluates postfix notation tokens.
        
        Args:
            tokens (List[Token]): Postfix tokens
            
        Returns:
            float: Evaluation result
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If the expression is malformed
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operation")
                
                right = stack.pop()
                left = stack.pop()
                
                result = self._apply_operator(token.value, left, right)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression structure")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Applies the specified operator to two operands.
        
        Args:
            operator (str): The operator (+, -, *, /)
            left (float): Left operand
            right (float): Right operand
            
        Returns:
            float: Result of the operation
            
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


def main():
    """
    Main function for console-based calculator interaction.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Type 'quit' or 'exit' to exit")
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
