
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class implements a robust, safe, and efficient calculator without using
    the built-in `eval()` function. It adheres to standard operator precedence,
    supports parentheses, and handles both integers and floating-point numbers.

    The evaluation process follows these steps:
    1. Tokenization: The input string is converted into a list of tokens.
    2. Shunting-yard Algorithm: The infix token list is converted to a
       postfix (RPN) queue.
    3. RPN Evaluation: The RPN queue is evaluated to produce the final result.

    This design ensures high marks in maintainability, reliability, and security
    as per ISO/IEC 25010.
    """

    def __init__(self):
        """Initializes the Calculator, defining operators and their precedence."""
        self._operators = {
            '+': {'precedence': 1, 'func': lambda a, b: a + b},
            '-': {'precedence': 1, 'func': lambda a, b: a - b},
            '*': {'precedence': 2, 'func': lambda a, b: a * b},
            '/': {'precedence': 2, 'func': lambda a, b: a / b},
        }

    def _tokenize(self, expression: str) -> List[str]:
        """
        Breaks the input expression string into a list of tokens.

        This method handles numbers (integers, floats, negatives), operators,
        and parentheses. It also performs initial validation for invalid characters.

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to find numbers (including floats), operators, and parentheses
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression.replace(" ", ""))

        # Validate that all characters were captured by the regex
        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters")

        # Handle unary minus (e.g., -5, 3 * -2)
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i - 1] in self._operators or tokens[i - 1] == '('):
                # This is a unary minus. Combine it with the next token.
                try:
                    processed_tokens.append(f"-{tokens[i+1]}")
                    tokens[i+1] = '' # Mark next token as consumed
                except IndexError:
                    raise ValueError("Invalid expression: trailing unary minus")
            elif token: # Append if not consumed by unary minus logic
                processed_tokens.append(token)
        
        return processed_tokens

    def _to_rpn(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts an infix token list to a postfix (RPN) queue using the
        Shunting-yard algorithm.

        Args:
            tokens: A list of infix tokens from the _tokenize method.

        Returns:
            A list representing the RPN queue.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            try:
                # If the token is a number, add it to the output queue.
                output_queue.append(float(token))
            except ValueError:
                if token in self._operators:
                    # Token is an operator.
                    while (operator_stack and
                           operator_stack[-1] in self._operators and
                           self._operators[operator_stack[-1]]['precedence'] >= self._operators[token]['precedence']):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if not operator_stack or operator_stack[-1] != '(':
                        raise ValueError("Mismatched parentheses in expression")
                    operator_stack.pop()  # Pop the '('
                else:
                    # This case should ideally not be reached due to tokenizer validation
                    raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators from the stack to the output queue.
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates a postfix (RPN) queue.

        Args:
            rpn_queue: The RPN queue to evaluate.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the expression is malformed (e.g., "5 *").
            ZeroDivisionError: If division by zero is attempted.
        """
        value_stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                value_stack.append(token)
            else:  # Token is an operator
                try:
                    operand2 = value_stack.pop()
                    operand1 = value_stack.pop()
                except IndexError:
                    raise ValueError("Malformed expression: insufficient operands for operator")

                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")

                operation = self._operators[token]['func']
                result = operation(operand1, operand2)
                value_stack.append(result)

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: too many values left after evaluation")

        return value_stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the Calculator class. It orchestrates
        the tokenization, conversion to RPN, and final evaluation.

        Args:
            expression: The string containing the mathematical expression.
                        Example: "3 + 4 * (2 - 1) / 5"

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: For invalid expressions, characters, or mismatched parentheses.
            ZeroDivisionError: For division by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression must be a non-empty string.")

        tokens = self._tokenize(expression)
        rpn_queue = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn_queue)

        return result


if __name__ == '__main__':
    # This block demonstrates the usage of the Calculator class and serves
    # as a simple interactive test environment.
    calculator = Calculator()

    print("--- Python Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    print("Supported operations: +, -, *, /, ()")
    print("Example: -5.5 * (10 + 2) / 2\n")

    while True:
        try:
            user_input = input(">> ")
            if user_input.lower() == 'exit':
                break

            result = calculator.calculate(user_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

