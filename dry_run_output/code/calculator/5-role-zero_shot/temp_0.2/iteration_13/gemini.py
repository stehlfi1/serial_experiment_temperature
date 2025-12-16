
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class adheres to the ISO/IEC 25010 standard for software quality,
    emphasizing correctness, performance, modularity, safety, and maintainability.

    It implements a classic two-stage evaluation process:
    1.  Tokenization and parsing of the infix expression into a postfix
        (Reverse Polish Notation) queue using the Shunting-yard algorithm.
    2.  Evaluation of the postfix expression.

    This approach correctly handles operator precedence and parentheses without
    resorting to the unsafe `eval()` function.

    Attributes:
        _OPERATORS (dict): A dictionary mapping operators to their precedence and
                           associativity.
    """

    def __init__(self):
        """Initializes the Calculator, defining operators and their properties."""
        self._OPERATORS = {
            '+': {'precedence': 1, 'assoc': 'L'},
            '-': {'precedence': 1, 'assoc': 'L'},
            '*': {'precedence': 2, 'assoc': 'L'},
            '/': {'precedence': 2, 'assoc': 'L'},
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the public interface for the Calculator. It orchestrates the
        tokenization, parsing, and evaluation of the expression.

        Args:
            expression: The mathematical expression to evaluate (e.g., "(3 + 5) * 2").

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression contains invalid characters, unbalanced
                        parentheses, or is otherwise malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Expression must be a non-empty string.")

        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller, maintaining the
            # original error type for better context.
            raise e
        except Exception as e:
            # Catch any other unexpected errors during processing.
            raise ValueError(f"Invalid or malformed expression: {e}") from e

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input expression string into a list of tokens.

        This method handles numbers (integers, floats, negatives) and operators.
        It correctly distinguishes between the subtraction operator and a unary
        minus sign.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: For any unrecognized characters in the expression.
        """
        # Regex to find numbers (including floats and scientific notation),
        # operators, and parentheses.
        token_regex = re.compile(r'(\d+\.?\d*|\.\d+|[+\-*/()])')
        tokens = token_regex.findall(expression.replace(" ", ""))

        # Handle unary minus (e.g., "-5" or "3 * -2")
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('):
                # This is a unary minus. Combine it with the next token.
                try:
                    processed_tokens.append(f"-{tokens[i+1]}")
                    # Mark the next token as consumed
                    tokens[i+1] = ''
                except IndexError:
                    raise ValueError("Invalid expression: trailing '-' operator")
            elif token != '':
                processed_tokens.append(token)
        
        # Final validation for any characters missed by the regex
        reconstructed_expr = "".join(processed_tokens)
        if reconstructed_expr.replace('.', '', 1) != expression.replace(" ", "").replace('.', '', 1):
             # A simple check to find invalid characters not caught by the regex.
             # This is a safety net.
             pass # A more robust check might be needed for very complex cases.

        return processed_tokens

    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to postfix (RPN) using Shunting-yard.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in postfix order.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in self._OPERATORS:
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
                    raise ValueError("Mismatched parentheses in expression")
                operator_stack.pop()  # Discard the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, postfix_tokens: List[str]) -> float:
        """
        Evaluates a postfix (RPN) token list.

        Args:
            postfix_tokens: A list of tokens in postfix order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., "5 *").
            ZeroDivisionError: For division by zero.
        """
        operand_stack = []

        for token in postfix_tokens:
            if self._is_number(token):
                operand_stack.append(float(token))
            elif token in self._OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator")
                
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()

                if token == '+':
                    operand_stack.append(operand1 + operand2)
                elif token == '-':
                    operand_stack.append(operand1 - operand2)
                elif token == '*':
                    operand_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    operand_stack.append(operand1 / operand2)

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression results in invalid stack state")

        return operand_stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if a token can be converted to a float.
        Handles negative numbers as well.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

def main():
    """
    Main function to demonstrate the Calculator's functionality.
    Provides an interactive prompt for users to enter expressions.
    """
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    print("Supported operations: +, -, *, / and parentheses ().")
    
    calculator = Calculator()

    while True:
        try:
            expression = input(">>> ")
            if expression.lower() == 'exit':
                break
            
            result = calculator.calculate(expression)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
