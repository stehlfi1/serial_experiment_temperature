
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting addition, subtraction,
    multiplication, division, and parentheses (with correct precedence).
    Conforms to ISO/IEC 25010 requirements for reliability, safety, 
    maintainability, and usability.
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
        Evaluates the arithmetic expression provided as a string.
        Args:
            expression (str): The arithmetic expression to evaluate.
        Returns:
            float: The result of the evaluation.
        Raises:
            ValueError: For invalid input, such as invalid characters,
                        unbalanced parentheses, or division by zero.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._to_rpn(tokens)
        return self._eval_rpn(rpn)

    def _tokenize(self, expr: str) -> List[str]:
        """
        Tokenizes the input expression into numbers, operators, and parentheses.
        Handles negative numbers appropriately.
        Raises ValueError for unexpected characters.
        """
        # Remove all whitespace for easier parsing
        expr = expr.replace(' ', '')
        if not expr:
            raise ValueError("Empty expression.")

        # Regex pattern for tokenizing numbers (integers/floats), operators, and parentheses
        token_pattern = re.compile(r'(\d+\.\d+|\d+|[+\-*/()]|\.\d+)')
        tokens_raw = token_pattern.findall(expr)
        tokens = []

        idx = 0
        while idx < len(tokens_raw):
            token = tokens_raw[idx]
            
            # Handle negative numbers
            if token == '-' and (
                idx == 0 or tokens_raw[idx - 1] in ('(', '+', '-', '*', '/')
            ):
                # Attach to number after
                if idx + 1 < len(tokens_raw) and re.match(r'^(\d+\.\d+|\d+|\.\d+)$', tokens_raw[idx + 1]):
                    tokens.append(token + tokens_raw[idx + 1])
                    idx += 2
                    continue
                else:
                    raise ValueError("Invalid negative value in expression.")
            tokens.append(token)
            idx += 1

        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the syntax of expression tokens.
        Checks for invalid characters and balanced parentheses.
        Raises ValueError for invalid input.
        """
        valid_tokens = set(self._OPERATORS.keys()) | {'(', ')'}
        paren_count = 0

        prev_token = None
        for token in tokens:
            # Validate numbers and legal tokens
            if token not in valid_tokens:
                try:
                    float(token)
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many closing ')'.")
            prev_token = token
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: too many opening '('.")

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts a list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.
        Returns:
            List in RPN order.
        """
        output: List[Union[str, float]] = []
        stack: List[str] = []
        for token in tokens:
            if token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS and
                       self._OPERATORS[stack[-1]][0] >= self._OPERATORS[token][0]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Unbalanced parentheses: missing opening '('.")
                stack.pop()  # Remove '('
            else:
                # Numbers
                try:
                    output.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid number: {token}")

        while stack:
            if stack[-1] in '()':
                raise ValueError("Unbalanced parentheses at end of expression.")
            output.append(stack.pop())

        return output

    def _eval_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation.
        Returns:
            float: The evaluation result.
        Raises:
            ValueError: On division by zero or malformed expressions.
        """
        stack: List[float] = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                # Division by zero check
                if token == '/' and b == 0:
                    raise ValueError("Division by zero.")
                result = self._OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Unexpected token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Malformed expression: leftover operands.")
        return stack[0]


if __name__ == "__main__":
    # Basic manual tests
    calc = Calculator()
    test_expressions = [
        "2 + 3 * 4",
        "5 - (6 / 3)",
        "-7 + 2",
        "3.5 * 2",
        "((2 - 3.5) * 4.1) / -2",
        "3 + (4 * 2 - 1) / (1 + 1)",
        "-2.5 * -2.0",
        "2 * (3 + )",                   # Invalid: syntax error
        "3 / 0",                        # Division by zero
        "2 + 4 *",                      # Invalid: syntax error
        "2 + (3 - 1",                   # Unbalanced parentheses
        "bad + 3",                      # Invalid character
    ]

    for expr in test_expressions:
        print(f"Expression: {expr}")
        try:
            result = calc.calculate(expr)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        print('-' * 40)
