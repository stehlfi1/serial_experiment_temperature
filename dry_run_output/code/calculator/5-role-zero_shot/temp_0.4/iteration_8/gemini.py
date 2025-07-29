
import re
from typing import List, Union

class Calculator:
    """
    A robust, console-based arithmetic calculator that evaluates string expressions.

    This class adheres to the ISO/IEC 25010 standard by focusing on:
    - **Functional Suitability (Correctness):** Implements addition, subtraction,
      multiplication, division, parentheses, and correct operator precedence.
    - **Performance Efficiency:** Uses the Shunting-yard algorithm and RPN
      evaluation, both of which operate in linear time O(n).
    - **Maintainability (Modularity, Readability, Testability):** The logic is
      separated into distinct, private methods for tokenization, parsing (Shunting-yard),
      and evaluation. The code is documented with docstrings, type hints, and
      clear variable names.
    - **Reliability (Maturity, Fault Tolerance):** Includes comprehensive validation
      and error handling for invalid expressions, division by zero, and other
      edge cases, using standard Python exceptions.
    - **Security:** Avoids the use of `eval()` to prevent code injection vulnerabilities.
    """

    # Operator precedence mapping. Higher numbers mean higher precedence.
    _OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the public interface for the Calculator class.

        Args:
            expression: A string containing the mathematical expression to evaluate.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., mismatched parentheses,
                        invalid characters, malformed expression).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._shunting_yard(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions with a clear, user-friendly context.
            print(f"Error evaluating expression: '{expression}'")
            raise e
        except Exception:
            # Catch any other unexpected errors.
            raise ValueError("An unexpected error occurred during calculation.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an infix expression string into a list of tokens.

        This method handles numbers (integers, floats), operators, parentheses,
        and correctly identifies unary minuses.

        Args:
            expression: The raw expression string.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        # Regex to find numbers (including floats), operators, and parentheses.
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression.replace(" ", ""))

        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters.")

        # Handle unary minus: A '-' is unary if it's the first token or
        # if it follows an operator or an opening parenthesis.
        output_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._OPERATOR_PRECEDENCE or tokens[i-1] == '('):
                # This is a unary minus. Combine it with the next token.
                if i + 1 < len(tokens) and tokens[i+1].replace('.', '', 1).isdigit():
                    # The next token is a number, so prepend the minus sign.
                    # We will handle this in the next iteration by skipping this token.
                    continue
                else:
                    raise ValueError("Invalid use of unary minus.")
            elif token.replace('.', '', 1).isdigit() and i > 0 and tokens[i-1] == '-':
                 # Check if the previous token was a unary minus
                 if i-1 == 0 or tokens[i-2] in self._OPERATOR_PRECEDENCE or tokens[i-2] == '(':
                    output_tokens.append('-' + token)
                 else:
                    output_tokens.append(token)
            else:
                output_tokens.append(token)

        return output_tokens

    def _shunting_yard(self, tokens: List[str]) -> List[str]:
        """
        Converts a token list from infix to postfix (RPN) using Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in Reverse Polish Notation.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue: List[str] = []
        operator_stack: List[str] = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                output_queue.append(token)
            elif token in self._OPERATOR_PRECEDENCE:
                while (operator_stack and operator_stack[-1] in self._OPERATOR_PRECEDENCE and
                       self._OPERATOR_PRECEDENCE[operator_stack[-1]] >= self._OPERATOR_PRECEDENCE[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Discard the '('

        # Pop any remaining operators from the stack to the queue
        while operator_stack:
            operator = operator_stack.pop()
            if operator == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(operator)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[str]) -> float:
        """
        Evaluates a token queue in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of tokens in RPN.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: On division by zero.
        """
        value_stack: List[float] = []

        for token in rpn_queue:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                value_stack.append(float(token))
            elif token in self._OPERATOR_PRECEDENCE:
                try:
                    operand2 = value_stack.pop()
                    operand1 = value_stack.pop()
                except IndexError:
                    raise ValueError("Malformed expression: insufficient operands for an operator.")

                result = self._apply_operator(token, operand1, operand2)
                value_stack.append(result)
            else:
                # This case should not be reached with valid input from shunting_yard
                raise ValueError(f"Unknown token in RPN queue: {token}")

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: the final stack should have one value.")

        return value_stack[0]

    def _apply_operator(self, operator: str, operand1: float, operand2: float) -> float:
        """Helper function to apply a single arithmetic operator."""
        if operator == '+':
            return operand1 + operand2
        if operator == '-':
            return operand1 - operand2
        if operator == '*':
            return operand1 * operand2
        if operator == '/':
            if operand2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return operand1 / operand2
        # This line should be unreachable if the operator is validated before.
        raise ValueError(f"Unsupported operator: {operator}")

# --- Example Usage ---
if __name__ == "__main__":
    calculator = Calculator()

    # --- Test Cases ---
    expressions = [
        "3 + 4 * 2 / ( 1 - 5 )",
        "100 * ( 2 + 12 ) / 14",
        "5.5 + 2.2 * 10",
        "-5 + 2",
        "5 * -2",
        "-(3 + 4)",
        "10 / 3",
        "((10 + 5) * 2) - 3",
        # Invalid expressions for error handling demonstration
        "3 + 4 * (2 - 1",  # Mismatched parentheses
        "5 * / 2",         # Malformed expression
        "10 / 0",          # Division by zero
        "5 & 4",           # Invalid character
    ]

    print("--- Calculator Demo ---")
    for expr in expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}'\nResult: {result}\n")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}'\nError: {e}\n")

