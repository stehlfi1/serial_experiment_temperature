
"""
A module for evaluating arithmetic expressions from strings.

This module provides a Calculator class that can parse and evaluate mathematical
expressions, supporting addition, subtraction, multiplication, division, and
parentheses. It adheres to standard operator precedence.

This implementation is designed with the ISO/IEC 25010 standard in mind,
focusing on:
- Functional Suitability: Correctly evaluates complex expressions.
- Performance Efficiency: Uses an efficient O(n) algorithm (Shunting-yard variant).
- Reliability & Security: Gracefully handles errors and invalid input without
  using the insecure `eval()` function.
- Maintainability: Code is modular, documented, and easy to understand.
- Testability: The core logic is encapsulated in a class, making it
  straightforward to unit test.
"""

import operator
from typing import List, Union


class Calculator:
    """
    A robust, safe, and efficient arithmetic expression evaluator.

    This class evaluates standard infix arithmetic expressions, including support
    for parentheses and operator precedence. It does not use `eval()` and is
    therefore safe from code injection vulnerabilities.

    Attributes:
        _operators (dict): A mapping of operator symbols to their corresponding
                           functions and precedence levels.
    """

    def __init__(self):
        """Initializes the Calculator with operator definitions."""
        self._operators = {
            '+': {'func': operator.add, 'prec': 1},
            '-': {'func': operator.sub, 'prec': 1},
            '*': {'func': operator.mul, 'prec': 2},
            '/': {'func': operator.truediv, 'prec': 2},
        }

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an infix expression string into a list of tokens.

        This method handles multi-digit numbers, floating-point numbers, and
        distinguishes between binary subtraction and unary negation.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of string tokens (numbers, operators, parentheses).

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        tokens: List[str] = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            # Handle operators and parentheses
            if char in self._operators or char in '()':
                # Distinguish unary minus from binary subtraction
                if char == '-':
                    is_unary = (
                        not tokens or
                        tokens[-1] in self._operators or
                        tokens[-1] == '('
                    )
                    if is_unary:
                        # Start of a negative number, not a subtraction operator
                        j = i + 1
                        # Find the end of the number
                        while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                            j += 1
                        
                        num_str = expression[i:j]
                        if num_str == '-':
                            raise ValueError("Invalid expression: isolated '-' operator")
                        tokens.append(num_str)
                        i = j
                        continue
                
                tokens.append(char)
                i += 1
                continue

            # Handle numbers (integers and floats)
            if char.isdigit() or char == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue

            raise ValueError(f"Invalid character in expression: '{char}' at position {i}")
        
        return tokens

    def _apply_operation(self, ops: List[str], values: List[float]) -> None:
        """
        Applies a single operation to the values stack.

        Pops an operator from the 'ops' stack, pops the required number of
        operands from the 'values' stack, performs the operation, and pushes
        the result back onto the 'values' stack.

        Args:
            ops: The stack of operators.
            values: The stack of numerical values.

        Raises:
            ValueError: If there are insufficient values on the stack for an operation.
            ZeroDivisionError: If a division by zero is attempted.
        """
        if not ops or not values:
            raise ValueError("Syntax error: trying to apply operation on empty stacks")
        
        op_symbol = ops.pop()
        op_info = self._operators[op_symbol]

        if len(values) < 2:
            raise ValueError(f"Syntax error: insufficient values for operator '{op_symbol}'")
        
        right_operand = values.pop()
        left_operand = values.pop()

        if op_symbol == '/' and right_operand == 0:
            raise ZeroDivisionError("Error: Division by zero is not allowed.")

        result = op_info['func'](left_operand, right_operand)
        values.append(result)

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This method implements a variant of the Shunting-yard algorithm to correctly
        evaluate an expression with respect for operator precedence and parentheses.

        Args:
            expression: The arithmetic expression to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: For syntax errors like mismatched parentheses, invalid
                        characters, or malformed expressions.
            ZeroDivisionError: For division by zero.
        """
        tokens = self._tokenize(expression)
        values: List[float] = []
        ops: List[str] = []

        for token in tokens:
            try:
                # If token is a number, push it to the values stack
                values.append(float(token))
            except ValueError:
                # Token is not a number, so it must be an operator or parenthesis
                if token == '(':
                    ops.append(token)
                elif token == ')':
                    # Evaluate everything inside the parentheses
                    while ops and ops[-1] != '(':
                        self._apply_operation(ops, values)
                    if not ops or ops[-1] != '(':
                        raise ValueError("Syntax error: Mismatched parentheses")
                    ops.pop()  # Pop the opening parenthesis '('
                elif token in self._operators:
                    # Token is an operator, handle precedence
                    current_op_prec = self._operators[token]['prec']
                    while (ops and ops[-1] in self._operators and
                           self._operators[ops[-1]]['prec'] >= current_op_prec):
                        self._apply_operation(ops, values)
                    ops.append(token)
                else:
                    # This case should be caught by _tokenize, but serves as a safeguard
                    raise ValueError(f"Internal error: Unhandled token '{token}'")

        # Apply any remaining operations
        while ops:
            if ops[-1] == '(':
                raise ValueError("Syntax error: Mismatched parentheses")
            self._apply_operation(ops, values)

        if len(values) != 1 or ops:
            raise ValueError("Syntax error: Malformed expression")

        return values[0]


def main():
    """
    Main function to run the interactive calculator console.
    """
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'quit' to exit.")
    
    calculator = Calculator()

    while True:
        try:
            expression = input(">>> ")
            if expression.lower() == 'quit':
                print("Exiting calculator. Goodbye!")
                break
            
            if not expression.strip():
                continue

            result = calculator.calculate(expression)
            # Format to avoid floating point inaccuracies for simple integers
            if result == int(result):
                print(f"= {int(result)}")
            else:
                print(f"= {result:.10f}".rstrip('0').rstrip('.'))

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
