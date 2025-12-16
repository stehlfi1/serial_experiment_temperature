
import re

class Calculator:
    """
    A robust, console-based arithmetic calculator that evaluates string expressions.

    This class provides a safe and efficient way to compute mathematical
    expressions containing integers, floating-point numbers, parentheses, and
    the basic arithmetic operations (+, -, *, /).

    It adheres to standard operator precedence and is designed with principles
    from ISO/IEC 25010 in mind, focusing on correctness, reliability,
    efficiency, and maintainability.

    Attributes:
        _operators (dict): A mapping of operator symbols to their precedence level.
    """

    def __init__(self):
        """Initializes the Calculator."""
        self._operators = {'+': 1, '-': 1, '*': 2, '/': 2}

    def _precedence(self, op: str) -> int:
        """
        Returns the precedence of a given operator.

        Args:
            op: The operator character (e.g., '+', '*').

        Returns:
            An integer representing the operator's precedence.
        """
        return self._operators.get(op, 0)

    def _apply_op(self, op: str, b: float, a: float) -> float:
        """
        Applies an operator to two operands.

        Args:
            op: The operator to apply.
            b: The second operand.
            a: The first operand.

        Returns:
            The result of the operation.

        Raises:
            ZeroDivisionError: If the operator is '/' and the second operand is 0.
        """
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return a / b
        # This part should not be reached with valid operators
        raise ValueError(f"Unsupported operator: {op}")

    def _tokenize(self, expression: str) -> list:
        """
        Converts an infix expression string into a list of tokens.

        This method handles numbers (including floating-point and negative),
        operators, and parentheses. It also performs initial validation for
        invalid characters.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens (floats and strings).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to find numbers (including scientific notation), operators, and parentheses
        token_regex = re.compile(r'(\d+\.?\d*([eE][-+]?\d+)?|\.\d+([eE][-+]?\d+)?|[+\-*/()])')
        tokens = token_regex.findall(expression)
        
        # The regex findall may return tuples for matched groups, flatten them.
        raw_tokens = [item[0] for item in tokens]

        # Verify that all parts of the string were tokenized
        if ''.join(raw_tokens) != expression.replace(' ', ''):
            raise ValueError("Expression contains invalid characters or formatting.")

        # Process tokens to handle unary minus and convert numbers
        processed_tokens = []
        for i, token in enumerate(raw_tokens):
            if token == '-' and (i == 0 or raw_tokens[i-1] in self._operators or raw_tokens[i-1] == '('):
                # This is a unary minus, not subtraction. Combine with the next token.
                # This case is handled by parsing the number directly in the next step.
                continue
            
            # Check for number (including a preceding unary minus)
            if token.isdigit() or token.startswith('.') or (token.startswith('-') and len(token) > 1):
                processed_tokens.append(float(token))
            elif token == '-' and i + 1 < len(raw_tokens) and (raw_tokens[i+1].isdigit() or raw_tokens[i+1].startswith('.')):
                # Combine unary minus with the following number
                next_token = raw_tokens[i+1]
                processed_tokens.append(float(f"-{next_token}"))
                # Skip the next token as it has been consumed
                raw_tokens[i+1] = '' # Mark as consumed
            elif token: # Append operators and parentheses
                processed_tokens.append(token)
                
        return processed_tokens

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This method implements a variant of the Shunting-yard algorithm to
        correctly evaluate expressions with proper operator precedence and
        parentheses.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid
                        characters, or has unbalanced parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression must be a non-empty string.")

        try:
            tokens = self._tokenize(expression)
        except ValueError as e:
            # Re-raise tokenization errors with context
            raise ValueError(f"Invalid expression format: {e}") from e

        values: list[float] = []  # Stack for number values
        ops: list[str] = []       # Stack for operators and parentheses

        for token in tokens:
            if isinstance(token, float):
                values.append(token)
            elif token == '(':
                ops.append(token)
            elif token == ')':
                # Evaluate expression inside the parentheses
                while ops and ops[-1] != '(':
                    op = ops.pop()
                    # Ensure there are enough values to perform the operation
                    if len(values) < 2:
                        raise ValueError("Invalid syntax: operator missing operands.")
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(self._apply_op(op, val2, val1))
                if not ops or ops.pop() != '(':
                    raise ValueError("Mismatched or unbalanced parentheses.")
            else:  # Token is an operator
                # Process operators with higher or equal precedence on the stack first
                while (ops and ops[-1] != '(' and
                       self._precedence(ops[-1]) >= self._precedence(token)):
                    op = ops.pop()
                    if len(values) < 2:
                        raise ValueError("Invalid syntax: operator missing operands.")
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(self._apply_op(op, val2, val1))
                ops.append(token)

        # Evaluate remaining operators on the stack
        while ops:
            op = ops.pop()
            if op == '(':
                raise ValueError("Mismatched or unbalanced parentheses.")
            if len(values) < 2:
                raise ValueError("Invalid syntax: operator missing operands.")
            val2 = values.pop()
            val1 = values.pop()
            values.append(self._apply_op(op, val2, val1))

        if len(values) != 1 or ops:
            raise ValueError("Malformed expression.")

        return values[0]


def main():
    """
    Main function to run the interactive calculator console.
    """
    print("--- Console Arithmetic Calculator ---")
    print("Enter a mathematical expression or 'exit' to quit.")
    
    calculator = Calculator()

    while True:
        try:
            expression = input(">>> ")
            if expression.lower() == 'exit':
                print("Exiting calculator. Goodbye!")
                break
            
            result = calculator.calculate(expression)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
