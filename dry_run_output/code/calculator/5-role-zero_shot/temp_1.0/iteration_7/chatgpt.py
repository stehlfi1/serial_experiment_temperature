
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, and parentheses,
    following operator precedence and proper validation.

    Implements:
        calculate(expression: str) -> float
    """

    # Supported operators with their precedence and associativity
    _OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L'),
    }

    # Regex for tokenizing (numbers, parentheses, operators)
    _TOKEN_REGEX = re.compile(
        r'''
        (?P<NUMBER>    -?\d+(\.\d+)? ) |   # Integer or decimal (support negative values)
        (?P<OP>        [\+\-\*/]     ) |   # Arithmetic operators
        (?P<LPAREN>    [(]           ) |   # Left parenthesis
        (?P<RPAREN>    [)]           ) |   # Right parenthesis
        (?P<SPACE>     \s+           )     # Spaces (to be ignored)
        ''',
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression string

        Returns:
            float: Calculated result

        Raises:
            ValueError: For invalid expressions or characters
            ZeroDivisionError: For division by zero
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: On invalid characters or malformed numbers.
        """
        tokens = []
        position = 0
        prev_token = None

        while position < len(expression):
            match = self._TOKEN_REGEX.match(expression, position)
            if not match:
                raise ValueError(f"Invalid character at position {position}: '{expression[position]}'")

            if match.lastgroup == 'NUMBER':
                token = match.group('NUMBER')
                # To handle unary minus only at start or after '(' or operator
                if prev_token is None or prev_token in ('(', '+', '-', '*', '/'):
                    tokens.append(token)
                else:
                    # Negative numbers must be signaled with operator
                    if token.startswith('-'):
                        raise ValueError(f"Unexpected negative number at position {position}")
                    tokens.append(token)
                prev_token = 'NUMBER'
            elif match.lastgroup == 'OP':
                op = match.group('OP')
                # Unary minus handling: transform "-3" to "-3", not as subtraction
                if op == '-' and (
                    prev_token is None or prev_token in ('(', '+', '-', '*', '/')
                ):
                    # Expect a number immediately after, handled by regex (will parse "-3" as a number)
                    prev_token = 'OP'
                    tokens.append(op)
                else:
                    tokens.append(op)
                    prev_token = op
            elif match.lastgroup in ('LPAREN', 'RPAREN'):
                tokens.append(match.group(match.lastgroup))
                prev_token = match.lastgroup
            # Ignore white space
            position = match.end()
        tokens = self._merge_unary_minus(tokens)
        self._validate_parentheses(tokens)
        return tokens

    def _merge_unary_minus(self, tokens: List[str]) -> List[str]:
        """
        Merges unary minus with numbers to properly handle negatives.

        Example: ['-', '3', '+', '(', '-', '2', ')'] -> ['-3', '+', '(', '-2', ')']
        """
        result = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '-' and (
                i == 0 or tokens[i - 1] in ('(', '+', '-', '*', '/')
            ):
                # Unary minus detected
                next_token = tokens[i + 1] if i + 1 < len(tokens) else None
                if self._is_number(next_token):
                    result.append(f"-{next_token}")
                    i += 2
                else:
                    raise ValueError("Unary minus must be followed by number or parenthesis")
            else:
                result.append(token)
                i += 1
        return result

    def _validate_parentheses(self, tokens: List[str]):
        """
        Validates that the parentheses in the token list are balanced.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        stack = []
        for token in tokens:
            if token == '(':
                stack.append('(')
            elif token == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: too many closing parens")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: too many opening parens")

    def _is_number(self, token: Union[str, None]) -> bool:
        if token is None:
            return False
        try:
            float(token)
            return True
        except (ValueError, TypeError):
            return False

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts the token list from infix notation to Reverse Polish Notation (RPN)
        using the shunting-yard algorithm.

        Raises:
            ValueError: On malformed expressions (e.g., consecutive operators).
        """
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS and (
                    (self._OPERATORS[token][1] == 'L' and self._OPERATORS[token][0] <= self._OPERATORS[stack[-1]][0]) or
                    (self._OPERATORS[token][1] == 'R' and self._OPERATORS[token][0] < self._OPERATORS[stack[-1]][0])
                )):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token during RPN conversion: {token}")

        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Mismatched parentheses in expression")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, tokens: List[str]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation.

        Raises:
            ValueError: On malformed expressions (e.g., missing operands).
            ZeroDivisionError: On division by zero.
        """
        stack = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator '{}'.".format(token))
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
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Malformed expression. Stack residual: {}".format(stack))
        return stack[0]

# Example usage and test:
if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        "1 + 2 * 3",               # 7
        " (1 + 2) * 3 ",           # 9
        "-1 + 2",                  # 1
        "4 / 2 + 7 * (3 - 1)",     # 16
        "(1+2.5)/0.5",             # 7.0
        "-(3 + 2) * -2",           # 10
        "3 + -(-3)",               # 6
        "3.5 * (2 - 5.5 / (1 + 1))" # 3.5 * (2 - 5.5/2) = 3.5 * (2 - 2.75) = 3.5 * -0.75 = -2.625
    ]

    for expr in test_cases:
        try:
            result = calc.calculate(expr)
            print(f"{expr.strip()} = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr}': {e}")
