
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses, 
    integers, floating-point numbers, and negative values.

    Adheres to ISO/IEC 25010 quality requirements:
        - Correctness
        - Performance
        - Modularity
        - Safety
        - Testability
        - Readability and Documentation

    Usage:
        calc = Calculator()
        result = calc.calculate("2 + 3 * (4 - 1)")
    """

    # Allowed operators and their precedence/associativity
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'}
    }

    # Regular expression for valid tokens (numbers, operators, parentheses)
    TOKEN_REGEX = re.compile(
        r"""
        (?P<NUMBER>   -?\d+(\.\d+)? )   |   # integer or float, possibly negative
        (?P<OPERATOR> [+\-*/]        )   |   # operators
        (?P<LPAREN>   \(             )   |   # left parenthesis
        (?P<RPAREN>   \)             )       # right parenthesis
        """,
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result.

        :param expression: The arithmetic expression as a string.
        :return: The result as a float.
        :raises ValueError, ZeroDivisionError, SyntaxError: For invalid inputs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Tokenizes the input expression string into numbers, operators, and parentheses.

        :param expression: The arithmetic expression as a string.
        :return: List of tokens (numbers as float, operators as str).
        :raises ValueError: If invalid characters or malformed numbers are encountered.
        """
        tokens = []
        index = 0
        expr = expression.replace(' ', '')  # Remove whitespace

        if not expr:
            raise ValueError("Empty expression.")

        prev_token = None  # To handle unary minus

        while index < len(expr):
            match = self.TOKEN_REGEX.match(expr, index)
            if not match:
                raise ValueError(f"Invalid character at position {index}: '{expr[index]}'")

            kind = match.lastgroup
            value = match.group()

            if kind == 'NUMBER':
                try:
                    tokens.append(float(value))
                except ValueError:
                    raise ValueError(f"Malformed number at position {index}: '{value}'")
                prev_token = 'NUMBER'
            elif kind == 'OPERATOR':
                # Handle unary minus (negative numbers)
                if value == '-' and (prev_token is None or prev_token in ('OPERATOR', 'LPAREN')):
                    # Look ahead to next number
                    num_match = re.match(r'-?\d+(\.\d+)?', expr[match.end():])
                    if num_match:
                        num_value = value + num_match.group()
                        try:
                            tokens.append(float(num_value))
                        except ValueError:
                            raise ValueError(f"Malformed negative number at position {index}: '{num_value}'")
                        index = match.end() + num_match.end()
                        prev_token = 'NUMBER'
                        continue
                    else:
                        # Standalone '-', treat as 0 - next expression
                        tokens.append(0.0)
                        tokens.append('-')
                        prev_token = 'OPERATOR'
                else:
                    tokens.append(value)
                    prev_token = 'OPERATOR'
            elif kind == 'LPAREN':
                tokens.append('(')
                prev_token = 'LPAREN'
            elif kind == 'RPAREN':
                tokens.append(')')
                prev_token = 'RPAREN'
            else:
                raise ValueError(f"Unknown token at position {index}: '{value}'")
            index = match.end()

        return tokens

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts the list of tokens from infix to Reverse Polish Notation (RPN)
        using the shunting yard algorithm.

        :param tokens: List of tokens (numbers as float, operators as str).
        :return: List of tokens in RPN order.
        :raises SyntaxError: If parentheses are unbalanced.
        """
        output_queue: List[Union[str, float]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and
                       operator_stack[-1] in self.OPERATORS and
                       ((self.OPERATORS[token]['associativity'] == 'L' and
                         self.OPERATORS[token]['precedence'] <= self.OPERATORS[operator_stack[-1]]['precedence']) or
                        (self.OPERATORS[token]['associativity'] == 'R' and
                         self.OPERATORS[token]['precedence'] < self.OPERATORS[operator_stack[-1]]['precedence']))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                found_lparen = False
                while operator_stack:
                    top = operator_stack.pop()
                    if top == '(':
                        found_lparen = True
                        break
                    else:
                        output_queue.append(top)
                if not found_lparen:
                    raise SyntaxError("Unbalanced parentheses: ')' encountered without matching '('")
            else:
                raise ValueError(f"Unknown token in expression: {token}")

        # Pop any remaining operators
        while operator_stack:
            top = operator_stack.pop()
            if top in ('(', ')'):
                raise SyntaxError("Unbalanced parentheses in expression.")
            output_queue.append(top)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Union[str, float]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        :param rpn_tokens: List of tokens in RPN order.
        :return: The computed result as a float.
        :raises ZeroDivisionError: If division by zero occurs.
        :raises SyntaxError: If the expression is malformed.
        """
        stack: List[float] = []

        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise SyntaxError("Insufficient operands for operator.")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(a / b)
            else:
                raise ValueError(f"Unknown token in RPN evaluation: {token}")

        if len(stack) != 1:
            raise SyntaxError("Malformed expression.")

        return stack[0]

# Example usage and test cases
if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        "2 + 3 * 4",              # 14
        "(2 + 3) * 4",            # 20
        "7 + (6 * 5^2 + 3)",      # Should raise ValueError (invalid character '^')
        "3 + 4 * 2 / (1 - 5)",    # 1
        "-2 + 3",                 # 1
        "2 + -3",                 # -1
        "-2 + -3",                # -5
        "3.5 * 2",                # 7.0
        "4 / 0",                  # Should raise ZeroDivisionError
        "((2+3)*2",               # Should raise SyntaxError (unbalanced parentheses)
        "2 + (3 - (4 + 5))",      # -4
        "",                       # Should raise ValueError (empty)
        "2 ++ 2",                 # Should raise SyntaxError or ValueError (malformed)
    ]
    for expr in test_cases:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr!r} => Error: {e}")
