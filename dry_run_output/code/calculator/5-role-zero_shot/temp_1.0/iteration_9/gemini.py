
import re
from typing import List, Union

class Calculator:
    """
    A high-quality, console-based calculator that evaluates infix arithmetic expressions.

    This calculator adheres to ISO/IEC 25010 principles by being functionally
    correct, efficient, maintainable, reliable, and secure. It uses the
    Shunting-yard algorithm to safely evaluate expressions without using `eval()`.

    Supported operations:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (*)
    - Division (/)
    - Parentheses for grouping ()

    Handles integers, floating-point numbers, and negative values.
    """

    # Class constants for clarity and maintainability
    _OPERATORS = {'+', '-', '*', '/'}
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Performs lexical analysis, converting the expression string into tokens.

        This method handles numbers (including floats and negatives), operators,
        and parentheses. It also disambiguates the unary minus from the binary
        subtraction operator.

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens (floats for numbers, strings for operators/parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to find numbers, operators, or parentheses
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression)
        
        # Post-process to handle invalid characters and unary minus
        processed_tokens = []
        last_token = None
        
        # Validate that the original string only contained valid tokens and whitespace
        if "".join(tokens) != re.sub(r'\s+', '', expression):
            raise ValueError("Expression contains invalid characters")

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                # Handle unary minus: check if the preceding token is an operator or '('
                if (last_token == '-') and \
                   (not processed_tokens or processed_tokens[-2] in self._OPERATORS or processed_tokens[-2] == '('):
                    # It's a negative number, combine it with the previous '-' token
                    processed_tokens[-1] = -float(token)
                else:
                    processed_tokens.append(float(token))
            elif token in self._OPERATORS or token in '()':
                processed_tokens.append(token)
            
            last_token = token
            
        return processed_tokens

    def _to_postfix(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a list of infix tokens to postfix (Reverse Polish Notation).

        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in postfix order.

        Raises:
            ValueError: For mismatched parentheses.
        """
        postfix_queue = []
        ops_stack = []

        for token in tokens:
            if isinstance(token, float):
                postfix_queue.append(token)
            elif token in self._OPERATORS:
                while (ops_stack and ops_stack[-1] in self._OPERATORS and
                       self._PRECEDENCE.get(ops_stack[-1], 0) >= self._PRECEDENCE.get(token, 0)):
                    postfix_queue.append(ops_stack.pop())
                ops_stack.append(token)
            elif token == '(':
                ops_stack.append(token)
            elif token == ')':
                while ops_stack and ops_stack[-1] != '(':
                    postfix_queue.append(ops_stack.pop())
                if not ops_stack or ops_stack.pop() != '(':
                    raise ValueError("Mismatched parentheses in expression")
            
        while ops_stack:
            operator = ops_stack.pop()
            if operator == '(':
                raise ValueError("Mismatched parentheses in expression")
            postfix_queue.append(operator)

        return postfix_queue

    def _evaluate_postfix(self, postfix_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix_tokens: A list of tokens in postfix order.

        Returns:
            The final result of the calculation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero is attempted.
        """
        eval_stack = []

        for token in postfix_tokens:
            if isinstance(token, float):
                eval_stack.append(token)
            elif token in self._OPERATORS:
                if len(eval_stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands for operator")
                
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
                        raise ZeroDivisionError("Division by zero is not allowed")
                    eval_stack.append(op1 / op2)

        if len(eval_stack) != 1:
            raise ValueError("Malformed expression: operands remain after evaluation")

        return eval_stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the Calculator class. It orchestrates
        the tokenization, parsing, and evaluation of the expression.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the expression as a float.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input must be a non-empty string.")
            
        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller, maintaining the
            # original error type and message for clarity.
            raise e
        except Exception:
            # Catch any other unexpected errors during processing
            raise ValueError("Invalid or malformed expression")


if __name__ == "__main__":
    # This block serves as a simple command-line interface and demonstration.
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'quit' to exit.")
    
    calculator = Calculator()

    while True:
        try:
            user_input = input(">> ")
            if user_input.lower() == 'quit':
                print("Exiting calculator. Goodbye!")
                break
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting calculator. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

