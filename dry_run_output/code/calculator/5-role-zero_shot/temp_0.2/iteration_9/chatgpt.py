
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.
    Adheres to ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    # Allowed characters (digits, operators, parentheses, dot, whitespace)
    TOKEN_REGEX = re.compile(
        r"""
        (?P<NUMBER>   -?\d+(\.\d+)? ) |   # Integer or float, possibly negative
        (?P<OP>       [+\-*/]        ) |   # Operators
        (?P<LPAREN>   \(             ) |   # Left parenthesis
        (?P<RPAREN>   \)             ) |   # Right parenthesis
        (?P<SPACE>    \s+            )     # Whitespace
        """,
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
            ValueError: If the expression is invalid (syntax, unbalanced parentheses, etc.).
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenizes the input expression into numbers, operators, and parentheses.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            List[str]: List of tokens.

        Raises:
            ValueError: If invalid characters or malformed numbers are found.
        """
        tokens = []
        pos = 0
        prev_token = None
        while pos < len(expression):
            match = self.TOKEN_REGEX.match(expression, pos)
            if not match:
                raise ValueError(f"Invalid character at position {pos}: '{expression[pos]}'")
            if match.lastgroup == 'NUMBER':
                num_str = match.group('NUMBER')
                # Handle unary minus (negative numbers)
                if prev_token in (None, 'OP', 'LPAREN'):
                    # Accept negative numbers at start or after operator/left paren
                    tokens.append(num_str)
                else:
                    # Only positive numbers allowed here
                    if num_str.startswith('-'):
                        raise ValueError(f"Unexpected negative number at position {pos}")
                    tokens.append(num_str)
                prev_token = 'NUMBER'
            elif match.lastgroup == 'OP':
                op = match.group('OP')
                # Handle unary minus for negative numbers
                if op == '-' and (prev_token in (None, 'OP', 'LPAREN')):
                    # Will be handled as part of the next number token
                    # So skip adding as operator
                    pass
                else:
                    tokens.append(op)
                    prev_token = 'OP'
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
                prev_token = 'LPAREN'
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
                prev_token = 'RPAREN'
            # Ignore whitespace
            pos = match.end()
        # Validate parentheses balance
        if tokens.count('(') != tokens.count(')'):
            raise ValueError("Unbalanced parentheses in expression.")
        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts the list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        Args:
            tokens (List[str]): List of tokens in infix notation.

        Returns:
            List[Union[str, float]]: Tokens in RPN.

        Raises:
            ValueError: For invalid syntax (e.g., misplaced operators or parentheses).
        """
        output = []
        stack = []
        for idx, token in enumerate(tokens):
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
                    raise ValueError("Mismatched parentheses.")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Invalid token: {token}")
        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Mismatched parentheses.")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation.

        Args:
            rpn (List[Union[str, float]]): The RPN expression.

        Returns:
            float: The result.

        Raises:
            ValueError: For malformed RPN expressions.
            ZeroDivisionError: For division by zero.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero.")
                result = self.OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Malformed expression: too many operands.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if the token is a valid number.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example usage and test cases
if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        "1 + 2 * 3",                   # 7.0
        "(1 + 2) * 3",                 # 9.0
        "10 / 2 + 3.5",                # 8.5
        "-5 + 3 * (2 - 8)",            # -23.0
        "4 + -3",                      # 1.0
        "((2.5 + 2.5) * 2) / 2",       # 5.0
        "3 + 4 * 2 / (1 - 5)",         # 1.0
        "3.5 + 2.5",                   # 6.0
        "-3.5 * 2",                    # -7.0
        "0 / 1",                       # 0.0
    ]
    for expr in test_cases:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
