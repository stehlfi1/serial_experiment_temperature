
"""
Console-based Arithmetic Calculator

A high-quality calculator implementation that evaluates mathematical expressions
with support for basic arithmetic operations and parentheses, following
ISO/IEC 25010 quality standards.
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


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports:
    - Basic arithmetic operations: +, -, *, /
    - Parentheses for grouping
    - Integer and floating-point numbers (including negative values)
    - Proper operator precedence
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
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
            expression: String containing the mathematical expression
            
        Returns:
            float: The calculated result
            
        Raises:
            ValueError: If the expression is invalid
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
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        self._reset_state()
        
        try:
            # Step 1: Tokenize the expression
            self._tokenize(expression)
            
            # Step 2: Validate tokens
            self._validate_tokens()
            
            # Step 3: Convert to postfix notation using Shunting Yard algorithm
            postfix_tokens = self._to_postfix()
            
            # Step 4: Evaluate postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, ZeroDivisionError):
            raise
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def _tokenize(self, expression: str) -> None:
        """
        Convert the input expression into tokens.
        
        Args:
            expression: The mathematical expression to tokenize
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Remove whitespace and validate characters
        cleaned_expr = re.sub(r'\s+', '', expression)
        
        # Check for invalid characters
        valid_chars = r'[0-9+\-*/().]'
        if not re.match(f'^{valid_chars}+$', cleaned_expr):
            invalid_chars = re.sub(valid_chars, '', cleaned_expr)
            raise ValueError(f"Invalid characters in expression: {invalid_chars}")
        
        i = 0
        while i < len(cleaned_expr):
            char = cleaned_expr[i]
            
            if char.isdigit() or char == '.':
                # Parse number (integer or float)
                number_str = ''
                while i < len(cleaned_expr) and (cleaned_expr[i].isdigit() or cleaned_expr[i] == '.'):
                    number_str += cleaned_expr[i]
                    i += 1
                
                # Validate number format
                if number_str.count('.') > 1:
                    raise ValueError(f"Invalid number format: {number_str}")
                
                try:
                    number_value = float(number_str)
                    self._tokens.append(Token(TokenType.NUMBER, number_value))
                except ValueError:
                    raise ValueError(f"Invalid number: {number_str}")
                
            elif char in '+-*/':
                # Handle unary minus
                if char == '-' and self._is_unary_context():
                    # Parse negative number
                    i += 1
                    if i >= len(cleaned_expr) or not (cleaned_expr[i].isdigit() or cleaned_expr[i] == '.'):
                        raise ValueError("Invalid unary minus usage")
                    
                    number_str = '-'
                    while i < len(cleaned_expr) and (cleaned_expr[i].isdigit() or cleaned_expr[i] == '.'):
                        number_str += cleaned_expr[i]
                        i += 1
                    
                    if number_str.count('.') > 1:
                        raise ValueError(f"Invalid number format: {number_str}")
                    
                    try:
                        number_value = float(number_str)
                        self._tokens.append(Token(TokenType.NUMBER, number_value))
                    except ValueError:
                        raise ValueError(f"Invalid number: {number_str}")
                else:
                    self._tokens.append(Token(TokenType.OPERATOR, char))
                    i += 1
                    
            elif char == '(':
                self._tokens.append(Token(TokenType.LEFT_PAREN, char))
                i += 1
                
            elif char == ')':
                self._tokens.append(Token(TokenType.RIGHT_PAREN, char))
                i += 1
                
            else:
                raise ValueError(f"Unexpected character: {char}")
    
    def _is_unary_context(self) -> bool:
        """
        Check if the current context allows for a unary minus operator.
        
        Returns:
            bool: True if unary minus is valid in current context
        """
        if not self._tokens:
            return True
        
        last_token = self._tokens[-1]
        return last_token.type in [TokenType.OPERATOR, TokenType.LEFT_PAREN]
    
    def _validate_tokens(self) -> None:
        """
        Validate the tokenized expression for structural correctness.
        
        Raises:
            ValueError: If the token sequence is invalid
        """
        if not self._tokens:
            raise ValueError("Empty expression")
        
        # Check balanced parentheses
        paren_count = 0
        for token in self._tokens:
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
        
        if paren_count > 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
        
        # Validate token sequence
        for i, token in enumerate(self._tokens):
            if token.type == TokenType.OPERATOR:
                # Operators cannot be at the beginning or end
                if i == 0 or i == len(self._tokens) - 1:
                    raise ValueError("Invalid operator placement")
                
                # Operators cannot be adjacent
                if (self._tokens[i-1].type == TokenType.OPERATOR or 
                    self._tokens[i+1].type == TokenType.OPERATOR):
                    raise ValueError("Adjacent operators are not allowed")
            
            elif token.type == TokenType.LEFT_PAREN:
                # Left parenthesis cannot be followed by an operator (except unary minus)
                if (i < len(self._tokens) - 1 and 
                    self._tokens[i+1].type == TokenType.OPERATOR):
                    raise ValueError("Invalid expression after opening parenthesis")
            
            elif token.type == TokenType.RIGHT_PAREN:
                # Right parenthesis cannot be preceded by an operator
                if (i > 0 and self._tokens[i-1].type == TokenType.OPERATOR):
                    raise ValueError("Invalid expression before closing parenthesis")
    
    def _to_postfix(self) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Returns:
            List[Token]: Tokens in postfix order
        """
        output_queue: List[Token] = []
        operator_stack: List[Token] = []
        
        for token in self._tokens:
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
                
                operator_stack.pop()  # Remove the left parenthesis
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1].type in [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN]:
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens: List of tokens in postfix order
            
        Returns:
            float: The calculated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack: List[float] = []
        
        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
                
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
        Apply an arithmetic operator to two operands.
        
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
                raise ZeroDivisionError("Division by zero is not allowed")
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
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
