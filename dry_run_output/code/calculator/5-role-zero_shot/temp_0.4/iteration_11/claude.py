
"""
High-Quality Console-Based Arithmetic Calculator

This module implements a robust arithmetic calculator that supports basic operations
with proper operator precedence and parentheses handling, adhering to ISO/IEC 25010
quality standards.

Author: Senior Software Developer
Version: 1.0.0
"""

import re
from typing import List, Union, Tuple
from enum import Enum


class TokenType(Enum):
    """Enumeration of token types for expression parsing."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Represents a token in the mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: Union[float, str]):
        """
        Initialize a token.
        
        Args:
            token_type (TokenType): The type of the token
            value (Union[float, str]): The value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        """String representation of the token for debugging."""
        return f"Token({self.type}, {self.value})"


class ExpressionValidator:
    """Validates mathematical expressions for correctness."""
    
    @staticmethod
    def validate_characters(expression: str) -> None:
        """
        Validate that expression contains only allowed characters.
        
        Args:
            expression (str): The expression to validate
            
        Raises:
            ValueError: If invalid characters are found
        """
        allowed_pattern = r'^[0-9+\-*/().\s]*$'
        if not re.match(allowed_pattern, expression):
            raise ValueError("Invalid characters in expression. Only numbers, +, -, *, /, (, ), and . are allowed.")
    
    @staticmethod
    def validate_parentheses(expression: str) -> None:
        """
        Validate that parentheses are balanced.
        
        Args:
            expression (str): The expression to validate
            
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
                    raise ValueError("Unbalanced parentheses: closing parenthesis without matching opening.")
        
        if balance != 0:
            raise ValueError("Unbalanced parentheses: unclosed opening parenthesis.")
    
    @staticmethod
    def validate_expression_structure(expression: str) -> None:
        """
        Validate the overall structure of the expression.
        
        Args:
            expression (str): The expression to validate
            
        Raises:
            ValueError: If expression structure is invalid
        """
        if not expression.strip():
            raise ValueError("Empty expression.")
        
        # Check for consecutive operators
        operator_pattern = r'[+\-*/]{2,}'
        if re.search(operator_pattern, expression):
            raise ValueError("Consecutive operators are not allowed.")
        
        # Check for operators at the beginning or end (except minus for negative numbers)
        if re.match(r'[+*/]', expression.strip()):
            raise ValueError("Expression cannot start with +, *, or /.")
        
        if re.search(r'[+\-*/]$', expression.strip()):
            raise ValueError("Expression cannot end with an operator.")


class ExpressionTokenizer:
    """Tokenizes mathematical expressions into a list of tokens."""
    
    def tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize the expression into a list of tokens.
        
        Args:
            expression (str): The mathematical expression to tokenize
            
        Returns:
            List[Token]: List of tokens representing the expression
            
        Raises:
            ValueError: If the expression contains invalid tokens
        """
        tokens = []
        i = 0
        expression = expression.replace(' ', '')  # Remove whitespace
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimals)
                number_str, i = self._parse_number(expression, i)
                tokens.append(Token(TokenType.NUMBER, float(number_str)))
            elif char == '-':
                # Handle negative numbers vs subtraction
                if self._is_negative_number(tokens):
                    number_str, i = self._parse_number(expression, i)
                    tokens.append(Token(TokenType.NUMBER, float(number_str)))
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
            elif char in '+-*/':
                tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
            else:
                raise ValueError(f"Invalid character: {char}")
        
        return tokens
    
    def _parse_number(self, expression: str, start_index: int) -> Tuple[str, int]:
        """
        Parse a number from the expression starting at the given index.
        
        Args:
            expression (str): The expression being parsed
            start_index (int): The starting index for parsing
            
        Returns:
            Tuple[str, int]: The parsed number string and the next index
        """
        i = start_index
        number_str = ''
        
        # Handle negative sign
        if i < len(expression) and expression[i] == '-':
            number_str += expression[i]
            i += 1
        
        # Parse digits and decimal point
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
            raise ValueError("Invalid number format.")
        
        return number_str, i
    
    def _is_negative_number(self, tokens: List[Token]) -> bool:
        """
        Determine if a minus sign represents a negative number.
        
        Args:
            tokens (List[Token]): Current list of tokens
            
        Returns:
            bool: True if the minus represents a negative number
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)


class ExpressionEvaluator:
    """Evaluates tokenized mathematical expressions using the Shunting Yard algorithm."""
    
    # Operator precedence mapping
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def evaluate(self, tokens: List[Token]) -> float:
        """
        Evaluate the tokenized expression using the Shunting Yard algorithm.
        
        Args:
            tokens (List[Token]): List of tokens to evaluate
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        # Convert infix to postfix using Shunting Yard algorithm
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate postfix expression
        return self._evaluate_postfix(postfix)
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix notation to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens (List[Token]): Tokens in infix notation
            
        Returns:
            List[Token]: Tokens in postfix notation
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
                    raise ValueError("Mismatched parentheses.")
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise ValueError("Mismatched parentheses.")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens (List[Token]): Tokens in postfix notation
            
        Returns:
            float: The result of the evaluation
            
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
                    raise ValueError("Invalid expression: insufficient operands.")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(token.value, left_operand, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: malformed structure.")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator (str): The operator to apply
            left (float): Left operand
            right (float): Right operand
            
        Returns:
            float: Result of the operation
            
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
                raise ZeroDivisionError("Division by zero is not allowed.")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")


class Calculator:
    """
    High-quality arithmetic calculator supporting basic operations with proper precedence.
    
    This calculator supports addition (+), subtraction (-), multiplication (*), and division (/)
    with proper operator precedence and parentheses handling. It validates input expressions
    and provides detailed error messages for invalid inputs.
    """
    
    def __init__(self):
        """Initialize the calculator with its components."""
        self._validator = ExpressionValidator()
        self._tokenizer = ExpressionTokenizer()
        self._evaluator = ExpressionEvaluator()
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): The mathematical expression to evaluate
            
        Returns:
            float: The result of the calculation
            
        Raises:
            ValueError: If the expression is invalid or malformed
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5 + 3")
            -2.0
        """
        try:
            # Validate the expression
            self._validator.validate_characters(expression)
            self._validator.validate_parentheses(expression)
            self._validator.validate_expression_structure(expression)
            
            # Tokenize the expression
            tokens = self._tokenizer.tokenize(expression)
            
            # Evaluate the expression
            result = self._evaluator.evaluate(tokens)
            
            return result
            
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise with context for better error handling
            raise type(e)(f"Error evaluating expression '{expression}': {str(e)}")


def main():
    """
    Main function to run the calculator in interactive mode.
    
    Provides a console interface for users to input mathematical expressions
    and receive calculated results or error messages.
    """
    calculator = Calculator()
    
    print("=== High-Quality Arithmetic Calculator ===")
    print("Supported operations: +, -, *, /, ()")
    print("Enter 'quit' or 'exit' to stop.")
    print("=" * 45)
    
    while True:
        try:
            expression = input("\nEnter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Thank you for using the calculator!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
