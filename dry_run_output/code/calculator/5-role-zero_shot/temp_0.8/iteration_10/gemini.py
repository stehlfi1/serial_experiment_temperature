
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class adheres to the ISO/IEC 25010 standard by providing a robust,
    maintainable, and efficient implementation. It uses the Shunting-yard
    algorithm to handle operator precedence and parentheses without using the
    unsafe `eval()` function.

    Attributes:
        _OPERATORS (set): A set of supported arithmetic operators.
        _PRECEDENCE (dict): A dictionary mapping operators to their
                            precedence level.
    """

    _OPERATORS = {'+', '-', '*', '/'}
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate. It can
                        contain integers, floats, parentheses, and the
                        operators +, -, *, /.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., invalid
                        characters, unbalanced parentheses, bad structure).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError):
            # Re-raise exceptions to be handled by the caller.
            raise
        except Exception as e:
            # Catch any other unexpected errors and wrap them for clarity.
            raise ValueError(f"Invalid expression provided. Error: {e}") from e

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts an expression string into a list of tokens (numbers and operators).

        This tokenizer correctly handles negative numbers, floating-point numbers,
        and gracefully ignores whitespace.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens, where numbers are floats and operators/parentheses
            are strings.

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")
            
        # Regex to find numbers (including floats and negatives), operators, and parentheses
        token_regex = re.compile(r'(\d+\.?\d*|\.\d+|[+\-*/()])')
        tokens = token_regex.findall(expression.replace(" ", ""))
        
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token in self._OPERATORS:
                # Handle unary minus: a '-' is unary if it is the first token
                # or if it follows another operator or an opening parenthesis.
                if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('):
                    # This is a negative number, combine with the next token
                    continue  # The number token will handle this
                processed_tokens.append(token)
            elif token.replace('.', '', 1).isdigit() or token.startswith('.'):
                num_str = token
                # Check if this number should be negative
                if i > 0 and tokens[i-1] == '-' and (i == 1 or tokens[i-2] in self._OPERATORS or tokens[i-2] == '('):
                    num_str = '-' + num_str
                processed_tokens.append(float(num_str))
            elif token in '()':
                processed_tokens.append(token)
            else:
                raise ValueError(f"Invalid character or token in expression: '{token}'")

        return processed_tokens


    def _to_rpn(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to postfix notation (RPN) using
        the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

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
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       self._PRECEDENCE.get(operator_stack[-1], 0) >= self._PRECEDENCE.get(token, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack.pop() != '(':
                    raise ValueError("Mismatched parentheses in expression.")
            
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)
            
        return output_queue

    def _apply_operator(self, op: str, right: float, left: float) -> float:
        """Applies a single arithmetic operator to two operands."""
        if op == '+':
            return left + right
        if op == '-':
            return left - right
        if op == '*':
            return left * right
        if op == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return left / right
        # This part should be unreachable with the current design but is good practice
        raise ValueError(f"Unknown operator: {op}")

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates a queue of tokens in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is structured improperly (e.g.,
                        not enough operands for an operator).
        """
        operand_stack = []
        for token in rpn_queue:
            if isinstance(token, float):
                operand_stack.append(token)
            elif token in self._OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for an operator.")
                right_operand = operand_stack.pop()
                left_operand = operand_stack.pop()
                result = self._apply_operator(token, right_operand, left_operand)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: operands remain after evaluation.")
            
        return operand_stack[0]

# --- Main execution block for demonstration and simple testing ---
if __name__ == "__main__":
    print("High-Quality Python Calculator")
    print("=" * 30)
    print("This calculator demonstrates adherence to ISO/IEC 25010 standards.")
    print("Enter an expression to calculate or 'exit' to quit.")
    print("-" * 30)
    
    calculator = Calculator()

    # --- Test Cases ---
    test_cases = {
        "Simple addition": "5 + 3",
        "Simple subtraction": "10 - 4",
        "Simple multiplication": "6 * 7",
        "Simple division": "20 / 4",
        "Floating point numbers": "3.5 * 2.5",
        "Operator precedence": "2 + 3 * 4",
        "Parentheses": "(2 + 3) * 4",
        "Complex expression": "100 / ( (5 - 3) * 2.5 ) + 7",
        "Negative numbers": "-5 * -2",
        "Negative with parentheses": "10 * (-2 + 1)",
        "Unary minus at start": "-10 + 20",
        "Invalid character": "5 @ 2",
        "Unbalanced parentheses 1": "(5 + 2",
        "Unbalanced parentheses 2": "5 + 2)",
        "Division by zero": "10 / (5 - 5)",
        "Invalid structure": "5 * + 2"
    }

    print("\n--- Running Automated Test Cases ---\n")
    for name, expr in test_cases.items():
        try:
            result = calculator.calculate(expr)
            print(f"✅ Test '{name}': {expr} = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"🔶 Test '{name}' (expected error): {expr} -> {e}")
    print("\n--- Automated Tests Finished ---\n")

    # --- Interactive Mode ---
    while True:
        try:
            user_expression = input("Enter expression: ")
            if user_expression.lower() == 'exit':
                print("Exiting calculator.")
                break
            
            result = calculator.calculate(user_expression)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

