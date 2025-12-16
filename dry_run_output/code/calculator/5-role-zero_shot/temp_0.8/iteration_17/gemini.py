
import operator
from typing import List, Union

class Calculator:
    """
    A high-quality, safe, and maintainable arithmetic calculator.

    This class evaluates mathematical expressions from a string, supporting addition,
    subtraction, multiplication, division, and parentheses. It adheres to standard
    operator precedence.

    The implementation uses the Shunting-yard algorithm to convert the infix
    expression to Reverse Polish Notation (RPN), which is then evaluated.
    This approach is efficient and avoids the use of `eval()`, ensuring safety.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Correctly evaluates expressions.
    - Performance Efficiency: O(n) time complexity.
    - Modularity: Logic is separated into tokenization, parsing, and evaluation.
    - Reliability: Robust error handling for invalid input and operations.
    - Security: No `eval()` is used, preventing code injection vulnerabilities.
    - Maintainability: Clean, documented, and easily extensible.
    """

    # Define operators, their precedence, and their associativity.
    # Higher precedence value means it's evaluated first.
    # Unary minus ('_') has the highest precedence.
    _OPERATORS = {
        '+': {'precedence': 1, 'func': operator.add, 'assoc': 'L'},
        '-': {'precedence': 1, 'func': operator.sub, 'assoc': 'L'},
        '*': {'precedence': 2, 'func': operator.mul, 'assoc': 'L'},
        '/': {'precedence': 2, 'func': operator.truediv, 'assoc': 'L'},
        '_': {'precedence': 3, 'func': operator.neg, 'assoc': 'R'}, # Unary minus
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression in infix notation.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid
                        characters, or has unbalanced parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")
        
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError):
            # Re-raising to provide a clear public error interface.
            raise
        except Exception as e:
            # Catch any other unexpected errors during processing.
            raise ValueError(f"Invalid expression provided: {e}") from e

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts the input string into a list of tokens (numbers and operators).
        Handles negative numbers and floating-point values correctly.
        """
        tokens = []
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

            if char in self._OPERATORS:
                # Distinguish between unary and binary minus
                if char == '-':
                    is_unary = (
                        not tokens or
                        isinstance(tokens[-1], str) and tokens[-1] in self._OPERATORS or
                        tokens[-1] == '('
                    )
                    if is_unary:
                        tokens.append('_') # Use '_' for unary minus
                    else:
                        tokens.append('-') # Binary minus
                else:
                    tokens.append(char)
                i += 1
                continue

            if char in '()':
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Invalid character in expression: '{char}'")
        
        return tokens

    def _to_rpn(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._OPERATORS:
                op1 = self._OPERATORS[token]
                while (operator_stack and operator_stack[-1] != '(' and
                       (self._OPERATORS[operator_stack[-1]]['precedence'] > op1['precedence'] or
                        (self._OPERATORS[operator_stack[-1]]['precedence'] == op1['precedence'] and op1['assoc'] == 'L'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses: missing '('")
                operator_stack.pop() # Discard the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses: missing ')'")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates a queue of tokens in Reverse Polish Notation (RPN).
        """
        stack = []
        for token in rpn_queue:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                op_info = self._OPERATORS[token]
                
                # Unary operator
                if token == '_':
                    if not stack:
                        raise ValueError("Invalid expression: unary minus needs an operand.")
                    operand = stack.pop()
                    stack.append(op_info['func'](operand))
                # Binary operators
                else:
                    if len(stack) < 2:
                        raise ValueError(f"Invalid expression: operator '{token}' needs two operands.")
                    op2 = stack.pop()
                    op1 = stack.pop()
                    
                    if token == '/' and op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                        
                    result = op_info['func'](op1, op2)
                    stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values or operators.")
            
        return stack[0]

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()

    # A list of expressions to test
    expressions = [
        "3 + 4 * 2 / ( 1 - 5 )",
        "10 + -5.5",
        "-2 * (3 + 4)",
        "100 / (10 * (2 + 3))",
        "3.14 * (2 ^ 2)", # Invalid character test
        "10 / 0",         # Division by zero test
        "(1 + 2",         # Mismatched parentheses test
        "5 * ",           # Malformed expression test
    ]

    print("--- Console Calculator Demonstration ---")
    for expr in expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}'\nResult: {result}\n")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Expression: '{expr}'\nError: {e}\n")

    # Example of correct outputs:
    # '3 + 4 * 2 / ( 1 - 5 )' -> 3 + 8 / -4 -> 3 + -2 -> 1.0
    # '10 + -5.5' -> 4.5
    # '-2 * (3 + 4)' -> -2 * 7 -> -14.0
    # '100 / (10 * (2 + 3))' -> 100 / (10 * 5) -> 100 / 50 -> 2.0
