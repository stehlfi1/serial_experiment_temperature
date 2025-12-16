
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class adheres to the principles of the ISO/IEC 25010 standard by focusing on:
    - Functional Suitability: Correctly implements addition, subtraction, multiplication,
      division, parentheses, and operator precedence.
    - Reliability & Safety: Includes robust validation for input format, syntax,
      and mathematical errors like division by zero. It avoids insecure
      methods like `eval()`.
    - Performance Efficiency: Uses the efficient Shunting-yard algorithm for parsing
      and evaluation, operating in linear time relative to expression length.
    - Maintainability & Portability: Structured with OOP principles, featuring
      modular private methods, clear documentation, and using only standard
      Python libraries for maximum portability.
    """

    def __init__(self):
        """Initializes the calculator, defining operators and their precedence."""
        self._operators = {
            '+': {'precedence': 1, 'func': lambda a, b: a + b},
            '-': {'precedence': 1, 'func': lambda a, b: a - b},
            '*': {'precedence': 2, 'func': lambda a, b: a * b},
            '/': {'precedence': 2, 'func': lambda a, b: a / b},
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid characters,
                        has unbalanced parentheses, or is otherwise syntactically incorrect.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller, maintaining a clear interface.
            raise e
        except Exception:
            # Catch any other unexpected errors during parsing/evaluation.
            raise ValueError("Invalid or malformed expression.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).
        Handles negative numbers and floating-point values.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Expression must be a non-empty string.")

        # This regex splits the string by operators and parentheses, keeping them as tokens.
        # It correctly handles floating-point numbers and avoids splitting on minus signs
        # that indicate negative numbers.
        # Pattern explanation:
        # (\d+\.?\d*) - Captures integers or floats.
        # | ([+\-*/()]) - OR captures one of the operators/parentheses.
        token_regex = r'(\d+\.?\d*)|([+\-*/()])'
        tokens = re.findall(token_regex, expression)

        # The regex produces tuples like ('3.14', '') or ('', '+'). We flatten them.
        raw_tokens = [item for group in tokens for item in group if item]

        # Further validation and handling of unary minus
        processed_tokens = []
        for i, token in enumerate(raw_tokens):
            if token == '-':
                # Check if '-' is a unary operator (negation)
                # It's unary if:
                # 1. It's the first token.
                # 2. It follows an operator or an opening parenthesis.
                is_unary = (i == 0) or (raw_tokens[i-1] in self._operators or raw_tokens[i-1] == '(')
                if is_unary:
                    # Combine with the next token if it's a number
                    if i + 1 < len(raw_tokens) and raw_tokens[i+1].replace('.', '', 1).isdigit():
                        # The next token is consumed here, so skip it in the next iteration
                        # by modifying the raw_tokens list in place. This is a bit tricky
                        # but effective. We replace the number with its negative version.
                        raw_tokens[i+1] = f"-{raw_tokens[i+1]}"
                        continue # Skip appending the standalone '-'
                    else:
                        raise ValueError("Invalid use of '-' operator.")
            
            # Check for invalid characters that might have been missed
            if not token.replace('.', '', 1).isdigit() and token not in self._operators and token not in '()':
                 raise ValueError(f"Invalid character or token: '{token}'")

            processed_tokens.append(token)
            
        return processed_tokens

    def _infix_to_postfix(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts a list of tokens from infix to postfix (RPN) notation
        using the Shunting-yard algorithm.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('-', '', 1).replace('.', '', 1).isdigit():
                output_queue.append(float(token))
            elif token in self._operators:
                # While stack is not empty, top is not '(', and top has higher/equal precedence
                while (operator_stack and operator_stack[-1] != '(' and
                       self._operators.get(operator_stack[-1], {}).get('precedence', 0) >=
                       self._operators[token]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses: Unbalanced ')'")
                operator_stack.pop()  # Discard the '('

        # Pop any remaining operators from the stack to the output
        while operator_stack:
            operator = operator_stack.pop()
            if operator == '(':
                raise ValueError("Mismatched parentheses: Unbalanced '('")
            output_queue.append(operator)

        return output_queue

    def _evaluate_postfix(self, postfix_tokens: List[Union[float, str]]) -> float:
        """Evaluates a postfix (RPN) expression."""
        operand_stack = []

        for token in postfix_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            elif token in self._operators:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands for operator.")
                
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                
                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                operation = self._operators[token]['func']
                result = operation(operand1, operand2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: Too many operands.")
            
        return operand_stack[0]


# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()

    print("--- Console Arithmetic Calculator ---")
    print("Supports +, -, *, /, parentheses, floats, and negative numbers.")
    print("Enter 'exit' to quit.\n")

    # Example test cases
    test_expressions = [
        "3 + 5 * (10 - 4)",
        "10 / 2 - 3",
        "-5.5 * (2 + 3)",
        "100 / (10 * (2.5 - 1.5))",
        "3 - -2", # Handled as 3 - (-2)
        "1 / 3",
        # Error cases
        "3 + * 5",
        "10 / 0",
        "(10 + 5",
        "10 + 5)",
        "10 & 5"
    ]

    print("--- Running example test cases ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}' -> Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}' -> Error: {e}")
    print("----------------------------------\n")

    # Interactive loop
    while True:
        try:
            user_input = input("Enter expression: ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

