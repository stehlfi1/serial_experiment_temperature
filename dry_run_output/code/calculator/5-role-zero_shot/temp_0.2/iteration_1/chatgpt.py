
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers and floating-point numbers (including negatives).
    Adheres to ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    # Valid token regex: numbers, operators, parentheses, whitespace
    TOKEN_REGEX = re.compile(
        r"""
        (?P<NUMBER>    -?\d+(\.\d+)? ) |   # Integer or float, possibly negative
        (?P<OPERATOR>  [+\-*/]       ) |   # Operators
        (?P<LPAREN>    \(            ) |   # Left parenthesis
        (?P<RPAREN>    \)            ) |   # Right parenthesis
        (?P<SPACE>     \s+           )     # Whitespace
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
            ValueError: If the expression is invalid or contains errors.
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
            ValueError: If invalid characters are found.
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
                op = match.group('OPERATOR')
                # Handle unary minus (negative numbers)
                if op == '-' and (prev_token is None or prev_token in {'OPERATOR', 'LPAREN'}):
                    # Look ahead for a number
                    next_match = self.TOKEN_REGEX.match(expression, match.end())
                    if next_match and next_match.lastgroup == 'NUMBER':
                        # Merge '-' with the number
                        num = '-' + next_match.group('NUMBER')
                        tokens.append(num)
                        pos = next_match.end() - 1  # -1 because pos will be incremented at end
                        prev_token = 'NUMBER'
                    else:
                        raise ValueError("Invalid use of unary minus.")
                else:
                    tokens.append(op)
                    prev_token = 'OPERATOR'
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
                prev_token = 'LPAREN'
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
                prev_token = 'RPAREN'
            # Ignore whitespace
            pos = match.end()
        self._validate_tokens(tokens)
        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the list of tokens for balanced parentheses and valid syntax.

        Args:
            tokens (List[str]): List of tokens.

        Raises:
            ValueError: If parentheses are unbalanced or syntax is invalid.
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
            elif token in self.OPERATORS:
                if prev_token in self.OPERATORS or prev_token is None or prev_token == '(':
                    raise ValueError("Invalid operator placement.")
            prev_token = token
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: too many '('")

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts the list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        Args:
            tokens (List[str]): List of tokens.

        Returns:
            List[Union[str, float]]: RPN token list.
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
                    raise ValueError("Unbalanced parentheses.")
                stack.pop()  # Remove '('
        while stack:
            if stack[-1] in {'(', ')'}:
                raise ValueError("Unbalanced parentheses.")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates the RPN expression.

        Args:
            rpn (List[Union[str, float]]): RPN token list.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the expression is invalid.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero.")
                result = self.OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid syntax: too many operands.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if a token is a valid number.

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
    test_expressions = [
        "1 + 2 * 3",                # 7.0
        "(1 + 2) * 3",              # 9.0
        "-5 + 3 * (2 - 4.5)",       # -12.5
        "10 / 2 + 3 * 2",           # 11.0
        "((2.5 + 2.5) * 2) / 2",    # 5.0
        "-3.5 + (2 * -2)",          # -7.5
        "4 / (2 - 2)",              # Division by zero
        "2 + (3 * 4",               # Unbalanced parentheses
        "2 + 3 ** 2",               # Invalid character
        "2 + * 3",                  # Invalid operator placement
    ]

    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
