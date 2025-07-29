
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class implements a calculator that adheres to standard operator precedence,
    supports parentheses, and handles integers, floating-point numbers, and
    negative values. It uses the Shunting-yard algorithm to convert infix
    expressions to Reverse Polish Notation (RPN) for safe and efficient
    evaluation.

    ISO/IEC 25010 Principles Adherence:
    - Functional Suitability: Correctly computes expressions.
    - Performance Efficiency: O(n) time complexity via Shunting-yard.
    - Reliability: Graceful error handling for invalid input.
    - Security: Avoids `eval()` to prevent code injection.
    - Maintainability: Modular design with clear, documented methods.
    """

    # Operator precedence and associativity definitions.
    # Higher numbers indicate higher precedence.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'left'},
        '-': {'precedence': 1, 'assoc': 'left'},
        '*': {'precedence': 2, 'assoc': 'left'},
        '/': {'precedence': 2, 'assoc': 'left'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the calculator. It orchestrates
        the tokenization, parsing (Shunting-yard), and evaluation steps.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., invalid characters,
                        unbalanced parentheses, or invalid operator sequence).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        tokens = self._tokenize(expression)
        rpn_queue = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn_queue)
        return result

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts an expression string into a list of tokens (numbers and operators).

        This method uses regular expressions to correctly identify numbers (including
        negative and floating-point) and operators. It also handles unary minus
        at the beginning of an expression or after an opening parenthesis.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens. For example, "3 + 4" -> [3.0, '+', 4.0].

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove all whitespace for easier parsing
        expression = expression.replace(" ", "")

        # Regex to find numbers (including floats/negatives) or operators/parentheses
        # It captures:
        # 1. A number (e.g., 5, -5, 3.14, -3.14)
        # 2. An operator or parenthesis (e.g., +, *, ()
        token_regex = re.compile(r"(-?\d+\.?\d*)|([+\-*/()])")
        
        tokens = []
        last_token = None
        
        pos = 0
        while pos < len(expression):
            match = token_regex.match(expression, pos)
            if not match:
                raise ValueError(f"Invalid character in expression at position {pos}: '{expression[pos]}'")
            
            token_str = match.group(0)
            
            # Handle unary minus vs. binary subtraction
            if token_str == '-' and (last_token is None or last_token in self._OPERATORS or last_token == '('):
                # This is a unary minus. We look for the number that follows.
                # We need to re-run the regex from the next position to find the number part.
                num_match = re.match(r"(\d+\.?\d*)", expression, pos + 1)
                if not num_match:
                    raise ValueError("Invalid expression: '-' must be followed by a number.")
                
                # Combine '-' with the number
                token_str = '-' + num_match.group(0)
                pos += len(token_str)
                token = float(token_str)
            elif token_str in self._OPERATORS or token_str in "()":
                token = token_str
                pos += len(token_str)
            else: # It's a number
                token = float(token_str)
                pos += len(token_str)

            tokens.append(token)
            last_token = token
            
        return tokens


    def _to_rpn(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of numbers and operators in infix order.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._OPERATORS:
                op1 = token
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       (self._OPERATORS[operator_stack[-1]]['precedence'] > self._OPERATORS[op1]['precedence'] or
                        (self._OPERATORS[operator_stack[-1]]['precedence'] == self._OPERATORS[op1]['precedence'] and
                         self._OPERATORS[op1]['assoc'] == 'left'))):
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

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates a token queue in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero occurs.
        """
        stack = []
        for token in rpn_queue:
            if isinstance(token, float):
                stack.append(token)
            else: # Token is an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands for operator.")
                
                op2 = stack.pop()
                op1 = stack.pop()

                if token == '+':
                    stack.append(op1 + op2)
                elif token == '-':
                    stack.append(op1 - op2)
                elif token == '*':
                    stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    stack.append(op1 / op2)

        if len(stack) != 1:
            raise ValueError("Invalid expression: The final stack should have one value.")

        return stack[0]

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'quit' to exit.")

    # Example test cases to demonstrate correctness
    print("\n--- Running Correctness Tests ---")
    test_cases = {
        "5 + 3": 8.0,
        "10 - 4 * 2": 2.0,
        "(10 - 4) * 2": 12.0,
        "3 * (4 + 2) / (9 - 3)": 3.0,
        "5.5 + 2.5": 8.0,
        "10 / 4": 2.5,
        "-5 + 10": 5.0,
        "5 * -2": -10.0,
        "5 * (-2 + 1)": -5.0,
        "100 / (5 * (2 + 2))": 5.0,
    }

    for expr, expected in test_cases.items():
        try:
            result = calculator.calculate(expr)
            status = "PASSED" if abs(result - expected) < 1e-9 else f"FAILED (Got {result})"
            print(f"'{expr}' => {expected} ... {status}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"'{expr}' => ERROR: {e}")

    # Interactive loop
    print("\n--- Interactive Mode ---")
    while True:
        try:
            expression_input = input("> ")
            if expression_input.lower() == 'quit':
                break
            
            result = calculator.calculate(expression_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

