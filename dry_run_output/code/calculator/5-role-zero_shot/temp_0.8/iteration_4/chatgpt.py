
from typing import List, Union
import re

class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, / and parentheses.
    Evaluates string expressions with correct precedence and supports both integers
    and floating-point numbers (including negatives).
    """

    # Allowed operators and their precedences
    _OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    # Regular expression for tokenizing the input
    _TOKEN_REGEX = re.compile(
        r'\s*('
        r'\d+\.\d+|\d+\.\d*|\.\d+|'            # Floating point numbers
        r'\d+|'                                # Integers
        r'[+\-*/()]'                           # Operators and parentheses
        r')\s*'
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression provided as a string.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The evaluated result.

        Raises:
            SyntaxError: On invalid syntax (unbalanced parentheses, invalid characters).
            ZeroDivisionError: If division by zero occurs.
            ValueError: On other invalid input.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._eval_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Parses the input expression into tokens.

        Args:
            expression (str): The string expression.

        Returns:
            List[str]: List of tokens.

        Raises:
            SyntaxError: On invalid or unexpected characters.
        """
        tokens = []
        pos = 0
        while pos < len(expression):
            match = self._TOKEN_REGEX.match(expression, pos)
            if not match:
                raise SyntaxError(f"Invalid character in input at position {pos}: '{expression[pos]}'")
            token = match.group(1)
            tokens.append(token)
            pos = match.end()
        
        # Handle unary minus
        tokens = self._handle_unary_minus(tokens)
        return tokens

    def _handle_unary_minus(self, tokens: List[str]) -> List[str]:
        """
        Processes the tokens to handle unary minus (negative numbers).

        Args:
            tokens (List[str]): List of tokens.

        Returns:
            List[str]: Updated token list with unary minus handled.
        """
        result = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '-' and (
                i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('
            ):
                # It's a unary minus
                # Merge with next number (must exist and be a number)
                if i+1 < len(tokens) and self._is_number(tokens[i+1]):
                    result.append(str(-float(tokens[i+1])))
                    i += 2
                    continue
                else:
                    raise SyntaxError("Invalid placement of unary minus or missing number after '-'")
            else:
                result.append(token)
            i += 1
        return result

    def _is_number(self, token: str) -> bool:
        """Checks if token is a number."""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts list of tokens from infix to postfix (RPN) using the shunting yard algorithm.

        Args:
            tokens (List[str]): List of tokens.

        Returns:
            List[Union[str, float]]: RPN expression.

        Raises:
            SyntaxError: On unbalanced parentheses or invalid syntax.
        """
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
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
                if not stack:
                    raise SyntaxError("Unbalanced parentheses: missing '('")
                stack.pop()  # Remove '('
            else:
                raise SyntaxError(f"Unknown token: {token}")

        while stack:
            if stack[-1] == '(' or stack[-1] == ')':
                raise SyntaxError("Unbalanced parentheses: missing ')' or '('")
            output.append(stack.pop())
        return output

    def _eval_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (postfix).

        Args:
            rpn (List[Union[str, float]]): RPN tokens.

        Returns:
            float: Evaluation result.

        Raises:
            ZeroDivisionError: On division by zero.
            ValueError: On syntax errors.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator '{}'".format(token))
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = self._OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: leftover operands on stack")
        return stack[0]


# Example usage and test cases (can be placed under if __name__ == '__main__' for testability)
if __name__ == '__main__':
    calc = Calculator()
    expressions = [
        "2 + 3 * 4",                       # 14
        "10 / 2 + 3",                      # 8
        "10 / (2 + 3)",                    # 2
        "(2 + 3) * 4",                     # 20
        "-5 + 2",                          # -3
        "3 + -2 * 5",                      # -7
        "-3.5 * (2 + 1)",                  # -10.5
        "3.5 + 2.5",                       # 6.0
        "10 / 0.5",                        # 20.0
        "((3))",                           # 3
        "2 + (3 * (4 - 1))",               # 11
        "-(3 + 2)",                        # -5
        "4 / 2 * (1 + 1)",                 # 4.0
    ]
    for expr in expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
