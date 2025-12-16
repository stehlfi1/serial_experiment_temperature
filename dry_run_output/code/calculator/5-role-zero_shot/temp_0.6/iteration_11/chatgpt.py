
from typing import List, Union
import re

class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass

class Calculator:
    """
    A robust, safe arithmetic calculator adhering to ISO/IEC 25010 quality standards.
    Supports +, -, *, /, parentheses, correct precedence, integers and floats.
    """

    # Allowed operator tokens and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: Calculator._safe_divide(a, b)),
    }
    # Regular expression for allowed tokens (numbers, operators, parentheses, whitespace)
    TOKEN_REGEX = re.compile(r'''
        (?P<NUMBER>   -?\d+(?:\.\d*)?   ) |
        (?P<LPAREN>   \()               |
        (?P<RPAREN>   \))               |
        (?P<OPERATOR> [+\-*/]           ) |
        (?P<WS>       \s+               )
    ''', re.VERBOSE)

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression string.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            CalculatorError: If the expression is invalid.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    @staticmethod
    def _safe_divide(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Division by zero.")
        return a / b

    def _tokenize(self, expr: str) -> List[Union[str, float]]:
        """
        Tokenizes the input expression.

        Args:
            expr (str): Input expression.

        Returns:
            List[Union[str, float]]: List of tokens.

        Raises:
            SyntaxError: If invalid characters or malformed tokens.
        """
        tokens = []
        idx = 0
        prev_token = None
        while idx < len(expr):
            match = self.TOKEN_REGEX.match(expr, idx)
            if not match:
                raise SyntaxError(f"Invalid character at position {idx}: '{expr[idx]}'.")

            kind = match.lastgroup
            value = match.group()
            idx = match.end()

            if kind == 'WS':
                continue
            elif kind == 'NUMBER':
                # Coerce all literals (int or float) to float for consistency
                try:
                    num = float(value)
                except ValueError:
                    raise SyntaxError(f"Invalid number: {value}")
                tokens.append(num)
                prev_token = 'NUMBER'
            elif kind == 'OPERATOR':
                # To distinguish between binary minus and unary minus, e.g., '-3+5'
                if value == '-' and (prev_token is None or prev_token in ('OPERATOR', 'LPAREN')):
                    # This is a unary negative, treat as part of number if possible
                    # Try to consume the next number
                    next_match = self.TOKEN_REGEX.match(expr, idx)
                    if next_match and next_match.lastgroup == 'NUMBER':
                        full_number = value + next_match.group()
                        idx = next_match.end()
                        try:
                            num = float(full_number)
                        except ValueError:
                            raise SyntaxError(f"Invalid number: {full_number}")
                        tokens.append(num)
                        prev_token = 'NUMBER'
                        continue
                    else:
                        # It's a standalone '-', which is not valid
                        raise SyntaxError("Invalid negative sign usage.")
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
                raise SyntaxError("Unknown token during parsing.")
        return tokens

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN) using Shunting Yard Algorithm.

        Args:
            tokens (List[Union[str, float]]): Infix tokens.

        Returns:
            List[Union[str, float]]: RPN tokens.

        Raises:
            SyntaxError: If parentheses are unbalanced or operator misuse.
        """
        output = []
        stack = []
        for token in tokens:
            if isinstance(token, float):
                output.append(token)
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
                    raise SyntaxError("Unbalanced parentheses detected.")
                stack.pop()  # Discard the '('
            else:
                raise SyntaxError(f"Invalid token encountered: {token}")
        while stack:
            if stack[-1] in ('(', ')'):
                raise SyntaxError("Unbalanced parentheses detected.")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            rpn (List[Union[str, float]]): Tokens in RPN.

        Returns:
            float: Result of the calculation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            SyntaxError: If stack underflows (malformed expression).
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                try:
                    b = stack.pop()
                    a = stack.pop()
                except IndexError:
                    raise SyntaxError("Malformed expression: insufficient values for operation.")
                try:
                    result = self.OPERATORS[token][1](a, b)
                except ZeroDivisionError:
                    raise ZeroDivisionError("Division by zero.")
                stack.append(result)
            else:
                raise SyntaxError(f"Unknown token in RPN: {token}")
        if len(stack) != 1:
            raise SyntaxError("Malformed expression: too many values or operators.")
        return stack[0]

# === EXAMPLE TESTS ===
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",                 # 1 + (2 * 3) = 7
        "(1 + 2) * 3",               # (1 + 2) * 3 = 9
        "-2 + 2 * 5",                # -2 + (2 * 5) = 8
        "3 * (2 + -4.5)",            # 3 * (2 + -4.5) = 3 * -2.5 = -7.5
        "-3.14 + 2.14",              # -3.14 + 2.14 = -1.0
        "(1 + (2 * 3)) - (4 / 2)",   # (1 + 6) - 2 = 5
        "4 / (2 - 2)",               # Division by zero
        "2 +",                       # Syntax error
        "(1 + 2",                    # Unbalanced parentheses
    ]
    for expr in test_expressions:
        print(f"Expression: {expr!r}")
        try:
            result = calc.calculate(expr)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {e.__class__.__name__}: {e}\n")
