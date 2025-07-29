
import operator
from typing import List, Dict, Union, Callable

# Define a type alias for more readable type hints
Token = Union[float, str]
OperatorDetails = Dict[str, Union[int, Callable]]

class Calculator:
    """
    A high-quality, maintainable calculator that evaluates arithmetic expressions.

    This class adheres to the principles of ISO/IEC 25010, focusing on
    functional suitability, performance, reliability, security, and maintainability.

    It uses the Shunting-yard algorithm to correctly handle operator precedence
    and parentheses without using the insecure `eval()` function.
    """

    # Operator properties: precedence and the actual function.
    # A special token '~' is used for unary minus to distinguish it from
    # binary subtraction. It has the highest precedence.
    OPERATORS: Dict[str, OperatorDetails] = {
        '+': {'precedence': 1, 'func': operator.add},
        '-': {'precedence': 1, 'func': operator.sub},
        '*': {'precedence': 2, 'func': operator.mul},
        '/': {'precedence': 2, 'func': operator.truediv},
        '~': {'precedence': 3, 'func': operator.neg},  # Unary minus
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression string and returns the result.

        Args:
            expression: The arithmetic expression string to evaluate.
                        It can contain numbers, operators (+, -, *, /),
                        and parentheses.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid
                        characters, or has mismatched parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller, ensuring a
            # clean and predictable error interface.
            raise e
        except Exception:
            # Catch any other unexpected errors during processing.
            raise ValueError("Invalid or malformed expression")

    def _tokenize(self, expression: str) -> List[Token]:
        """
        Converts the input string into a list of numbers and operators.

        This tokenizer correctly handles floating-point numbers, negative
        numbers, and distinguishes between binary subtraction and unary negation.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (floats and strings).

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        tokens: List[Token] = []
        num_buffer = ""
        last_token_was_operator_or_paren = True

        for char in expression:
            if char.isspace():
                continue

            if char.isdigit() or char == '.':
                num_buffer += char
                last_token_was_operator_or_paren = False
            else:
                if num_buffer:
                    tokens.append(float(num_buffer))
                    num_buffer = ""

                if char in self.OPERATORS:
                    # Distinguish between unary minus and binary subtraction.
                    # A minus is unary if it's at the start of the expression
                    # or follows another operator or an opening parenthesis.
                    if char == '-' and last_token_was_operator_or_paren:
                        tokens.append('~')  # Use special token for unary minus
                    else:
                        tokens.append(char)
                    last_token_was_operator_or_paren = True
                elif char in '()':
                    tokens.append(char)
                    last_token_was_operator_or_paren = (char == '(')
                else:
                    raise ValueError(f"Invalid character in expression: '{char}'")

        if num_buffer:
            tokens.append(float(num_buffer))

        return tokens

    def _to_rpn(self, tokens: List[Token]) -> List[Token]:
        """
        Converts a token list from infix to Reverse Polish Notation (RPN).

        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If there are mismatched parentheses.
        """
        output_queue: List[Token] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                op1 = token
                while (operator_stack and operator_stack[-1] != '(' and
                       self.OPERATORS[operator_stack[-1]]['precedence'] >= self.OPERATORS[op1]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op1)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack.pop() != '(':
                    raise ValueError("Mismatched parentheses in expression")

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Token]) -> float:
        """
        Evaluates a token list in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        stack: List[float] = []

        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                op_details = self.OPERATORS[token]
                # Unary operators take one operand, binary operators take two.
                num_operands = 1 if token == '~' else 2

                if len(stack) < num_operands:
                    raise ValueError("Malformed expression: insufficient operands for operator")

                operands = [stack.pop() for _ in range(num_operands)]
                
                # For binary operators, operands are popped in reverse order (b, then a for a op b)
                if num_operands == 2:
                    b, a = operands
                    if token == '/' and b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    result = op_details['func'](a, b)
                else: # Unary operator
                    result = op_details['func'](operands[0])
                
                stack.append(result)

        if len(stack) != 1:
            raise ValueError("Malformed expression: too many operands")

        return stack[0]

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    # This block demonstrates the usage of the Calculator class and serves
    # as a basic interactive test harness.
    calc = Calculator()
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'exit' to quit.")

    # Example test cases to showcase functionality and correctness
    test_expressions = [
        "3 + 5 * (10 - 4)",
        "10 / 2 - 3",
        "-5 * -2",
        "10.5 + 2.5 * (4 / 2)",
        "1 + (2 * (3 - (4 / 5)))",
        "-(3 + 2)",
        "100 / (10 * (2 - 2))", # Should raise ZeroDivisionError
        "5 * (3 + 2",          # Should raise ValueError (mismatched parentheses)
        "5 & 4",               # Should raise ValueError (invalid character)
        "5 *",                 # Should raise ValueError (malformed expression)
    ]

    print("\n--- Running Automated Test Cases ---")
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"Expression: '{expr}' -> Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}' -> Error: {e}")
    print("--- End of Automated Test Cases ---\n")

    # Interactive loop
    while True:
        try:
            user_input = input("Calculate: ")
            if user_input.lower() == 'exit':
                break
            if not user_input:
                continue
            
            output = calc.calculate(user_input)
            print(f"Result: {output}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

