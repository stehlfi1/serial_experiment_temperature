
import re
from typing import List, Union

class Calculator:
    """
    A high-quality, safe, and maintainable arithmetic calculator.

    This class evaluates mathematical expressions from a string, supporting addition,
    subtraction, multiplication, division, and parentheses. It adheres to standard
    operator precedence.

    The implementation uses a two-stack approach, a variant of Dijkstra's
    Shunting-yard algorithm, to safely parse and evaluate the expression
    without using Python's `eval()` function.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Correctly computes expressions.
    - Performance Efficiency: O(n) time complexity.
    - Maintainability: Modular design with private helpers and clear documentation.
    - Reliability: Robust error handling for invalid inputs.
    - Security: Avoids `eval()` to prevent code injection vulnerabilities.
    - Testability: Clear, single-point-of-entry public method.
    """

    def __init__(self):
        """Initializes the Calculator, setting up operator precedence."""
        self._precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        self._operators = set(self._precedence.keys())

    def _apply_operator(self, operators: List[str], values: List[float]) -> None:
        """
        Applies the top operator from the stack to the top two values.

        Pops one operator and two values, performs the calculation, and pushes
        the result back to the values stack.

        Args:
            operators: The stack of operators.
            values: The stack of numerical values.

        Raises:
            ValueError: If there are not enough values for the operation.
            ZeroDivisionError: If attempting to divide by zero.
        """
        if len(values) < 2 or len(operators) < 1:
            raise ValueError("Invalid expression: Mismatched operators and operands.")

        operator = operators.pop()
        right_operand = values.pop()
        left_operand = values.pop()

        if operator == '+':
            values.append(left_operand + right_operand)
        elif operator == '-':
            values.append(left_operand - right_operand)
        elif operator == '*':
            values.append(left_operand * right_operand)
        elif operator == '/':
            if right_operand == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            values.append(left_operand / right_operand)

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an expression string into a list of tokens.

        This tokenizer correctly handles integers, floating-point numbers,
        operators, parentheses, and unary minus (e.g., '-5' or '3 * -2').

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to find numbers (int/float), operators, or parentheses
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression)
        
        # Post-process to handle unary minus
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._operators or tokens[i-1] == '('):
                # This is a unary minus. Combine it with the next number.
                if i + 1 < len(tokens) and re.match(r"\d+\.?\d*|\.\d+", tokens[i+1]):
                    processed_tokens.append(f"-{tokens[i+1]}")
                    # Skip the next token since we've consumed it
                    tokens[i+1] = '' 
                else:
                    raise ValueError(f"Invalid expression: Dangling unary minus.")
            elif token: # Skip empty tokens created by unary minus handling
                processed_tokens.append(token)
        
        # Final validation for any characters not caught by the regex
        reconstructed_expr = "".join(processed_tokens)
        if len(reconstructed_expr) != len(expression.replace(" ", "")):
            raise ValueError("Invalid characters in expression.")

        return processed_tokens

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: A string containing the arithmetic expression.
                        e.g., "3 + 5 * (2 - 8)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., unbalanced
                        parentheses, invalid characters).
            ZeroDivisionError: If the expression involves division by zero.
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")
        
        tokens = self._tokenize(expression)
        values: List[float] = []
        operators: List[str] = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                values.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                if not operators or operators.pop() != '(':
                    raise ValueError("Invalid expression: Mismatched parentheses.")
            elif token in self._operators:
                while (operators and operators[-1] != '(' and
                       self._precedence.get(operators[-1], 0) >= self._precedence.get(token, 0)):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                # This case should ideally be caught by the tokenizer
                raise ValueError(f"Invalid token in expression: {token}")

        # Apply remaining operators
        while operators:
            if operators[-1] == '(':
                raise ValueError("Invalid expression: Mismatched parentheses.")
            self._apply_operator(operators, values)

        if len(values) != 1 or operators:
            raise ValueError("Invalid expression: Malformed structure.")

        return values[0]

# --- Main execution block for demonstration and simple testing ---
if __name__ == "__main__":
    calculator = Calculator()

    print("--- Console Arithmetic Calculator ---")
    print("Enter 'exit' to quit.")

    # A suite of test cases to demonstrate correctness and robustness
    test_expressions = {
        "Simple Addition": "5 + 3",
        "Simple Subtraction": "10 - 4",
        "Simple Multiplication": "6 * 7",
        "Simple Division": "20 / 4",
        "Operator Precedence": "2 + 3 * 4",
        "Parentheses": "(2 + 3) * 4",
        "Floating Point Numbers": "1.5 + 2.5 * 4",
        "Negative Numbers": "-5 + 10",
        "Complex Expression": "10 + 2 * (6 - (25 / 5) + 3) - 1",
        "Unary Minus Complex": "5 * -2 + (-10 / -2)",
        "Invalid Character": "5 @ 2",
        "Unbalanced Parentheses 1": "(5 + 2",
        "Unbalanced Parentheses 2": "5 + 2)",
        "Division by Zero": "10 / (5 - 5)",
        "Malformed Expression": "5 * + 2"
    }

    print("\n--- Running Automated Test Cases ---")
    for name, expr in test_expressions.items():
        try:
            result = calculator.calculate(expr)
            print(f"✅ {name:<25} | Expression: {expr:<30} | Result: {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"❌ {name:<25} | Expression: {expr:<30} | Error: {e}")
    
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("Enter expression: ")
            if user_input.lower() == 'exit':
                break
            if user_input:
                result = calculator.calculate(user_input)
                print(f"Result: {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

