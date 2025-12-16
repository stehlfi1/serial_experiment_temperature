
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class provides a safe and efficient way to evaluate mathematical
    expressions containing integers, floating-point numbers, parentheses, and
    the basic arithmetic operators (+, -, *, /).

    It adheres to standard operator precedence and does not use the built-in
    `eval()` function, ensuring security and control over the evaluation process.

    The implementation follows the classic Shunting-yard algorithm to convert
    the infix expression to postfix (Reverse Polish Notation), which is then
    evaluated.
    """

    # Define operator precedence and associativity for the Shunting-yard algorithm.
    # Higher numbers indicate higher precedence.
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    _OPERATORS = set(_PRECEDENCE.keys())

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.
                        Example: "3 + 4 * (2 - 1)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, malformed expression).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller.
            # This maintains a clear and testable interface.
            raise e
        except Exception:
            # Catch any other unexpected errors during processing.
            raise ValueError("Invalid or malformed expression")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string expression into a list of tokens.

        This method handles numbers (integers, floats, negatives) and operators.
        It also performs initial validation for invalid characters and
        unbalanced parentheses.

        Args:
            expression: The raw string expression.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: For invalid characters or unbalanced parentheses.
        """
        # 1. Validate parentheses balance
        if expression.count('(') != expression.count(')'):
            raise ValueError("Mismatched parentheses")

        # 2. Use regex to find all numbers, operators, and parentheses.
        # This pattern correctly captures floating-point numbers and operators.
        token_regex = re.compile(r"(\d+\.?\d*|[+\-*/()])")
        tokens = token_regex.findall(expression)

        # 3. Validate for any characters not captured by the regex.
        # This ensures the expression contains only valid components.
        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters")

        # 4. Handle unary minus (e.g., "-5" or "3 * -2")
        # A minus sign is unary if it's the first token or follows an operator or '('.
        output_tokens = []
        for i, token in enumerate(tokens):
            if (token == '-' and
                    (i == 0 or tokens[i - 1] in self._OPERATORS or tokens[i - 1] == '(')):
                # This is a unary minus, so combine it with the next number.
                try:
                    output_tokens.append(f"-{tokens[i + 1]}")
                    # Skip the next token since we've consumed it.
                    tokens.pop(i + 1)
                except (IndexError, ValueError):
                    raise ValueError("Invalid use of unary minus")
            else:
                output_tokens.append(token)

        return output_tokens

    def _to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to postfix (RPN) using Shunting-yard.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in postfix order.
        """
        output_queue: List[str] = []
        operator_stack: List[str] = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                output_queue.append(token)
            elif token in self._OPERATORS:
                # While there's an operator on the stack with higher or equal precedence
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       self._PRECEDENCE[operator_stack[-1]] >= self._PRECEDENCE[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop operators until an opening parenthesis is found
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    # This case should be caught by the initial parenthesis check,
                    # but it's good practice for robustness.
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Discard the '('

        # Pop any remaining operators from the stack to the output queue
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, tokens: List[str]) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens: A list of tokens in postfix order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero occurs.
        """
        value_stack: List[float] = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                value_stack.append(float(token))
            elif token in self._OPERATORS:
                if len(value_stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                
                operand2 = value_stack.pop()
                operand1 = value_stack.pop()

                if token == '+':
                    value_stack.append(operand1 + operand2)
                elif token == '-':
                    value_stack.append(operand1 - operand2)
                elif token == '*':
                    value_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    value_stack.append(operand1 / operand2)

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: too many operands")

        return value_stack[0]


# --- Demonstration ---
if __name__ == "__main__":
    calculator = Calculator()

    print("--- High-Quality Python Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")

    # Example test cases to demonstrate correctness
    test_cases = [
        "3 + 4 * 2 / ( 1 - 5 )",
        "10 + 2.5 * 4",
        "100 / ( 2 + 3 )",
        "-5 * (-2 + 1)",
        "3.14 * (10 * 10)",
        "100 / 0",  # Error case: Division by zero
        "5 * (3 + 2",  # Error case: Unbalanced parentheses
        "5 + & 3",  # Error case: Invalid character
        "5 5 +",    # Error case: Malformed expression
    ]

    print("\n--- Running Automated Test Cases ---")
    for expr in test_cases:
        try:
            result = calculator.calculate(expr)
            print(f'Expression: "{expr}"  =>  Result: {result}')
        except (ValueError, ZeroDivisionError) as e:
            print(f'Expression: "{expr}"  =>  Error: {e}')

    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                break
            if not user_input:
                continue
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

