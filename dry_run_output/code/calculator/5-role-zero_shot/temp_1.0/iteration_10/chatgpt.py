
from typing import List, Union

class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, /, and parentheses.
    Input: arithmetic expression as a string (supports negative numbers, floats, ints).
    Output: float result.
    """

    # Define supported operators and their precedence/associativity
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'}
    }
    PARENTHESES = {'(', ')'}
    VALID_CHARS = set('0123456789.+-*/() ')

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.
        :param expression: str, the arithmetic expression to evaluate
        :return: float, the evaluation result
        :raises ValueError: if the expression contains invalid input or parentheses are unbalanced
        :raises ZeroDivisionError: if division by zero occurs
        """
        tokens = self._tokenize(expression)
        rpn = self._infix_to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).
        Handles negative numbers and validates characters.
        :param expression: str
        :return: list of tokens (numbers as float, operators as str)
        :raises ValueError: for invalid characters or malformed numbers
        """
        if not expression or not any(char.strip() for char in expression):
            raise ValueError("Input is empty or blank.")

        # Check for invalid characters
        for char in expression:
            if char not in self.VALID_CHARS:
                raise ValueError(f"Invalid character: '{char}'")

        tokens = []
        i = 0
        n = len(expression)

        while i < n:
            char = expression[i]

            # Skip whitespace
            if char.isspace():
                i += 1
                continue

            # Number token (integer or float, possibly negative)
            if char.isdigit() or (char == '.' and i + 1 < n and expression[i+1].isdigit()) or \
                (char in '+-' and (i == 0 or (tokens and tokens[-1] in self.OPERATORS or tokens[-1] == '('))):

                # Handle sign
                sign = 1
                if char == '+':
                    i += 1
                    if i < n and not expression[i].isdigit() and expression[i] != '.':
                        # Standalone '+', not a sign
                        tokens.append('+')
                        continue
                elif char == '-':
                    sign = -1
                    i += 1
                    if i < n and not expression[i].isdigit() and expression[i] != '.':
                        # Standalone '-', not a sign
                        tokens.append('-')
                        continue

                # Parse number part
                num_str = ''
                decimal_found = False
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        if decimal_found:
                            raise ValueError("Malformed number: multiple decimal points")
                        decimal_found = True
                    num_str += expression[i]
                    i += 1
                if not num_str or num_str == '.':
                    raise ValueError(f"Malformed number at position {i-len(num_str)}")
                number = float(num_str) * sign
                tokens.append(number)
                continue

            # Operator or Parenthesis
            elif char in self.OPERATORS or char in self.PARENTHESES:
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character: '{char}'")
        return tokens

    def _infix_to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts an infix token list to Reverse Polish Notation (RPN) using the shunting yard algorithm.
        :param tokens: list of tokens (output from _tokenize)
        :return: list in RPN order
        :raises ValueError: for unbalanced parentheses or invalid token sequence
        """
        output = []
        stack = []
        parentheses_balance = 0

        for idx, token in enumerate(tokens):
            if isinstance(token, float):
                output.append(token)
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                       ((self.OPERATORS[token]['associativity'] == 'L' and
                         self.OPERATORS[token]['precedence'] <= self.OPERATORS[stack[-1]]['precedence']) or
                        (self.OPERATORS[token]['associativity'] == 'R' and
                         self.OPERATORS[token]['precedence'] < self.OPERATORS[stack[-1]]['precedence']))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
                parentheses_balance += 1
            elif token == ')':
                parentheses_balance -= 1
                if parentheses_balance < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses: no matching '('")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Invalid token in expression: {token}")

        if parentheses_balance > 0:
            raise ValueError("Unbalanced parentheses: too many '('")

        while stack:
            op = stack.pop()
            if op in self.PARENTHESES:
                raise ValueError("Unbalanced parentheses in expression")
            output.append(op)
        return output

    def _evaluate_rpn(self, rpn_tokens: List[Union[str, float]]) -> float:
        """
        Evaluates an expression given in Reverse Polish Notation.
        :param rpn_tokens: list in RPN order
        :return: float result
        :raises ValueError: on incorrect RPN sequence
        :raises ZeroDivisionError: on division by zero
        """
        stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid RPN token: {token}")

        if len(stack) != 1:
            raise ValueError("Malformed expression: too many operands")

        return float(stack[0])

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """
        Applies an arithmetic operator to operands a and b.
        :param a: float
        :param b: float
        :param op: str operator (+, -, *, /)
        :return: float result
        :raises ZeroDivisionError: on division by zero
        :raises ValueError: on unknown operator
        """
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0.0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {op}")

if __name__ == "__main__":
    """Basic test cases for demonstration and testability."""

    def format_test(expr, expected=None):
        try:
            calc = Calculator()
            result = calc.calculate(expr)
            print(f"Expr: {expr!r:25s} Result: {result}")
            if expected is not None:
                assert abs(result - expected) < 1e-9, f"Expected {expected}, got {result}"
        except Exception as e:
            print(f"Expr: {expr!r:25s} Error: {e}")

    # Valid expressions
    format_test("1 + 2 * 3", 7)
    format_test("(1 + 2) * 3", 9)
    format_test("3 + 4 * 2 / (1 - 5)", 1)
    format_test("3.5 + -2.2 * (1.7 - 0.2) / 3", 2.41)
    format_test("-(2 + 3) * 4", -20)
    format_test("--3 + 5", 8)
    format_test("0.5 * (3 - 2.5)", 0.25)

    # Error handling
    format_test("2 + * 3")
    format_test("(1 + 2", None)
    format_test("3 / 0")
    format_test("abc + 3")
    format_test("")
