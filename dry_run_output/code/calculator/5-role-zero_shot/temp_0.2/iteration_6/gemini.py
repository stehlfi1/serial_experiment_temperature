
"""
A high-quality, console-based arithmetic calculator adhering to ISO/IEC 25010.

This module provides a Calculator class that can parse and evaluate mathematical
expressions from a string, without using `eval()`.
"""

import re
from typing import List, Union

class Calculator:
    """
    A robust calculator that evaluates arithmetic expressions from a string.

    This class implements a parser and evaluator for expressions containing
    integers, floating-point numbers, addition, subtraction, multiplication,
    division, and parentheses. It follows standard operator precedence.

    The evaluation process is based on Dijkstra's Shunting-yard algorithm to
    convert the infix expression to Reverse Polish Notation (RPN), which is
    then evaluated. This approach is secure, efficient, and reliable.
    """

    # Define operator properties for clarity and maintainability
    _OPERATORS = {
        '+': {'precedence': 1, 'func': lambda a, b: a + b},
        '-': {'precedence': 1, 'func': lambda a, b: a - b},
        '*': {'precedence': 2, 'func': lambda a, b: a * b},
        '/': {'precedence': 2, 'func': lambda a, b: a / b}
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public method that orchestrates the tokenization,
        parsing (Shunting-yard), and evaluation of the expression.

        Args:
            expression: The arithmetic expression string to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, malformed expression).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError):
            # Re-raise specific errors to the caller
            raise
        except Exception as e:
            # Catch any other unexpected errors during processing
            raise ValueError(f"Invalid expression provided: {e}") from e

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts the input string into a list of tokens (numbers and operators).

        This method handles integers, floats, and all supported operators,
        including parentheses. It also correctly handles unary minus (negative
        numbers) at the beginning of an expression or after an opening parenthesis.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens, where numbers are floats and operators are strings.

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        # Regex to find numbers (int/float), operators, or parentheses
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression)
        
        # Check for any characters that were not tokenized
        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError("Expression contains invalid characters.")

        processed_tokens: List[Union[float, str]] = []
        
        for i, token in enumerate(tokens):
            if token.isdigit() or '.' in token:
                processed_tokens.append(float(token))
            elif token in self._OPERATORS or token in "()":
                # Handle unary minus: e.g., "-5" or "( -5 )"
                if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('):
                    # This is a negative number, not subtraction.
                    # The next token must be a number.
                    if i + 1 < len(tokens) and (tokens[i+1].isdigit() or '.' in tokens[i+1]):
                        # We will handle this in the next iteration by skipping this '-'
                        continue 
                    else:
                        raise ValueError("Invalid use of unary minus.")
                
                # If the previous token was a unary minus, combine them
                if i > 0 and tokens[i-1] == '-' and (i-1 == 0 or tokens[i-2] in self._OPERATORS or tokens[i-2] == '('):
                    processed_tokens.append(float(token) * -1)
                else:
                    processed_tokens.append(token)
            else:
                # This case should theoretically not be reached due to the regex check above,
                # but it's good practice for robustness.
                raise ValueError(f"Invalid token found: {token}")

        return processed_tokens

    def _to_rpn(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[Union[float, str]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
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
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates a token queue in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack: List[float] = []

        for token in rpn_queue:
            if isinstance(token, float):
                operand_stack.append(token)
            elif token in self._OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands for operator.")
                
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                
                if token == '/' and op2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                operation = self._OPERATORS[token]['func']
                result = operation(op1, op2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression: too many operands.")

        return operand_stack[0]


# --- Main execution block for demonstration and manual testing ---
if __name__ == "__main__":
    # This block demonstrates the usage of the Calculator class.
    # It makes the script executable for quick tests while also being a reusable module.
    
    calculator = Calculator()
    
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'quit' to exit.")
    
    # Example expressions for demonstration
    test_expressions = [
        "3 + 5 * (10 - 4)",
        "10 / 2 - 3",
        "2.5 * 4 + 1.5",
        "-5 + 10",
        "10 * ( -2 )",
        "10 / 3",
        "1 / 0",  # Expected: ZeroDivisionError
        "(3 + 2))", # Expected: ValueError (mismatched parentheses)
        "5 + * 3",  # Expected: ValueError (malformed)
        "3 + a",    # Expected: ValueError (invalid character)
    ]
    
    print("\n--- Running Pre-defined Test Cases ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}' -> Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}' -> Error: {e}")
    
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() == 'quit':
                break
            if not user_input:
                continue
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

