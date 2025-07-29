
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.
    Adheres to ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence
    _OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'},
    }

    # Allowed characters in the expression (digits, operators, parentheses, dot, whitespace)
    _VALID_CHAR_PATTERN = re.compile(r'^[\d\s+\-*/().]+$')

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
        self._validate_tokens(tokens)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            List[str]: List of tokens.

        Raises:
            ValueError: If invalid characters are found.
        """
        expr = expression.replace(' ', '')  # Remove whitespace

        if not expr:
            raise ValueError("Empty expression.")

        if not self._VALID_CHAR_PATTERN.match(expr):
            raise ValueError("Expression contains invalid characters.")

        # Tokenization regex: numbers (including floats), operators, parentheses
        token_pattern = re.compile(r"""
            (?P<number>   -?\d+(\.\d+)? ) |   # Integer or float (possibly negative)
            (?P<op>       [+\-*/]       ) |   # Operators
            (?P<paren>    [()]          )     # Parentheses
        """, re.VERBOSE)

        tokens = []
        i = 0
        length = len(expr)
        while i < length:
            match = token_pattern.match(expr, i)
            if not match:
                raise ValueError(f"Invalid token at position {i}: '{expr[i]}'")

            token = match.group()
            # Handle unary minus (negative numbers)
            if token == '-' and (
                i == 0 or expr[i-1] in '(*+/ -'
            ):
                # Look ahead for a number
                num_match = re.match(r'-\d+(\.\d+)?', expr[i:])
                if num_match:
                    token = num_match.group()
                    tokens.append(token)
                    i += len(token)
                    continue
                else:
                    raise ValueError(f"Invalid negative number at position {i}")
            else:
                tokens.append(token)
                i += len(token)
        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the list of tokens for balanced parentheses and correct syntax.

        Args:
            tokens (List[str]): List of tokens.

        Raises:
            ValueError: If parentheses are unbalanced or syntax is invalid.
        """
        paren_count = 0
        prev_token = None
        for idx, token in enumerate(tokens):
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'.")
            elif token in self._OPERATORS:
                if prev_token is None or prev_token in self._OPERATORS or prev_token == '(':
                    # Only allow unary minus, which is handled in tokenization
                    if token != '-':
                        raise ValueError(f"Operator '{token}' at invalid position.")
            prev_token = token

        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: too many '('.")

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

        Args:
            tokens (List[str]): List of tokens in infix notation.

        Returns:
            List[Union[str, float]]: Tokens in RPN.

        Raises:
            ValueError: If syntax errors are detected.
        """
        output = []
        stack = []

        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS and
                       ((self._OPERATORS[token]['associativity'] == 'L' and
                         self._OPERATORS[token]['precedence'] <= self._OPERATORS[stack[-1]]['precedence']) or
                        (self._OPERATORS[token]['associativity'] == 'R' and
                         self._OPERATORS[token]['precedence'] < self._OPERATORS[stack[-1]]['precedence']))):
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
                raise ValueError(f"Unknown token: {token}")

        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Mismatched parentheses.")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, rpn_tokens: List[Union[str, float]]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation.

        Args:
            rpn_tokens (List[Union[str, float]]): Tokens in RPN.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the expression is invalid.
        """
        stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid RPN token: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operator to two operands.

        Args:
            a (float): Left operand.
            b (float): Right operand.
            operator (str): Operator symbol.

        Returns:
            float: Result of the operation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero.")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {operator}")

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
        "10 / 2 + 3 * (2 - 1)",     # 8.0
        "-5 + 3",                   # -2.0
        "4 + -2 * 3",               # -2.0
        "3.5 * 2 - (1.5 / -3)",     # 7.5 + 0.5 = 8.0
        "((2+3)*4.5) / -1.5",       # (5*4.5)/-1.5 = 22.5/-1.5 = -15.0
        "1 / (2 - 2)",              # Division by zero
        "2 + (3 * (4 - 1)",         # Unbalanced parentheses
        "2 + 3a",                   # Invalid character
        "",                         # Empty expression
    ]

    for expr in test_expressions:
        print(f"Expression: {expr}")
        try:
            result = calc.calculate(expr)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")
