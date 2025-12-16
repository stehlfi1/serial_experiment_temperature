
import re

class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.

    This class provides a safe and efficient way to compute expressions
    containing integers, floating-point numbers, parentheses, and the basic
    arithmetic operations (+, -, *, /).

    It adheres to the ISO/IEC 25010 standard by prioritizing correctness,
    performance, security, and maintainability.

    The evaluation process follows a standard two-step approach:
    1.  The infix expression is converted to a postfix (Reverse Polish Notation)
        expression using Dijkstra's Shunting-yard algorithm.
    2.  The RPN expression is then evaluated using a stack-based algorithm.

    This approach avoids the use of Python's `eval()` function, thus preventing
    potential code injection security vulnerabilities.
    """

    # --- Class-level constants for clarity and maintainability ---
    _OPERATORS = {
        '+': {'precedence': 1, 'func': lambda a, b: a + b},
        '-': {'precedence': 1, 'func': lambda a, b: a - b},
        '*': {'precedence': 2, 'func': lambda a, b: a * b},
        '/': {'precedence': 2, 'func': lambda a, b: a / b},
    }
    _LEFT_PAREN = '('
    _RIGHT_PAREN = ')'

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid
                        characters, or has unbalanced parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raising exceptions to be handled by the caller,
            # maintaining a clear and testable interface.
            raise e
        except IndexError:
            # An IndexError during evaluation typically means a malformed
            # expression (e.g., "5 *").
            raise ValueError("Invalid or malformed expression.")

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts the input string into a list of tokens (numbers and operators).

        This tokenizer correctly handles floating-point numbers, negative numbers,
        and operators, while validating for illegal characters.

        Args:
            expression: The raw expression string.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to find numbers (including floats), operators, and parentheses.
        # It also captures any invalid characters to raise an error.
        token_regex = re.compile(r'(\d+\.?\d*|\.\d+|[+\-*/()]|[^\s])')
        tokens = token_regex.findall(expression.replace(" ", ""))

        # Validate for any characters not matching the allowed set
        allowed_chars = set("0123456789.+-*/()")
        for token in tokens:
            if not all(char in allowed_chars for char in token):
                 raise ValueError(f"Invalid character in expression: '{token}'")

        # --- Handle unary minus ---
        # A minus sign is unary if it's the first token or follows an operator or left parenthesis.
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == self._LEFT_PAREN):
                # This is a unary minus. Combine it with the next number.
                if i + 1 < len(tokens) and tokens[i+1].replace('.', '', 1).isdigit():
                    # The next token is a number, so we prepend the minus sign.
                    # We will handle this combined token later in the loop.
                    continue
            
            if i > 0 and tokens[i-1] == '-' and (i == 1 or tokens[i-2] in self._OPERATORS or tokens[i-2] == self._LEFT_PAREN):
                # The previous token was a unary minus, so combine them.
                processed_tokens.append('-' + token)
            else:
                processed_tokens.append(token)
                
        return processed_tokens

    def _to_rpn(self, tokens: list[str]) -> list[str]:
        """
        Converts a list of tokens in infix notation to RPN using Shunting-yard.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in Reverse Polish Notation.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                output_queue.append(token)
            elif token in self._OPERATORS:
                op1 = token
                while (operator_stack and
                       operator_stack[-1] in self._OPERATORS and
                       self._OPERATORS[operator_stack[-1]]['precedence'] >= self._OPERATORS[op1]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op1)
            elif token == self._LEFT_PAREN:
                operator_stack.append(token)
            elif token == self._RIGHT_PAREN:
                while operator_stack and operator_stack[-1] != self._LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != self._LEFT_PAREN:
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop() # Discard the left parenthesis

        while operator_stack:
            op = operator_stack.pop()
            if op == self._LEFT_PAREN:
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: list[str]) -> float:
        """
        Evaluates a token list in Reverse Polish Notation.

        Args:
            rpn_tokens: A list of tokens in RPN.

        Returns:
            The final calculated result as a float.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the RPN expression is malformed.
        """
        stack = []

        for token in rpn_tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                stack.append(float(token))
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator.")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                operation = self._OPERATORS[token]

                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                result = operation['func'](operand1, operand2)
                stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression format.")

        return stack[0]

# --- Example Usage ---
if __name__ == "__main__":
    calculator = Calculator()
    print("--- Console Arithmetic Calculator ---")
    print("Enter 'exit' to quit.")

    while True:
        try:
            expression = input("Enter expression: ")
            if expression.lower() == 'exit':
                break
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            print("-" * 20)

    # --- Demonstration of test cases ---
    print("\n--- Running Automated Test Cases ---")
    test_cases = {
        "3 + 5 * 2": 13.0,
        "10 / 2 - 3": 2.0,
        "(3 + 5) * 2": 16.0,
        "10 / (2 - 3)": -10.0,
        "5.5 * 2": 11.0,
        "-5 + 10": 5.0,
        "10 + -5": 5.0,
        "3 * (4 + 2) / (9 - 3)": 3.0,
        "- (5 + 2)": -7.0, # Test with unary minus on parenthesis
        "10 * -2": -20.0
    }

    error_cases = [
        "10 / 0",          # Division by zero
        "5 * (2 + 3",     # Mismatched parentheses
        "5 + a",           # Invalid character
        "5 *",             # Malformed expression
        "(3+4))"           # Mismatched parentheses
    ]

    for expr, expected in test_cases.items():
        try:
            res = calculator.calculate(expr)
            status = "PASSED" if res == expected else f"FAILED (Got {res})"
            print(f"'{expr}' -> Expected: {expected}, Result: {res} [{status}]")
        except Exception as e:
            print(f"'{expr}' -> FAILED with exception: {e}")

    print("\n--- Testing Error Handling ---")
    for expr in error_cases:
        try:
            calculator.calculate(expr)
            print(f"'{expr}' -> FAILED (Expected an error but got none)")
        except (ValueError, ZeroDivisionError) as e:
            print(f"'{expr}' -> PASSED (Caught expected error: {e})")
        except Exception as e:
            print(f"'{expr}' -> FAILED (Caught unexpected error: {e})")

