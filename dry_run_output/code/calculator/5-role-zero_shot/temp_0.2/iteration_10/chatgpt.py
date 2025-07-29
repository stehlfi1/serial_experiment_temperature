
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    and both integer and floating-point numbers (including negatives).
    Adheres to ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence
    _OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression string and returns the result as a float.

        :param expression: The arithmetic expression to evaluate.
        :return: The evaluated result as a float.
        :raises ValueError: If the expression is invalid.
        :raises ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input expression string into a list of tokens.

        :param expression: The arithmetic expression.
        :return: List of tokens.
        :raises ValueError: If invalid characters are found.
        """
        # Remove whitespace for easier processing
        expr = expression.replace(' ', '')

        # Tokenization regex:
        #   - Numbers (including floats and negatives)
        #   - Operators
        #   - Parentheses
        token_pattern = re.compile(
            r"""
            (?P<number>    -?\d+(\.\d+)? ) |
            (?P<op>        [+\-*/]        ) |
            (?P<paren>     [()]           )
            """,
            re.VERBOSE
        )

        tokens = []
        idx = 0
        length = len(expr)
        while idx < length:
            match = token_pattern.match(expr, idx)
            if not match:
                raise ValueError(f"Invalid character at position {idx}: '{expr[idx]}'")
            token = match.group()
            # Handle unary minus (negative numbers)
            if token == '-' and (
                idx == 0 or expr[idx - 1] in '(*+/ -'
            ):
                # Look ahead for a number
                num_match = re.match(r'-\d+(\.\d+)?', expr[idx:])
                if num_match:
                    token = num_match.group()
                    tokens.append(token)
                    idx += len(token)
                    continue
            tokens.append(token)
            idx += len(token)
        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the token list for balanced parentheses and correct token sequence.

        :param tokens: List of tokens.
        :raises ValueError: If validation fails.
        """
        paren_count = 0
        prev_token = None
        for token in tokens:
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
            elif token in self._OPERATORS:
                if prev_token is None or prev_token in self._OPERATORS or prev_token == '(':
                    # Allow unary minus, but not other operators
                    if token != '-' or (prev_token is not None and prev_token != '('):
                        raise ValueError("Invalid operator sequence")
            else:
                # Should be a number
                try:
                    float(token)
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")
            prev_token = token
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: too many '('")

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

        :param tokens: List of tokens.
        :return: List of tokens in RPN.
        """
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS and
                       self._OPERATORS[token][0] <= self._OPERATORS[stack[-1]][0]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Unbalanced parentheses")
                stack.pop()  # Remove '('
        while stack:
            if stack[-1] in '()':
                raise ValueError("Unbalanced parentheses")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates a Reverse Polish Notation (RPN) expression.

        :param rpn: List of tokens in RPN.
        :return: The evaluated result as a float.
        :raises ZeroDivisionError: If division by zero occurs.
        :raises ValueError: If the expression is invalid.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values")
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = self._OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if a token is a valid number.

        :param token: The token to check.
        :return: True if token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example usage (for testing purposes)
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-4 + 5.5 * (2 - 3.2) / 2",
        "10 / (5 - 5)",  # Should raise ZeroDivisionError
        "2 + (3 * 4",    # Should raise ValueError (unbalanced parentheses)
        "2 + $ 3",       # Should raise ValueError (invalid character)
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
