
from typing import List, Union
import re

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses. Implements ISO/IEC 25010 quality
    requirements: correctness, performance, modularity, safety, testability, and readability.
    """
    # Supported operators and their precedence
    _OPERATORS = {
        '+': (1, 'L'),  # (precedence, associativity)
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }
    # Allowed characters for the expression (excluding whitespace)
    _VALID_CHAR_PATTERN = re.compile(r'^[\d+\-*/().\s]+$')

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression involving +, -, *, / operations and parentheses.

        :param expression: A string, such as "3 + 5 * (2 - 4) / -7"
        :return: Computed result as float
        :raises ValueError: For invalid expressions (unbalanced parentheses, invalid characters etc)
        :raises ZeroDivisionError: On division by zero
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        postfix = self._to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an expression string into a list of tokens (numbers, operators, parentheses).
        Handles negative numbers.

        :param expression: Input string.
        :return: List of string tokens.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression must be a non-empty string.")
        expr = expression.replace(' ', '')
        if not self._VALID_CHAR_PATTERN.match(expr):
            raise ValueError("Expression contains invalid characters.")

        tokens: List[str] = []
        i, n = 0, len(expr)
        while i < n:
            c = expr[i]
            if c in '0123456789.':
                # Parse a number (integer or float)
                start = i
                has_dot = c == '.'
                i += 1
                while i < n and (expr[i].isdigit() or (expr[i] == '.' and not has_dot)):
                    if expr[i] == '.':
                        if has_dot:
                            raise ValueError("Invalid number format (multiple dots).")
                        has_dot = True
                    i += 1
                tokens.append(expr[start:i])
            elif c in self._OPERATORS:
                # Handle unary minus (negative numbers)
                if c == '-' and (len(tokens) == 0 or tokens[-1] in self._OPERATORS or tokens[-1] == '('):
                    # Negative number, not subtraction
                    start = i
                    i += 1
                    if i < n and (expr[i].isdigit() or expr[i] == '.'):
                        has_dot = expr[i] == '.'
                        i += 1
                        while i < n and (expr[i].isdigit() or (expr[i] == '.' and not has_dot)):
                            if expr[i] == '.':
                                if has_dot:
                                    raise ValueError("Invalid number format (multiple dots).")
                                has_dot = True
                            i += 1
                        tokens.append(expr[start:i])
                    else:
                        raise ValueError("Invalid use of '-' in expression.")
                else:
                    tokens.append(c)
                    i += 1
            elif c in '()':
                tokens.append(c)
                i += 1
            else:
                # Should not reach here due to earlier regex check
                raise ValueError(f"Invalid character encountered: '{c}'")
        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the syntax of the token list (e.g., balanced parentheses, no misplaced operators).

        :param tokens: List of tokens from tokenizer.
        :raises ValueError: On invalid expression.
        """
        # Parentheses validation
        balance = 0
        prev_token = None
        for token in tokens:
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Unbalanced parentheses detected.")
            elif token in self._OPERATORS:
                if prev_token is None or prev_token in self._OPERATORS or prev_token == '(':
                    if not (token == '-' and (prev_token is None or prev_token == '(')):
                        # only unary minus is allowed here, others are syntax errors
                        raise ValueError(f"Misplaced operator '{token}'.")
            prev_token = token
        if balance != 0:
            raise ValueError("Unbalanced parentheses detected.")

    def _to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Converts infix tokens to postfix notation using the shunting yard algorithm.

        :param tokens: List of tokens.
        :return: List of postfix (RPN) tokens.
        """
        output: List[str] = []
        stack: List[str] = []

        for token in tokens:
            if self._is_number(token):
                output.append(token)
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
                    raise ValueError("Unbalanced parentheses detected.")
                stack.pop()
            else:
                raise ValueError(f"Unknown token during postfix conversion: '{token}'")
        while stack:
            if stack[-1] in '()':
                raise ValueError("Unbalanced parentheses detected at end.")
            output.append(stack.pop())
        return output

    def _evaluate_postfix(self, postfix: List[str]) -> float:
        """
        Evaluates a postfix (RPN) list of tokens.

        :param postfix: List of postfix tokens.
        :return: Computed float result.
        """
        stack: List[float] = []
        for token in postfix:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operation.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Unknown token in postfix evaluation: '{token}'")
        if len(stack) != 1:
            raise ValueError("Error evaluating expression. Stack not empty after evaluation.")
        return float(stack[0])

    def _is_number(self, token: str) -> bool:
        """
        Checks if a token is a valid number (integer or float, negative or positive).
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operator to two operands.

        :param a: First operand.
        :param b: Second operand.
        :param operator: Operator string.
        :return: Computed result.
        :raises ZeroDivisionError: On division by zero.
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0.0:
                raise ZeroDivisionError("Division by zero detected.")
            return a / b
        else:
            raise ValueError(f"Unsupported operator '{operator}'.")

# Test example
if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        "3 + 2 * 4",
        "(1 + 2) * (3 - 4) / 5",
        "-2.5 + (3.5 * -4) / 8.0",
        "10 / (2 - 2)",  # expect ZeroDivisionError
        "2 + * 4",       # expect ValueError
        "(5 + (4 * 3",   # expect ValueError unbalanced parentheses
        "7 + 8#2"        # expect ValueError invalid character
    ]

    for expr in test_cases:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr!r} => Error: {e}")
