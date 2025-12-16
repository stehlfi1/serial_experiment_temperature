
"""
Console-based Arithmetic Calculator
Implements ISO/IEC 25010 software quality characteristics:
- Functional Suitability
- Reliability
- Usability
- Performance Efficiency
- Security
- Maintainability
- Portability
"""

import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses, 
    and both integer and floating point (including negative) numbers.
    """

    # Regular expression for valid tokens: numbers, operators, parentheses
    TOKEN_REGEX = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([+\-*/()]))\s*")

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the computed value.

        Args:
            expression (str): An arithmetic expression

        Returns:
            float: The evaluated result

        Raises:
            ValueError: For syntax errors, invalid characters, or invalid operations
            ZeroDivisionError: For division by zero
        """
        if not isinstance(expression, str):
            raise ValueError("Input must be a string.")
        
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenizes the input string into numbers, operators, and parentheses.

        Args:
            expression (str): Input arithmetic expression

        Returns:
            List[str]: List of tokens

        Raises:
            ValueError: If invalid characters are present
        """
        if not expression or not isinstance(expression, str):
            raise ValueError("Expression cannot be empty and must be a string.")

        tokens = []
        position = 0
        length = len(expression)

        while position < length:
            match = self.TOKEN_REGEX.match(expression, position)
            if not match:
                raise ValueError(f"Invalid character at position {position}: '{expression[position]}'")
            number, operator = match.groups()
            if number:
                tokens.append(number)
            elif operator:
                # Handle unary minus for negative numbers:
                if operator == '-' and (not tokens or tokens[-1] in ('+', '-', '*', '/', '(')):
                    # Parse as negative number
                    next_match = self.TOKEN_REGEX.match(expression, match.end())
                    if next_match and next_match.group(1):
                        neg_number = '-' + next_match.group(1)
                        tokens.append(neg_number)
                        position = next_match.end()
                        continue
                    else:
                        raise ValueError(f"Invalid negative number at position {position}")
                tokens.append(operator)
            position = match.end()
        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the syntax of the token list.

        Args:
            tokens (List[str]): List of tokens

        Raises:
            ValueError: For syntax errors or unbalanced parentheses
        """
        if not tokens:
            raise ValueError("Expression cannot be empty.")

        paren_balance = 0
        prev_token = None
        for idx, token in enumerate(tokens):
            if token == '(':
                paren_balance += 1
            elif token == ')':
                paren_balance -= 1
                if paren_balance < 0:
                    raise ValueError("Unbalanced parentheses detected.")

            if token in ('+', '-', '*', '/'):
                if idx == 0 or tokens[idx-1] in ('+', '-', '*', '/', '('):
                    raise ValueError(f"Invalid syntax: Operator '{token}' at position {idx}.")
                if idx == len(tokens) - 1:
                    raise ValueError(f"Invalid syntax: Trailing operator '{token}'.")

            prev_token = token

        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses detected.")

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Convert list of tokens to Reverse Polish Notation (RPN) using Shunting Yard algorithm.

        Args:
            tokens (List[str]): List of input tokens

        Returns:
            List[Union[str, float]]: RPN expression as list

        Operators precedence: *, / > +, -
        Operators associativity: left-associative
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output: List[Union[str, float]] = []
        operators: List[str] = []

        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in precedence:
                while (operators and operators[-1] in precedence and
                       precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if not operators or operators[-1] != '(':
                    raise ValueError("Mismatched parentheses.")
                operators.pop()  # Remove '('
        while operators:
            op = operators.pop()
            if op in ('(', ')'):
                raise ValueError("Mismatched parentheses in operators stack.")
            output.append(op)
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates the RPN expression and returns the computed result.

        Args:
            rpn (List[Union[str, float]]): RPN expression

        Returns:
            float: Evaluated result

        Raises:
            ValueError: For invalid RPN expressions
            ZeroDivisionError: For division by zero
        """
        stack: List[float] = []

        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    raise ValueError(f"Insufficient values for operator '{token}'.")
                right = stack.pop()
                left = stack.pop()
                result = None
                if token == '+':
                    result = left + right
                elif token == '-':
                    result = left - right
                elif token == '*':
                    result = left * right
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero.")
                    result = left / right
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: '{token}'")
        if len(stack) != 1:
            raise ValueError("Invalid expression: stack has leftover values.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if a string token is a valid integer or float.

        Args:
            token (str): Token to check

        Returns:
            bool: True if token is numeric, False otherwise
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    # Console UI for testing
    calc = Calculator()
    print("Welcome to Console Calculator. Type 'exit' to quit.")
    while True:
        expr = input("Enter expression: ")
        if expr.strip().lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        try:
            result = calc.calculate(expr)
            print(f"Result: {result}")
        except ZeroDivisionError as zde:
            print(f"Error: {zde}")
        except ValueError as ve:
            print(f"Error: {ve}")
