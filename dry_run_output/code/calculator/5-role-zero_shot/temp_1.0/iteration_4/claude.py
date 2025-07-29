
"""
Console-based Arithmetic Calculator

A robust calculator implementation that supports basic arithmetic operations
with proper operator precedence and parentheses handling.

Author: Senior Software Developer
Compliance: ISO/IEC 25010 Standard
"""

import re
from typing import List, Union, Tuple
from collections import deque


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports:
    - Basic operations: +, -, *, /
    - Parentheses for grouping
    - Both integers and floating-point numbers
    - Negative numbers
    - Proper operator precedence
    
    Thread-safe and follows defensive programming principles.
    """
    
    # Operator precedence mapping (higher value = higher precedence)
    _OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    # Valid operators set for quick lookup
    _VALID_OPERATORS = {'+', '-', '*', '/'}
    
    # Regular expression for tokenizing the input
    _TOKEN_PATTERN = re.compile(r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))')
    
    def __init__(self):
        """Initialize the calculator instance."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: The calculated result
            
        Raises:
            ValueError: If the expression is invalid (syntax errors, invalid characters)
            ZeroDivisionError: If division by zero is attempted
            TypeError: If input is not a string
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(1 + 2) * 3")
            9.0
            >>> calc.calculate("-5 + 3")
            -2.0
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string")
        
        if not expression or expression.isspace():
            raise ValueError("Expression cannot be empty")
        
        # Remove whitespace and validate
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
        Remove whitespace and prepare expression for processing.
        
        Args:
            expression (str): Raw input expression
            
        Returns:
            str: Cleaned expression without whitespace
        """
        return ''.join(expression.split())
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the expression for basic syntax rules.
        
        Args:
            expression (str): Expression to validate
            
        Raises:
            ValueError: If expression contains invalid characters or syntax
        """
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        # Check for invalid characters
        valid_chars = set('0123456789+-*/.() ')
        if not all(char in valid_chars for char in expression):
            invalid_chars = set(expression) - valid_chars
            raise ValueError(f"Invalid characters found: {invalid_chars}")
        
        # Check for balanced parentheses
        if not self._are_parentheses_balanced(expression):
            raise ValueError("Unbalanced parentheses")
        
        # Check for consecutive operators (except negative numbers)
        if self._has_invalid_operator_sequence(expression):
            raise ValueError("Invalid operator sequence")
    
    def _are_parentheses_balanced(self, expression: str) -> bool:
        """
        Check if parentheses are properly balanced.
        
        Args:
            expression (str): Expression to check
            
        Returns:
            bool: True if parentheses are balanced, False otherwise
        """
        balance = 0
        for char in expression:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:  # More closing than opening
                    return False
        return balance == 0
    
    def _has_invalid_operator_sequence(self, expression: str) -> bool:
        """
        Check for invalid consecutive operators.
        
        Args:
            expression (str): Expression to check
            
        Returns:
            bool: True if invalid sequences found, False otherwise
        """
        # Remove parentheses for this check
        expr_no_parens = expression.replace('(', '').replace(')', '')
        
        # Check for consecutive operators (excluding negative numbers)
        prev_char = ''
        for i, char in enumerate(expr_no_parens):
            if char in self._VALID_OPERATORS:
                # Allow negative numbers at start or after operators/opening parenthesis
                if char == '-' and (i == 0 or prev_char in self._VALID_OPERATORS or prev_char == '('):
                    prev_char = char
                    continue
                    
                # Check for consecutive operators
                if prev_char in self._VALID_OPERATORS:
                    return True
                    
            prev_char = char
        
        return False
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Break expression into tokens (numbers, operators, parentheses).
        
        Args:
            expression (str): Expression to tokenize
            
        Returns:
            List[str]: List of tokens
            
        Raises:
            ValueError: If tokenization fails
        """
        # Handle negative numbers by replacing minus signs with placeholders
        processed_expr = self._handle_negative_numbers(expression)
        
        # Find all tokens
        matches = self._TOKEN_PATTERN.findall(processed_expr)
        
        if not matches:
            raise ValueError("No valid tokens found in expression")
        
        # Restore negative numbers
        tokens = []
        for token in matches:
            if token.startswith('NEG'):
                # Convert back to negative number
                number_part = token[3:]  # Remove 'NEG' prefix
                tokens.append('-' + number_part)
            else:
                tokens.append(token)
        
        return tokens
    
    def _handle_negative_numbers(self, expression: str) -> str:
        """
        Replace negative number patterns with placeholders for easier tokenization.
        
        Args:
            expression (str): Original expression
            
        Returns:
            str: Expression with negative number placeholders
        """
        result = ""
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Check for negative number pattern
            if (char == '-' and 
                (i == 0 or expression[i-1] in '(+-*/')):
                
                # Look ahead to find the number
                j = i + 1
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                
                if j > i + 1:  # Found a number after minus
                    number = expression[i+1:j]
                    result += f"NEG{number}"
                    i = j
                else:
                    result += char
                    i += 1
            else:
                result += char
                i += 1
        
        return result
    
    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Convert infix expression to postfix using Shunting Yard algorithm.
        
        Args:
            tokens (List[str]): List of tokens in infix notation
            
        Returns:
            List[str]: List of tokens in postfix notation
        """
        output_queue = deque()
        operator_stack = deque()
        
        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in self._VALID_OPERATORS:
                # Pop operators with higher or equal precedence
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self._VALID_OPERATORS and
                       self._OPERATOR_PRECEDENCE.get(operator_stack[-1], 0) >= 
                       self._OPERATOR_PRECEDENCE.get(token, 0)):
                    output_queue.append(operator_stack.pop())
                
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop until opening parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                
                operator_stack.pop()  # Remove the opening parenthesis
            else:
                raise ValueError(f"Unknown token: {token}")
        
        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1] in '()':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return list(output_queue)
    
    def _is_number(self, token: str) -> bool:
        """
        Check if a token represents a number (including negative numbers).
        
        Args:
            token (str): Token to check
            
        Returns:
            bool: True if token is a number, False otherwise
        """
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def _evaluate_postfix(self, tokens: List[str]) -> float:
        """
        Evaluate postfix expression using stack-based approach.
        
        Args:
            tokens (List[str]): Postfix tokens
            
        Returns:
            float: Result of evaluation
            
        Raises:
            ValueError: If expression is malformed
            ZeroDivisionError: If division by zero is attempted
        """
        if not tokens:
            raise ValueError("Empty expression")
        
        stack = deque()
        
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self._VALID_OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                # Pop operands (note the order!)
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                # Perform operation
                result = self._perform_operation(operand1, operand2, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in postfix expression: {token}")
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        
        return stack[0]
    
    def _perform_operation(self, operand1: float, operand2: float, operator: str) -> float:
        """
        Perform arithmetic operation on two operands.
        
        Args:
            operand1 (float): First operand
            operand2 (float): Second operand
            operator (str): Operation to perform
            
        Returns:
            float: Result of operation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If operator is invalid
        """
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            return operand1 / operand2
        else:
            raise ValueError(f"Unknown operator: {operator}")


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of calculator functionality with basic error handling.
    """
    calc = Calculator()
    
    # Test cases
    test_expressions = [
        "2 + 3 * 4",           # Expected: 14.0
        "(1 + 2) * 3",         # Expected: 9.0
        "-5 + 3",              # Expected: -2.0
        "10 / 2 - 1",          # Expected: 4.0
        "(-3 + 7) * 2",        # Expected: 8.0
        "1.5 * 2.5",           # Expected: 3.75
    ]
    
    print("Calculator Test Results:")
    print("-" * 40)
    
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr:15} = {result}")
        except Exception as e:
            print(f"{expr:15} = Error: {e}")
    
    # Interactive mode
    print("\n" + "=" * 40)
    print("Interactive Calculator (type 'quit' to exit):")
    print("=" * 40)
    
    while True:
        try:
            expression = input("\nEnter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not expression:
                continue
                
            result = calc.calculate(expression)
            print(f"Result: {result}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
