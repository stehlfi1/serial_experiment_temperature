
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class implements a calculator that can handle addition, subtraction,
    multiplication, division, and parentheses. It adheres to standard operator
    precedence. The implementation follows the principles of the ISO/IEC 25010
    standard for software quality.

    Characteristics based on ISO/IEC 25010:
    - Functional Suitability: Correctly computes expressions with specified operators.
    - Performance Efficiency: Uses an O(n) algorithm (Shunting-yard).
    - Reliability: Handles invalid inputs and operational errors (e.g., division
      by zero) gracefully by raising specific, catchable exceptions.
    - Security: Avoids using `eval()` to prevent code injection vulnerabilities.
    - Maintainability: The code is modular, with distinct methods for tokenization,
      parsing (Shunting-yard), and evaluation. This improves analyzability and
      modifiability.
    - Testability: Each component (_tokenize, _shunting_yard, _evaluate_rpn) can be
      unit tested independently.
    - Usability (for developers): Clear documentation, type hints, and readable
      code make the class easy to integrate and understand.
    """

    def __init__(self):
        """Initializes the Calculator, defining operators and their precedence."""
        self._operators = {
            '+': {'precedence': 1, 'assoc': 'L'},
            '-': {'precedence': 1, 'assoc': 'L'},
            '*': {'precedence': 2, 'assoc': 'L'},
            '/': {'precedence': 2, 'assoc': 'L'},
        }

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an infix expression string into a list of tokens.

        This method handles integers, floating-point numbers, and operators.
        It is also responsible for distinguishing between a unary minus (e.g., -5)
        and a binary subtraction operator (e.g., 10 - 5).

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove all whitespace for easier parsing
        expression = expression.replace(" ", "")
        
        # Regex to find numbers (including floats), operators, and parentheses
        token_regex = re.compile(r"(\d+\.?\d*|[+\-*/()])")
        tokens = token_regex.findall(expression)

        # Post-process to handle unary minus
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-':
                # A minus sign is unary if:
                # 1. It's the first token.
                # 2. It follows an operator or an opening parenthesis.
                is_first_token = (i == 0)
                follows_operator_or_paren = (i > 0 and tokens[i-1] in self._operators or tokens[i-1] == '(')
                
                if is_first_token or follows_operator_or_paren:
                    # Combine with the next token (which must be a number)
                    if i + 1 < len(tokens) and tokens[i+1].replace('.', '', 1).isdigit():
                        # This is a unary minus, so we prepend it to the next number.
                        # The next token will be skipped in the next iteration.
                        # We mark it as 'processed' to avoid double-counting.
                        tokens[i+1] = '-' + tokens[i+1]
                        continue # Skip appending the standalone '-'
                    else:
                        raise ValueError(f"Invalid use of operator '-' at position {i}")
            
            # Check for invalid characters that were not matched by the regex
            # This check is implicitly handled by comparing the joined tokens with the original string
            processed_tokens.append(token)
        
        if "".join(processed_tokens) != expression:
            raise ValueError("Expression contains invalid characters.")

        return processed_tokens


    def _shunting_yard(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to a postfix (RPN) list.

        This method implements Dijkstra's Shunting-yard algorithm to handle
        operator precedence and associativity.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in Reverse Polish Notation (RPN).

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[str] = []
        operator_stack: List[str] = []

        for token in tokens:
            # If the token is a number, add it to the output queue.
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                output_queue.append(token)
            # If the token is an operator
            elif token in self._operators:
                while (operator_stack and operator_stack[-1] in self._operators and
                       self._operators[operator_stack[-1]]['precedence'] >= self._operators[token]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            # If the token is a left parenthesis
            elif token == '(':
                operator_stack.append(token)
            # If the token is a right parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Pop the left parenthesis

        # Pop any remaining operators from the stack to the output queue
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluates a tokenized expression in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN format.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero is attempted.
        """
        stack: List[float] = []

        for token in rpn_tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                stack.append(float(token))
            elif token in self._operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands for operator.")
                
                operand2 = stack.pop()
                operand1 = stack.pop()

                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Error: Division by zero.")
                    stack.append(operand1 / operand2)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: The final stack should have one value.")

        return stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public method that orchestrates the tokenization,
        parsing, and evaluation of the expression.

        Args:
            expression: The mathematical expression string.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: For invalid characters or mismatched parentheses.
            ZeroDivisionError: For division by zero.
            TypeError: If the input is not a string.
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")
        if not expression.strip():
            raise ValueError("Input expression cannot be empty.")

        tokens = self._tokenize(expression)
        rpn_tokens = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn_tokens)
        
        return result

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calc = Calculator()

    print("--- Welcome to the High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'exit' to quit.")
    print("Supported operations: +, -, *, /, ()")
    print("Example: -5.5 * (10 + 2) / 2\n")

    # --- A set of test cases to demonstrate correctness ---
    test_expressions = [
        "5 + 3",
        "10 - 4 * 2",
        "(10 - 4) * 2",
        "2 * (3 + 4) / 2",
        "10 / 2 / 5",
        "-5 + 10",
        "5 * -2",
        "-5 * -2",
        "10.5 + 2.5",
        "100 / (10 * (2 + 3))",
        "3 + 4 * 2 / ( 1 - 5 )",
        # Error cases
        "5 * (3 + 2",      # Mismatched parentheses
        "5 + * 3",        # Invalid operator sequence
        "10 / 0",         # Division by zero
        "5 & 4",          # Invalid character
        "",               # Empty expression
    ]

    print("--- Running Automated Test Cases ---")
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f'Expression: "{expr}"  =>  Result: {result}')
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f'Expression: "{expr}"  =>  Error: {e}')
    print("-" * 36)

    # --- Interactive loop ---
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("Calculate: ")
            if user_input.lower() == 'exit':
                print("Exiting calculator.")
                break
            
            result = calc.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

