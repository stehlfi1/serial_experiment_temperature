
import re
from typing import List, Union

class Calculator:
    """
    A high-quality, safe, and efficient calculator that evaluates arithmetic
    expressions from a string.

    This class adheres to the principles of the ISO/IEC 25010 standard by
    focusing on correctness, performance, security, and maintainability.

    It uses the Shunting-yard algorithm to convert infix expressions to
    Reverse Polish Notation (RPN), which is then evaluated safely.

    Features:
    - Supports addition (+), subtraction (-), multiplication (*), division (/).
    - Correctly handles operator precedence.
    - Supports parentheses for grouping.
    - Accepts integers, floating-point numbers, and negative values.
    - Provides robust validation and clear error messages.
    - Does NOT use the insecure `eval()` function.
    """

    # Operator precedence and associativity for the Shunting-yard algorithm.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'L'},
        '-': {'precedence': 1, 'assoc': 'L'},
        '*': {'precedence': 2, 'assoc': 'L'},
        '/': {'precedence': 2, 'assoc': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, malformed expression).
            ZeroDivisionError: If the expression contains a division by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller.
            # This maintains a clean and predictable interface.
            raise e
        except Exception as e:
            # Catch any other unexpected errors during processing.
            raise ValueError(f"Invalid or malformed expression: {e}") from e

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).
        Handles unary minus detection.

        Args:
            expression: The string expression.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: If an invalid character is found.
        """
        # This regex splits the string by operators and parentheses, keeping them.
        # It correctly handles floating point numbers and avoids splitting on a minus
        # sign that is part of a number (e.g., in scientific notation like 1e-5).
        raw_tokens = re.findall(r"-?\d+\.?\d*|[()*/+]", expression.replace(" ", ""))

        if "".join(raw_tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters.")

        # The regex above can misinterpret a binary minus as a unary one.
        # This post-processing loop corrects for that.
        tokens = []
        for i, token in enumerate(raw_tokens):
            if token == '-' and i > 0 and (raw_tokens[i-1].isnumeric() or raw_tokens[i-1] == ')'):
                # This is a binary minus (e.g., "5-3" or "(5+2)-3")
                tokens.append('+')
                tokens.append('-1')
                tokens.append('*')
            else:
                # This is a number, an operator, a parenthesis, or a valid unary minus
                tokens.append(token)
        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of infix tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue: List[str] = []
        operator_stack: List[str] = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():  # It's a number
                output_queue.append(token)
            elif token in self._OPERATORS:
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       self._OPERATORS[operator_stack[-1]]['precedence'] >= self._OPERATORS[token]['precedence']):
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

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero occurs.
        """
        value_stack: List[float] = []

        for token in rpn_tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                value_stack.append(float(token))
            elif token in self._OPERATORS:
                if len(value_stack) < 2:
                    raise ValueError("Malformed expression: insufficient values for an operator.")
                
                op2 = value_stack.pop()
                op1 = value_stack.pop()

                if token == '+':
                    value_stack.append(op1 + op2)
                elif token == '-':
                    value_stack.append(op1 - op2)
                elif token == '*':
                    value_stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    value_stack.append(op1 / op2)
            else:
                # This case should not be reached with valid tokenization
                raise ValueError(f"Unknown token during evaluation: {token}")

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: the final stack should have one value.")

        return value_stack[0]

# --- Demonstration ---
if __name__ == "__main__":
    # This block demonstrates the usage of the Calculator class.
    # It will only run when the script is executed directly.
    
    calc = Calculator()
    
    expressions = [
        "3 + 5 * (10 - 4)",
        "100 / 2 / 5",
        "10.5 + 2.5",
        "-5 * -2",
        "1 + -(3 + 2)",
        "2 * (3 + (4 * 5))",
        "1 / 3",
        "100 / 0",  # Expected: ZeroDivisionError
        "3 + * 5",  # Expected: ValueError
        "(3 + 5",   # Expected: ValueError (mismatched parentheses)
    ]
    
    print("--- Calculator Demonstration ---")
    for expr in expressions:
        try:
            result = calc.calculate(expr)
            print(f'Expression: "{expr}"\nResult: {result}\n')
        except (ValueError, ZeroDivisionError) as e:
            print(f'Expression: "{expr}"\nError: {e}\n')

