
import re
from typing import List, Union

class Calculator:
    """
    A robust, console-based arithmetic calculator that evaluates string expressions.

    This class adheres to the principles of ISO/IEC 25010, focusing on:
    - Functional Suitability: Correctly computes addition, subtraction,
      multiplication, division, and handles parentheses with correct precedence.
    - Reliability: Provides robust error handling for invalid inputs,
      unbalanced parentheses, and division by zero.
    - Performance Efficiency: Implements an efficient O(n) algorithm (Shunting-yard
      variant) for expression evaluation.
    - Security: Avoids the use of `eval()` to prevent code injection
      vulnerabilities.
    - Maintainability: Structured with clear, modular, and well-documented
      private methods, making it easy to understand, test, and extend.

    Public Interface:
        calculate(expression: str) -> float
    """

    _OPERATORS = set(['+', '-', '*', '/'])
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}

    def _apply_operation(self, ops: List[str], values: List[float]) -> None:
        """
        Applies the top operator from the ops stack to the top two values
        from the values stack.

        Args:
            ops: The stack of operators.
            values: The stack of numerical values.

        Raises:
            ValueError: If there are not enough values to perform the operation.
            ZeroDivisionError: If attempting to divide by zero.
        """
        if len(values) < 2:
            raise ValueError("Invalid expression: Not enough operands for an operator.")
        
        op = ops.pop()
        right = values.pop()
        left = values.pop()

        if op == '+':
            values.append(left + right)
        elif op == '-':
            values.append(left - right)
        elif op == '*':
            values.append(left * right)
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError("Error: Division by zero is not allowed.")
            values.append(left / right)

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts the input string expression into a list of tokens.

        This tokenizer correctly handles negative numbers, floating-point numbers,
        and operators.

        Args:
            expression: The arithmetic expression string.

        Returns:
            A list of tokens, where numbers are floats and operators/parentheses
            are strings.
        
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # This regex finds numbers (including floats and negatives), operators, and parentheses.
        # It correctly tokenizes expressions like "-5.5 * (2 + -3)"
        token_regex = re.compile(r"(\b\d+\.\d+\b|\b\d+\b|[()+\-*/])")
        tokens = token_regex.findall(expression.replace(" ", ""))

        # Check for any characters that were not captured by the regex
        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Invalid characters in expression.")

        processed_tokens: List[Union[float, str]] = []
        for i, token in enumerate(tokens):
            if token.isdigit() or '.' in token:
                processed_tokens.append(float(token))
            elif token in self._OPERATORS:
                # Handle unary minus (e.g., -5, 3 * -2)
                is_unary = (
                    i == 0 or 
                    (i > 0 and tokens[i-1] in self._OPERATORS) or
                    (i > 0 and tokens[i-1] == '(')
                )
                if token == '-' and is_unary:
                    # Combine with the next token if it's a number
                    if i + 1 < len(tokens) and (tokens[i+1].isdigit() or '.' in tokens[i+1]):
                        # This token will be handled by the next iteration, so skip.
                        tokens[i+1] = str(-float(tokens[i+1]))
                        continue 
                    else:
                        raise ValueError("Invalid use of unary minus.")
                processed_tokens.append(token)
            elif token in "()":
                processed_tokens.append(token)
        
        return processed_tokens

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The string containing the arithmetic expression.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., malformed,
                        unbalanced parentheses, invalid characters).
            ZeroDivisionError: If the expression involves division by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression must be a non-empty string.")

        tokens = self._tokenize(expression)
        
        values: List[float] = []
        ops: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                values.append(token)
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(':
                    self._apply_operation(ops, values)
                if not ops or ops[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                ops.pop()  # Pop the '('
            elif token in self._OPERATORS:
                while (ops and ops[-1] != '(' and
                       self._PRECEDENCE.get(ops[-1], 0) >= self._PRECEDENCE.get(token, 0)):
                    self._apply_operation(ops, values)
                ops.append(token)

        # Process remaining operators
        while ops:
            if ops[-1] == '(':
                raise ValueError("Mismatched parentheses in expression.")
            self._apply_operation(ops, values)

        if len(values) != 1 or ops:
            raise ValueError("Malformed expression.")

        return values[0]


if __name__ == '__main__':
    # This block demonstrates the usage of the Calculator class and serves
    # as a basic test suite.
    calculator = Calculator()

    print("--- Console Arithmetic Calculator ---")
    print("Enter 'exit' to quit.\n")

    # A dictionary of test cases to demonstrate correctness and robustness.
    test_expressions = {
        "Simple Addition": "5 + 3",
        "Simple Subtraction": "10 - 4",
        "Simple Multiplication": "6 * 7",
        "Simple Division": "8 / 4",
        "Floating Point": "2.5 * 4",
        "Operator Precedence": "2 + 3 * 4",
        "Parentheses": "(2 + 3) * 4",
        "Complex Expression": "100 / ( (1 + 1) * 2.5 ) - 5",
        "Negative Numbers": "-10 + (8 * 2.5) / -5",
        "Unary Minus Start": "-5 + 2",
        "Unary Minus Inside": "10 * -2",
        "Invalid - Division by Zero": "10 / 0",
        "Invalid - Unbalanced Parentheses": "((5 + 3) * 2",
        "Invalid - Malformed Expression": "5 * + 3",
        "Invalid - Characters": "5a + 3"
    }

    print("--- Running Automated Test Cases ---")
    for name, expr in test_expressions.items():
        try:
            result = calculator.calculate(expr)
            print(f"✅ {name}: '{expr}' = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"❌ {name}: '{expr}' -> Caught expected error: {e}")
    print("\n--- Interactive Mode ---")

    # Interactive loop
    while True:
        try:
            user_input = input("Enter expression: ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

