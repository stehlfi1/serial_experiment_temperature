
"""
Arithmetic Calculator Module

Implements a console-based arithmetic calculator that supports addition, subtraction,
multiplication, division, and parentheses with correct operator precedence, while adhering
to ISO/IEC 25010 quality standards.

Author: Senior Software Developer
"""

import re
from typing import List, Union


class Calculator:
    """
    Arithmetic Calculator supporting (+, -, *, /) operations with correct precedence and parentheses.

    Methods
    -------
    calculate(expression: str) -> float:
        Evaluates the arithmetic expression and returns the result.
    """

    # Supported operators with precedence and associativity
    OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L'),
    }

    # Regular expression for a token (number, operator, or parentheses)
    TOKEN_PATTERN = re.compile(
        r"""
        (?P<number>     -?\d+(\.\d+)? ) |  # Integer or float (with optional leading '-')
        (?P<operator>   [\+\-\*/]    ) |  # Arithmetic operators
        (?P<lparen>     \(           ) |  # Left parenthesis
        (?P<rparen>     \)           )    # Right parenthesis
        """,
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates the specified arithmetic expression.

        Parameters
        ----------
        expression : str
            Arithmetic expression to evaluate.

        Returns
        -------
        float
            Computed result.

        Raises
        ------
        ValueError
            If the expression is invalid or contains invalid characters.
        ZeroDivisionError
            If division by zero occurs.
        """

        tokens = self._tokenize(expression)
        postfix = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Tokenizes the input arithmetic expression into numbers, operators, and parentheses.

        Returns
        -------
        List[Union[str, float]]
            List of tokens (numbers are converted to float).

        Raises
        ------
        ValueError
            If invalid characters or malformed numbers are present.
        """

        tokens = []
        index = 0
        length = len(expression)
        last_token = None

        while index < length:
            char = expression[index]

            if char.isspace():
                index += 1
                continue

            # Match number (including negatives and floats)
            number_match = re.match(r'-?\d+(\.\d+)?', expression[index:])
            if number_match:
                num_str = number_match.group()
                try:
                    num = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number: {num_str}")
                tokens.append(num)
                index += len(num_str)
                last_token = 'number'
                continue

            # Handle operator or parenthesis
            if char in '+-*/()':
                # Disambiguate unary minus (preceding operators or parentheses)
                if char == '-' and (last_token in (None, 'operator', 'lparen')):
                    # It's a unary minus; try to read the number after '-'
                    next_match = re.match(r'-\d+(\.\d+)?', expression[index:])
                    if next_match:
                        num_str = next_match.group()
                        try:
                            num = float(num_str)
                        except ValueError:
                            raise ValueError(f"Invalid number: {num_str}")
                        tokens.append(num)
                        index += len(num_str)
                        last_token = 'number'
                        continue

                if char in '+-*/':
                    tokens.append(char)
                    last_token = 'operator'
                elif char == '(':
                    tokens.append(char)
                    last_token = 'lparen'
                elif char == ')':
                    tokens.append(char)
                    last_token = 'rparen'
                index += 1
                continue

            raise ValueError(f"Invalid character found: '{char}' at position {index}")

        # Final bracket balance validation here is unnecessary since _infix_to_postfix will perform it
        return tokens

    def _infix_to_postfix(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts infix expression tokens to postfix (RPN) using the Shunting Yard algorithm.

        Returns
        -------
        List[Union[str, float]]
            Tokens in postfix order.

        Raises
        ------
        ValueError
            If the parentheses are unbalanced or the syntax is invalid.
        """

        output = []
        stack = []

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                       ((self.OPERATORS[token][1] == 'L' and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses detected.")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token encountered: {token}")

        while stack:
            top = stack.pop()
            if top == '(' or top == ')':
                raise ValueError("Unbalanced parentheses detected.")
            output.append(top)

        return output

    def _evaluate_postfix(self, tokens: List[Union[str, float]]) -> float:
        """
        Evaluates a postfix (RPN) expression.

        Returns
        -------
        float
            Computed result.

        Raises
        ------
        ZeroDivisionError
            If division by zero occurs.
        ValueError
            If the expression is invalid or contains insufficient operands.
        """

        stack = []

        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                try:
                    b = stack.pop()
                    a = stack.pop()
                except IndexError:
                    raise ValueError("Insufficient operands for operator.")
                # Perform operation
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0.0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in postfix expression: {token}")

        if len(stack) != 1:
            raise ValueError("The input expression is malformed.")

        return stack[0]


if __name__ == "__main__":
    # Example interactive usage & testing
    calc = Calculator()
    print("Arithmetic Calculator (type 'exit' or 'quit' to stop)")

    while True:
        try:
            expr = input("Enter expression: ").strip()
            if expr.lower() in {'exit', 'quit'}:
                print("Exiting calculator.")
                break
            result = calc.calculate(expr)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

# For unit testing, import Calculator and call calculate method with test expressions
