
"""
A high-quality, console-based arithmetic calculator.

This module provides a Calculator class that can parse and evaluate
mathematical expressions from a string, adhering to standard operator
precedence and handling parentheses.
"""

import re
from typing import List, Union

class Calculator:
    """
    A calculator for evaluating arithmetic expressions from strings.

    This class implements a parser and evaluator for infix mathematical
    expressions using the Shunting-Yard algorithm. It supports addition,
    subtraction, multiplication, and division, as well as parentheses.

    Attributes:
        operators (dict): A dictionary mapping operators to their precedence
                          and implementation function.
    """

    def __init__(self) -> None:
        """Initializes the Calculator, defining operators and their properties."""
        self.operators = {
            '+': {'precedence': 1, 'func': lambda a, b: a + b},
            '-': {'precedence': 1, 'func': lambda a, b: a - b},
            '*': {'precedence': 2, 'func': lambda a, b: a * b},
            '/': {'precedence': 2, 'func': self._safe_divide}
        }

    def _safe_divide(self, a: float, b: float) -> float:
        """
        Performs division, raising a ZeroDivisionError for division by zero.

        Args:
            a (float): The dividend.
            b (float): The divisor.

        Returns:
            float: The result of the division.

        Raises:
            ZeroDivisionError: If the divisor 'b' is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Error: Division by zero is not allowed.")
        return a / b

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an infix expression string into a list of tokens.

        This method handles integers, floats, operators, parentheses, and
        correctly interprets unary minus (e.g., '-5' or '3 * -2').

        Args:
            expression (str): The mathematical expression string.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove whitespace to simplify parsing
        expression = expression.replace(" ", "")

        # Regex to find numbers (including floats), operators, and parentheses
        token_regex = re.compile(r"(\d+\.?\d*|[+\-*/()])")
        tokens = token_regex.findall(expression)

        # Post-process to handle unary minus
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self.operators or tokens[i-1] == '('):
                # This is a unary minus, attach it to the next number
                try:
                    processed_tokens.append(f"-{tokens[i+1]}")
                    # Skip the next token since we've consumed it
                    tokens.pop(i+1)
                except IndexError:
                    raise ValueError("Invalid expression: Trailing unary minus.")
            else:
                processed_tokens.append(token)
        
        # Validate that all parts of the original string were tokenized
        if "".join(processed_tokens).replace("-", "", 1) != expression.replace("-", "", 1) if processed_tokens and processed_tokens[0].startswith('-') else "".join(processed_tokens) != expression :
            raise ValueError(f"Invalid characters in expression: '{expression}'")
            
        return processed_tokens


    def _infix_to_rpn(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN).

        This method implements the Shunting-Yard algorithm.

        Args:
            tokens (List[str]): A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[Union[float, str]] = []
        operator_stack: List[str] = []

        for token in tokens:
            try:
                # If the token is a number, add it to the output queue.
                output_queue.append(float(token))
            except ValueError:
                if token in self.operators:
                    # Token is an operator.
                    while (operator_stack and
                           operator_stack[-1] in self.operators and
                           self.operators[operator_stack[-1]]['precedence'] >= self.operators[token]['precedence']):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if not operator_stack or operator_stack[-1] != '(':
                        raise ValueError("Mismatched parentheses in expression.")
                    operator_stack.pop()  # Pop the '('
                else:
                    # This case should ideally not be reached due to tokenizer validation
                    raise ValueError(f"Invalid token encountered: {token}")

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens (List[Union[float, str]]): A list of tokens in RPN.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
        """
        operand_stack: List[float] = []

        for token in rpn_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            else:  # Token is an operator
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands for an operator.")
                
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                
                operator_func = self.operators[token]['func']
                result = operator_func(operand1, operand2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: The final stack should have one value.")

        return operand_stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public method that orchestrates the tokenization,
        parsing (infix to RPN), and evaluation of the expression.

        Args:
            expression (str): The mathematical expression to evaluate.
                              Example: "3 + 4 * (2 - 1)"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: For syntax errors like invalid characters or
                        mismatched parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression must be a non-empty string.")

        try:
            tokens = self._tokenize(expression)
            rpn_expression = self._infix_to_rpn(tokens)
            result = self._evaluate_rpn(rpn_expression)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions with clear, user-friendly messages
            # Or handle them as per application requirements. Here, we let them propagate.
            raise e
        except Exception as e:
            # Catch any other unexpected errors during processing
            raise RuntimeError(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    """
    An interactive demonstration of the Calculator class.
    Allows users to enter expressions and see the results.
    """
    print("--- High-Quality Python Calculator ---")
    print("Enter a mathematical expression or 'exit' to quit.")
    
    calculator = Calculator()

    # --- Self-testing with various cases ---
    print("\n--- Running self-tests ---")
    test_cases = {
        "5 + 3": 8.0,
        "10 - 4": 6.0,
        "6 * 7": 42.0,
        "8 / 4": 2.0,
        "3 + 5 * 2": 13.0,
        "(3 + 5) * 2": 16.0,
        "10 / 2 - 3": 2.0,
        "10 / (2 - 3)": -10.0,
        "-5 + 10": 5.0,
        "10 * -2": -20.0,
        "3 * (-2 + 4)": 6.0,
        "1.5 + 2.5 * 2": 6.5,
        "100 / 10 * 2": 20.0,
    }

    for expr, expected in test_cases.items():
        try:
            res = calculator.calculate(expr)
            status = "PASSED" if abs(res - expected) < 1e-9 else f"FAILED (Got {res})"
            print(f"Test: '{expr}' -> Expected: {expected}, Result: {res}. Status: {status}")
        except Exception as e:
            print(f"Test: '{expr}' -> FAILED with exception: {e}")
    
    # Test error handling
    print("\n--- Testing error handling ---")
    error_cases = [
        "5 / 0",  # Division by zero
        "5 + * 3", # Malformed expression
        "(5 + 3",  # Mismatched parentheses
        "5 + 3)",  # Mismatched parentheses
        "5 & 3",   # Invalid character
    ]
    for expr in error_cases:
        try:
            calculator.calculate(expr)
            print(f"Error Test: '{expr}' -> FAILED (Expected an exception)")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error Test: '{expr}' -> PASSED (Caught expected exception: {e})")

    # --- Interactive Loop ---
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() == 'exit':
                print("Exiting calculator.")
                break
            
            result = calculator.calculate(user_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError, RuntimeError) as e:
            print(e)
        except Exception as e:
            print(f"An unexpected system error occurred: {e}")

