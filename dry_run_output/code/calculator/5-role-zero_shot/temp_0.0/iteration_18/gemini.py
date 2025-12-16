
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class implements a calculator that adheres to the ISO/IEC 25010 standard
    for software quality, focusing on correctness, efficiency, safety, and
    maintainability. It uses the Shunting-yard algorithm to parse and evaluate
    expressions, supporting addition, subtraction, multiplication, division,
    and parentheses.

    Attributes:
        supported_operators (dict): A dictionary mapping operators to their
                                    precedence and associativity.
    """

    def __init__(self):
        """Initializes the Calculator, defining operator precedence."""
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        self.operators = set(self.precedence.keys()) | {'(', ')'}

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an infix expression string into a list of tokens.

        This method handles integers, floating-point numbers, and operators.
        It also correctly tokenizes unary minus (e.g., '-5' or '3 * -2').

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens (numbers as strings, operators).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove all whitespace for easier parsing
        expression = expression.replace(" ", "")
        if not expression:
            raise ValueError("Input expression cannot be empty.")

        # Regex to find numbers (int/float) or operators
        token_regex = re.compile(r"(\d+\.?\d*|[+\-*/()])")
        tokens = token_regex.findall(expression)

        # Verify that the tokens constitute the entire expression
        if "".join(tokens) != expression:
            raise ValueError("Expression contains invalid characters.")

        # Handle unary minus: A '-' is unary if it's the first token or
        # is preceded by an operator or an opening parenthesis.
        # We transform it by inserting a '0' before the '-'
        # e.g., "-5" -> ["0", "-", "5"], "3*-5" -> ["3", "*", "0", "-", "5"]
        output_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self.operators - {')'}):
                output_tokens.append('0')
            output_tokens.append(token)
        
        return output_tokens

    def _infix_to_postfix(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts a list of infix tokens to a postfix (RPN) list.

        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in postfix order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[Union[float, str]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                output_queue.append(float(token))
            elif token in self.operators and token not in '()':
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       self.precedence.get(operator_stack[-1], 0) >= self.precedence.get(token, 0)):
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

        while operatorstack:
            if operator_stack[-1] in '()':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, postfix_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a postfix (RPN) expression.

        Args:
            postfix_tokens: A list of tokens in postfix order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero is attempted.
        """
        operand_stack: List[float] = []

        for token in postfix_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            else:  # Token is an operator
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator.")
                
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()

                if token == '+':
                    operand_stack.append(operand1 + operand2)
                elif token == '-':
                    operand_stack.append(operand1 - operand2)
                elif token == '*':
                    operand_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    operand_stack.append(operand1 / operand2)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: too many operands.")

        return operand_stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the Calculator. It orchestrates
        the tokenization, conversion to postfix, and evaluation steps.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: For invalid expressions, characters, or parentheses.
            ZeroDivisionError: For division by zero.
            TypeError: If the input is not a string.
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller, maintaining
            # the original error type and message for clarity.
            raise e
        except Exception:
            # Catch any other unexpected errors during parsing/evaluation
            raise ValueError("Invalid or malformed expression.")


if __name__ == '__main__':
    # This block demonstrates the usage of the Calculator class and serves
    # as a basic test suite, showcasing its functionality and error handling.
    
    calculator = Calculator()
    
    print("--- Welcome to the Console Calculator ---")
    print("Enter an arithmetic expression or 'exit' to quit.")
    
    # --- Demonstration with a set of test cases ---
    print("\n--- Running Automated Test Cases ---")
    test_cases = {
        "5 + 3": 8.0,
        "10 - 4 * 2": 2.0,
        "(10 - 4) * 2": 12.0,
        "3 * (4 + 2) / 2": 9.0,
        "10 / 2 / 5": 1.0,
        "2.5 * 4": 10.0,
        "-5 + 10": 5.0,
        "3 * -2": -6.0,
        "5 + (6 * -2)": -7.0,
        "100 / (10 * (2 + 3))": 2.0,
        "3.14 * (2 + 2)": 12.56
    }

    for expr, expected in test_cases.items():
        try:
            result = calculator.calculate(expr)
            status = "PASSED" if abs(result - expected) < 1e-9 else f"FAILED (Got {result})"
            print(f"'{expr}' => {expected} ... {status}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"'{expr}' => Error: {e} ... FAILED (Exception not expected)")

    print("\n--- Testing Error Handling ---")
    error_cases = [
        "5 +",          # Malformed expression
        "5 * (3 + 2",    # Mismatched parentheses
        "10 / 0",       # Division by zero
        "5 & 4",        # Invalid character
        "(3+4))"        # Mismatched parentheses
    ]

    for expr in error_cases:
        try:
            calculator.calculate(expr)
            print(f"'{expr}' ... FAILED (Expected an error but got none)")
        except (ValueError, ZeroDivisionError) as e:
            print(f"'{expr}' ... PASSED (Correctly caught error: {e})")
    
    # --- Interactive Loop ---
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

