
import re
from typing import List, Union

class Calculator:
    """
    A safe and efficient console-based arithmetic calculator.

    This class evaluates mathematical expressions from a string input, adhering to
    standard operator precedence. It is designed with the ISO/IEC 25010 standard
    in mind, emphasizing reliability, maintainability, and security.

    The evaluation process is implemented using the Shunting-yard algorithm to
    convert the infix expression to Reverse Polish Notation (RPN), which is then
    evaluated. This avoids the use of Python's `eval()` function, mitigating
    associated security risks.

    Supported features:
    - Operations: Addition (+), Subtraction (-), Multiplication (*), Division (/)
    - Numbers: Integers, floating-point numbers, and negative values.
    - Grouping: Parentheses () for overriding operator precedence.
    """

    # Operator precedence and associativity definitions.
    # Higher number means higher precedence.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'L'},
        '-': {'precedence': 1, 'assoc': 'L'},
        '*': {'precedence': 2, 'assoc': 'L'},
        '/': {'precedence': 2, 'assoc': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression string and returns the result.

        This is the public interface for the Calculator. It orchestrates the
        tokenization, parsing, and evaluation of the expression.

        Args:
            expression: The mathematical expression to evaluate (e.g., "3 + 4 * 2").

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression contains invalid characters, unbalanced
                        parentheses, or is otherwise malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions with a more informative context.
            raise type(e)(f"Invalid expression: {e}") from e
        except IndexError:
            # Catches errors from popping from empty stacks, indicating a malformed expression.
            raise ValueError("Malformed expression, check operators and operands.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the raw expression string into a list of tokens.

        This method handles numbers (including floats and negatives), operators,
        and parentheses. It also performs initial validation for invalid characters.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens (e.g., ['-3.5', '+', '(', '10', ')']).

        Raises:
            ValueError: If an unrecognized character is found.
        """
        # Regex to find numbers (int/float), operators, or parentheses.
        # This pattern correctly handles negative numbers at the start or after an operator/paren.
        token_regex = re.compile(r'(-?\d+\.?\d*)|([+\-*/()])')
        
        tokens = token_regex.findall(expression)
        # The regex findall returns tuples, so we flatten the list.
        processed_tokens = [item for group in tokens for item in group if item]

        # Validate that the entire string was tokenized.
        if ''.join(processed_tokens).replace(" ", "") != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters.")
            
        return processed_tokens

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If parentheses are mismatched.
        """
        output_queue: List[str] = []
        operator_stack: List[str] = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in self._OPERATORS:
                op1 = token
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       (self._OPERATORS[operator_stack[-1]]['precedence'] > self._OPERATORS[op1]['precedence'] or
                        (self._OPERATORS[operator_stack[-1]]['precedence'] == self._OPERATORS[op1]['precedence'] and self._OPERATORS[op1]['assoc'] == 'L'))):
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

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        value_stack: List[float] = []

        for token in rpn_tokens:
            if self._is_number(token):
                value_stack.append(float(token))
            elif token in self._OPERATORS:
                if len(value_stack) < 2:
                    raise ValueError("Not enough operands for operator.")
                
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
                        raise ZeroDivisionError("Division by zero.")
                    value_stack.append(operand1 / operand2)

        if len(value_stack) != 1:
            raise ValueError("Expression is malformed.")

        return value_stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """Utility method to check if a token can be converted to a float."""
        try:
            float(token)
            return True
        except ValueError:
            return False


# --- Main execution block for demonstration and simple testing ---
if __name__ == "__main__":
    calculator = Calculator()

    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'exit' to quit.")

    # A set of test cases to demonstrate correctness
    test_expressions = [
        "3 + 4 * 2 / ( 1 - 5 )",
        "10 * (2 + 3)",
        "100 / 10 * 2",
        "3.5 + 4.5",
        "-5 * -2",
        "10 / 3",
        "1 + 1",
        # Error cases
        "1 / 0",
        "1 + (2 * 3",
        "1 + 2)",
        "1 + a",
        "5 * + 3",
    ]

    print("\n--- Running Automated Test Cases ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f'Expression: "{expr}"  =>  Result: {result}')
        except (ValueError, ZeroDivisionError) as e:
            print(f'Expression: "{expr}"  =>  Error: {e}')
    
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

