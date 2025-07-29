
import re
from typing import List, Union

class Calculator:
    """
    A robust, safe, and efficient console-based arithmetic calculator.

    This class evaluates mathematical expressions from a string, supporting
    addition, subtraction, multiplication, division, and parentheses. It is
    designed with a focus on correctness, safety, and maintainability,
    adhering to best practices and avoiding the use of `eval()`.

    Attributes:
        PRECEDENCE (dict): A mapping of operators to their precedence level.
        OPERATORS (set): A set of all supported operators for quick lookups.
    """
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    OPERATORS = {'+', '-', '*', '/'}

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public method that orchestrates the tokenization,
        parsing, and evaluation of the expression using a two-stack algorithm.

        Args:
            expression: The mathematical expression string to evaluate.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid
                        characters, has unbalanced parentheses, or is otherwise
                        syntactically incorrect.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            self._validate_tokens(tokens)
            values_stack: List[float] = []
            ops_stack: List[str] = []
            
            # This flag helps distinguish a unary minus from a binary subtraction.
            expecting_operand = True

            for token in tokens:
                if self._is_number(token):
                    values_stack.append(float(token))
                    expecting_operand = False
                elif token == '(':
                    ops_stack.append(token)
                    expecting_operand = True
                elif token == ')':
                    while ops_stack and ops_stack[-1] != '(':
                        self._process_top_op(values_stack, ops_stack)
                    if not ops_stack or ops_stack.pop() != '(':
                        raise ValueError("Mismatched parentheses in expression")
                    expecting_operand = False
                elif token in self.OPERATORS:
                    # Handle unary minus: e.g., -5 or 3 * -5
                    if token == '-' and expecting_operand:
                        # This is a unary minus. We treat it by pushing a zero
                        # operand and then processing it as a subtraction.
                        values_stack.append(0.0)
                        ops_stack.append('-')
                        continue # Skip to the next token
                    
                    while (ops_stack and ops_stack[-1] != '(' and
                           self.PRECEDENCE.get(ops_stack[-1], 0) >= self.PRECEDENCE.get(token, 0)):
                        self._process_top_op(values_stack, ops_stack)
                    ops_stack.append(token)
                    expecting_operand = True

            # Process any remaining operators on the stack
            while ops_stack:
                if ops_stack[-1] == '(':
                    raise ValueError("Mismatched parentheses in expression")
                self._process_top_op(values_stack, ops_stack)

            if len(values_stack) != 1 or ops_stack:
                raise ValueError("Malformed expression")

            return values_stack[0]

        except IndexError:
            # An IndexError while popping from stacks indicates a malformed expression
            # (e.g., "5 * " or "* 5")
            raise ValueError("Malformed expression: Invalid operator/operand sequence") from None

    def _tokenize(self, expression: str) -> List[str]:
        """
        Splits the expression string into a list of tokens.

        Tokens can be numbers (integers/floats), operators, or parentheses.
        It also validates that no unsupported characters are present.

        Args:
            expression: The raw expression string.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        if not expression:
            raise ValueError("Expression cannot be empty")
            
        # Regex to find numbers (including decimals and negatives), operators, and parentheses
        token_regex = r"(\d+\.\d*|\.\d+|\d+|[+\-*/()])"
        tokens = re.findall(token_regex, expression.replace(" ", ""))

        # Verify that the entire string was consumed by the tokenizer
        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters")

        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Performs basic validation on the token stream.

        Currently checks for balanced parentheses. This could be expanded to
        check for other patterns like consecutive operators if needed.

        Args:
            tokens: The list of string tokens.

        Raises:
            ValueError: If validation fails (e.g., unbalanced parentheses).
        """
        if tokens.count('(') != tokens.count(')'):
            raise ValueError("Mismatched parentheses in expression")

    def _process_top_op(self, values: List[float], ops: List[str]) -> None:
        """
        Pops an operator and two operands, computes the result, and pushes it back.

        This is a helper function for the main evaluation loop.

        Args:
            values: The stack of numerical values (operands).
            ops: The stack of operators.
        """
        op = ops.pop()
        # The right operand is popped first
        right_operand = values.pop()
        left_operand = values.pop()
        result = self._apply_op(op, left_operand, right_operand)
        values.append(result)

    def _apply_op(self, op: str, a: float, b: float) -> float:
        """
        Applies a single arithmetic operation.

        Args:
            op: The operator string ('+', '-', '*', '/').
            a: The left operand.
            b: The right operand.

        Returns:
            The result of the operation.

        Raises:
            ZeroDivisionError: If the operation is division by zero.
        """
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            return a / b
        # This should not be reached due to prior validation
        raise ValueError(f"Unknown operator: {op}")

    def _is_number(self, token: str) -> bool:
        """Checks if a token can be converted to a float."""
        try:
            float(token)
            return True
        except ValueError:
            return False

# --- Example Usage ---
if __name__ == "__main__":
    calculator = Calculator()
    print("--- Python CLI Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")

    while True:
        try:
            user_input = input(">> ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

