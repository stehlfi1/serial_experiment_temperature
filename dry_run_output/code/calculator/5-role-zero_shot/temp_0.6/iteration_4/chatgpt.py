
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    and both integer and floating-point numbers (including negatives).
    Adheres to ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b if b != 0 else Calculator._raise_zero_division()),
    }

    # Pattern for matching tokens (numbers, operators, parentheses)
    TOKEN_REGEX = re.compile(
        r"""
        (?P<NUMBER>    -?\d+(\.\d+)?   ) |   # Integer or decimal number, possibly negative
        (?P<OPERATOR>  [+\-*/]         ) |   # Operators
        (?P<LPAREN>    \(              ) |   # Left parenthesis
        (?P<RPAREN>    \)              )     # Right parenthesis
        """,
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression string and return the result as a float.
        Raises:
            ValueError: If the input is invalid.
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        postfix = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        return result

    @staticmethod
    def _raise_zero_division():
        raise ZeroDivisionError("Division by zero.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenize the input expression into a list of numbers, operators, and parentheses.
        Handles negative numbers. Raises ValueError for invalid characters.
        """
        tokens = []
        pos = 0
        last_token = None

        # Remove all whitespace
        expression = expression.replace(' ', '')

        while pos < len(expression):
            match = self.TOKEN_REGEX.match(expression, pos)
            if not match:
                raise ValueError(f"Invalid character at position {pos}: '{expression[pos]}'")

            token = match.group()
            # Handle unary minus for negative numbers
            if token == '-' and (last_token is None or last_token in '(*+/ -'):
                # Next token must be a number
                next_match = self.TOKEN_REGEX.match(expression, match.end())
                if next_match and next_match.group('NUMBER'):
                    token += next_match.group('NUMBER')
                    pos = next_match.end()
                else:
                    raise ValueError(f"Invalid syntax near '-' at position {pos}")
            else:
                pos = match.end()

            tokens.append(token)
            last_token = token

        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validate the tokens for balanced parentheses and invalid sequences.
        Raises ValueError for invalid expressions.
        """
        paren_balance = 0
        last_token = None

        for idx, token in enumerate(tokens):
            if token == '(':
                paren_balance += 1
            elif token == ')':
                paren_balance -= 1
                if paren_balance < 0:
                    raise ValueError("Unbalanced parentheses: too many closing ')'")
            elif self._is_operator(token):
                if last_token is None or self._is_operator(last_token) or last_token == '(':
                    # Allow unary minus only (already handled in tokenization)
                    if token != '-' or (last_token is not None and last_token != '('):
                        raise ValueError(f"Invalid operator sequence at token {idx}: '{token}'")
            elif not self._is_number(token) and token not in ('(', ')'):
                raise ValueError(f"Invalid token: '{token}'")
            last_token = token

        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses: mismatched '(' and ')'.")

    def _infix_to_postfix(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Convert infix tokens to postfix (Reverse Polish Notation) using the Shunting Yard algorithm.
        """
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif self._is_operator(token):
                while (stack and stack[-1] != '(' and
                       self._is_operator(stack[-1]) and
                       self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses during parsing.")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token during parsing: '{token}'")

        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses at the end of parsing.")
            output.append(stack.pop())

        return output

    def _evaluate_postfix(self, postfix: List[Union[str, float]]) -> float:
        """
        Evaluate a postfix (RPN) expression and return the result.
        """
        stack = []
        for token in postfix:
            if isinstance(token, float):
                stack.append(token)
            elif self._is_operator(token):
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                try:
                    result = self.OPERATORS[token][1](a, b)
                except ZeroDivisionError as zde:
                    raise ZeroDivisionError("Division by zero.") from zde
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in postfix expression: '{token}'")

        if len(stack) != 1:
            raise ValueError("Invalid syntax: too many operands.")
        return stack[0]

    @staticmethod
    def _is_operator(token: str) -> bool:
        return token in Calculator.OPERATORS

    @staticmethod
    def _is_number(token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example usage (for demonstration and testability):
if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-4 + 6 / 2",
        "3 + 4 * 2 / (1 - 5)",
        "((2.5 + 3.5) * 2) / -2",
        "5 / 0",  # Should raise ZeroDivisionError
        "2 + (3 - (4 + 5)",  # Should raise ValueError (unbalanced)
        "2 + abc",  # Should raise ValueError (invalid characters)
    ]

    for expr in test_cases:
        try:
            result = calc.calculate(expr)
            print(f"Expression: {expr} = {result}")
        except Exception as e:
            print(f"Expression: {expr} raised error: {e}")
