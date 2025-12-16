
import re
from typing import List, Dict, Union, Literal

class Calculator:
    """
    A console-based arithmetic calculator that safely evaluates mathematical
    expressions from a string.

    This class adheres to the ISO/IEC 25010 standard by providing a correct,
    efficient, secure, and maintainable implementation. It uses the Shunting-yard
    algorithm to handle operator precedence and parentheses without using the
    insecure `eval()` function.

    Attributes:
        _OPERATORS (Dict): A dictionary defining the supported operators, their
                           precedence, and their associativity.
    """

    # Operator properties: precedence and associativity.
    # Higher precedence value means it's evaluated first.
    _OPERATORS: Dict[str, Dict[str, Union[int, Literal['Left', 'Right']]]] = {
        '+': {'precedence': 1, 'assoc': 'Left'},
        '-': {'precedence': 1, 'assoc': 'Left'},
        '*': {'precedence': 2, 'assoc': 'Left'},
        '/': {'precedence': 2, 'assoc': 'Left'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the public interface for the calculator. It orchestrates the
        tokenization, parsing (infix to postfix), and evaluation steps.

        Args:
            expression: The mathematical expression string to evaluate.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is otherwise malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an infix expression string into a list of tokens.

        This method handles integers, floating-point numbers, and negative
        numbers, while correctly identifying operators and parentheses.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens. e.g., ['3', '+', '5.5', '*', '(', '-2', ')']

        Raises:
            ValueError: If an unrecognized character is found.
        """
        # Regex to find numbers (including floats/negatives), operators, or parentheses
        token_regex = re.compile(r'(\d+\.?\d*|[+\-*/()])')
        tokens = token_regex.findall(expression)

        # Post-process to handle unary minus. A minus is unary if it is the
        # first token or is preceded by an operator or an opening parenthesis.
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i - 1] in self._OPERATORS or tokens[i - 1] == '('):
                # This is a unary minus. Combine it with the next token.
                try:
                    next_token = tokens[i + 1]
                    # This is a special case to avoid a ValueError if the next token is not a number
                    if next_token in self._OPERATORS or next_token in '()':
                        raise ValueError("Invalid expression: Unary minus must be followed by a number.")
                    processed_tokens.append(f"-{next_token}")
                    # Mark the next token as consumed
                    tokens[i + 1] = ''
                except IndexError:
                    raise ValueError("Invalid expression: Expression cannot end with an operator.")
            elif token != '':
                processed_tokens.append(token)

        # Validate that the original expression was fully tokenized
        reconstructed_expr = "".join(processed_tokens)
        if reconstructed_expr.replace('.', '', 1).replace('-', '', 1) != expression.replace(" ", ""):
            raise ValueError(f"Invalid characters or format in expression: '{expression}'")
            
        return processed_tokens

    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to postfix (RPN) using Shunting-yard.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in postfix order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[str] = []
        operator_stack: List[str] = []

        for token in tokens:
            try:
                # If the token is a number, add it to the output queue.
                float(token)
                output_queue.append(token)
            except ValueError:
                # Token is not a number, so it must be an operator or parenthesis.
                if token in self._OPERATORS:
                    # Token is an operator.
                    op1 = token
                    while (operator_stack and operator_stack[-1] in self._OPERATORS and
                           (self._OPERATORS[operator_stack[-1]]['precedence'] > self._OPERATORS[op1]['precedence'] or
                            (self._OPERATORS[operator_stack[-1]]['precedence'] == self._OPERATORS[op1]['precedence'] and
                             self._OPERATORS[op1]['assoc'] == 'Left'))):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(op1)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    
                    if not operator_stack or operator_stack[-1] != '(':
                        raise ValueError("Mismatched parentheses in expression.")
                    operator_stack.pop() # Pop the '('
                else:
                    # This case should ideally not be reached if _tokenize is correct
                    raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators from the stack to the output queue.
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, postfix_tokens: List[str]) -> float:
        """
        Evaluates a postfix (RPN) expression.

        Args:
            postfix_tokens: A list of tokens in postfix order.

        Returns:
            The final result of the evaluation.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        eval_stack: List[float] = []

        for token in postfix_tokens:
            try:
                # If the token is a number, push it onto the stack.
                eval_stack.append(float(token))
            except ValueError:
                # Token is an operator.
                if len(eval_stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands for operator.")
                
                op2 = eval_stack.pop()
                op1 = eval_stack.pop()

                if token == '+':
                    eval_stack.append(op1 + op2)
                elif token == '-':
                    eval_stack.append(op1 - op2)
                elif token == '*':
                    eval_stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    eval_stack.append(op1 / op2)

        if len(eval_stack) != 1:
            raise ValueError("Invalid expression format.")

        return eval_stack[0]


# --- Demonstration ---
if __name__ == "__main__":
    calculator = Calculator()

    print("--- High-Quality Python Calculator ---")
    print("Enter 'exit' to quit.")

    # Example test cases to demonstrate correctness
    test_expressions = [
        "3 + 4 * 2 / ( 1 - 5 )",
        "10 + -2 * 5",
        "3.14 * (2 + 2)",
        "(1 + 2) * 3",
        "100 / ( 5 * 2 )",
        "5 * -2",
        "-5 + 2",
        "10 / 0",  # Error case: Division by zero
        "3 + * 4", # Error case: Malformed expression
        "(3 + 4",  # Error case: Mismatched parentheses
        "3 + a",   # Error case: Invalid character
    ]

    print("\n--- Running Automated Test Cases ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}' -> Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}' -> Error: {e}")

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

