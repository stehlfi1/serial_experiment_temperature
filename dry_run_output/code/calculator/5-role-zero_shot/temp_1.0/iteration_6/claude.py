
"""
A high-quality console-based arithmetic calculator implementation.

This module provides a Calculator class that can evaluate mathematical expressions
containing basic arithmetic operations (+, -, *, /) with proper operator precedence
and parentheses support.

Author: Senior Software Developer
Version: 1.0.0
"""

import re
from typing import List, Union


class Calculator:
    """
    A calculator class that evaluates arithmetic expressions without using eval().
    
    This implementation uses the Shunting Yard algorithm to convert infix notation
    to postfix notation, then evaluates the postfix expression using a stack.
    
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
    
    # Valid operators
    OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the Calculator instance."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): The mathematical expression to evaluate.
                            Must contain only numbers, operators (+, -, *, /),
                            parentheses, and whitespace.
        
        Returns:
            float: The result of the mathematical expression.
        
        Raises:
            ValueError: If the expression contains invalid characters,
                       has unbalanced parentheses, or is malformed.
            ZeroDivisionError: If division by zero is attempted.
            
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
        
        # Clean and validate the expression
        cleaned_expression = self._clean_expression(expression)
        self._validate_expression(cleaned_expression)
        
        # Tokenize the expression
        tokens = self._tokenize(cleaned_expression)
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix_tokens)
        
        return result
    
    def _clean_expression(self, expression: str) -> str:
        """
        Clean the expression by removing whitespace and normalizing format.
        
        Args:
            expression (str): The raw expression string.
            
        Returns:
            str: The cleaned expression string.
        """
        # Remove all whitespace
        cleaned = re.sub(r'\s+', '', expression)
        return cleaned
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the expression for proper format and characters.
        
        Args:
            expression (str): The expression to validate.
            
        Raises:
            ValueError: If the expression is invalid.
        """
        # Check for valid characters only
        valid_chars = set('0123456789+-*/.()_')
        if not all(c in valid_chars for c in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Check for balanced parentheses
        if not self._has_balanced_parentheses(expression):
            raise ValueError("Unbalanced parentheses")
        
        # Check for empty parentheses
        if '()' in expression:
            raise ValueError("Empty parentheses are not allowed")
    
    def _has_balanced_parentheses(self, expression: str) -> bool:
        """
        Check if parentheses are balanced in the expression.
        
        Args:
            expression (str): The expression to check.
            
        Returns:
            bool: True if parentheses are balanced, False otherwise.
        """
        balance = 0
        for char in expression:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenize the expression into numbers, operators, and parentheses.
        
        Args:
            expression (str): The expression to tokenize.
            
        Returns:
            List[str]: List of tokens.
            
        Raises:
            ValueError: If the expression is malformed.
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (including decimal numbers)
                number = self._parse_number(expression, i)
                tokens.append(number)
                i += len(number)
            elif char in self.OPERATORS:
                # Handle negative numbers
                if char == '-' and self._is_negative_sign(tokens):
                    # This is a negative sign, parse the negative number
                    number = self._parse_negative_number(expression, i)
                    tokens.append(number)
                    i += len(number)
                else:
                    # Regular operator
                    tokens.append(char)
                    i += 1
            elif char in '()':
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character: {char}")
        
        # Validate token sequence
        self._validate_token_sequence(tokens)
        return tokens
    
    def _parse_number(self, expression: str, start_index: int) -> str:
        """
        Parse a number starting at the given index.
        
        Args:
            expression (str): The full expression.
            start_index (int): The starting index of the number.
            
        Returns:
            str: The parsed number as a string.
        """
        end_index = start_index
        decimal_count = 0
        
        while end_index < len(expression):
            char = expression[end_index]
            if char.isdigit():
                end_index += 1
            elif char == '.' and decimal_count == 0:
                decimal_count += 1
                end_index += 1
            else:
                break
        
        number = expression[start_index:end_index]
        
        # Validate number format
        if number == '.' or number.endswith('.') and len(number) == 1:
            raise ValueError("Invalid number format")
        
        return number
    
    def _parse_negative_number(self, expression: str, start_index: int) -> str:
        """
        Parse a negative number starting at the given index.
        
        Args:
            expression (str): The full expression.
            start_index (int): The starting index of the negative sign.
            
        Returns:
            str: The parsed negative number as a string.
        """
        if start_index + 1 >= len(expression):
            raise ValueError("Invalid negative number")
        
        # Skip the negative sign and parse the actual number
        number_part = self._parse_number(expression, start_index + 1)
        return '-' + number_part
    
    def _is_negative_sign(self, tokens: List[str]) -> bool:
        """
        Determine if a minus sign is a negative sign or subtraction operator.
        
        Args:
            tokens (List[str]): The current list of tokens.
            
        Returns:
            bool: True if it's a negative sign, False if it's subtraction.
        """
        if not tokens:
            return True
        
        last_token = tokens[-1]
        
        # It's a negative sign if the last token is an operator or opening parenthesis
        return last_token in self.OPERATORS or last_token == '('
    
    def _validate_token_sequence(self, tokens: List[str]) -> None:
        """
        Validate the sequence of tokens for proper mathematical expression format.
        
        Args:
            tokens (List[str]): The list of tokens to validate.
            
        Raises:
            ValueError: If the token sequence is invalid.
        """
        if not tokens:
            raise ValueError("Empty expression")
        
        # Check for consecutive operators
        for i in range(len(tokens) - 1):
            current = tokens[i]
            next_token = tokens[i + 1]
            
            # Two consecutive operators (except for negative numbers)
            if (current in self.OPERATORS and next_token in self.OPERATORS):
                raise ValueError("Consecutive operators are not allowed")
            
            # Operator followed by closing parenthesis
            if current in self.OPERATORS and next_token == ')':
                raise ValueError("Operator cannot be followed by closing parenthesis")
            
            # Opening parenthesis followed by operator (except negative)
            if (current == '(' and next_token in self.OPERATORS and 
                next_token != '-'):
                raise ValueError("Opening parenthesis cannot be followed by operator")
        
        # First token validation
        first_token = tokens[0]
        if first_token in self.OPERATORS and first_token != '-':
            raise ValueError("Expression cannot start with operator")
        
        # Last token validation
        last_token = tokens[-1]
        if last_token in self.OPERATORS:
            raise ValueError("Expression cannot end with operator")
    
    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Convert infix notation to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens (List[str]): List of tokens in infix notation.
            
        Returns:
            List[str]: List of tokens in postfix notation.
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.OPERATORS and
                       self.OPERATOR_PRECEDENCE[operator_stack[-1]] >= 
                       self.OPERATOR_PRECEDENCE[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Remove the '('
        
        while operator_stack:
            if operator_stack[-1] in '()':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _is_number(self, token: str) -> bool:
        """
        Check if a token is a number (including negative numbers).
        
        Args:
            token (str): The token to check.
            
        Returns:
            bool: True if the token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def _evaluate_postfix(self, postfix_tokens: List[str]) -> float:
        """
        Evaluate a postfix expression using a stack.
        
        Args:
            postfix_tokens (List[str]): List of tokens in postfix notation.
            
        Returns:
            float: The result of the evaluation.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression is malformed.
        """
        if not postfix_tokens:
            raise ValueError("Empty postfix expression")
        
        stack = []
        
        for token in postfix_tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                result = self._perform_operation(operand1, operand2, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in postfix expression: {token}")
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: malformed")
        
        return stack[0]
    
    def _perform_operation(self, operand1: float, operand2: float, 
                          operator: str) -> float:
        """
        Perform a single arithmetic operation.
        
        Args:
            operand1 (float): The first operand.
            operand2 (float): The second operand.
            operator (str): The operator (+, -, *, /).
            
        Returns:
            float: The result of the operation.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If an invalid operator is provided.
        """
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise ZeroDivisionError("Division by zero")
            return operand1 / operand2
        else:
            raise ValueError(f"Invalid operator: {operator}")


def main():
    """
    Main function to run the calculator in console mode.
    
    Provides a simple command-line interface for the calculator.
    """
    calculator = Calculator()
    
    print("=== Console Arithmetic Calculator ===")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and negative numbers")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 40)
    
    while True:
        try:
            expression = input("\nEnter expression: ").strip()
            
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
