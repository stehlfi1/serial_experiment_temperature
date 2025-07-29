
import re
from typing import List, Union

class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.

    Methods
    -------
    calculate(expression: str) -> float
        Evaluates the arithmetic expression and returns the result as a float.
    """

    # Supported operators and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    # Token specification for numbers, operators, parentheses, and whitespace
    TOKEN_SPEC = re.compile(
        r"""
        (?P<NUMBER>   -?\d+(\.\d+)? ) |   # Integer or decimal number, possibly negative
        (?P<OP>       [+\-*/]       ) |   # Arithmetic operators
        (?P<LPAREN>   \(            ) |   # Left parenthesis
        (?P<RPAREN>   \)            ) |   # Right parenthesis
        (?P<WS>       \s+           )     # Whitespace
        """,
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.

        Parameters
        ----------
        expression : str
            The arithmetic expression to evaluate.

        Returns
        -------
        float
            The result of the evaluated expression.

        Raises
        ------
        ValueError
            If the expression is invalid or contains errors.
        ZeroDivisionError
            If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenizes the input expression into numbers, operators, and parentheses.

        Parameters
        ----------
        expression : str
            The arithmetic expression to tokenize.

        Returns
        -------
        List[str]
            List of tokens.

        Raises
        ------
        ValueError
            If invalid characters are found.
        """
        tokens = []
        pos = 0
        last_token = None
        while pos < len(expression):
            match = self.TOKEN_SPEC.match(expression, pos)
            if not match:
                raise ValueError(f"Invalid character at position {pos}: '{expression[pos]}'")
            kind = match.lastgroup
            value = match.group()
            if kind == 'WS':
                pos = match.end()
                continue
            if kind == 'OP' and value == '-' and (
                last_token is None or last_token in ('OP', 'LPAREN')
            ):
                # Handle unary minus: attach to the next number
                # Look ahead for a number
                num_match = self.TOKEN_SPEC.match(expression, match.end())
                if num_match and num_match.lastgroup == 'NUMBER':
                    num_value = '-' + num_match.group().lstrip('-')
                    tokens.append(num_value)
                    pos = num_match.end()
                    last_token = 'NUMBER'
                    continue
                else:
                    # Standalone unary minus (e.g., "-(2+3)")
                    tokens.append('-1')
                    tokens.append('*')
                    pos = match.end()
                    last_token = 'OP'
                    continue
            if kind == 'NUMBER':
                tokens.append(value)
                last_token = 'NUMBER'
            elif kind in ('OP', 'LPAREN', 'RPAREN'):
                tokens.append(value)
                last_token = kind
            pos = match.end()
        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts the list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        Parameters
        ----------
        tokens : List[str]
            List of tokens in infix notation.

        Returns
        -------
        List[Union[str, float]]
            List of tokens in RPN.

        Raises
        ------
        ValueError
            If parentheses are unbalanced or tokens are invalid.
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
                    raise ValueError("Unbalanced parentheses detected.")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Invalid token: {token}")
        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses detected.")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates the RPN expression.

        Parameters
        ----------
        rpn : List[Union[str, float]]
            List of tokens in RPN.

        Returns
        -------
        float
            The result of the evaluated RPN expression.

        Raises
        ------
        ZeroDivisionError
            If division by zero occurs.
        ValueError
            If the RPN is invalid.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero.")
                result = self.OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if the token is a valid number.

        Parameters
        ----------
        token : str
            The token to check.

        Returns
        -------
        bool
            True if token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example usage and test cases
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",                # 7.0
        "(1 + 2) * 3",              # 9.0
        "-2 + 3 * 4",               # 10.0
        "3 + 4 * 2 / (1 - 5)",      # 1.0
        "3.5 + 2.1 * (2 - 0.1)",    # 7.49
        "-(2 + 3) * 4",             # -20.0
        "((2.5))",                  # 2.5
        "1 / 0",                    # ZeroDivisionError
        "2 + (3 * 4",               # ValueError (unbalanced parentheses)
        "2 + 3a",                   # ValueError (invalid character)
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
