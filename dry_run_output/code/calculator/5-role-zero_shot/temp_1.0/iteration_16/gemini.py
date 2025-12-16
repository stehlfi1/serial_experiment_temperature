
"""
A high-quality, console-based arithmetic calculator in Python.

This module provides a Calculator class that can parse and evaluate arithmetic
expressions from a string, adhering to standard operator precedence.
"""

import re
from typing import List, Union

class Calculator:
    """
    A calculator for evaluating arithmetic expressions from strings.

    This class implements a robust, safe, and efficient calculator that
    supports addition, subtraction, multiplication, division, and parentheses.
    It adheres to standard operator precedence (PEMDAS/BODMAS).

    The implementation uses a two-stack algorithm to evaluate expressions,
    avoiding the use of Python's `eval()` for safety and control.

    ISO/IEC 25010 quality characteristics considered:
    - Functional Suitability: Correctly evaluates complex expressions.
    - Reliability: Handles invalid inputs and errors gracefully (e.g.,
      division by zero, syntax errors).
    - Performance Efficiency: Uses an O(n) algorithm for evaluation.
    - Maintainability: Code is modular, documented, and readable.
    - Security: Avoids `eval()` to prevent code injection vulnerabilities.
    """

    def __init__(self):
        """Initializes the Calculator, defining operators and their precedence."""
        self._precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        self._operators = set(self._precedence.keys())

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts an expression string into a list of tokens.

        This tokenizer handles integers, floats, operators, parentheses, and
        correctly distinguishes between binary subtraction and unary negation.

        Args:
            expression: The arithmetic expression string.

        Returns:
            A list of tokens (floats for numbers, strings for operators).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove all whitespace for easier parsing
        expression = expression.replace(" ", "")
        
        # Regex to find numbers (including floats), operators, and parentheses
        token_regex = r"(\d+\.?\d*|[\+\-\*\/\(\)])"
        tokens = re.findall(token_regex, expression)
        
        # Post-process to handle unary minuses
        processed_tokens = []
        for i, token in enumerate(tokens):
            if (token == '-' and
                (i == 0 or tokens[i-1] in self._operators or tokens[i-1] == '(')):
                # This is a unary minus for a negative number
                # Combine it with the next token, which must be a number
                try:
                    next_token = tokens[i+1]
                    processed_tokens.append(float(f"-{next_token}"))
                    # Skip the next token since we've consumed it
                    tokens.pop(i+1)
                except (IndexError, ValueError):
                    raise ValueError("Invalid expression: '-' is not followed by a number.")
            elif token.replace('.', '', 1).isdigit():
                processed_tokens.append(float(token))
            elif token in self._operators or token in '()':
                processed_tokens.append(token)
            else:
                 # This should theoretically not be reached if the regex is correct
                 # and we've handled unary minus. It's a safeguard.
                 raise ValueError(f"Invalid character or token sequence: '{token}'")

        # Final validation for characters missed by regex
        reconstructed = "".join(str(t) for t in processed_tokens).replace("--", "-")
        if len(reconstructed) != len(expression):
            raise ValueError("Expression contains invalid characters.")

        return processed_tokens

    def _validate_parentheses(self, tokens: List[Union[float, str]]):
        """
        Validates that parentheses in the token list are balanced.

        Args:
            tokens: The list of tokens from the expression.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        balance = 0
        for token in tokens:
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
            if balance < 0:
                raise ValueError("Mismatched parentheses: ')' found before '('")
        if balance != 0:
            raise ValueError("Mismatched parentheses: not all '(' were closed")

    def _apply_op(self, op: str, b: float, a: float) -> float:
        """
        Applies a single arithmetic operation.

        Args:
            op: The operator ('+', '-', '*', '/').
            b: The second operand.
            a: The first operand.

        Returns:
            The result of the operation.

        Raises:
            ZeroDivisionError: If attempting to divide by zero.
        """
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return a / b
        # This line should not be reachable if operators are pre-validated
        raise ValueError(f"Unsupported operator: {op}")

    def _evaluate_tokens(self, tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a list of tokens using a two-stack algorithm.
        
        Args:
            tokens: A list of numbers (floats) and operators (strings).

        Returns:
            The final result of the evaluation.
            
        Raises:
            ValueError: For malformed expressions (e.g., missing operands).
        """
        values: List[float] = [] # Stack for number values
        ops: List[str] = []      # Stack for operators and parentheses

        def process_ops_stack(precedence_check: str = ''):
            """Helper to process operators from the ops stack."""
            while (ops and ops[-1] != '(' and
                   (not precedence_check or
                    self._precedence.get(ops[-1], 0) >= self._precedence.get(precedence_check, 0))):
                try:
                    op = ops.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(self._apply_op(op, val2, val1))
                except IndexError:
                    raise ValueError("Malformed expression: invalid operator/operand sequence.")

        for token in tokens:
            if isinstance(token, float):
                values.append(token)
            elif token == '(':
                ops.append(token)
            elif token == ')':
                process_ops_stack()
                if not ops or ops.pop() != '(':
                    # This case should be caught by _validate_parentheses
                    raise ValueError("Mismatched parentheses.")
            elif token in self._operators:
                process_ops_stack(token)
                ops.append(token)

        # Process any remaining operators on the stack
        process_ops_stack()

        if len(values) != 1 or ops:
            raise ValueError("Malformed expression: final stacks are invalid.")
            
        return values[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a complete arithmetic expression string.

        This is the main public method that orchestrates the tokenization,
        validation, and evaluation of the expression.

        Args:
            expression: A string containing the arithmetic expression.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid, malformed, or contains
                        unsupported characters.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression must be a non-empty string.")

        tokens = self._tokenize(expression)
        self._validate_parentheses(tokens)
        result = self._evaluate_tokens(tokens)
        
        return result


def main():
    """
    Main function to run the calculator in an interactive console loop.
    Includes a set of test cases to demonstrate correctness.
    """
    calculator = Calculator()
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to evaluate or 'quit' to exit.")
    
    # --- Demonstration and Test Cases ---
    print("\n--- Running built-in test cases ---")
    test_cases = {
        "5 + 3 * 2": 11.0,
        "(5 + 3) * 2": 16.0,
        "10 / 2 - 3": 2.0,
        "10 / (2 - 3)": -10.0,
        "5 * -3": -15.0,
        "-5 + -3": -8.0,
        "2 * (3 + (4 * 5))": 46.0,
        "7 + 3 * (10 / (12 / (3 + 1) - 1))": 22.0,
        "2.5 * 4": 10.0,
        "-10": -10.0,
        "3--2": 5.0 # Interpreted as 3 - (-2)
    }

    for expr, expected in test_cases.items():
        try:
            result = calculator.calculate(expr)
            status = "PASSED" if abs(result - expected) < 1e-9 else f"FAILED (Got {result})"
            print(f"'{expr}' => {expected} ... {status}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"'{expr}' => ERROR: {e} ... FAILED")

    # Error cases
    error_cases = ["5 * (3 + 2", "5 + * 3", "10 / 0", "abc + 123"]
    print("\n--- Running built-in error test cases ---")
    for expr in error_cases:
        try:
            calculator.calculate(expr)
            print(f"'{expr}' ... FAILED (Expected an error, but none was raised)")
        except (ValueError, ZeroDivisionError) as e:
            print(f"'{expr}' ... PASSED (Correctly raised: {type(e).__name__}: {e})")
            
    # --- Interactive Loop ---
    print("\n--- Interactive Mode ---")
    while True:
        try:
            expression = input("> ")
            if expression.lower() == 'quit':
                print("Exiting calculator.")
                break
            
            result = calculator.calculate(expression)
            # Format output to be clean for integers
            if result.is_integer():
                print(f"= {int(result)}")
            else:
                print(f"= {result:.4f}")

        except (ValueError, ZeroDivisionError, KeyboardInterrupt) as e:
            if isinstance(e, KeyboardInterrupt):
                print("\nExiting calculator.")
                break
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
