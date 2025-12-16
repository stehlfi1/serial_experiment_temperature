
"""
A high-quality, console-based arithmetic calculator adhering to ISO/IEC 25010.

This module provides a Calculator class capable of parsing and evaluating
standard arithmetic expressions from a string format.

ISO/IEC 25010 Compliance:
- Functional Suitability: Correctly evaluates expressions with +, -, *, /, and ().
- Performance Efficiency: Implements the Shunting-yard algorithm for efficient O(n) evaluation.
- Reliability: Mature and fault-tolerant with robust error handling for invalid
  expressions and mathematical errors (e.g., division by zero).
- Security: Avoids `eval()` to prevent arbitrary code execution vulnerabilities.
- Maintainability: Highly modular with clear separation of concerns (tokenizing,
  parsing, evaluation), making it easy to analyze, test, and modify.
- Portability: Uses only standard Python libraries, ensuring it can run on any
  platform with a Python interpreter.
"""

import re
from typing import List, Union

# Define a type alias for tokens for better readability.
Token = Union[float, str]


class Calculator:
    """
    A robust calculator that evaluates arithmetic expressions from a string.

    This class parses and computes expressions containing integers, floating-point
    numbers, parentheses, and the basic arithmetic operators (+, -, *, /),
    while respecting standard operator precedence.
    """

    # Define operator precedence and associativity for the Shunting-yard algorithm.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'L'},
        '-': {'precedence': 1, 'assoc': 'L'},
        '*': {'precedence': 2, 'assoc': 'L'},
        '/': {'precedence': 2, 'assoc': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string.

        This is the main public method that orchestrates the tokenizing,
        parsing (to RPN), and evaluation of the expression.

        Args:
            expression: The arithmetic expression string to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid
                        characters, or has unbalanced parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise specific errors to provide clear feedback to the caller.
            raise e
        except Exception as e:
            # Catch any other unexpected errors during processing.
            raise ValueError(f"Invalid or malformed expression: {e}") from e

    def _tokenize(self, expression: str) -> List[Token]:
        """
        Converts the input string into a list of tokens (numbers and operators).

        This method handles integers, floats, and operators, and correctly
        interprets unary minus (e.g., '-5' or '3 * -2').

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (floats and strings).

        Raises:
            ValueError: If an unknown character is encountered.
        """
        # Regex to find numbers (including floats) and operators/parentheses.
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression)

        # Check for any characters that were not matched by the regex.
        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters.")

        processed_tokens: List[Token] = []
        for i, token in enumerate(tokens):
            if token.isdigit() or '.' in token:
                processed_tokens.append(float(token))
            elif token in self._OPERATORS:
                # Handle unary minus: if '-' is the first token or follows
                # an operator or an opening parenthesis.
                is_unary = (
                    token == '-' and
                    (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '(')
                )
                if is_unary:
                    # Mark unary minus with a special operator '~' for evaluation.
                    processed_tokens.append('~')
                else:
                    processed_tokens.append(token)
            elif token in '()':
                processed_tokens.append(token)
            # The regex should prevent this, but as a safeguard:
            else:
                raise ValueError(f"Unknown token: {token}")

        return processed_tokens

    def _to_rpn(self, tokens: List[Token]) -> List[Token]:
        """
        Converts a token list from infix to Reverse Polish Notation (RPN).

        This method implements the Shunting-yard algorithm to handle
        operator precedence and associativity correctly. Unary minus is treated
        as a high-precedence right-associative operator.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[Token] = []
        operator_stack: List[str] = []
        
        # Special handling for unary minus within the Shunting-yard context.
        unary_operator = {'~': {'precedence': 3, 'assoc': 'R'}}

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._OPERATORS or token == '~':
                # Use a combined dictionary for precedence/associativity checks.
                all_ops = {**self._OPERATORS, **unary_operator}
                op1 = token
                while (operator_stack and operator_stack[-1] != '(' and
                       (all_ops[operator_stack[-1]]['precedence'] > all_ops[op1]['precedence'] or
                        (all_ops[operator_stack[-1]]['precedence'] == all_ops[op1]['precedence'] and
                         all_ops[op1]['assoc'] == 'L'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op1)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Discard the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Token]) -> float:
        """
        Evaluates a token queue in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the RPN expression is malformed.
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack: List[float] = []

        for token in rpn_queue:
            if isinstance(token, float):
                operand_stack.append(token)
            else:
                try:
                    # Handle unary operator '~'
                    if token == '~':
                        operand = operand_stack.pop()
                        operand_stack.append(-operand)
                        continue

                    # Handle binary operators
                    op2 = operand_stack.pop()
                    op1 = operand_stack.pop()

                    if token == '+':
                        operand_stack.append(op1 + op2)
                    elif token == '-':
                        operand_stack.append(op1 - op2)
                    elif token == '*':
                        operand_stack.append(op1 * op2)
                    elif token == '/':
                        if op2 == 0:
                            raise ZeroDivisionError("Division by zero is not allowed.")
                        operand_stack.append(op1 / op2)
                except IndexError:
                    raise ValueError("Malformed expression: Invalid operator usage.")

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression: Too many values.")

        return operand_stack[0]


# --- Example Usage ---
if __name__ == "__main__":
    # This block demonstrates how to use the Calculator class and provides
    # a simple interactive console for testing.
    calculator = Calculator()

    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    print("Example: 3 + 5 * (10 - 4) / 2")

    while True:
        expression_input = input(">> ")
        if expression_input.lower() == 'exit':
            break

        if not expression_input.strip():
            continue

        try:
            result = calculator.calculate(expression_input)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")

    print("Calculator exited.")
