
import math
from typing import List, Union

class Calculator:
    """
    A robust, safe, and efficient calculator that evaluates arithmetic expressions
    from a string. It adheres to ISO/IEC 25010 quality standards by being
    modular, testable, and secure (it does not use eval()).

    The evaluation process is performed in three stages:
    1.  Tokenization: The input string is broken down into a list of numbers
        and operators.
    2.  Shunting-yard Algorithm: The infix token list is converted to a
        postfix (Reverse Polish Notation) queue. This correctly handles
        operator precedence and parentheses.
    3.  RPN Evaluation: The postfix queue is evaluated to produce the final result.
    """

    def __init__(self):
        """Initializes the Calculator, defining operators and their properties."""
        self._operators = {
            '+': {'precedence': 1, 'func': lambda a, b: a + b},
            '-': {'precedence': 1, 'func': lambda a, b: a - b},
            '*': {'precedence': 2, 'func': lambda a, b: a * b},
            '/': {'precedence': 2, 'func': lambda a, b: self._safe_divide(a, b)},
        }
        self._parentheses = {'(', ')'}

    def _safe_divide(self, a: float, b: float) -> float:
        """
        Performs division, raising a specific error for division by zero.

        Raises:
            ZeroDivisionError: If the divisor 'b' is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Math error: Division by zero is not allowed.")
        return a / b

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts the raw expression string into a list of tokens.

        This method handles multi-digit numbers, floating-point numbers, and
        correctly identifies unary minus operators.

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens (numbers as floats, operators/parentheses as strings).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                continue

            if char in self._operators or char in self._parentheses:
                # Handle unary minus: a '-' is unary if it's the first token,
                # or if it follows an operator or an opening parenthesis.
                if char == '-' and (not tokens or tokens[-1] in self._operators or tokens[-1] == '('):
                    tokens.append(0.0) # Prepend a zero for expressions like "-5" -> "0-5"
                tokens.append(char)
                i += 1
                continue
            
            raise ValueError(f"Invalid character in expression: '{char}'")
        
        return tokens

    def _shunting_yard(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to postfix (RPN) using the
        Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in postfix (RPN) order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._operators:
                while (operator_stack and
                       operator_stack[-1] in self._operators and
                       self._operators[operator_stack[-1]]['precedence'] >= self._operators[token]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop() # Discard the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates a postfix (RPN) token queue.

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: Propagated from the division function.
        """
        operand_stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                operand_stack.append(token)
            elif token in self._operators:
                if len(operand_stack) < 2:
                    raise ValueError("Malformed expression: Not enough operands for operator.")
                
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                
                operation = self._operators[token]['func']
                result = operation(operand1, operand2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression: Too many operands.")

        return operand_stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public method that orchestrates the tokenization,
        conversion to RPN, and final evaluation.

        Args:
            expression: The mathematical expression to evaluate.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: For invalid expressions (e.g., syntax errors,
                        mismatched parentheses).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression must be a non-empty string.")

        tokens = self._tokenize(expression)
        rpn_queue = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn_queue)

        return result


if __name__ == '__main__':
    # This block serves as a simple demonstration and integration test.
    # For a production system, these would be in a separate test suite.
    
    calculator = Calculator()
    
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")

    # Example test cases
    test_expressions = [
        "3 + 5 * 2",              # Precedence
        "(3 + 5) * 2",            # Parentheses
        "10 / 2 - 3",             # Subtraction and Division
        "2.5 * 4 + 1.5",          # Floating point numbers
        "-5 + 10",                # Unary minus at the start
        "10 + -5",                # Unary minus after operator
        "10 * (5 - -2)",          # Unary minus inside parentheses
        "100 / (10 * (2 + 3))",   # Nested parentheses
        "10 / 0",                 # Division by zero (expected error)
        "5 * (2 + 1",             # Mismatched parentheses (expected error)
        "5 +",                    # Malformed expression (expected error)
        "5 @ 2"                   # Invalid character (expected error)
    ]

    print("\n--- Running Pre-defined Test Cases ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}'  =>  Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}'  =>  Error: {e}")
    print("--------------------------------------\n")
    
    # Interactive loop
    while True:
        try:
            user_input = input("Calculate: ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

