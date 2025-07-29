
from typing import List, Union, Tuple
import re


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supports basic arithmetic operations (+, -, *, /) with proper operator precedence,
    parentheses, and both integer and floating-point numbers (including negative values).
    
    This implementation follows ISO/IEC 25010 quality standards for:
    - Functional Suitability: Correct arithmetic operations with proper precedence
    - Performance Efficiency: Efficient parsing and evaluation algorithms
    - Compatibility: Works with standard Python environments
    - Usability: Clear error messages and intuitive interface
    - Reliability: Robust error handling and input validation
    - Security: Protection against malicious input (no eval() usage)
    - Maintainability: Clean, modular, well-documented code
    - Portability: Pure Python implementation
    """
    
    # Define operator precedence (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    OPERATORS = {'+', '-', '*', '/'}
    
    def __init__(self):
        """Initialize the Calculator instance."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: Result of the evaluated expression
            
        Raises:
            ValueError: If the expression contains invalid characters, 
                       unbalanced parentheses, or invalid syntax
            ZeroDivisionError: If division by zero is attempted
            
        Examples:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 2) / 4")
            2.0
            >>> calc.calculate("-5 + 3")
            -2.0
        """
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string")
        
        if not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        # Validate and tokenize the expression
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        
        # Convert to postfix notation and evaluate
        postfix = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        
        return result
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenize the input expression into numbers, operators, and parentheses.
        
        Args:
            expression (str): Input expression
            
        Returns:
            List[str]: List of tokens
            
        Raises:
            ValueError: If invalid characters are found
        """
        # Remove whitespace
        expression = re.sub(r'\s+', '', expression)
        
        # Validate characters
        valid_chars = r'[0-9+\-*/.()]'
        if not re.match(f'^{valid_chars}+$', expression):
            raise ValueError("Invalid characters in expression")
        
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                # Parse number (integer or float)
                number = self._parse_number(expression, i)
                tokens.append(number[0])
                i = number[1]
            elif char in '+-':
                # Handle unary minus/plus or binary operators
                if (i == 0 or expression[i-1] in '(+*/-'):
                    # Unary operator - parse as part of number
                    if i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        number = self._parse_number(expression, i)
                        tokens.append(number[0])
                        i = number[1]
                    else:
                        raise ValueError("Invalid unary operator usage")
                else:
                    # Binary operator
                    tokens.append(char)
                    i += 1
            elif char in '*/()':
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character: {char}")
        
        return tokens
    
    def _parse_number(self, expression: str, start_index: int) -> Tuple[str, int]:
        """
        Parse a number (integer or float) from the expression starting at given index.
        
        Args:
            expression (str): Input expression
            start_index (int): Starting index for parsing
            
        Returns:
            Tuple[str, int]: Parsed number as string and next index to process
            
        Raises:
            ValueError: If number format is invalid
        """
        i = start_index
        number_str = ""
        
        # Handle sign
        if i < len(expression) and expression[i] in '+-':
            number_str += expression[i]
            i += 1
        
        has_decimal = False
        
        while i < len(expression):
            char = expression[i]
            if char.isdigit():
                number_str += char
            elif char == '.' and not has_decimal:
                has_decimal = True
                number_str += char
            else:
                break
            i += 1
        
        # Validate number format
        if not number_str or number_str in ['+', '-', '.', '+.', '-.']:
            raise ValueError("Invalid number format")
        
        # Check if it's just a decimal point
        if number_str.replace('+', '').replace('-', '') == '.':
            raise ValueError("Invalid number format")
        
        return number_str, i
    
    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validate the tokenized expression for correct syntax.
        
        Args:
            tokens (List[str]): List of tokens to validate
            
        Raises:
            ValueError: If syntax errors are found
        """
        if not tokens:
            raise ValueError("Empty expression")
        
        # Check balanced parentheses
        paren_count = 0
        for token in tokens:
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses")
        
        # Check operator and operand placement
        for i, token in enumerate(tokens):
            if token in self.OPERATORS:
                # Operators must have operands or parentheses around them
                if i == 0 or i == len(tokens) - 1:
                    raise ValueError("Invalid operator placement")
                
                prev_token = tokens[i - 1]
                next_token = tokens[i + 1]
                
                # Previous token should be number or closing parenthesis
                if not (self._is_number(prev_token) or prev_token == ')'):
                    raise ValueError("Invalid operator placement")
                
                # Next token should be number or opening parenthesis
                if not (self._is_number(next_token) or next_token == '('):
                    raise ValueError("Invalid operator placement")
            
            elif token == '(':
                # Opening parenthesis validation
                if i < len(tokens) - 1:
                    next_token = tokens[i + 1]
                    if next_token == ')':
                        raise ValueError("Empty parentheses")
            
            elif token == ')':
                # Closing parenthesis must follow number or another closing parenthesis
                if i == 0:
                    raise ValueError("Invalid closing parenthesis")
                
                prev_token = tokens[i - 1]
                if not (self._is_number(prev_token) or prev_token == ')'):
                    raise ValueError("Invalid closing parenthesis placement")
    
    def _is_number(self, token: str) -> bool:
        """
        Check if a token represents a valid number.
        
        Args:
            token (str): Token to check
            
        Returns:
            bool: True if token is a valid number
        """
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Convert infix expression to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens (List[str]): Tokenized infix expression
            
        Returns:
            List[str]: Expression in postfix notation
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.OPERATORS and
                       self.OPERATOR_PRECEDENCE[operator_stack[-1]] >= self.OPERATOR_PRECEDENCE[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()  # Remove the '('
        
        # Pop remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _evaluate_postfix(self, postfix_tokens: List[str]) -> float:
        """
        Evaluate postfix expression and return the result.
        
        Args:
            postfix_tokens (List[str]): Expression in postfix notation
            
        Returns:
            float: Evaluation result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Malformed expression")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                result = self._perform_operation(operand1, operand2, token)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Malformed expression")
        
        return stack[0]
    
    def _perform_operation(self, operand1: float, operand2: float, operator: str) -> float:
        """
        Perform arithmetic operation on two operands.
        
        Args:
            operand1 (float): First operand
            operand2 (float): Second operand
            operator (str): Arithmetic operator
            
        Returns:
            float: Operation result
            
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
                raise ZeroDivisionError("Division by zero")
            return operand1 / operand2
        else:
            raise ValueError(f"Invalid operator: {operator}")


def main():
    """
    Console interface for the calculator application.
    Provides interactive calculation functionality with error handling.
    """
    calculator = Calculator()
    
    print("=== Arithmetic Calculator ===")
    print("Supported operations: +, -, *, /")
    print("Supports parentheses and negative numbers")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 30)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
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
