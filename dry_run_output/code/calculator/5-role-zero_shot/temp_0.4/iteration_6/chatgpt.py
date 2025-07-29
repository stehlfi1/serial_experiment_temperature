
from typing import List, Union
import re

class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, /, parentheses,
    correct operator precedence, and both integers and floating-point numbers.
    Implements ISO/IEC 25010 quality requirements.
    """

    # Allowed operators and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    # Regular expression for tokenization
    TOKEN_REGEX = re.compile(
        r"""
        (?P<NUMBER>    -?\d+(?:\.\d+)? ) |   # Integer or float (possibly negative)
        (?P<OPERATOR>  [+\-*/]         ) |   # Operators
        (?P<LPAREN>    \(              ) |   # Left parenthesis
        (?P<RPAREN>    \)              ) |   # Right parenthesis
        (?P<SPACE>     \s+             )     # Spaces
        """,
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.

        :param expression: The arithmetic expression as a string.
        :return: The result of the evaluated expression.
        :raises ValueError: If the input is invalid (e.g., unbalanced parentheses, invalid characters).
        :raises ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenizes the input expression into numbers, operators, and parentheses.

        :param expression: The arithmetic expression as a string.
        :return: List of tokens.
        :raises ValueError: If invalid characters are found.
        """
        tokens = []
        pos = 0
        prev_token = None

        while pos < len(expression):
            match = self.TOKEN_REGEX.match(expression, pos)
            if not match:
                raise ValueError(f"Invalid character at position {pos}: '{expression[pos]}'")
            if match.lastgroup == 'NUMBER':
                tokens.append(match.group('NUMBER'))
                prev_token = 'NUMBER'
            elif match.lastgroup == 'OPERATOR':
                # Handle unary minus for negative numbers
                op = match.group('OPERATOR')
                # If '-' is at start, or after '(', or another operator, treat as unary minus
                if op == '-' and (prev_token is None or prev_token in {'OPERATOR', 'LPAREN'}):
                    # Look ahead for a number
                    next_match = self.TOKEN_REGEX.match(expression, match.end())
                    if next_match and next_match.lastgroup == 'NUMBER':
                        # Merge '-' and number
                        tokens.append('-' + next_match.group('NUMBER'))
                        pos = next_match.end() - 1  # -1 because pos will be incremented below
                        prev_token = 'NUMBER'
                    else:
                        raise ValueError(f"Invalid use of unary minus at position {pos}")
                else:
                    tokens.append(op)
                    prev_token = 'OPERATOR'
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
                prev_token = 'LPAREN'
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
                prev_token = 'RPAREN'
            # Ignore spaces
            pos = match.end()
        self._validate_parentheses(tokens)
        return tokens

    def _validate_parentheses(self, tokens: List[str]) -> None:
        """
        Validates that parentheses are balanced.

        :param tokens: List of tokens.
        :raises ValueError: If parentheses are unbalanced.
        """
        balance = 0
        for token in tokens:
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Unbalanced parentheses: too many closing ')'")
        if balance != 0:
            raise ValueError("Unbalanced parentheses: too many opening '('")

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

        :param tokens: List of tokens in infix notation.
        :return: List of tokens in RPN.
        """
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                       self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses")
                stack.pop()
        while stack:
            if stack[-1] in {'(', ')'}:
                raise ValueError("Unbalanced parentheses")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates the expression in Reverse Polish Notation.

        :param rpn: List of tokens in RPN.
        :return: The result as a float.
        :raises ZeroDivisionError: If division by zero occurs.
        :raises ValueError: If the expression is invalid.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = self.OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        return stack[0]

    def _is_number(self, token: str) -> bool:
        """
        Checks if the token is a valid number.

        :param token: Token string.
        :return: True if token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example usage and simple test cases
if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        "2 + 3 * 4",              # 14.0
        "(2 + 3) * 4",            # 20.0
        "3 + 4 * 2 / (1 - 5)",    # 1.0
        "-2 + 3",                 # 1.0
        "3.5 * (2 - 0.5)",        # 5.25
        "-(2 + 3) * 4",           # -20.0
        "2 + -3",                 # -1.0
        "2 + (-3)",               # -1.0
        "10 / 2",                 # 5.0
        "10 / 0",                 # ZeroDivisionError
        "((2 + 3) * 2",           # ValueError: Unbalanced parentheses
        "2 + 3a",                 # ValueError: Invalid character
    ]
    for expr in test_cases:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
