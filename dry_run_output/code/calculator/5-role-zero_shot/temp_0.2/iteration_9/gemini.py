
# -*- coding: utf-8 -*-
"""
A console-based arithmetic calculator that safely evaluates mathematical expressions.

This module provides a Calculator class that adheres to the ISO/IEC 25010 standard
for software quality, focusing on functional suitability, reliability, performance,
and maintainability.
"""

import operator
from typing import List, Union, Dict, Callable

# Type alias for better readability
Token = Union[float, str]
OperatorDetails = Dict[str, Union[int, Callable[[float, float], float]]]


class Calculator:
    """
    A safe, OOP-based calculator for evaluating arithmetic expressions.

    This class implements a calculator that can parse and evaluate strings
    containing mathematical expressions. It supports addition, subtraction,
    multiplication, division, and parentheses.

    The evaluation is performed using the Shunting-yard algorithm to convert
    the infix expression to postfix (RPN), which is then evaluated. This
    approach is safe and avoids the use of `eval()`.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Correctly computes expressions with specified operators.
    - Performance Efficiency: Uses an O(n) algorithm for parsing and evaluation.
    - Reliability: Gracefully handles invalid inputs and runtime errors like
      division by zero through custom exceptions.
    - Security: Avoids `eval()`, preventing code injection vulnerabilities.
    - Maintainability: The code is modular (tokenize, parse, evaluate), with
      clear separation of concerns, making it easy to extend or modify.
    - Testability: Private methods can be unit-tested individually.
    - Readability: Adheres to PEP 8, with clear variable names, type hints,
      and comprehensive documentation.
    """

    # --- Class constants for maintainability ---
    OPERATORS: Dict[str, OperatorDetails] = {
        "+": {"precedence": 1, "func": operator.add},
        "-": {"precedence": 1, "func": operator.sub},
        "*": {"precedence": 2, "func": operator.mul},
        "/": {"precedence": 2, "func": operator.truediv},
    }
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface of the calculator.

        Args:
            expression: A string containing the mathematical expression.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, malformed expression).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")
        
        tokens = self._tokenize(expression)
        rpn_queue = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn_queue)
        return result

    def _tokenize(self, expression: str) -> List[Token]:
        """
        Converts an expression string into a list of tokens (numbers and operators).

        This tokenizer handles integers, floats, and unary minus operators.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens. e.g., ['3', '+', '5.5'] -> [3.0, '+', 5.5]

        Raises:
            ValueError: For any unrecognized characters in the expression.
        """
        tokens: List[Token] = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or (char == '.'):
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                continue

            if char in self.OPERATORS or char in (self.LEFT_PAREN, self.RIGHT_PAREN):
                # Handle unary minus: a '-' is unary if it's the first token
                # or if it follows an operator or an opening parenthesis.
                if char == '-' and (not tokens or tokens[-1] in self.OPERATORS or tokens[-1] == self.LEFT_PAREN):
                    tokens.append(0.0) # Represent "-x" as "0 - x"
                tokens.append(char)
                i += 1
                continue
            
            raise ValueError(f"Invalid character in expression: '{char}'")

        return tokens

    def _to_rpn(self, tokens: List[Token]) -> List[Token]:
        """
        Converts a token list from infix to postfix notation (RPN) using Shunting-yard.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue: List[Token] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                op1 = token
                while (operator_stack and operator_stack[-1] in self.OPERATORS and
                       self.OPERATORS[operator_stack[-1]]["precedence"] >= self.OPERATORS[op1]["precedence"]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op1)
            elif token == self.LEFT_PAREN:
                operator_stack.append(token)
            elif token == self.RIGHT_PAREN:
                while operator_stack and operator_stack[-1] != self.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != self.LEFT_PAREN:
                    raise ValueError("Mismatched parentheses: Unbalanced ')'")
                operator_stack.pop()  # Discard the left parenthesis

        while operator_stack:
            op = operator_stack.pop()
            if op == self.LEFT_PAREN:
                raise ValueError("Mismatched parentheses: Unbalanced '('")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Token]) -> float:
        """
        Evaluates a token queue in RPN.

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the expression is malformed (e.g., "5 *").
            ZeroDivisionError: For division by zero.
        """
        operand_stack: List[float] = []

        for token in rpn_queue:
            if isinstance(token, float):
                operand_stack.append(token)
            elif token in self.OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands for operator.")
                
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                
                operation = self.OPERATORS[token]["func"]
                
                if token == '/' and op2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                result = operation(op1, op2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: Too many operands.")

        return operand_stack[0]


def main():
    """
    Main function to demonstrate the Calculator's functionality.
    Provides a simple command-line interface for testing expressions.
    """
    print("--- High-Quality Python Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    
    calculator = Calculator()

    # --- Demonstration with predefined test cases ---
    print("\n--- Running Predefined Test Cases ---")
    test_expressions = [
        "5 + 3",
        "10 - 4 * 2",
        "(10 - 4) * 2",
        "2 * (3 + 4 * 5)",
        "7 / 2",
        "7 / (3 - 3)",  # Division by zero
        "10 * -5",
        "-5 * -5",
        "1.5 * (2.5 + 3.5)",
        "(5 + 3) * 2 - (4 / 2)",
        "5 + (3 * 2",  # Unbalanced parentheses
        "5 + 3)",      # Unbalanced parentheses
        "5 & 3",       # Invalid character
        "5 *",         # Malformed expression
    ]

    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}' -> Result: {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Expression: '{expr}' -> Error: {e}")
    
    # --- Interactive Loop ---
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("calc> ")
            if user_input.lower() == 'exit':
                break
            if not user_input:
                continue

            result = calculator.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()
