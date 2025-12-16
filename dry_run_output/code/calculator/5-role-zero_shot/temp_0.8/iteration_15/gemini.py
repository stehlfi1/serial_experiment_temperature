
import math

class Calculator:
    """
    A high-quality, safe, and efficient calculator for evaluating arithmetic
    expressions from a string.

    This class adheres to the principles of ISO/IEC 25010, focusing on
    correctness, performance, security, and maintainability. It uses the
    Shunting-yard algorithm to handle operator precedence and parentheses
    without using the insecure `eval()` function.

    Attributes:
        _OPERATORS (set): A set of supported operators.
        _PRECEDENCE (dict): A dictionary mapping operators to their
                            precedence level.
    """
    _OPERATORS = {'+', '-', '*', '/'}
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression string to evaluate.
                        It can contain integers, floats, parentheses, and the
                        operators +, -, *, /.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError):
            # Re-raise exceptions to be handled by the caller.
            raise
        except Exception as e:
            # Catch any other unexpected errors during processing.
            raise ValueError(f"Invalid or malformed expression: {e}") from e

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts the input string expression into a list of tokens.

        This method handles multi-digit numbers, floating-point numbers,
        and unary minus (e.g., '-5' or '3 * -2').

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: For any invalid characters in the expression.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
                continue

            if char in self._OPERATORS:
                # Handle unary minus: it occurs at the start of an expression
                # or after an opening parenthesis or another operator.
                is_unary = (
                    char == '-' and
                    (not tokens or tokens[-1] in self._OPERATORS or tokens[-1] == '(')
                )
                if is_unary:
                    num_str = "-"
                    i += 1
                    # Skip any whitespace after the unary minus
                    while i < len(expression) and expression[i].isspace():
                        i += 1
                    # Find the number part
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    if len(num_str) == 1: # Just a '-' without a number
                        raise ValueError("Invalid use of unary minus.")
                    tokens.append(num_str)
                    continue

                tokens.append(char)
                i += 1
                continue

            if char in '()':
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Invalid character in expression: '{char}'")

        return tokens


    def _to_rpn(self, tokens: list[str]) -> list[str]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: For mismatched or unbalanced parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            try:
                # If the token is a number, add it to the output queue.
                float(token)
                output_queue.append(token)
            except ValueError:
                # The token is not a number, so it must be an operator or parenthesis.
                if token in self._OPERATORS:
                    while (operator_stack and
                           operator_stack[-1] in self._OPERATORS and
                           self._PRECEDENCE[operator_stack[-1]] >= self._PRECEDENCE[token]):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    
                    if not operator_stack or operator_stack[-1] != '(':
                        raise ValueError("Mismatched parentheses in expression.")
                    operator_stack.pop() # Pop the '('

        # Pop any remaining operators from the stack to the output queue.
        while operator_stack:
            operator = operator_stack.pop()
            if operator == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(operator)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: list[str]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN.

        Returns:
            The final result of the calculation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., too many operands).
            ZeroDivisionError: If division by zero occurs.
        """
        value_stack = []

        for token in rpn_tokens:
            try:
                # If token is a number, push it to the stack.
                value_stack.append(float(token))
            except ValueError:
                # Token is an operator.
                if len(value_stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands for operator.")
                
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
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    value_stack.append(operand1 / operand2)

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: too many operands.")

        return value_stack[0]


if __name__ == "__main__":
    # This block demonstrates the usage of the Calculator class
    # and serves as a simple, interactive test harness.
    calc = Calculator()
    
    print("--- Console Arithmetic Calculator ---")
    print("Enter 'exit' to quit.")
    
    while True:
        try:
            expression = input("Enter expression: ")
            if expression.lower() == 'exit':
                break
            
            result = calc.calculate(expression)
            # Format to avoid floating point inaccuracies for simple integers
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
