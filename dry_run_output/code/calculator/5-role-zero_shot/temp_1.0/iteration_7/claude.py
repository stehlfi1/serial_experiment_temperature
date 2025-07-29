
"""
High-quality arithmetic calculator implementation following ISO/IEC 25010 standards.

This module provides a Calculator class that can evaluate arithmetic expressions
with proper operator precedence, parentheses support, and comprehensive error handling.
"""

from typing import List, Union
import re


class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid syntax or characters."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class Token:
    """Represents a token in the arithmetic expression."""
    
    def __init__(self, token_type: str, value: Union[str, float]):
        """
        Initialize a token.
        
        Args:
            token_type: Type of token ('NUMBER', 'OPERATOR', 'LPAREN', 'RPAREN')
            value: The actual value of the token
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class ExpressionTokenizer:
    """Tokenizes arithmetic expressions into a list of tokens."""
    
    # Regular expression pattern for valid tokens
    TOKEN_PATTERN = re.compile(r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))')
    
    @staticmethod
    def tokenize(expression: str) -> List[Token]:
        """
        Tokenize an arithmetic expression.
        
        Args:
            expression: The arithmetic expression to tokenize
            
        Returns:
            List of tokens representing the expression
            
        Raises:
            InvalidExpressionError: If the expression contains invalid characters
        """
        # Remove whitespace
        expression = expression.replace(' ', '')
        
        if not expression:
            raise InvalidExpressionError("Empty expression")
        
        # Validate that expression contains only valid characters
        valid_chars = set('0123456789+-*/().')
        if not all(char in valid_chars for char in expression):
            invalid_chars = set(expression) - valid_chars
            raise InvalidExpressionError(f"Invalid characters found: {invalid_chars}")
        
        # Find all tokens using regex
        token_matches = ExpressionTokenizer.TOKEN_PATTERN.findall(expression)
        
        # Verify that tokenization captured the entire expression
        reconstructed = ''.join(token_matches)
        if reconstructed != expression:
            raise InvalidExpressionError("Expression contains invalid token sequences")
        
        tokens = []
        for i, match in enumerate(token_matches):
            if match in '()':
                token_type = 'LPAREN' if match == '(' else 'RPAREN'
                tokens.append(Token(token_type, match))
            elif match in '+-*/':
                # Handle unary minus
                if (match == '-' and 
                    (i == 0 or token_matches[i-1] in '(+-*/')):
                    tokens.append(Token('OPERATOR', 'unary_minus'))
                else:
                    tokens.append(Token('OPERATOR', match))
            else:
                # It's a number
                try:
                    number_value = float(match)
                    tokens.append(Token('NUMBER', number_value))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number format: {match}")
        
        return tokens


class ExpressionValidator:
    """Validates arithmetic expressions for correctness."""
    
    @staticmethod
    def validate_parentheses(tokens: List[Token]) -> None:
        """
        Validate that parentheses are balanced.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            UnbalancedParenthesesError: If parentheses are not balanced
        """
        balance = 0
        for token in tokens:
            if token.type == 'LPAREN':
                balance += 1
            elif token.type == 'RPAREN':
                balance -= 1
                if balance < 0:
                    raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        if balance != 0:
            raise UnbalancedParenthesesError("Unbalanced parentheses")
    
    @staticmethod
    def validate_syntax(tokens: List[Token]) -> None:
        """
        Validate expression syntax.
        
        Args:
            tokens: List of tokens to validate
            
        Raises:
            InvalidExpressionError: If syntax is invalid
        """
        if not tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Check for valid token sequences
        for i, token in enumerate(tokens):
            if token.type == 'OPERATOR' and token.value != 'unary_minus':
                # Binary operators need operands on both sides
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError("Operator without operand")
                
                prev_token = tokens[i-1]
                next_token = tokens[i+1]
                
                if (prev_token.type not in ['NUMBER', 'RPAREN'] or 
                    next_token.type not in ['NUMBER', 'LPAREN', 'OPERATOR']):
                    if not (next_token.type == 'OPERATOR' and next_token.value == 'unary_minus'):
                        raise InvalidExpressionError("Invalid operator placement")


class ExpressionEvaluator:
    """Evaluates tokenized arithmetic expressions using the Shunting Yard algorithm."""
    
    # Operator precedence mapping
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, 'unary_minus': 3}
    
    @staticmethod
    def evaluate(tokens: List[Token]) -> float:
        """
        Evaluate a list of tokens using the Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens representing the expression
            
        Returns:
            The result of the arithmetic expression
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If expression is malformed
        """
        # Convert to postfix notation using Shunting Yard algorithm
        postfix = ExpressionEvaluator._to_postfix(tokens)
        
        # Evaluate postfix expression
        return ExpressionEvaluator._evaluate_postfix(postfix)
    
    @staticmethod
    def _to_postfix(tokens: List[Token]) -> List[Token]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens: List of tokens in infix notation
            
        Returns:
            List of tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            if token.type == 'NUMBER':
                output.append(token)
            elif token.type == 'OPERATOR':
                while (operator_stack and 
                       operator_stack[-1].type == 'OPERATOR' and
                       ExpressionEvaluator.PRECEDENCE[operator_stack[-1].value] >= 
                       ExpressionEvaluator.PRECEDENCE[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.type == 'LPAREN':
                operator_stack.append(token)
            elif token.type == 'RPAREN':
                while (operator_stack and 
                       operator_stack[-1].type != 'LPAREN'):
                    output.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # Remove the left parenthesis
        
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    @staticmethod
    def _evaluate_postfix(postfix_tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_tokens: List of tokens in postfix notation
            
        Returns:
            The result of the evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
            InvalidExpressionError: If expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if token.type == 'NUMBER':
                stack.append(token.value)
            elif token.type == 'OPERATOR':
                if token.value == 'unary_minus':
                    if not stack:
                        raise InvalidExpressionError("Invalid expression")
                    operand = stack.pop()
                    stack.append(-operand)
                else:
                    if len(stack) < 2:
                        raise InvalidExpressionError("Invalid expression")
                    
                    right_operand = stack.pop()
                    left_operand = stack.pop()
                    
                    if token.value == '+':
                        result = left_operand + right_operand
                    elif token.value == '-':
                        result = left_operand - right_operand
                    elif token.value == '*':
                        result = left_operand * right_operand
                    elif token.value == '/':
                        if right_operand == 0:
                            raise DivisionByZeroError("Division by zero")
                        result = left_operand / right_operand
                    
                    stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression")
        
        return stack[0]


class Calculator:
    """
    A high-quality arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports basic arithmetic operations (+, -, *, /), parentheses,
    and follows proper operator precedence. It handles both integers and floating-point
    numbers, including negative values.
    """
    
    def __init__(self):
        """Initialize the calculator."""
        self._tokenizer = ExpressionTokenizer()
        self._validator = ExpressionValidator()
        self._evaluator = ExpressionEvaluator()
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression: A string containing the arithmetic expression to evaluate.
                       Supported operations: +, -, *, /
                       Supports parentheses and negative numbers.
                       Example: "3.5 + 2 * (10 - 4) / 3"
        
        Returns:
            The numerical result of the expression as a float.
        
        Raises:
            InvalidExpressionError: If the expression contains invalid syntax or characters.
            UnbalancedParenthesesError: If parentheses are not properly balanced.
            DivisionByZeroError: If attempting to divide by zero.
            CalculatorError: For other calculation-related errors.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) * 2")
            10.0
            >>> calc.calculate("-5 + 3")
            -2.0
        """
        try:
            # Step 1: Tokenize the expression
            tokens = self._tokenizer.tokenize(expression)
            
            # Step 2: Validate the expression
            self._validator.validate_parentheses(tokens)
            self._validator.validate_syntax(tokens)
            
            # Step 3: Evaluate the expression
            result = self._evaluator.evaluate(tokens)
            
            return result
            
        except CalculatorError:
            # Re-raise calculator-specific errors
            raise
        except Exception as e:
            # Convert unexpected errors to calculator errors
            raise CalculatorError(f"Unexpected error during calculation: {str(e)}")


# Example usage and testing
if __name__ == "__main__":
    def main():
        """Demonstrate calculator usage with various test cases."""
        calc = Calculator()
        
        # Test cases
        test_cases = [
            "2 + 3 * 4",           # Expected: 14.0
            "(10 - 5) * 2",        # Expected: 10.0
            "-5 + 3",              # Expected: -2.0
            "10 / 2 + 3",          # Expected: 8.0
            "((2 + 3) * 4)",       # Expected: 20.0
            "3.14 + 2.86",         # Expected: 6.0
            "-(-5)",               # Expected: 5.0
            "100 / (25 - 20)",     # Expected: 20.0
        ]
        
        print("Calculator Test Cases:")
        print("-" * 40)
        
        for expression in test_cases:
            try:
                result = calc.calculate(expression)
                print(f"{expression:<20} = {result}")
            except CalculatorError as e:
                print(f"{expression:<20} = Error: {e}")
        
        # Interactive mode
        print("\n" + "-" * 40)
        print("Interactive Calculator (type 'quit' to exit):")
        
        while True:
            try:
                user_input = input("Enter expression: ").strip()
                if user_input.lower() == 'quit':
                    break
                
                result = calc.calculate(user_input)
                print(f"Result: {result}")
                
            except CalculatorError as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    main()
