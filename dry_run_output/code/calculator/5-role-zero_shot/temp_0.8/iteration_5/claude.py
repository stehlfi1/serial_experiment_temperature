
"""
Arithmetic Calculator Module

A console-based calculator that evaluates mathematical expressions with support for
basic arithmetic operations, parentheses, and proper operator precedence.

This module implements the Shunting Yard algorithm for expression parsing and
evaluation, adhering to ISO/IEC 25010 software quality standards.
"""

from typing import List, Union, Optional
import re


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when an expression contains invalid syntax or characters."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class Calculator:
    """
    A mathematical expression calculator using the Shunting Yard algorithm.
    
    This calculator supports basic arithmetic operations (+, -, *, /) with proper
    operator precedence and parentheses grouping. It can handle both integers
    and floating-point numbers, including negative values.
    
    The implementation follows ISO/IEC 25010 quality standards for:
    - Functional Suitability: Correct arithmetic evaluation
    - Performance Efficiency: O(n) time complexity
    - Compatibility: Standard Python types and operations
    - Usability: Clear error messages and intuitive interface
    - Reliability: Comprehensive input validation
    - Security: Safe expression evaluation without eval()
    - Maintainability: Clean, modular code structure
    - Portability: Pure Python implementation
    """
    
    # Operator definitions with precedence and associativity
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'left'},
        '-': {'precedence': 1, 'associativity': 'left'},
        '*': {'precedence': 2, 'associativity': 'left'},
        '/': {'precedence': 2, 'associativity': 'left'}
    }
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for new calculation."""
        self._output_queue: List[Union[float, str]] = []
        self._operator_stack: List[str] = []
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): Mathematical expression to evaluate.
                            Supports +, -, *, /, parentheses, and numeric values.
        
        Returns:
            float: The calculated result of the expression.
        
        Raises:
            InvalidExpressionError: If the expression contains invalid syntax.
            UnbalancedParenthesesError: If parentheses are not balanced.
            DivisionByZeroError: If division by zero is attempted.
            ValueError: If the expression is empty or contains invalid numbers.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(2 + 3) * 4")
            20.0
            >>> calc.calculate("-5 + 3.5")
            -1.5
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        self._reset_state()
        
        try:
            # Tokenize and validate the expression
            tokens = self._tokenize(expression)
            self._validate_expression(tokens)
            
            # Convert to postfix notation using Shunting Yard algorithm
            postfix_tokens = self._to_postfix(tokens)
            
            # Evaluate the postfix expression
            result = self._evaluate_postfix(postfix_tokens)
            
            return float(result)
            
        except (ValueError, OverflowError) as e:
            raise InvalidExpressionError(f"Invalid numeric value in expression: {e}")
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression (str): The mathematical expression to tokenize.
        
        Returns:
            List[str]: List of tokens (numbers, operators, parentheses).
        
        Raises:
            InvalidExpressionError: If invalid characters are found.
        """
        # Remove whitespace
        expression = re.sub(r'\s+', '', expression)
        
        # Pattern to match numbers (including negative), operators, and parentheses
        token_pattern = r'(-?\d+\.?\d*)|([+\-*/()])'
        tokens = []
        
        for match in re.finditer(token_pattern, expression):
            token = match.group(0)
            if token:
                tokens.append(token)
        
        # Validate that all characters were matched
        reconstructed = ''.join(tokens)
        if reconstructed != expression:
            invalid_chars = set(expression) - set(reconstructed)
            raise InvalidExpressionError(
                f"Invalid characters found: {', '.join(invalid_chars)}"
            )
        
        return self._handle_negative_numbers(tokens)
    
    def _handle_negative_numbers(self, tokens: List[str]) -> List[str]:
        """
        Process tokens to correctly handle negative numbers and unary minus.
        
        Args:
            tokens (List[str]): Raw tokens from tokenization.
        
        Returns:
            List[str]: Processed tokens with proper negative number handling.
        """
        processed_tokens = []
        
        for i, token in enumerate(tokens):
            if token == '-':
                # Check if this is a unary minus (negative number)
                is_unary = (i == 0 or 
                           tokens[i-1] in self.OPERATORS or 
                           tokens[i-1] == '(')
                
                if is_unary and i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if self._is_number(next_token):
                        # Combine minus with the next number
                        processed_tokens.append('-' + next_token)
                        tokens[i + 1] = ''  # Mark as processed
                    elif next_token == '(':
                        # Handle -(expression) by inserting 0
                        processed_tokens.extend(['0', '-'])
                    else:
                        processed_tokens.append(token)
                else:
                    processed_tokens.append(token)
            elif token:  # Skip empty tokens
                processed_tokens.append(token)
        
        return processed_tokens
    
    def _is_number(self, token: str) -> bool:
        """
        Check if a token represents a valid number.
        
        Args:
            token (str): Token to check.
        
        Returns:
            bool: True if token is a valid number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def _validate_expression(self, tokens: List[str]) -> None:
        """
        Validate the tokenized expression for syntax errors.
        
        Args:
            tokens (List[str]): Tokenized expression.
        
        Raises:
            InvalidExpressionError: If syntax errors are found.
            UnbalancedParenthesesError: If parentheses are unbalanced.
        """
        if not tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for token in tokens:
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise UnbalancedParenthesesError("Mismatched closing parenthesis")
        
        if paren_count != 0:
            raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        # Validate token sequence
        self._validate_token_sequence(tokens)
    
    def _validate_token_sequence(self, tokens: List[str]) -> None:
        """
        Validate the sequence of tokens for proper syntax.
        
        Args:
            tokens (List[str]): Tokenized expression.
        
        Raises:
            InvalidExpressionError: If invalid token sequences are found.
        """
        for i, token in enumerate(tokens):
            if self._is_number(token):
                # Number should not be followed by another number or opening parenthesis
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if self._is_number(next_token) or next_token == '(':
                        raise InvalidExpressionError(
                            f"Invalid sequence: {token} followed by {next_token}"
                        )
            
            elif token in self.OPERATORS:
                # Operator should not be at the end or followed by another operator
                if i == len(tokens) - 1:
                    raise InvalidExpressionError(f"Expression cannot end with operator: {token}")
                if i + 1 < len(tokens) and tokens[i + 1] in self.OPERATORS:
                    raise InvalidExpressionError(
                        f"Invalid sequence: operator {token} followed by operator {tokens[i + 1]}"
                    )
            
            elif token == '(':
                # Opening parenthesis should not be followed by closing parenthesis or operator
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if next_token == ')':
                        raise InvalidExpressionError("Empty parentheses not allowed")
                    if next_token in self.OPERATORS and next_token != '-':
                        raise InvalidExpressionError(
                            f"Opening parenthesis cannot be followed by operator: {next_token}"
                        )
            
            elif token == ')':
                # Closing parenthesis should not be followed by number or opening parenthesis
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if self._is_number(next_token) or next_token == '(':
                        raise InvalidExpressionError(
                            f"Closing parenthesis cannot be followed by: {next_token}"
                        )
    
    def _to_postfix(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens (List[str]): Tokenized infix expression.
        
        Returns:
            List[Union[float, str]]: Expression in postfix notation.
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if self._is_number(token):
                output_queue.append(float(token))
            
            elif token in self.OPERATORS:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.OPERATORS and
                       (self.OPERATORS[operator_stack[-1]]['precedence'] > 
                        self.OPERATORS[token]['precedence'] or
                        (self.OPERATORS[operator_stack[-1]]['precedence'] == 
                         self.OPERATORS[token]['precedence'] and
                         self.OPERATORS[token]['associativity'] == 'left'))):
                    output_queue.append(operator_stack.pop())
                
                operator_stack.append(token)
            
            elif token == '(':
                operator_stack.append(token)
            
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Remove the '('
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, postfix_tokens: List[Union[float, str]]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens (List[Union[float, str]]): Expression in postfix notation.
        
        Returns:
            float: The calculated result.
        
        Raises:
            DivisionByZeroError: If division by zero is attempted.
            InvalidExpressionError: If the expression is malformed.
        """
        stack = []
        
        for token in postfix_tokens:
            if isinstance(token, float):
                stack.append(token)
            
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operator")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                result = self._apply_operator(token, operand1, operand2)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: incorrect number of operands")
        
        return stack[0]
    
    def _apply_operator(self, operator: str, operand1: float, operand2: float) -> float:
        """
        Apply an arithmetic operator to two operands.
        
        Args:
            operator (str): The operator to apply (+, -, *, /).
            operand1 (float): First operand.
            operand2 (float): Second operand.
        
        Returns:
            float: Result of the operation.
        
        Raises:
            DivisionByZeroError: If attempting to divide by zero.
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
    Main function to run the calculator in interactive mode.
    
    Provides a console interface for users to input mathematical expressions
    and receive calculated results with proper error handling.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Enter 'quit' or 'exit' to stop")
    print("-" * 40)
    
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
            
        except CalculatorError as e:
            print(f"Calculator Error: {e}")
        except ValueError as e:
            print(f"Input Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
