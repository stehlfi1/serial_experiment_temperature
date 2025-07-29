
import re
from typing import List, Union

class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, /, parentheses, integers, floats. 
    Evaluates expressions with correct operator precedence.
    """

    # Supported operators and their precedence
    _OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L'),
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression string and return the result as a float.

        Parameters:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            SyntaxError: If there are syntax errors (invalid characters, unbalanced parentheses).
            ZeroDivisionError: If division by zero occurs.
            ValueError: For malformed numbers or unknown errors.
        """
        tokens = self._tokenize(expression)
        self._validate_parentheses(tokens)
        rpn = self._to_rpn(tokens)
        return self._evaluate_rpn(rpn)

    def _tokenize(self, expr: str) -> List[str]:
        """
        Convert input string into a list of tokens: numbers, operators, parentheses.

        Supports negative numbers and floating-point numbers.

        Raises:
            SyntaxError: If invalid characters are found.
        """
        # Regex for tokenizing numbers, operators, and parentheses
        token_pattern = re.compile(
            r"""
                (?P<NUMBER>       # Integer or float (with optional leading sign)
                    (?<!\w)       # Not preceded by word character (for unary minus)
                    [+-]?         # Optional sign
                    (?:\d*\.\d+|\d+\.\d*|\d+)  # Float or integer
                    (?:[eE][+-]?\d+)?          # Optional exponent
                )
                |(?P<OP>[+\-*/])
                |(?P<LPAREN>\()
                |(?P<RPAREN>\))
                |(?P<SPACE>\s+)
                |(?P<INVALID>.)
            """,
            re.VERBOSE
        )

        tokens = []
        pos = 0
        while pos < len(expr):
            match = token_pattern.match(expr, pos)
            if not match:
                raise SyntaxError(f"Invalid syntax near '{expr[pos:]}'")
            if match.lastgroup == 'NUMBER':
                num = match.group('NUMBER')
                tokens.append(num)
            elif match.lastgroup == 'OP':
                tokens.append(match.group('OP'))
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
            elif match.lastgroup == 'SPACE':
                pass  # Ignore whitespace
            elif match.lastgroup == 'INVALID':
                raise SyntaxError(f"Invalid character: '{match.group('INVALID')}'")
            pos = match.end()
        return self._handle_unary_minus(tokens)

    def _handle_unary_minus(self, tokens: List[str]) -> List[str]:
        """
        Adjust token list so that unary minus is correctly interpreted as negative numbers.
        """
        result = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            # Detect unary minus: at start or after '(', operator
            if token == '-' and (i == 0 or tokens[i - 1] in ('(', '+', '-', '*', '/')):
                # Attach unary minus to the next number
                if i + 1 < len(tokens) and self._is_number(tokens[i + 1]):
                    result.append(str(-float(tokens[i + 1])))
                    i += 2
                    continue
                elif i + 1 < len(tokens) and tokens[i + 1] == '(':
                    # For cases like: - (3 + 2)
                    result.append('-1')
                    result.append('*')
                    i += 1
                    continue
                else:
                    raise SyntaxError("Invalid use of unary minus.")
            else:
                result.append(token)
            i += 1
        return result

    def _validate_parentheses(self, tokens: List[str]):
        """
        Ensure that parentheses are balanced.
        """
        balance = 0
        for token in tokens:
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
            if balance < 0:
                raise SyntaxError("Unbalanced parentheses: too many ')'")
        if balance != 0:
            raise SyntaxError("Unbalanced parentheses: too many '('")

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Convert tokens from infix to postfix (Reverse Polish Notation) using the shunting yard algorithm.

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
                if not stack:
                    raise SyntaxError("Unbalanced parentheses: missing '('")
                stack.pop()  # Remove '('
            else:
                raise SyntaxError(f"Unknown token: '{token}'")
        while stack:
            op = stack.pop()
            if op in ('(', ')'):
                raise SyntaxError("Unbalanced parentheses in expression.")
            output.append(op)
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluate an expression in Reverse Polish Notation.

        Returns:
            float: Result of evaluation.

        Raises:
            ZeroDivisionError: On division by zero.
            ValueError: On malformed expression.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Unknown token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Malformed expression: leftover items in stack.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """
        Apply arithmetic operator to two operands.
        """
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0.0:
                raise ZeroDivisionError("Division by zero.")
            return a / b
        else:
            raise ValueError(f"Unsupported operator '{op}'.")

    def _is_number(self, s: str) -> bool:
        """
        Determine if string s represents a number.
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    calc = Calculator()
    tests = [
        "1 + 2",
        "2 * (3 + 4)",
        "-5.2 + 3 * (2 - -7.0) / 4",
        "3 + 4 * 2 / (1 - 5)",
        "((1 + 2)) * (3 - 4) / -7.5",
        "-(2 + 3)",
        "2 + -3",
        "6 / 0",  # Should raise ZeroDivisionError
        "3 + (4", # Should raise SyntaxError
        "1 + 2a", # Should raise SyntaxError
    ]

    for expr in tests:
        print(f"Expression: {expr}")
        try:
            result = calc.calculate(expr)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
