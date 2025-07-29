
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    operator precedence, and both integer and floating-point numbers (including negatives).

    Adheres to ISO/IEC 25010 requirements for correctness, safety, modularity, and maintainability.
    """

    # Supported operators and their precedence
    _OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    # Regular expression for tokenizing the input
    _TOKEN_REGEX = re.compile(
        r'''
        (?P<NUMBER>   -?\d+(\.\d+)? ) |    # Integer or decimal number, possibly negative
        (?P<OP>       [+\-*/]        ) |   # Operators
        (?P<LPAREN>   \(             ) |   # Left parenthesis
        (?P<RPAREN>   \)             ) |   # Right parenthesis
        (?P<SPACE>    \s+            )     # Spaces
        ''',
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: For invalid characters, unbalanced parentheses, or malformed expressions.
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List[Union[str, float]]:
        """
        Tokenizes the input string into numbers, operators, and parentheses.
        Handles negative numbers and validates allowed characters.

        Args:
            expr (str): The input arithmetic expression.

        Returns:
            List[Union[str, float]]: List of tokens.

        Raises:
            ValueError: If invalid characters are found.
        """
        tokens = []
        last_token = None
        pos = 0

        while pos < len(expr):
            match = self._TOKEN_REGEX.match(expr, pos)
            if not match:
                raise ValueError(f"Invalid character at position {pos}: '{expr[pos]}'")
            if match.lastgroup == 'NUMBER':
                number = float(match.group())
                tokens.append(number)
                last_token = 'NUMBER'
            elif match.lastgroup == 'OP':
                op = match.group()
                # Handle unary minus (negative number)
                if op == '-' and (last_token is None or last_token in {'OP', 'LPAREN'}):
                    # Look ahead for a number
                    num_match = self._TOKEN_REGEX.match(expr, match.end())
                    if num_match and num_match.lastgroup == 'NUMBER':
                        number = float('-' + num_match.group())
                        tokens.append(number)
                        pos = num_match.end() - 1
                        last_token = 'NUMBER'
                    else:
                        raise ValueError(f"Invalid usage of unary minus at position {pos}")
                else:
                    tokens.append(op)
                    last_token = 'OP'
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
                last_token = 'LPAREN'
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
                last_token = 'RPAREN'
            # Ignore spaces
            pos = match.end()
        return tokens

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts tokens from infix to postfix notation (RPN) using the shunting yard algorithm.

        Args:
            tokens (List[Union[str, float]]): List of tokens.

        Returns:
            List[Union[str, float]]: Tokens in RPN order.

        Raises:
            ValueError: For unbalanced parentheses or malformed expressions.
        """
        output = []
        stack = []
        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS and
                       self._OPERATORS[stack[-1]][0] >= self._OPERATORS[token][0]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses detected")
                stack.pop()  # Pop '('
            else:
                raise ValueError(f"Unknown token: {token}")

        while stack:
            top = stack.pop()
            if top in ('(', ')'):
                raise ValueError("Unbalanced parentheses detected")
            output.append(top)
        return output

    def _evaluate_rpn(self, tokens: List[Union[str, float]]) -> float:
        """
        Evaluates a postfix (RPN) expression.

        Args:
            tokens (List[Union[str, float]]): RPN tokens.

        Returns:
            float: Evaluated result.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: For malformed expressions.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                try:
                    b = stack.pop()
                    a = stack.pop()
                except IndexError:
                    raise ValueError("Malformed expression: insufficient operands")
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = self._OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in evaluation: {token}")
        if len(stack) != 1:
            raise ValueError("Malformed expression: too many operands")
        return stack[0]

if __name__ == "__main__":
    # Example usage and basic test cases
    calc = Calculator()
    examples = [
        "1 + 2 * 3",              # 7.0
        "(1 + 2) * 3",            # 9.0
        "-2 + 3 * 4",             # 10.0
        "2 / (3 - 1)",            # 1.0
        "3 + 4 * 2 / (1 - 5)",    # 1.0
        "-3.5 + (2 * 4.2)",       # 5.9
        "((2+3)*4)-5/(1+4)",      # 19.0
        "2 + -3",                 # -1.0
        "-(2 + 3)",               # -5.0 (should raise error, as unary minus before parentheses is not supported)
        "5 / 0",                  # Division by zero
        "1 + (2 * 3",             # Unbalanced parentheses
        "2 + 2a",                 # Invalid character
    ]

    for expr in examples:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
