
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator implementing addition, subtraction,
    multiplication, division, and parentheses, with operator precedence.
    Implements calculate(expression: str) -> float.
    """

    # Allowed operators and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }
    PARENTHESIS = {'(', ')'}
    TOKEN_REGEX = re.compile(
        r'''
        (?P<number>   -?\d*\.?\d+   ) |   # Integer or decimal number, possibly negative
        (?P<op>       [\+\-\*/]     ) |   # Arithmetic operators
        (?P<lparen>   \(            ) |   # Left parenthesis
        (?P<rparen>   \)            )     # Right parenthesis
        ''',
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression string and return the result as float.
        Raises:
            ValueError: for invalid syntax, unbalanced parentheses, or invalid characters.
            ZeroDivisionError: for division by zero.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._infix_to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List[str]:
        """
        Tokenizes the input expression string.
        Returns a list of string tokens.
        Raises ValueError if invalid characters are found.
        """
        tokens = []
        pos = 0
        expr = expr.replace(' ', '')  # Remove whitespace
        while pos < len(expr):
            match = self.TOKEN_REGEX.match(expr, pos)
            if not match:
                raise ValueError(f"Invalid character at position {pos}: '{expr[pos]}'")
            group = match.lastgroup
            token = match.group(group)
            if group == 'number':
                tokens.append(token)
            elif group == 'op':
                # Handle unary minus
                if token == '-' and (len(tokens) == 0 or tokens[-1] in self.OPERATORS or tokens[-1] == '('):
                    # Next token must be a number (negative)
                    match_next_number = self.TOKEN_REGEX.match(expr, match.end())
                    if match_next_number and match_next_number.lastgroup == 'number':
                        next_number = '-' + match_next_number.group('number')
                        tokens.append(next_number)
                        pos = match_next_number.end()
                        continue
                    else:
                        raise ValueError("Invalid syntax: unary minus not followed by a number")
                tokens.append(token)
            elif group in ('lparen', 'rparen'):
                tokens.append(token)
            else:
                raise ValueError(f"Unknown token: {token}")
            pos = match.end()
        if not tokens:
            raise ValueError("Empty expression")
        return tokens

    def _validate_tokens(self, tokens: List[str]):
        """
        Validates tokens for balanced parentheses and correct composition.
        Raises ValueError if invalid.
        """
        balance = 0
        prev_token = None
        for idx, token in enumerate(tokens):
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
            elif token in self.OPERATORS:
                if prev_token is None or prev_token in self.OPERATORS or prev_token == '(':
                    raise ValueError("Invalid syntax: operator at invalid position")
            prev_token = token
        if balance != 0:
            raise ValueError("Unbalanced parentheses: too many '('")

    def _infix_to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN) using the
        shunting yard algorithm.
        Returns a list of tokens in RPN.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(float(token))
            elif token in self.OPERATORS:
                while (operator_stack and operator_stack[-1] in self.OPERATORS and
                       self.OPERATORS[operator_stack[-1]][0] >= self.OPERATORS[token][0]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Unbalanced parenthesis")
                operator_stack.pop()  # Pop '('
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            op = operator_stack.pop()
            if op in self.PARENTHESIS:
                raise ValueError("Unbalanced parenthesis")
            output_queue.append(op)
        return output_queue

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation.
        Returns the result as float.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: insufficient operands")
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = self.OPERATORS[token][1](a, b)
                stack.append(result)
            else:
                raise ValueError(f"Invalid RPN token: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid syntax: leftover operands")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Returns True if the token is a number (int or float), else False.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example usage (for testing purposes)
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "2 + 3 * 4",              # 14
        "(2 + 3) * 4",            # 20
        "-2 + 3",                 # 1
        "2 + -3",                 # -1
        "2.5 * 4 - 1.5 / 2",      # 9.25
        "10 / (5 - 5)",           # ZeroDivisionError
        "3 + (4 * 2 - (1 + 1))",  # 8
        "((2))",                  # 2
        "-(3 + 2)",               # Should raise invalid syntax
        "2 ++ 2",                 # Should raise invalid syntax
        "abc",                    # Should raise invalid character
        "",                       # Should raise empty expression
        "2 + (3 * 4",             # Should raise unbalanced parentheses
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"{expr} => Error: {e}")
