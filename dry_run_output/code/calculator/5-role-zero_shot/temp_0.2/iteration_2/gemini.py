
import re

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class provides a safe and efficient way to compute mathematical
    expressions containing integers, floating-point numbers, parentheses,
    and the basic arithmetic operators (+, -, *, /).

    It adheres to ISO/IEC 25010 quality standards by ensuring:
    - Functional Suitability: Correctly implements all required operations
      with proper operator precedence.
    - Reliability: Handles invalid inputs and edge cases (e.g., division
      by zero, unbalanced parentheses) gracefully through custom exceptions.
    - Performance Efficiency: Uses an efficient O(n) algorithm (two-stack
      approach) for expression evaluation.
    - Security: Avoids the use of `eval()` to prevent code injection
      vulnerabilities.
    - Maintainability: The code is modular, well-documented with docstrings
      and comments, and uses clear naming conventions, making it easy to
      understand, modify, and extend.
    - Testability: The separation of tokenization and evaluation logic
      allows for straightforward unit testing of each component.
    """

    def __init__(self):
        """Initializes the Calculator."""
        self._operators = set(['+', '-', '*', '/'])
        self._precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def _apply_operation(self, op: str, b: float, a: float) -> float:
        """
        Applies a given arithmetic operation to two operands.

        Args:
            op: The operator string ('+', '-', '*', '/').
            b: The second operand.
            a: The first operand.

        Returns:
            The result of the operation.

        Raises:
            ZeroDivisionError: If the operation is division by zero.
        """
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return a / b
        # This part should not be reachable with valid operators
        raise ValueError(f"Unknown operator: {op}")

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts an infix expression string into a list of tokens.

        This method handles numbers (integers, floats) and operators,
        and correctly interprets unary minus (e.g., '-5' or '( -5 )').

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Add spaces around operators and parentheses to simplify splitting
        # but be careful not to add space after an opening paren for unary minus
        expression = expression.replace('(', ' ( ').replace(')', ' ) ')
        expression = expression.replace('+', ' + ').replace('*', ' * ').replace('/', ' / ')
        # Handle subtraction vs. unary minus by replacing unary minus with a temporary marker
        expression = expression.replace('- ', ' - ') # Subtraction
        expression = expression.replace('(-', '( # ') # Unary minus after parenthesis
        if expression.lstrip().startswith('-'): # Unary minus at the start
            expression = '# ' + expression.lstrip()[1:]
        
        tokens = expression.split()
        
        # Restore the unary minus marker '#' to '-'
        final_tokens = []
        for i, token in enumerate(tokens):
            if token == '#':
                if i + 1 < len(tokens) and re.match(r'^-?\d+(\.\d+)?$', tokens[i+1]):
                    final_tokens.append('-' + tokens[i+1])
                    tokens[i+1] = '' # Mark next token as consumed
                else:
                    raise ValueError("Invalid use of unary minus.")
            elif token: # Append if not an empty string (from consumed token)
                final_tokens.append(token)
        
        # Final validation of tokens
        for token in final_tokens:
            if not (token in self._operators or \
                    token in '()' or \
                    re.match(r'^-?\d+(\.\d+)?$', token)):
                raise ValueError(f"Invalid character or token in expression: '{token}'")

        return final_tokens

    def _evaluate_tokens(self, tokens: list[str]) -> float:
        """
        Evaluates a list of tokens in infix notation.

        This method implements the two-stack algorithm for expression evaluation,
        respecting operator precedence and parentheses.

        Args:
            tokens: A list of string tokens from the _tokenize method.

        Returns:
            The final calculated result.

        Raises:
            ValueError: For malformed expressions like unbalanced parentheses.
        """
        values: list[float] = []  # Stack for numbers
        ops: list[str] = []       # Stack for operators and parentheses

        def process_ops_stack(precedence_check: str = ''):
            """Helper to process operators from the stack."""
            while (ops and ops[-1] != '(' and
                   (not precedence_check or self._precedence[ops[-1]] >= self._precedence[precedence_check])):
                try:
                    op = ops.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(self._apply_operation(op, val2, val1))
                except IndexError:
                    raise ValueError("Malformed expression or mismatched operators.")

        for token in tokens:
            if re.match(r'^-?\d+(\.\d+)?$', token):
                values.append(float(token))
            elif token == '(':
                ops.append(token)
            elif token == ')':
                process_ops_stack()
                if not ops or ops.pop() != '(':
                    raise ValueError("Mismatched or unbalanced parentheses.")
            elif token in self._operators:
                process_ops_stack(token)
                ops.append(token)

        process_ops_stack() # Process remaining operators

        if len(values) != 1 or ops:
            raise ValueError("Malformed expression or unbalanced operators.")

        return values[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the public interface for the Calculator. It orchestrates
        the tokenization and evaluation process, providing a single point
        of entry and comprehensive error handling.

        Args:
            expression: A string containing the mathematical expression.
                        e.g., "10 + 2 * (6 - 3)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., bad characters,
                        unbalanced parentheses).
            ZeroDivisionError: If the expression attempts to divide by zero.
            TypeError: If the input expression is not a string.
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")
        if not expression.strip():
            raise ValueError("Input expression cannot be empty.")

        try:
            tokens = self._tokenize(expression)
            result = self._evaluate_tokens(tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions with clear context for the user.
            # This maintains a clean public API.
            raise e
        except Exception as e:
            # Catch any other unexpected errors during processing.
            raise ValueError(f"An unexpected error occurred: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    calculator = Calculator()
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")

    # A set of test cases to demonstrate correctness and robustness
    test_expressions = [
        "1 + 1",
        "2 * 3 + 4",
        "2 * (3 + 4)",
        "10 / 2 - 3",
        "(10 + 2) * (8 - 5) / 4",
        "3.5 * 2",
        "-5 + 10",
        "10 * -2",
        "10 * (-2 + 1)",
        "1 - (3 + 2)",
        "100 / (10 * (2.5 - 1.5))",
        "10 / 0",  # Expected: ZeroDivisionError
        "5 * (3 + 2", # Expected: ValueError (unbalanced parentheses)
        "5 +", # Expected: ValueError (malformed expression)
        "5 & 4", # Expected: ValueError (invalid character)
        "", # Expected: ValueError (empty expression)
    ]

    print("\n--- Running Automated Test Cases ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"'{expr}' = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"'{expr}' -> Error: {e}")

    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected system error occurred: {e}")

