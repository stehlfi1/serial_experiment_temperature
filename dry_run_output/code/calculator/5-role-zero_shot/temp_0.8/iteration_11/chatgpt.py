
from typing import List, Union
import re

class CalculatorError(Exception):
    """Base class for calculator exceptions."""
    pass

class InvalidExpressionError(CalculatorError, ValueError):
    """Raised when the expression syntax is invalid."""
    pass

class DivisionByZeroError(CalculatorError, ZeroDivisionError):
    """Raised when division by zero occurs."""
    pass

class Calculator:
    """
    A class-based, maintainable arithmetic calculator that parses
    and evaluates mathematical expressions safely and efficiently.

    Supported features:
        - Basic arithmetic operations: +, -, *, /
        - Operator precedence and parentheses
        - Integer and floating point numbers (including negatives)
        - Input validation (balanced parentheses, invalid characters, division by zero)

    Example:
        calc = Calculator()
        result = calc.calculate('(2.5 + -3) * 4/5')
    """

    # Supported operators: (precedence, associativity, function)
    OPERATORS = {
        '+': (1, 'L', lambda a, b: a + b),
        '-': (1, 'L', lambda a, b: a - b),
        '*': (2, 'L', lambda a, b: a * b),
        '/': (2, 'L', lambda a, b: Calculator._div(a, b)),
    }
    # Allowed characters in input
    VALID_CHARS = set("0123456789.+-*/() ")

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression string and returns the result.

        :param expression: The arithmetic expression (e.g. "(1+2.5) * 3/4")
        :return: The result as a float
        :raises CalculatorError: If a parsing or arithmetic error occurs
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    @staticmethod
    def _div(a: float, b: float) -> float:
        """Division with explicit zero check."""
        if b == 0:
            raise DivisionByZeroError("Division by zero")
        return a / b

    def _tokenize(self, expr: str) -> List[Union[str, float]]:
        """
        Parse the expression into tokens (float numbers, operators, parentheses).
        Handles negative numbers.

        :param expr: Expression string
        :return: List of tokens
        :raises InvalidExpressionError: On invalid characters or syntax
        """
        if not isinstance(expr, str):
            raise InvalidExpressionError("Expression must be a string.")
        expr = expr.strip()
        if not expr:
            raise InvalidExpressionError("Empty expression.")

        # Validation: Only allowed characters
        if not all(c in self.VALID_CHARS for c in expr):
            raise InvalidExpressionError("Invalid character(s) detected.")

        # Tokenization REGEX:
        token_pattern = re.compile(r"""
            (?P<number>
                (?<!\w)
                (?:-)?                # Optional negative sign (not after a word)
                (?:\d+(\.\d*)?|\.\d+) # Integer or decimal number
                (?![\w.])
            )
            |(?P<lparen>\()
            |(?P<rparen>\))
            |(?P<op>[+\-*/])
        """, re.VERBOSE)

        tokens = []
        pos = 0
        prev_token = None  # Track previous to distinguish unary minus

        while pos < len(expr):
            m = token_pattern.match(expr, pos)
            if not m:
                if expr[pos].isspace():
                    pos += 1
                    continue
                raise InvalidExpressionError(f"Unexpected token at position {pos}: '{expr[pos]}'")
            token = m.group()
            if m.lastgroup == 'number':
                try:
                    tokens.append(float(token))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number at position {pos}")
                prev_token = 'number'
            elif m.lastgroup == 'lparen':
                tokens.append('(')
                prev_token = '('
            elif m.lastgroup == 'rparen':
                tokens.append(')')
                prev_token = ')'
            elif m.lastgroup == 'op':
                # Disambiguate unary minus: if at start or after "(", or after another operator
                if token == '-' and (prev_token in (None, '(', 'op')):
                    # Try to parse as unary minus followed by a number (e.g. -5)
                    num_match = re.match(r'-((\d+(\.\d*)?)|\.\d+)', expr[m.start():])
                    if num_match:
                        number = float(num_match.group())
                        tokens.append(number)
                        pos += len(num_match.group()) - 1  # -1 since pos will be incremented after this
                        prev_token = 'number'
                    else:
                        tokens.append('-')
                        prev_token = 'op'
                else:
                    tokens.append(token)
                    prev_token = 'op'
            pos = m.end()
        # Validation: balanced parentheses and other checks
        self._validate_tokens(tokens)
        return tokens

    def _validate_tokens(self, tokens: List[Union[str, float]]):
        """
        Perform various syntactic validations (balanced parentheses, operator placement, etc.)

        :param tokens: List of tokens from _tokenize
        :raises InvalidExpressionError: On syntax errors
        """
        paren_count = 0
        last_tok = None
        for tok in tokens:
            if tok == '(':
                paren_count += 1
            elif tok == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError("Unbalanced parentheses: too many ')'")
            elif isinstance(tok, str) and tok in self.OPERATORS:
                if last_tok is None or (isinstance(last_tok, str) and last_tok in self.OPERATORS and last_tok != ')'):
                    raise InvalidExpressionError("Operator misplacement.")
            last_tok = tok
        if paren_count != 0:
            raise InvalidExpressionError("Unbalanced parentheses.")

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Transform tokens from infix to RPN using the shunting yard algorithm.

        :param tokens: Token list
        :return: RPN token list
        """
        output: List[Union[str, float]] = []
        op_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self.OPERATORS:
                while (op_stack and op_stack[-1] in self.OPERATORS):
                    cur_prec, cur_assoc, _ = self.OPERATORS[token]
                    stack_prec, _, _ = self.OPERATORS[op_stack[-1]]
                    if (cur_assoc == 'L' and cur_prec <= stack_prec) or \
                       (cur_assoc == 'R' and cur_prec < stack_prec):
                        output.append(op_stack.pop())
                    else:
                        break
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    output.append(op_stack.pop())
                if not op_stack or op_stack[-1] != '(':
                    raise InvalidExpressionError("Unbalanced parentheses.")
                op_stack.pop()
            else:
                raise InvalidExpressionError("Invalid token encountered in parsing.")

        while op_stack:
            top = op_stack.pop()
            if top in ('(', ')'):
                raise InvalidExpressionError("Unbalanced parentheses in expression.")
            output.append(top)

        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluate the RPN representation of the expression.

        :param rpn: RPN token list
        :return: Evaluation result
        :raises CalculatorError: On invalid tokens or division by zero
        """
        stack: List[float] = []

        for tok in rpn:
            if isinstance(tok, float):
                stack.append(tok)
            elif tok in self.OPERATORS:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operator")
                b = stack.pop()
                a = stack.pop()
                try:
                    result = self.OPERATORS[tok][2](a, b)
                except ZeroDivisionError:
                    raise DivisionByZeroError("Division by zero")
                stack.append(result)
            else:
                raise InvalidExpressionError(f"Invalid token '{tok}' during evaluation")

        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression: too many operands")

        return stack[0]

# Example usage and test cases:

if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        # (expression, expected)
        ("1 + 2", 3),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("(3.5-2.5)*4", 4.0),
        ("-4 + 2", -2),
        ("--4", 4),
        ("-(2 + 3)", -5),
        ("(2.5 + -3) * 4/5", -0.4),
        ("-3.14", -3.14),
        ("2/0", DivisionByZeroError),
        ("2+(3", InvalidExpressionError),
        ("", InvalidExpressionError),
        ("1 + ab", InvalidExpressionError),
    ]

    for expr, expected in test_cases:
        try:
            result = calc.calculate(expr)
            if isinstance(expected, type) and issubclass(expected, Exception):
                print(f"FAIL: '{expr}' expected error but got result {result}")
            else:
                assert abs(result - expected) < 1e-8
                print(f"PASS: '{expr}' = {result}")
        except Exception as e:
            if isinstance(expected, type) and isinstance(e, expected):
                print(f"PASS: '{expr}' raised expected exception {e.__class__.__name__}")
            else:
                print(f"FAIL: '{expr}' unexpected exception {e.__class__.__name__}: {e}")
