
"""
Console-based Arithmetic Calculator

A high-quality, maintainable calculator implementation that supports basic arithmetic
operations with proper error handling and validation according to ISO/IEC 25010 standards.
"""

import re
from typing import List, Union
from enum import Enum


class TokenType(Enum):
    """Enumeration of token types for expression parsing."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Represents a token in the mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: Union[str, float]):
        """
        Initialize a token.
        
        Args:
            token_type: The type of the token
            value: The value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class ExpressionValidator:
    """Validates mathematical expressions for correctness."""
    
    @staticmethod
    def validate_characters(expression: str) -> None:
        """
        Validate that expression contains only allowed characters.
        
        Args:
            expression: The mathematical expression to validate
            
        Raises:
            ValueError: If expression contains invalid characters
        """
        allowed_pattern = r'^[0-9+\-*/().\s]+$'
        if not re.match(allowed_pattern, expression):
            raise ValueError("Expression contains invalid characters")
    
    @staticmethod
    def validate_parentheses(expression: str) -> None:
        """
        Validate that parentheses are balanced in the expression.
        
        Args:
            expression: The mathematical expression to validate
            
        Raises:
            ValueError: If parentheses are unbalanced
        """
        balance = 0
        for char in expression:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Unbalanced parentheses: closing parenthesis without opening")
        
        if balance != 0:
            raise ValueError("Unbalanced parentheses: unclosed opening parenthesis")
    
    @staticmethod
    def validate_expression_structure(tokens: List[Token]) -> None:
        """
        Validate the structural correctness of tokenized expression.
        
        Args:
            tokens: List of tokens representing the expression
            
        Raises:
            ValueError: If expression structure is invalid
        """
        if not tokens:
            raise ValueError("Empty expression")
        
        # Check for consecutive operators or invalid token sequences
        for i, token in enumerate(tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end (except unary minus)
                if i == 0 and token.value != '-':
                    raise ValueError("Expression cannot start with an operator")
                if i == len(tokens) - 1:
                    raise ValueError("Expression cannot end with an operator")
                
                # Check for consecutive operators (except unary minus)
                if i > 0 and tokens[i-1].type == TokenType.OPERATOR and token.value != '-':
                    raise ValueError("Consecutive operators are not allowed")


class ExpressionTokenizer:
    """Tokenizes mathematical expressions into a list of tokens."""
    
    def tokenize(self, expression: str) -> List[Token]:
        """
        Convert a mathematical expression string into a list of tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Returns:
            List of tokens representing the expression
            
        Raises:
            ValueError: If the expression contains invalid syntax
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle numbers (including decimals and negative numbers)
            if char.isdigit() or char == '.':
                number_str = self._extract_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, float(number_str)))
                i += len(number_str)
            
            # Handle operators
            elif char in '+-*/':
                # Handle unary minus
                if (char == '-' and 
                    (not tokens or 
                     tokens[-1].type in [TokenType.OPERATOR, TokenType.LEFT_PAREN])):
                    # This is a unary minus, combine with the next number
                    i += 1
                    if i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        number_str = self._extract_number(expression, i)
                        tokens.append(Token(TokenType.NUMBER, -float(number_str)))
                        i += len(number_str)
                    else:
                        raise ValueError("Invalid unary minus usage")
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
            
            else:
                raise ValueError(f"Invalid character: {char}")
        
        return tokens
    
    def _extract_number(self, expression: str, start_index: int) -> str:
        """
        Extract a complete number (including decimals) from the expression.
        
        Args:
            expression: The full expression string
            start_index: Starting index of the number
            
        Returns:
            String representation of the number
        """
        i = start_index
        has_decimal = False
        
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                i += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                i += 1
            else:
                break
        
        return expression[start_index:i]


class ExpressionEvaluator:
    """Evaluates tokenized mathematical expressions using the Shunting Yard algorithm."""
    
    # Operator precedence mapping
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def evaluate(self, tokens: List[Token]) -> float:
        """
        Evaluate a list of tokens using the Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens representing the mathematical expression
            
        Returns:
            The result of the mathematical expression
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        # Convert infix to postfix notation
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate postfix expression
        return self._evaluate_postfix(postfix)
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix notation to postfix notation using Shunting Yard algorithm.
        
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
                    raise ValueError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens: List of tokens in postfix notation
            
        Returns:
            The result of the evaluation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._perform_operation(left_operand, right_operand, token.value)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: malformed")
        
        return stack[0]
    
    def _perform_operation(self, left: float, right: float, operator: str) -> float:
        """
        Perform a mathematical operation on two operands.
        
        Args:
            left: Left operand
            right: Right operand
            operator: Mathematical operator
            
        Returns:
            Result of the operation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")


class Calculator:
    """
    A comprehensive calculator class that evaluates mathematical expressions.
    
    This calculator supports basic arithmetic operations (+, -, *, /), parentheses,
    and handles both integers and floating-point numbers including negative values.
    """
    
    def __init__(self):
        """Initialize the calculator with its components."""
        self.validator = ExpressionValidator()
        self.tokenizer = ExpressionTokenizer()
        self.evaluator = ExpressionEvaluator()
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing the mathematical expression to evaluate.
                       Supports +, -, *, /, parentheses, integers, and floating-point numbers.
        
        Returns:
            The numerical result of the expression evaluation.
        
        Raises:
            ValueError: If the expression contains invalid characters, has unbalanced
                       parentheses, or is structurally invalid.
            ZeroDivisionError: If the expression attempts division by zero.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) * 2")
            10.0
            >>> calc.calculate("-3.5 + 2.1")
            -1.4
        """
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string")
        
        expression = expression.strip()
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        try:
            # Validate the expression
            self.validator.validate_characters(expression)
            self.validator.validate_parentheses(expression)
            
            # Tokenize the expression
            tokens = self.tokenizer.tokenize(expression)
            
            # Validate token structure
            self.validator.validate_expression_structure(tokens)
            
            # Evaluate the expression
            result = self.evaluator.evaluate(tokens)
            
            return result
            
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise with more context if needed
            raise e
        except Exception as e:
            # Catch any unexpected errors and wrap them
            raise ValueError(f"Unexpected error during calculation: {str(e)}")


def main():
    """
    Main function to run the calculator in interactive mode.
    
    Provides a console interface for users to input mathematical expressions
    and receive calculated results with proper error handling.
    """
    calculator = Calculator()
    
    print("=== Console Arithmetic Calculator ===")
    print("Supported operations: +, -, *, /, ()")
    print("Supports integers and floating-point numbers")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("\nEnter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not expression:
                print("Please enter a valid expression.")
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
