
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.

    This class provides a safe and efficient way to evaluate mathematical
    expressions containing integers, floating-point numbers, basic arithmetic
    operations (+, -, *, /), and parentheses.

    It adheres to ISO/IEC 25010 quality standards by focusing on:
    - Functional Suitability: Correctly implements the required arithmetic logic.
    - Performance Efficiency: Uses an efficient O(n) algorithm (Shunting-yard).
    - Reliability: Handles errors gracefully (e.g., invalid input, div by zero).
    - Security: Avoids `eval()` to prevent code injection vulnerabilities.
    - Maintainability: Employs a modular, well-documented, and object-oriented design.
    - Testability: Internal logic is separated into distinct, testable methods.
    """

    # Operator precedence and associativity. Unary minus '~' has the highest precedence.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'left'},
        '-': {'precedence': 1, 'assoc': 'left'},
        '*': {'precedence': 2, 'assoc': 'left'},
        '/': {'precedence': 2, 'assoc': 'left'},
        '~': {'precedence': 3, 'assoc': 'right'}  # Unary minus
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression string and returns the result.

        This is the main public interface for the Calculator.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., syntax error,
                        unbalanced parentheses, invalid characters).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(rpn_tokens)
            return result
        except (ValueError, IndexError) as e:
            # Catch internal errors and re-raise as a more user-friendly ValueError.
            # IndexError can occur from popping from empty stacks on malformed expressions.
            raise ValueError(f"Invalid expression provided: {e}") from e
        except ZeroDivisionError:
            # Re-raise ZeroDivisionError as it's a specific and clear error.
            raise ZeroDivisionError("Division by zero is not allowed.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens.

        This method handles numbers (integers, floats), operators, and parentheses.
        It also distinguishes between binary subtraction (-) and unary negation (~).

        Args:
            expression: The raw expression string.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: If an unrecognized character is found.
        """
        # Regex to find numbers (including floats), operators, and parentheses.
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression.replace(" ", ""))

        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters.")

        # Process tokens to handle unary minus
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-':
                # It's a unary minus if it's the first token, or if it follows
                # an operator or an opening parenthesis.
                is_unary = (i == 0) or (tokens[i-1] in "+-*/(")
                if is_unary:
                    processed_tokens.append('~')
                else:
                    processed_tokens.append('-')
            else:
                processed_tokens.append(token)
        return processed_tokens

    def _infix_to_postfix(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts a list of infix tokens to a postfix (RPN) list.

        This implementation uses the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in Reverse Polish Notation.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue: List[Union[float, str]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if token.replace('.', '', 1).replace('~', '', 1).isdigit():
                output_queue.append(float(token))
            elif token in self._OPERATORS:
                while (operator_stack and operator_stack[-1] != '(' and
                       (self._OPERATORS[operator_stack[-1]]['precedence'] > self._OPERATORS[token]['precedence'] or
                        (self._OPERATORS[operator_stack[-1]]['precedence'] == self._OPERATORS[token]['precedence'] and
                         self._OPERATORS[token]['assoc'] == 'left'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses.")
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses.")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, rpn_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a postfix (RPN) token list.

        Args:
            rpn_tokens: A list of tokens in RPN.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero occurs.
        """
        value_stack: List[float] = []

        for token in rpn_tokens:
            if isinstance(token, float):
                value_stack.append(token)
            else:  # Token is an operator
                if token == '~':  # Unary minus
                    if not value_stack:
                        raise ValueError("Invalid syntax for unary minus.")
                    operand = value_stack.pop()
                    value_stack.append(-operand)
                else: # Binary operator
                    if len(value_stack) < 2:
                        raise ValueError("Invalid syntax, missing operands.")
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
                            raise ZeroDivisionError()
                        value_stack.append(operand1 / operand2)

        if len(value_stack) != 1:
            raise ValueError("Expression is malformed.")

        return value_stack[0]


# --- Demonstration ---
if __name__ == "__main__":
    # This block demonstrates the usage of the Calculator class
    # and serves as a simple set of integration tests.
    calc = Calculator()
    
    expressions_to_test = [
        "3 + 4 * 2 / ( 1 - 5 )",
        "10 + 2 * 6",
        "100 * 2 + 12",
        "100 * ( 2 + 12 )",
        "100 * ( 2 + 12 ) / 14",
        "3 * (3 + 3) / 6",
        "-3 * 2",
        "5 + -2",
        "-(3 + 4)",
        "1 / 3",
        ".5 * 2",
        "10 / -2.5"
    ]

    print("--- Calculator Demonstration ---")
    for expr in expressions_to_test:
        try:
            result = calc.calculate(expr)
            print(f'Expression: "{expr}"  =>  Result: {result}')
        except (ValueError, ZeroDivisionError) as e:
            print(f'Expression: "{expr}"  =>  Error: {e}')

    print("\n--- Testing Error Cases ---")
    error_expressions = [
        "3 +",                 # Incomplete expression
        "3 + 4 )",             # Mismatched parentheses
        "(3 + 4",              # Mismatched parentheses
        "5 * (3 + 2",          # Mismatched parentheses
        "1 / 0",               # Division by zero
        "3 & 4",               # Invalid character
        "3 3 + 4"              # Invalid syntax (missing operator)
    ]
    
    for expr in error_expressions:
        try:
            calc.calculate(expr)
        except (ValueError, ZeroDivisionError) as e:
            print(f'Expression: "{expr}"  =>  Successfully caught error: {e}')

