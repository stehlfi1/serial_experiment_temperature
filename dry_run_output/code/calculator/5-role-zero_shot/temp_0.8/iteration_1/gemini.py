
import collections

class Calculator:
    """
    A robust, console-based arithmetic calculator that evaluates string expressions.

    This class adheres to ISO/IEC 25010 quality standards by providing a
    correct, efficient, secure, and maintainable implementation. It does not
    use `eval()` or similar unsafe functions.

    The evaluation process is implemented using a combination of a tokenizer,
    the Shunting-yard algorithm to handle operator precedence, and a
    Reverse Polish Notation (RPN) evaluator.

    Supported features:
    - Operations: Addition (+), Subtraction (-), Multiplication (*), Division (/)
    - Precedence: Correctly handles that * and / are evaluated before + and -
    - Grouping: Supports parentheses () for overriding precedence.
    - Numbers: Accepts integers, floating-point numbers, and negative values.

    Attributes:
        OPERATORS (dict): A dictionary mapping operators to their precedence and
                          the function that implements them.
    """

    OPERATORS = {
        '+': {'precedence': 1, 'func': lambda a, b: a + b},
        '-': {'precedence': 1, 'func': lambda a, b: a - b},
        '*': {'precedence': 2, 'func': lambda a, b: a * b},
        '/': {'precedence': 2, 'func': lambda a, b: a / b},
    }

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input string into a list of tokens (numbers and operators).

        This tokenizer correctly handles floating-point numbers, integers, and
        distinguishes between binary subtraction and unary negation.

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens, where numbers are floats and operators are strings.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or (char == '.'):
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                continue

            if char in self.OPERATORS or char in '()':
                # Handle unary minus (negation) vs. binary minus (subtraction)
                if char == '-' and (i == 0 or tokens[-1] in self.OPERATORS or tokens[-1] == '('):
                    # This is a unary minus (negation)
                    num_str = "-"
                    i += 1
                    # Skip any whitespace after the unary minus
                    while i < len(expression) and expression[i].isspace():
                        i += 1
                    if i == len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                        raise ValueError("Invalid expression: '-' must be followed by a number.")
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    try:
                        tokens.append(float(num_str))
                    except ValueError:
                        raise ValueError(f"Invalid number format: '{num_str}'")
                    continue
                else:
                    tokens.append(char)
            else:
                raise ValueError(f"Invalid character in expression: '{char}'")
            i += 1
        return tokens

    def _shunting_yard(self, tokens: list) -> collections.deque:
        """
        Converts a list of infix tokens to a postfix (RPN) queue.

        This implementation of Dijkstra's Shunting-yard algorithm handles
        operator precedence and associativity.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A deque containing the expression in RPN.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = collections.deque()
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and operator_stack[-1] != '(' and
                       self.OPERATORS[operator_stack[-1]]['precedence'] >= self.OPERATORS[token]['precedence']):
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

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: collections.deque) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A deque of tokens in RPN format.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero is attempted.
        """
        value_stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                value_stack.append(token)
            elif token in self.OPERATORS:
                if len(value_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator")
                operand2 = value_stack.pop()
                operand1 = value_stack.pop()

                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")

                operation = self.OPERATORS[token]['func']
                result = operation(operand1, operand2)
                value_stack.append(result)

        if len(value_stack) != 1:
            raise ValueError("Invalid expression: too many operands")

        return value_stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the public interface for the Calculator. It orchestrates the
        tokenization, parsing (Shunting-yard), and evaluation (RPN) of the
        expression.

        Args:
            expression: The string containing the arithmetic expression.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: For invalid expressions, characters, or parentheses.
            ZeroDivisionError: For division by zero.
            TypeError: If the input is not a string.
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")
        if not expression.strip():
            raise ValueError("Input expression cannot be empty.")

        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._shunting_yard(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller.
            # This maintains a clear and testable error propagation path.
            raise e
        except IndexError:
            # Catches errors from popping from empty stacks, usually due to a
            # malformed expression like "5 *".
            raise ValueError("Invalid or incomplete expression")


# --- Main execution block for demonstration ---
if __name__ == "__main__":
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    print("-" * 35)

    calculator = Calculator()

    # --- Pre-defined test cases to demonstrate correctness and robustness ---
    test_cases = [
        "5 + 3",
        "10 - 4 * 2",
        "(10 - 4) * 2",
        "3.5 * (2 + 3)",
        "10 / 2 / 5",
        "2 * (3 + (4 * 5))",
        "-5 + 10",
        "10 + -5",
        "5 * -2",
        "-5 * -2",
        "100 / (10 * -2) + 5",
        "1 / 3",
        # Error cases
        "10 / 0",
        "(5 + 3",
        "5 + 3)",
        "5 + & 3",
        "5 * ",
    ]

    print("--- Running Automated Test Cases ---")
    for expr in test_cases:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}'\nResult: {result}\n")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Expression: '{expr}'\nError: {e}\n")
    print("-" * 35)

    # --- Interactive Loop ---
    while True:
        try:
            user_input = input("Calculate: ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

