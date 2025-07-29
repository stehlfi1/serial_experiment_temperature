
import re
from typing import List, Union

class Calculator:
    """
    A high-quality, safe, and maintainable calculator for evaluating arithmetic
    expressions from a string.

    This class implements a classic two-stage evaluation process:
    1.  The Shunting-yard algorithm to convert the infix expression to a
        postfix (Reverse Polish Notation) queue.
    2.  Evaluation of the RPN queue to compute the final result.

    This approach correctly handles operator precedence and parentheses without
    using the unsafe `eval()` function.
    """

    # Define operator precedence and associativity
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'left'},
        '-': {'precedence': 1, 'assoc': 'left'},
        '*': {'precedence': 2, 'assoc': 'left'},
        '/': {'precedence': 2, 'assoc': 'left'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: A string containing the arithmetic expression.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., invalid characters,
                        unbalanced parentheses, or invalid operator sequence).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        tokens = self._tokenize(expression)
        rpn_queue = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn_queue)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).

        This tokenizer correctly handles floating-point numbers and negative values.

        Args:
            expression: The raw expression string.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")

        # This regex captures floating point numbers, integers (including negatives),
        # and operators/parentheses.
        token_regex = r"(-?\d+\.\d+|-?\d+|[+\-*/()])"
        tokens = re.findall(token_regex, expression.replace(" ", ""))

        # Validate for any characters that were not tokenized
        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters.")

        # Handle unary minus ambiguity. A minus is unary if it's the first token
        # or if it follows an operator or an opening parenthesis.
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-':
                is_unary = (i == 0) or (tokens[i-1] in self._OPERATORS or tokens[i-1] == '(')
                if is_unary:
                    # Combine with the next number to form a negative number token
                    try:
                        next_token = tokens[i+1]
                        processed_tokens.append(f"-{next_token}")
                        # Mark the next token as consumed
                        tokens[i+1] = ''
                    except IndexError:
                        raise ValueError("Invalid expression: trailing '-' operator")
                else:
                    processed_tokens.append(token)
            elif token != '': # Skip tokens consumed by unary minus logic
                processed_tokens.append(token)

        return processed_tokens


    def _shunting_yard(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Implements the Shunting-yard algorithm to convert infix tokens to postfix (RPN).

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list representing the expression in RPN.

        Raises:
            ValueError: For mismatched parentheses or invalid expression structure.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(float(token))
            elif token in self._OPERATORS:
                # While there's an operator on the stack with higher or equal precedence
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       self._OPERATORS[operator_stack[-1]]['precedence'] >= self._OPERATORS[token]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Discard the '('
            else:
                # This case should ideally not be reached due to tokenizer validation
                raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators from the stack to the queue
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of numbers and operators in RPN order.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the RPN queue is malformed.
            ZeroDivisionError: For division by zero.
        """
        stack = []
        for token in rpn_queue:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator.")
                
                op2 = stack.pop()
                op1 = stack.pop()

                if token == '+':
                    stack.append(op1 + op2)
                elif token == '-':
                    stack.append(op1 - op2)
                elif token == '*':
                    stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    stack.append(op1 / op2)

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")

        return stack[0]

    def _is_number(self, token: str) -> bool:
        """Utility to check if a token can be converted to a float."""
        try:
            float(token)
            return True
        except (ValueError, TypeError):
            return False


if __name__ == '__main__':
    """
    An interactive command-line interface to demonstrate the Calculator class.
    """
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'quit' to exit.")
    
    calculator = Calculator()

    while True:
        try:
            expression = input(">> ")
            if expression.lower() == 'quit':
                print("Exiting calculator.")
                break
            
            if not expression:
                continue

            result = calculator.calculate(expression)
            # Format to avoid floating point inaccuracies for simple integers
            if result == int(result):
                print(f"= {int(result)}")
            else:
                print(f"= {result:.4f}")

        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

