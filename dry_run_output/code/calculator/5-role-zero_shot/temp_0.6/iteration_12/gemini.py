
import re

class Calculator:
    """
    A robust, console-based arithmetic calculator that evaluates string expressions.

    This class provides a safe and efficient way to compute mathematical expressions
    containing integers, floating-point numbers, parentheses, and the basic
    arithmetic operators (+, -, *, /). It adheres to standard operator
    precedence.

    The implementation uses a two-stack algorithm (a variant of Shunting-yard)
    to parse and evaluate expressions, avoiding the use of Python's `eval()`
    for security and control.

    Attributes:
        _operators (set): A set of supported operators.
        _precedence (dict): A mapping of operators to their precedence level.
    """

    _operators = {'+', '-', '*', '/'}
    _precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., malformed,
                        contains invalid characters, unbalanced parentheses).
            ZeroDivisionError: If the expression contains a division by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Expression must be a non-empty string.")

        tokens = self._tokenize(expression)
        values_stack = []
        ops_stack = []

        try:
            for token in tokens:
                if self._is_number(token):
                    values_stack.append(float(token))
                elif token == '(':
                    ops_stack.append(token)
                elif token == ')':
                    # Process operators until an opening parenthesis is found
                    while ops_stack and ops_stack[-1] != '(':
                        self._apply_top_operator(ops_stack, values_stack)
                    if not ops_stack or ops_stack.pop() != '(':
                        raise ValueError("Mismatched parentheses in expression.")
                elif token in self._operators:
                    # Process operators with higher or equal precedence
                    while (ops_stack and ops_stack[-1] in self._precedence and
                           self._precedence.get(ops_stack[-1], 0) >= self._precedence.get(token, 0)):
                        self._apply_top_operator(ops_stack, values_stack)
                    ops_stack.append(token)
                else:
                    # This case should ideally not be reached if tokenization is correct
                    raise ValueError(f"Invalid character or token: {token}")

            # Process any remaining operators on the stack
            while ops_stack:
                if ops_stack[-1] == '(':
                    raise ValueError("Mismatched parentheses in expression.")
                self._apply_top_operator(ops_stack, values_stack)

            if len(values_stack) != 1 or ops_stack:
                raise ValueError("Malformed expression.")

        except IndexError:
            # Catches errors from popping empty stacks, indicating a malformed expression
            raise ValueError("Malformed expression, check operators and operands.")

        return values_stack[0]

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts an expression string into a list of tokens.

        This tokenizer correctly handles multi-digit numbers, floating-point numbers,
        and unary minus at the beginning of an expression or after an opening parenthesis.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).
        
        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        # Add spaces around operators and parentheses to simplify splitting
        # but handle cases like '(-' to not separate the unary minus.
        expression = expression.replace('(', ' ( ').replace(')', ' ) ')
        expression = expression.replace('+', ' + ').replace('-', ' - ')
        expression = expression.replace('*', ' * ').replace('/', ' / ')
        
        raw_tokens = expression.split()
        
        # Post-process to handle unary minus
        tokens = []
        for i, token in enumerate(raw_tokens):
            is_unary_minus = (
                token == '-' and
                (i == 0 or raw_tokens[i-1] in self._operators or raw_tokens[i-1] == '(')
            )
            if is_unary_minus:
                # Combine with the next token if it's a number
                if i + 1 < len(raw_tokens) and self._is_number(raw_tokens[i+1]):
                    # The next token will be skipped in the next iteration.
                    # This is a simple lookahead, handled by modifying the list in-place.
                    raw_tokens[i+1] = '-' + raw_tokens[i+1]
                    continue # Skip appending the standalone '-'
                else:
                    raise ValueError("Invalid use of unary minus.")
            
            tokens.append(token)

        # Final validation of tokens
        for token in tokens:
            if not (self._is_number(token) or token in self._operators or token in '()'):
                raise ValueError(f"Invalid character or token found: {token}")

        return tokens

    def _apply_top_operator(self, ops_stack: list, values_stack: list) -> None:
        """
        Applies the operator at the top of the ops_stack to the top two
        values on the values_stack.

        Args:
            ops_stack: The stack of operators.
            values_stack: The stack of numerical values.

        Raises:
            ValueError: If there are not enough values on the stack for the operation.
            ZeroDivisionError: If the operation is a division by zero.
        """
        if len(values_stack) < 2:
            raise ValueError("Invalid expression: not enough operands for an operator.")
            
        op = ops_stack.pop()
        right_operand = values_stack.pop()
        left_operand = values_stack.pop()

        if op == '+':
            values_stack.append(left_operand + right_operand)
        elif op == '-':
            values_stack.append(left_operand - right_operand)
        elif op == '*':
            values_stack.append(left_operand * right_operand)
        elif op == '/':
            if right_operand == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            values_stack.append(left_operand / right_operand)

    @staticmethod
    def _is_number(s: str) -> bool:
        """Checks if a string can be converted to a float."""
        try:
            float(s)
            return True
        except ValueError:
            return False

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()
    print("--- Console Arithmetic Calculator ---")
    print("Enter 'exit' to quit.")
    
    # Example test cases to demonstrate functionality and correctness
    test_expressions = [
        "3 + 5 * 2",              # Precedence
        "(3 + 5) * 2",            # Parentheses
        "10 / 2 - 3",             # Subtraction and Division
        "2.5 * 4",                # Floating point numbers
        "-5 + 10",                # Unary minus at start
        "10 * -2",                # Unary minus after operator
        "10 * (-2 + 1)",          # Complex unary minus
        "1 / 3",                  # Floating point result
        "10 / (2 - 2)",           # Division by zero error
        "5 + (3 *",               # Malformed expression (unbalanced parentheses)
        "5 + * 3",                # Malformed expression (operator sequence)
        "hello + world",          # Invalid characters
    ]

    print("\n--- Running Demonstration Tests ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: {expr:<20} | Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: {expr:<20} | Error: {e}")

    print("\n--- Interactive Mode ---")
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

