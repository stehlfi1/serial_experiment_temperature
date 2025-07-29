
"""
Console-based Arithmetic Calculator

A high-quality calculator implementation that evaluates mathematical expressions
with support for basic arithmetic operations and parentheses while adhering
to ISO/IEC 25010 quality standards.
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
    
    def __init__(self, token_type: TokenType, value: Union[float, str]):
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


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator
    precedence and parentheses handling. Uses the Shunting Yard algorithm
    for expression parsing and evaluation.
    """
    
    # Operator precedence mapping (higher values = higher precedence)
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    # Valid operators
    VALID_OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            float: The calculated result
            
        Raises:
            ValueError: If the expression is invalid or contains unsupported operations
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) * 2")
            10.0
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        # Remove whitespace and validate basic format
        expression = expression.replace(" ", "")
        self._validate_expression_format(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Validate tokens
        self._validate_tokens(tokens)
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix_tokens)
        
        return result
    
    def _validate_expression_format(self, expression: str) -> None:
        """
        Validates the basic format of the expression.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        # Check for valid characters only
        valid_pattern = r'^[0-9+\-*/().]+$'
        if not re.match(valid_pattern, expression):
            raise ValueError("Expression contains invalid characters")
        
        # Check for balanced parentheses
        paren_count = 0
        for char in expression:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: closing parenthesis without opening")
        
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: unclosed opening parenthesis")
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Tokenizes the expression into a list of tokens.
        
        Args:
            expression: The expression to tokenize
            
        Returns:
            List[Token]: List of tokens representing the expression
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Handle numbers (including decimals)
                number_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                
                try:
                    number_value = float(number_str)
                    tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                continue
            
            elif char in self.VALID_OPERATORS:
                # Handle operators, including unary minus
                if char == '-' and self._is_unary_minus(tokens):
                    # This is a unary minus, treat as negative number
                    i += 1
                    if i >= len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                        raise ValueError("Invalid unary minus: must be followed by a number")
                    
                    # Parse the negative number
                    number_str = "-"
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        number_str += expression[i]
                        i += 1
                    
                    try:
                        number_value = float(number_str)
                        tokens.append(Token(TokenType.NUMBER, number_value))
                    except ValueError:
                        raise ValueError(f"Invalid number format: {number_str}")
                    continue
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
            
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
            
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
            
            else:
                raise ValueError(f"Invalid character: {char}")
            
            i += 1
        
        return tokens
    
    def _is_unary_minus(self, tokens: List[Token]) -> bool:
        """
        Determines if a minus sign should be treated as unary.
        
        Args:
            tokens: Current list of tokens
            
        Returns:
            bool: True if the minus should be treated as unary
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        return (last_token.type == TokenType.OPERATOR or 
                last_token.type == TokenType.LEFT_PAREN)
    
    def _validate_tokens(self, tokens: List[Token]) -> None:
        """
        Validates the sequence of tokens for logical consistency.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            ValueError: If token sequence is invalid
        """
        if not tokens:
            raise ValueError("Empty expression")
        
        # Check for consecutive operators or invalid sequences
        for i in range(len(tokens)):
            current_token = tokens[i]
            
            if i > 0:
                prev_token = tokens[i - 1]
                
                # Two consecutive operators (not allowed)
                if (current_token.type == TokenType.OPERATOR and 
                    prev_token.type == TokenType.OPERATOR):
                    raise ValueError("Consecutive operators not allowed")
                
                # Operator followed by right parenthesis
                if (prev_token.type == TokenType.OPERATOR and 
                    current_token.type == TokenType.RIGHT_PAREN):
                    raise ValueError("Operator cannot be followed by closing parenthesis")
                
                # Left parenthesis followed by operator (except unary minus, handled in tokenization)
                if (prev_token.type == TokenType.LEFT_PAREN and 
                    current_token.type == TokenType.OPERATOR):
                    raise ValueError("Opening parenthesis cannot be followed by operator")
            
            # First token cannot be a binary operator
            if i == 0 and current_token.type == TokenType.OPERATOR:
                raise ValueError("Expression cannot start with an operator")
            
            # Last token cannot be an operator
            if i == len(tokens) - 1 and current_token.type == TokenType.OPERATOR:
                raise ValueError("Expression cannot end with an operator")
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Converts infix notation to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens in infix notation
            
        Returns:
            List[Token]: List of tokens in postfix notation
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
            
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.OPERATOR_PRECEDENCE[operator_stack[-1].value] >= 
                       self.OPERATOR_PRECEDENCE[token.value]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RIGHT_PAREN:
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                
                # Pop the left parenthesis
                operator_stack.pop()
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in (TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN):
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            tokens: List of tokens in postfix notation
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator")
                
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                result = self._apply_operator(token.value, left_operand, right_operand)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: incorrect number of operands")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, left: float, right: float) -> float:
        """
        Applies an arithmetic operator to two operands.
        
        Args:
            operator: The operator to apply
            left: Left operand
            right: Right operand
            
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
                raise ZeroDivisionError("Division by zero")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {operator}")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ('quit', 'exit'):
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}\n")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
