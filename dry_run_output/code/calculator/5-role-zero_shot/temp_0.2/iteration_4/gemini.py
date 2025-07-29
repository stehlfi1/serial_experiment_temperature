
import re
from typing import List, Union

class Calculator:
    """
    A high-quality, safe, and efficient arithmetic expression evaluator.

    This class implements a calculator that can parse and evaluate string-based
    mathematical expressions, adhering to standard operator precedence. It is
    designed with the ISO/IEC 25010 standard in mind, focusing on correctness,
    reliability, performance, and maintainability.

    Features:
    - Supports addition (+), subtraction (-), multiplication (*), division (/).
    - Correctly handles operator precedence (PEMDAS/BODMAS).
    - Supports parentheses for grouping.
    - Accepts integers and floating-point numbers, including negative values.
    - Provides robust validation and clear error messages.
    - Does NOT use the unsafe `eval()` function.

    The implementation uses the Shunting-yard algorithm to convert the infix
    expression to Reverse Polish Notation (RPN), which is then evaluated.
    """

    # Define operator precedence and associativity for the Shunting-yard algorithm.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'L'},
        '-': {'precedence': 1, 'assoc': 'L'},
        '*': {'precedence': 2, 'assoc': 'L'},
        '/': {'precedence': 2, 'assoc': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the calculator. It orchestrates
        the tokenization, parsing (infix to RPN), and evaluation steps.

        Args:
            expression: The mathematical expression to evaluate (e.g., "3 + 4 * (2 - 1)").

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., contains unknown
                        characters, unbalanced parentheses, or is malformed).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        self._validate_expression(expression)
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, IndexError) as e:
            # Catch potential errors during parsing/evaluation (e.g., malformed expression)
            # and re-raise as a more user-friendly error.
            raise ValueError(f"Invalid or malformed expression: {e}") from e

    def _validate_expression(self, expression: str) -> None:
        """
        Performs initial validation on the input expression string.

        Args:
            expression: The expression string to validate.

        Raises:
            ValueError: If validation fails.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Expression must be a non-empty string.")

        # 1. Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            raise ValueError("Mismatched parentheses in expression.")

        # 2. Check for invalid characters
        allowed_chars = "0123456789.+-*/() "
        if any(char not in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the expression string into a list of tokens (numbers, operators, parentheses).

        This tokenizer correctly handles multi-digit numbers, floating-point numbers,
        and unary minus (e.g., "-5" or "(-5)").

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of string tokens.
        """
        # Add spaces around operators and parentheses to simplify splitting.
        # This regex uses lookbehind and lookahead to insert spaces without consuming the characters.
        expression = re.sub(r'([+\-*/()])', r' \1 ', expression)
        tokens = expression.split()

        # Handle unary minus: A '-' is unary if it's the first token or
        # follows an operator or an opening parenthesis.
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('):
                # This is a unary minus. We represent it by prepending a '0'.
                # e.g., "-5" becomes "0 - 5", and "( -5 )" becomes "( 0 - 5 )"
                processed_tokens.append('0')
            processed_tokens.append(token)
        return processed_tokens

    def _to_rpn(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN) using Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order. Numbers are converted to floats.

        Raises:
            ValueError: For mismatched parentheses or other syntax errors.
        """
        output_queue: List[Union[float, str]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                output_queue.append(float(token))
            elif token in self._OPERATORS:
                op1 = token
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       (self._OPERATORS[operator_stack[-1]]['precedence'] > self._OPERATORS[op1]['precedence'] or
                        (self._OPERATORS[operator_stack[-1]]['precedence'] == self._OPERATORS[op1]['precedence'] and
                         self._OPERATORS[op1]['assoc'] == 'L'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op1)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses.")
                operator_stack.pop()  # Discard the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a token list in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the expression is malformed.
        """
        operand_stack: List[float] = []

        for token in rpn_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            elif token in self._OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands for operator.")
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()

                if token == '+':
                    operand_stack.append(op1 + op2)
                elif token == '-':
                    operand_stack.append(op1 - op2)
                elif token == '*':
                    operand_stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    operand_stack.append(op1 / op2)

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression: too many operands.")

        return operand_stack[0]


# --- Main execution block for demonstration and manual testing ---
if __name__ == "__main__":
    calculator = Calculator()
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    print("Example: 3.5 + 4 * (2 - 1) / 2\n")

    while True:
        try:
            expression_input = input(">>> ")
            if expression_input.lower() == 'exit':
                print("Exiting calculator.")
                break

            result = calculator.calculate(expression_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        print("-" * 20)

