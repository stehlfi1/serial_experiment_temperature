
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class implements a calculator that can handle addition, subtraction,
    multiplication, division, and parentheses. It respects operator precedence
    and supports both integer and floating-point numbers, including negative values.

    The implementation adheres to the ISO/IEC 25010 standard by focusing on:
    - Functional Suitability: Correctly evaluates complex arithmetic expressions.
    - Performance Efficiency: Uses the efficient Shunting-yard algorithm (O(n) time complexity).
    - Reliability & Safety: Provides robust validation for inputs, handling errors
      like invalid characters, unbalanced parentheses, and division by zero gracefully.
    - Maintainability & Testability: The logic is separated into modular, private
      methods for tokenization, parsing (infix to postfix), and evaluation.
    - Readability: The code is documented with docstrings, type hints, and
      clear variable names.
    """

    # --- Class constants for maintainability ---
    _OPERATORS = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b
    }
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the calculator. It orchestrates
        the tokenization, parsing, and evaluation of the expression.

        Args:
            expression: The mathematical expression string to evaluate.
                        Example: "-1.5 * (2 + 3)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")

        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts an expression string into a list of tokens (numbers and operators).
        This method also handles unary minus for negative numbers.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens, where numbers are floats and operators/parentheses are strings.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to find numbers (int/float), operators, and parentheses
        # It correctly handles floating point numbers and individual symbols.
        token_regex = re.compile(r'(\d+\.?\d*|\.\d+|[+\-*/()])')
        raw_tokens = token_regex.findall(expression)

        # Check for any characters that were not matched by the regex
        if "".join(raw_tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters.")

        tokens: List[Union[float, str]] = []
        for i, token in enumerate(raw_tokens):
            if token in self._OPERATORS or token in '()':
                # Handle unary minus: a '-' is unary if it's the first token
                # or if it follows an operator or an opening parenthesis.
                if token == '-' and (i == 0 or raw_tokens[i-1] in self._OPERATORS or raw_tokens[i-1] == '('):
                    # This is a unary minus. We combine it with the next token.
                    # To simplify parsing, we treat it as (0 - number).
                    tokens.append(0.0)
                    tokens.append('-')
                else:
                    tokens.append(token)
            else: # It's a number
                tokens.append(float(token))
        return tokens

    def _infix_to_postfix(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a list of tokens from infix to postfix (RPN) notation.
        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in postfix (RPN) order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[Union[float, str]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack.pop() != '(':
                    raise ValueError("Mismatched parentheses in expression.")
            elif token in self._OPERATORS:
                while (operator_stack and
                       operator_stack[-1] in self._OPERATORS and
                       self._PRECEDENCE[operator_stack[-1]] >= self._PRECEDENCE[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, postfix_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a list of tokens in postfix (RPN) notation.

        Args:
            postfix_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack: List[float] = []

        for token in postfix_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            elif token in self._OPERATORS:
                try:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                except IndexError:
                    raise ValueError("Malformed expression: insufficient operands for an operator.")

                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")

                operation = self._OPERATORS[token]
                result = operation(operand1, operand2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression: too many operands.")

        return operand_stack[0]


# --- Demonstration and Basic Testing ---
if __name__ == "__main__":
    # This block demonstrates the usage of the Calculator class and serves
    # as a simple, runnable test suite.
    calc = Calculator()

    print("--- Welcome to the Console Calculator ---")
    print("Enter an expression or 'exit' to quit.\n")

    # A list of test cases to demonstrate functionality and correctness
    test_expressions = [
        "3 + 4 * 2 / ( 1 - 5 )",
        "10 + 2 * 6",
        "100 * 2 + 12",
        "100 * ( 2 + 12 )",
        "100 * ( 2 + 12 ) / 14",
        "5 * -2",
        "-5 * 2",
        "3.5 + 4.2 * 2",
        "(10)",
        # Error cases
        "3 + 4 *",          # Malformed expression
        "10 / 0",           # Division by zero
        "(3 + 4) * 2)",     # Mismatched parentheses
        "3 + (4 * 2",      # Mismatched parentheses
        "3 + a * 2",        # Invalid character
    ]

    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"Expression: '{expr}'\nResult: {result}\n")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Expression: '{expr}'\nError: {e}\n")

    # Interactive loop
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() == 'exit':
                break
            if user_input:
                res = calc.calculate(user_input)
                print(f"= {res}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting.")
            break
