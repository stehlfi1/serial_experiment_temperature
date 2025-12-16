
import re
from typing import List, Union

class Calculator:
    """
    Console-based arithmetic calculator adhering to ISO/IEC 25010 requirements.
    Supports +, -, *, /, parentheses, negative numbers, and floats.
    """

    # Supported operators and their precedence
    OPERATORS = {
        '+': (1, 'left'),
        '-': (1, 'left'),
        '*': (2, 'left'),
        '/': (2, 'left')
    }
    
    # Regular expression patterns for tokenizing
    TOKEN_REGEX = re.compile(
        r'''
        (?P<number>       # Integer or float (with optional negative sign)
            -?(?:\d+\.\d*|\.\d+|\d+)
        )
        |(?P<paren>[\(\)])
        |(?P<operator>[\+\-\*/])
        |(?P<ws>\s+)
        |(?P<invalid>.)
        ''', re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression string.

        Args:
            expression (str): Expression to evaluate.

        Returns:
            float: Result of the evaluation.

        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero is attempted.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List[str]:
        """
        Tokenizes the input expression string.

        Returns:
            List[str]: List of tokens.

        Raises:
            ValueError: For invalid characters or malformed numbers.
        """
        tokens = []
        position = 0
        last_token = None
        while position < len(expr):
            match = self.TOKEN_REGEX.match(expr, position)
            if not match:
                raise ValueError(f"Invalid syntax at position {position} in expression.")
            if match.group('ws'):
                # Skip whitespace
                position = match.end()
                continue
            elif match.group('number'):
                num_str = match.group('number')
                # Prevent -- (double negative) or 5- -3 (which is valid)
                # Handle unary minus: only accept - as part of number if
                #   (this is at the start) or
                #   (after an operator or '(')
                if num_str.startswith('-'):
                    # Only permit unary minus if last token is None, operator, or left paren
                    if (last_token is not None and 
                        (last_token not in self.OPERATORS and last_token != '(')):
                        raise ValueError(f"Invalid syntax: misplaced unary minus at {position}.")
                tokens.append(num_str)
                last_token = num_str
            elif match.group('operator'):
                op = match.group('operator')
                # Disallow operator at start (except minus allowed for negative number, which is handled above)
                if last_token is None and op != '-':
                    raise ValueError(f"Expression cannot start with operator '{op}'.")
                # Disallow two operators in sequence (except minus, if directly followed by a number, allowed as unary minus)
                if last_token in self.OPERATORS and op != '-':
                    raise ValueError(f"Invalid sequence: two operators together at position {position}.")
                tokens.append(op)
                last_token = op
            elif match.group('paren'):
                tokens.append(match.group('paren'))
                last_token = match.group('paren')
            elif match.group('invalid'):
                raise ValueError(f"Invalid character '{match.group('invalid')}' in expression.")
            position = match.end()
        # Additional validation: no ending with operator (except after a closing parenthesis)
        if tokens and tokens[-1] in self.OPERATORS:
            raise ValueError("Expression cannot end with an operator.")
        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts infix tokens to Reverse Polish Notation using shunting yard algorithm.

        Args:
            tokens (List[str]): List of tokens.

        Returns:
            List[Union[str, float]]: RPN tokens.

        Raises:
            ValueError: For unbalanced parentheses or invalid sequence.
        """
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS):
                    curr_prec, curr_assoc = self.OPERATORS[token]
                    top_prec, _ = self.OPERATORS[stack[-1]]
                    if (curr_assoc == 'left' and curr_prec <= top_prec) or \
                       (curr_assoc == 'right' and curr_prec < top_prec):
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Unbalanced parentheses: missing '('")
                stack.pop()  # Remove '('
            else:
                # Should not get here
                raise ValueError(f"Unknown token '{token}' encountered.")
        # Empty remaining stack
        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses: unused parenthesis.")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates a Reverse Polish Notation expression.

        Args:
            rpn (List[Union[str,float]]): RPN tokens.

        Returns:
            float: Computed result.

        Raises:
            ZeroDivisionError: For division by zero.
            ValueError: For invalid expressions.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                try:
                    b = stack.pop()
                    a = stack.pop()
                except IndexError:
                    raise ValueError("Invalid syntax: insufficient values for operator.")
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(a / b)
            else:
                raise ValueError(f"Unknown operator: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid syntax: too many values in expression.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """Checks if the token is a number."""
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example usage and basic tests
if __name__ == '__main__':
    calc = Calculator()
    tests = [
        ("1+2", 3),
        ("2 * (3 + 4)", 14),
        ("2.5-0.5", 2.0),
        ("10 / 2", 5.0),
        ("-3 + 7", 4.0),
        ("(2 + 3) * 4", 20.0),
        ("4 / 0", ZeroDivisionError),
        ("5 + ", ValueError),
        ("1 + (2 * (3 + 4)", ValueError),
        ("abc", ValueError),
        ("-2.5*-4", 10.0),
        ("-2.5--4", 1.5),
        ("3 + (4 - (1 + 2))", 4.0),
        ("--5", ValueError),
        ("2 * -3", -6.0),
        ("-(2 + 3)", ValueError),  # currently, will reject negative before parenthesis
    ]
    for expr, expected in tests:
        try:
            result = calc.calculate(expr)
            correct = abs(result - expected) < 1e-9 if isinstance(expected, (float, int)) else False
            print(f"Test: {expr:20s} = {result:.4f} [{'PASS' if correct else 'FAIL'}]")
        except Exception as e:
            correct = isinstance(e, expected) if isinstance(expected, type) else False
            print(f"Test: {expr:20s} raised {type(e).__name__} [{'PASS' if correct else 'FAIL'}]")
