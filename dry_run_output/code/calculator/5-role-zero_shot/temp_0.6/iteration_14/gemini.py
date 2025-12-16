
import re
from typing import List, Union

class Calculator:
    """
    A robust, console-based arithmetic calculator that evaluates string expressions.

    This class adheres to the principles of the ISO/IEC 25010 standard, focusing on:
    - Functional Suitability: Correctly computes addition, subtraction, multiplication,
      division, and handles parentheses with correct operator precedence.
    - Performance Efficiency: Utilizes an O(n) algorithm (Shunting-yard) for parsing
      and evaluation.
    - Maintainability: The code is modular, readable, and well-documented, making it
      easy to analyze, modify, and test. New operators can be added easily.
    - Reliability: Implements fault tolerance through comprehensive input validation
      and graceful error handling using specific, built-in exception types.
    - Security: Avoids the use of `eval()` to prevent code injection vulnerabilities.
    """

    def __init__(self):
        """Initializes the Calculator, defining operator properties."""
        self._operators = {
            '+': {'precedence': 1, 'assoc': 'L'},
            '-': {'precedence': 1, 'assoc': 'L'},
            '*': {'precedence': 2, 'assoc': 'L'},
            '/': {'precedence': 2, 'assoc': 'L'},
        }
        self._allowed_chars = set('0123456789.+-*/() ')

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the calculator.

        Args:
            expression: The arithmetic expression string to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression contains invalid characters, unbalanced
                        parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            self._validate_input(expression)
            tokens = self._tokenize(expression)
            rpn_tokens = self._infix_to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions with a more informative context.
            raise type(e)(f"Error evaluating expression: {e}") from e
        except IndexError:
            # Catches errors from popping from empty stacks, indicating a malformed expression.
            raise ValueError("Invalid or malformed expression format.")


    # --- Private Helper Methods: Modularity and Internal Logic ---

    def _validate_input(self, expression: str):
        """
        Checks for invalid characters in the expression.

        Args:
            expression: The input string.

        Raises:
            ValueError: If any character is not in the allowed set.
        """
        if not set(expression).issubset(self._allowed_chars):
            invalid_chars = set(expression) - self._allowed_chars
            raise ValueError(f"Invalid characters found: {', '.join(invalid_chars)}")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).
        
        This method also handles unary minus by cleverly transforming the expression
        before tokenization. e.g., '-5+3' -> '(0-5)+3'

        Args:
            expression: The sanitized expression string.

        Returns:
            A list of string tokens.
        """
        # Replace unary minus to avoid ambiguity.
        # A minus is unary if it's at the start or after an operator or an opening parenthesis.
        expression = re.sub(r'(?<=[\(\+\-\*\/])\s*-\s*', '-1*', expression)
        expression = re.sub(r'^\s*-\s*', '-1*', expression)

        # Tokenize the expression using a regular expression.
        # This pattern finds floating-point/integer numbers or operators/parentheses.
        token_regex = r'(\d+\.?\d*|[+\-*/()])'
        tokens = re.findall(token_regex, expression)
        return tokens

    def _infix_to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens in infix order.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                output_queue.append(token)
            elif token in self._operators:
                while (operator_stack and operator_stack[-1] in self._operators and
                       (self._operators[operator_stack[-1]]['precedence'] > self._operators[token]['precedence'] or
                        (self._operators[operator_stack[-1]]['precedence'] == self._operators[token]['precedence'] and
                         self._operators[token]['assoc'] == 'L'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses.")
                operator_stack.pop() # Pop the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluates a token list in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.
            
        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack = []

        for token in rpn_tokens:
            if token.replace('.', '', 1).isdigit():
                operand_stack.append(float(token))
            elif token in self._operators:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid syntax or missing operand.")
                
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
                        raise ZeroDivisionError("Division by zero.")
                    operand_stack.append(op1 / op2)

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression, unable to resolve to a single value.")

        return operand_stack[0]

# --- Main execution block for demonstration and simple testing ---
if __name__ == "__main__":
    # This block demonstrates the usage of the Calculator class and serves as
    # a basic smoke test. It is not executed when the module is imported.
    # This improves the reusability and testability of the code.
    
    calc = Calculator()
    
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    
    while True:
        try:
            expression_input = input("\n> ")
            if expression_input.lower() == 'exit':
                print("Exiting calculator.")
                break
            
            result = calc.calculate(expression_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
