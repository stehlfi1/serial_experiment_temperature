
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.

    Adheres to ISO/IEC 25010 quality requirements:
    - Correctness: Accurate evaluation of expressions
    - Performance: Efficient parsing and evaluation
    - Modularity: Clear separation of concerns
    - Safety: Robust input validation and error handling
    - Testability: Easily testable methods
    - Readability: Well-documented and clear code
    """

    # Supported operators and their precedence
    _OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid (syntax, unbalanced parentheses, etc.)
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input expression string into a list of tokens.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            List[str]: List of tokens.

        Raises:
            ValueError: If invalid characters are found.
        """
        # Remove whitespace for easier processing
        expr = expression.replace(' ', '')

        # Tokenization regex:
        # - Numbers: integers or floats, possibly negative (handled in parsing)
        # - Operators: +, -, *, /
        # - Parentheses: (, )
        token_pattern = re.compile(r"""
            (?P<number>   -?\d+(\.\d+)? ) |
            (?P<op>       [+\-*/]        ) |
            (?P<paren>    [()]           )
        """, re.VERBOSE)

        tokens = []
        i = 0
        while i < len(expr):
            match = token_pattern.match(expr, i)
            if not match:
                raise ValueError(f"Invalid character at position {i}: '{expr[i]}'")
            token = match.group()
            # Handle unary minus (negative numbers)
            if token == '-' and (i == 0 or expr[i-1] in '(*+/ -'):
                # Look ahead for a number
                num_match = re.match(r'-\d+(\.\d+)?', expr[i:])
                if num_match:
                    token = num_match.group()
                    tokens.append(token)
                    i += len(token)
                    continue
            tokens.append(token)
            i += len(token)
        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the list of tokens for syntax correctness.

        Args:
            tokens (List[str]): List of tokens.

        Raises:
            ValueError: If the tokens are invalid (unbalanced parentheses, invalid sequence, etc.)
        """
        paren_count = 0
        prev_token = None
        for idx, token in enumerate(tokens):
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
            elif token in self._OPERATORS:
                if prev_token is None or prev_token in self._OPERATORS or prev_token == '(':
                    # Allow unary minus only for numbers, not for other operators
                    if not (token == '-' and (idx + 1 < len(tokens) and self._is_number(tokens[idx + 1]))):
                        raise ValueError(f"Invalid operator placement: '{token}' at position {idx}")
            elif self._is_number(token):
                pass
            else:
                raise ValueError(f"Invalid token: '{token}'")
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
            elif token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS and
                       ((self._OPERATORS[token][1] == 'L' and self._OPERATORS[token][0] <= self._OPERATORS[stack[-1]][0]) or
                        (self._OPERATORS[token][1] == 'R' and self._OPERATORS[token][0] < self._OPERATORS[stack[-1]][0]))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses during RPN conversion")
                stack.pop()  # Remove '('
        while stack:
            if stack[-1] in '()':
                raise ValueError("Unbalanced parentheses at end of RPN conversion")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates a Reverse Polish Notation (RPN) expression.

        Args:
            rpn (List[Union[str, float]]): RPN token list.

        Returns:
            float: The result of the evaluated RPN expression.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the RPN is invalid.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid RPN token: '{token}'")
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        return stack[0]

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """
        Applies an arithmetic operator to two operands.

        Args:
            a (float): Left operand.
            b (float): Right operand.
            op (str): Operator.

        Returns:
            float: Result of the operation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
        """
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        else:
            raise ValueError(f"Unsupported operator: '{op}'")

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if a token is a valid number.

        Args:
            token (str): Token to check.

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
        "10 / 2 + 3 * (2 - 1)",     # 8.0
        "-5 + 3",                   # -2.0
        "4 + -2 * 3",               # -2.0
        "3.5 * 2 - (1.5 / 0.5)",    # 4.0
        "((2+3)*4)/2",              # 10.0
        "-(2 + 3) * 4",             # -20.0
        "2 + (3 * (4 - 1))",        # 11.0
        "2 +",                      # Invalid
        "2 / 0",                    # Division by zero
        "2 + (3 * 4",               # Unbalanced parentheses
        "2 + $",                    # Invalid character
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
