
"""
A high-quality, console-based arithmetic calculator in Python.

This module provides a Calculator class that evaluates arithmetic expressions
from a string input, adhering to the principles of the ISO/IEC 25010
standard for software quality.
"""

import re
from typing import List, Union

class Calculator:
    """
    A robust calculator that evaluates string-based arithmetic expressions.

    This class implements a parser and evaluator for expressions containing
    integers, floating-point numbers, addition, subtraction, multiplication,
    division, and parentheses. It follows standard operator precedence.

    The implementation uses the Shunting-yard algorithm to convert the infix
    expression to Reverse Polish Notation (RPN), which is then evaluated.
    This approach avoids the use of Python's `eval()` function, enhancing
    security and control.
    """

    # Define operator properties for easy extension and maintenance
    _OPERATORS = {
        '+': {'precedence': 1, 'func': lambda a, b: a + b},
        '-': {'precedence': 1, 'func': lambda a, b: a - b},
        '*': {'precedence': 2, 'func': lambda a, b: a * b},
        '/': {'precedence': 2, 'func': lambda a, b: a / b},
    }
    _PARENTHESES = {'(', ')'}

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the Calculator.

        Args:
            expression: A string containing the arithmetic expression.
                        e.g., "3 + 5 * (10 - 4)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., mismatched
                        parentheses, invalid characters, malformed expression).
            ZeroDivisionError: If the expression involves division by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._shunting_yard(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raising the exception to allow for higher-level handling
            # while also providing immediate feedback if run directly.
            print(f"Error evaluating expression: {e}")
            raise

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens.

        This method handles numbers (integers, floats, negatives) and operators.
        It correctly distinguishes between a unary minus (e.g., "-5") and a
        binary subtraction operator (e.g., "10 - 5").

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: If an unrecognized character is found.
        """
        # Remove all whitespace for easier parsing
        expression = expression.replace(" ", "")
        if not expression:
            raise ValueError("Expression cannot be empty.")

        # Regex to find numbers (including floats) or operators/parentheses
        token_regex = re.compile(r"(\d+\.?\d*|[+\-*/()])")
        tokens = token_regex.findall(expression)

        # Post-process to handle unary minus
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-':
                # A minus is unary if it's the first token, or if the
                # preceding token is an operator or an opening parenthesis.
                is_unary = (i == 0) or (tokens[i - 1] in self._OPERATORS) or (tokens[i - 1] == '(')
                if is_unary:
                    # Combine with the next number
                    if i + 1 < len(tokens) and tokens[i+1].replace('.', '', 1).isdigit():
                        # This token will be handled by the next iteration
                        continue 
                    else:
                        raise ValueError("Invalid use of unary minus.")
                else: # Binary minus
                    processed_tokens.append(token)
            elif token.replace('.', '', 1).isdigit() and i > 0 and tokens[i-1] == '-' and ((i-1 == 0) or (tokens[i-2] in self._OPERATORS) or (tokens[i-2] == '(')):
                # This is a number preceded by a unary minus
                processed_tokens.append('-' + token)
            else:
                processed_tokens.append(token)

        # Final validation for unrecognized characters
        reconstructed_expr = "".join(t if t in self._PARENTHESES or t in self._OPERATORS else t.replace('-', '') for t in processed_tokens)
        if reconstructed_expr != expression.replace('-', ''):
             raise ValueError("Expression contains invalid characters.")

        return processed_tokens

    def _shunting_yard(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to postfix (RPN) notation.

        This method implements Dijkstra's Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list representing the expression in RPN.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                output_queue.append(float(token))
            elif token in self._OPERATORS:
                while (operator_stack and
                       operator_stack[-1] in self._OPERATORS and
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

        while operator_stack:
            operator = operator_stack.pop()
            if operator == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(operator)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of numbers and operators in RPN.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: For division by zero.
        """
        eval_stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                eval_stack.append(token)
            elif token in self._OPERATORS:
                if len(eval_stack) < 2:
                    raise ValueError("Invalid expression format (operator/operand mismatch).")
                
                operand2 = eval_stack.pop()
                operand1 = eval_stack.pop()

                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                operation = self._OPERATORS[token]['func']
                result = operation(operand1, operand2)
                eval_stack.append(result)

        if len(eval_stack) != 1:
            raise ValueError("Invalid expression format.")

        return eval_stack[0]

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    print("Welcome to the High-Quality Python Calculator!")
    print("Enter 'exit' to quit.")
    
    calculator = Calculator()
    
    while True:
        try:
            expression = input("Enter expression: ")
            if expression.lower() == 'exit':
                break
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError, IndexError) as e:
            # The calculate method already prints a message,
            # but we catch here to prevent the program from crashing.
            print(f"Please try again with a valid expression.\n")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

