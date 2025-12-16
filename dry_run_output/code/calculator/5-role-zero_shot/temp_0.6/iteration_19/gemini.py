
import re
from typing import Union, List

class Calculator:
    """
    A high-quality, maintainable calculator for evaluating arithmetic expressions.

    This class provides a robust implementation for parsing and evaluating
    standard arithmetic expressions, including support for addition, subtraction,
    multiplication, division, parentheses, and correct operator precedence.

    It is designed with the ISO/IEC 25010 software quality standard in mind:
    - Functional Suitability: Correctly computes results for valid expressions.
    - Performance Efficiency: Implements the Shunting-yard algorithm, which
      parses expressions in O(n) time complexity.
    - Reliability & Safety: Includes comprehensive validation to gracefully
      handle invalid inputs, syntax errors (e.g., mismatched parentheses),
      and runtime errors like division by zero.
    - Security: Explicitly avoids the use of `eval()` or similar functions to
      prevent code injection vulnerabilities.
    - Maintainability & Testability: The logic is separated into modular private
      methods for tokenization, parsing (infix to postfix), and evaluation.
      This separation of concerns makes the code easier to understand, test,
      and extend.
    - Readability: Employs clear variable names, type hints, and detailed
      docstrings to ensure the code is easy to read and understand.
    """

    # Class attributes for operator properties enhance modularity and readability.
    # A special character '~' is used to represent the unary minus operator.
    _OPERATORS = {'+', '-', '*', '/', '~'}
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '~': 3} # Unary minus has the highest precedence

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string.

        This is the main public interface of the calculator. It orchestrates
        the entire process of validation, tokenization, parsing, and evaluation.

        Args:
            expression: The arithmetic expression string to evaluate.
                        It can contain numbers, operators (+, -, *, /),
                        and parentheses.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is empty, contains invalid characters,
                        has mismatched parentheses, or has a syntax error.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        self._validate_input(expression)
        tokens = self._tokenize(expression)
        postfix_tokens = self._to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _validate_input(self, expression: str) -> None:
        """
        Performs initial validation on the raw expression string.

        Args:
            expression: The input string.

        Raises:
            ValueError: For invalid characters or unbalanced parentheses.
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")
            
        # Check for invalid characters. A whitelist approach is safer.
        allowed_chars = r"0-9\.\s\+\-\*\/\(\)"
        if re.search(f"[^{allowed_chars}]", expression):
            raise ValueError("Expression contains invalid characters.")

        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            raise ValueError("Mismatched parentheses in expression.")

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts the expression string into a list of tokens (numbers and operators).

        This method handles multi-digit numbers, floating-point numbers, and
        distinguishes between binary subtraction and unary negation.

        Args:
            expression: The sanitized arithmetic expression string.

        Returns:
            A list of tokens, where numbers are floats and operators are strings.
        """
        # Remove all whitespace for easier parsing
        expression = expression.replace(" ", "")
        if not expression:
            raise ValueError("Input expression cannot be empty.")

        # Regex to find numbers, operators, and parentheses
        token_regex = re.compile(r"(\d+\.?\d*|[+\-*/()])")
        raw_tokens = token_regex.findall(expression)
        
        tokens: List[Union[float, str]] = []
        for i, token in enumerate(raw_tokens):
            if token.replace('.', '', 1).isdigit():
                tokens.append(float(token))
            elif token == '-':
                # Determine if '-' is a unary or binary operator.
                # It's unary if it's the first token or follows another operator or '('.
                is_unary = (i == 0) or (raw_tokens[i - 1] in self._OPERATORS | {'('})
                if is_unary:
                    tokens.append('~')  # Use '~' for unary minus
                else:
                    tokens.append('-')  # Binary minus
            else:
                tokens.append(token)
        return tokens

    def _to_postfix(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a list of infix tokens to postfix (Reverse Polish Notation).

        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens in infix order.

        Returns:
            A list of tokens in postfix order.
        
        Raises:
            ValueError: If there's a syntax error like mismatched parentheses.
        """
        output_queue: List[Union[float, str]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._OPERATORS:
                # Pop operators from the stack to the output queue if they
                # have higher or equal precedence.
                while (operator_stack and
                       operator_stack[-1] in self._OPERATORS and
                       self._PRECEDENCE.get(operator_stack[-1], 0) >= self._PRECEDENCE.get(token, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                # If the stack runs out without finding a '(', parentheses are mismatched.
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses syntax error.")
                operator_stack.pop()  # Discard the '('

        # Pop any remaining operators from the stack to the output
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses syntax error.")
            output_queue.append(op)

        return output_queue

    def _apply_operator(self, op: str, b: float, a: float = 0.0) -> float:
        """
        Applies a given operator to its operand(s).

        Args:
            op: The operator string ('+', '-', '*', '/', '~').
            b: The right-hand operand (or the only operand for unary operators).
            a: The left-hand operand (ignored for unary operators).

        Returns:
            The result of the operation.
        
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return a / b
        if op == '~': return -b
        # This path should not be reachable with validated inputs
        raise ValueError(f"Unknown operator: {op}")

    def _evaluate_postfix(self, postfix_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates an expression in postfix (RPN) order.

        Args:
            postfix_tokens: A list of tokens in postfix order.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the expression has an invalid syntax
                        (e.g., not enough operands for an operator).
        """
        stack: List[float] = []
        for token in postfix_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if token == '~':  # Unary operator
                    if not stack:
                        raise ValueError("Invalid syntax: Not enough operands for unary minus.")
                    operand = stack.pop()
                    result = self._apply_operator(token, operand)
                    stack.append(result)
                else:  # Binary operator
                    if len(stack) < 2:
                        raise ValueError("Invalid syntax: Not enough operands for operator.")
                    right_operand = stack.pop()
                    left_operand = stack.pop()
                    result = self._apply_operator(token, right_operand, left_operand)
                    stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression syntax: The final stack should have one number.")
        
        return stack[0]

# --- Example Usage ---
if __name__ == "__main__":
    calculator = Calculator()
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    print("Supported operations: +, -, *, /, parentheses ().")
    print("Example: (3.5 + 1.5) * -2 / (1 - 3)\n")

    while True:
        try:
            expression_input = input(">>> ")
            if expression_input.lower() == 'exit':
                break
            
            result = calculator.calculate(expression_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

