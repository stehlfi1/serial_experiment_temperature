
import re
from typing import List, Union


class Calculator:
    """
    A console-based arithmetic calculator that supports +, -, *, /, parentheses,
    and both integers and floating-point numbers (including negatives).
    Follows ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence/associativity
    _OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses, invalid characters).
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List[str]:
        """
        Converts the input expression string into a list of tokens.

        Args:
            expr (str): The input arithmetic expression.

        Returns:
            List[str]: List of tokens.

        Raises:
            ValueError: If invalid characters are found or parentheses are unbalanced.
        """
        # Remove all whitespace
        expr = expr.replace(' ', '')

        # Validate and tokenize using regex
        token_pattern = re.compile(
            r"""
            (?P<NUMBER>    -?\d+(?:\.\d+)? ) |   # Integer or float, possibly negative
            (?P<LPAREN>    \( )             |   # Left parenthesis
            (?P<RPAREN>    \) )             |   # Right parenthesis
            (?P<OP>        [+\-*/] )            # Operators
            """,
            re.VERBOSE,
        )

        tokens = []
        i = 0
        length = len(expr)
        while i < length:
            match = token_pattern.match(expr, i)
            if not match:
                raise ValueError(f"Invalid character at position {i}: '{expr[i]}'")
            token = match.group()
            if token in self._OPERATORS or token in ('(', ')'):
                # Handle unary minus: If '-' is at start or after '(', or another operator, treat as unary
                if token == '-' and (i == 0 or expr[i-1] in "(+*/-"):
                    # Next token must be a number or left paren for negative value/group
                    next_match = token_pattern.match(expr, i + 1)
                    if not next_match or not (next_match.group('NUMBER') or next_match.group('LPAREN')):
                        raise ValueError("Invalid use of unary minus")
                    # Attach minus to number if possible
                    if next_match.group('NUMBER'):
                        tokens.append('-' + next_match.group('NUMBER'))
                        i = next_match.end()
                        continue
                    else:
                        # Negative group, e.g., '-(2+3)'
                        tokens.append('-1')
                        tokens.append('*')
                        i += 1  # move to '('
                        continue
                tokens.append(token)
            elif match.group('NUMBER'):
                tokens.append(token)
            else:
                raise ValueError(f"Invalid token: '{token}'")
            i = match.end()

        # Check for balanced parentheses
        if tokens.count('(') != tokens.count(')'):
            raise ValueError("Unbalanced parentheses in expression")

        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts a list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        Args:
            tokens (List[str]): List of tokens in infix notation.

        Returns:
            List[Union[str, float]]: List of tokens in RPN.

        Raises:
            ValueError: If parentheses are unbalanced or token sequence is invalid.
        """
        output = []
        op_stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in self._OPERATORS:
                while (
                    op_stack
                    and op_stack[-1] in self._OPERATORS
                    and (
                        (self._OPERATORS[token]['associativity'] == 'L' and
                         self._OPERATORS[token]['precedence'] <= self._OPERATORS[op_stack[-1]]['precedence'])
                        or
                        (self._OPERATORS[token]['associativity'] == 'R' and
                         self._OPERATORS[token]['precedence'] < self._OPERATORS[op_stack[-1]]['precedence'])
                    )
                ):
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    output.append(op_stack.pop())
                if not op_stack or op_stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses in expression")
                op_stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token: {token}")
        while op_stack:
            if op_stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses in expression")
            output.append(op_stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates an RPN (Reverse Polish Notation) expression.

        Args:
            rpn (List[Union[str, float]]): The RPN expression.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the RPN sequence is invalid.
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
                raise ValueError(f"Unknown RPN token: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if a token is a valid number.

        Args:
            token (str): The token string.

        Returns:
            bool: True if token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    @staticmethod
    def _apply_operator(a: float, b: float, op: str) -> float:
        """
        Applies an arithmetic operator to two operands.

        Args:
            a (float): Left operand.
            b (float): Right operand.
            op (str): Operator ('+', '-', '*', '/').

        Returns:
            float: Result of operation.

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
            raise ValueError(f"Unsupported operator: {op}")


if __name__ == "__main__":
    # Example usage and test cases
    calc = Calculator()
    test_cases = [
        ("1 + 2", 3.0),
        ("2 * (3 + 4)", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * (4 + 5)", 45.0),
        ("-2 + 3", 1.0),
        ("2 + -3", -1.0),
        ("-2 * -3", 6.0),
        ("-2 * (3 + 4)", -14.0),
        ("4 / 2", 2.0),
        ("7 / 2", 3.5),
        ("-7 / 2", -3.5),
        ("3.5 + 2.1", 5.6),
        ("-(2 + 3)", -5.0),
        ("-(-2)", 2.0),
        ("2 * -3 + 4", -2.0),
        ("2 * (-3 + 4)", 2.0),
        ("2 * (3 + -4)", -2.0),
        ("(2 + 3) * (4 - 2) / 2", 5.0),
    ]

    for expr, expected in test_cases:
        try:
            result = calc.calculate(expr)
            assert abs(result - expected) < 1e-9, f"Test failed: {expr} = {result}, expected {expected}"
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr}': {e}")
