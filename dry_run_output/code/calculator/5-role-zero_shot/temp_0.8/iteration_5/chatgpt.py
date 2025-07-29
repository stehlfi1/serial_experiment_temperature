
from typing import List, Tuple

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions with +, -, *, /,
    supports parentheses, correct operator precedence, and both integers and floats.
    Follows ISO/IEC 25010 requirements for software quality.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate the given arithmetic expression and return the result as a float.

        :param expression: A string representing the arithmetic expression to evaluate.
        :return: The result of the evaluated expression as a float.
        :raises ValueError: If the expression is invalid (e.g., unbalanced parentheses, invalid characters).
        :raises ZeroDivisionError: If the expression contains division by zero.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    # ==============================
    # TOKENIZATION
    # =============================
    def _tokenize(self, expr: str) -> List[str]:
        """
        Convert the input string into a list of tokens (numbers, operators, parentheses).
        Handles negative numbers and floating point numbers.
        """
        tokens = []
        i = 0
        length = len(expr)
        while i < length:
            char = expr[i]
            if char.isspace():
                i += 1
                continue
            elif char in '+-':
                # Determine if this is a unary operator (negative/positive sign)
                if (
                    (i == 0)
                    or (tokens and tokens[-1] in '(*+-/')
                ):
                    # It's a unary operator; consume number immediately after
                    j = i + 1
                    num, next_pos = self._read_number(expr, j)
                    if num is None:
                        raise ValueError(f"Invalid syntax at position {i}: expected number after unary '{char}'")
                    tokens.append(char + num)
                    i = next_pos
                else:
                    # Binary operator
                    tokens.append(char)
                    i += 1
            elif char in '*/()':
                tokens.append(char)
                i += 1
            elif char.isdigit() or char == '.':
                num, next_pos = self._read_number(expr, i)
                if num is None:
                    raise ValueError(f"Invalid number at position {i}")
                tokens.append(num)
                i = next_pos
            else:
                raise ValueError(f"Invalid character '{char}' in expression.")
        self._validate_tokens(tokens)
        return tokens

    def _read_number(self, expr: str, start: int) -> Tuple[str, int]:
        """
        Reads a (possibly floating point) number from expr starting at position start.
        Returns the number as a string and the position after the number.
        """
        i = start
        number = ''
        dot_count = 0
        length = len(expr)
        while i < length and (expr[i].isdigit() or expr[i] == '.'):
            if expr[i] == '.':
                dot_count += 1
                if dot_count > 1:
                    return None, i  # Invalid float (multiple dots)
            number += expr[i]
            i += 1
        if not number or number == '.':
            return None, i
        return number, i

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Check for invalid tokens, such as unbalanced parentheses or invalid number formats.
        """
        paren_balance = 0
        prev_token = None
        for token in tokens:
            if token == '(':
                paren_balance += 1
            elif token == ')':
                paren_balance -= 1
                if paren_balance < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
            elif token in '+-*/':
                if prev_token is None or prev_token in '+-*/(':
                    raise ValueError("Invalid sequence of operators.")
            else:
                # Try converting token to float
                try:
                    float(token)
                except ValueError:
                    raise ValueError(f"Invalid number token: {token}")
            prev_token = token
        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses: too many '('")

    # ==============================
    # SHUNTING-YARD PARSER (to RPN)
    # ==============================
    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Convert infix tokens to Reverse Polish Notation (RPN) using the shunting-yard algorithm.
        """
        out_queue = []
        op_stack = []

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L'}

        for token in tokens:
            if self._is_number(token):
                out_queue.append(token)
            elif token in precedence:
                while (
                    op_stack
                    and op_stack[-1] in precedence
                    and (
                        (associativity[token] == 'L' and precedence[token] <= precedence[op_stack[-1]])
                        or (associativity[token] == 'R' and precedence[token] < precedence[op_stack[-1]])
                    )
                ):
                    out_queue.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    out_queue.append(op_stack.pop())
                if not op_stack or op_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                op_stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token: {token}")
        while op_stack:
            if op_stack[-1] in '()':
                raise ValueError("Mismatched parentheses")
            out_queue.append(op_stack.pop())
        return out_queue

    # ==============================
    # EVALUATION OF RPN
    # ==============================
    def _evaluate_rpn(self, rpn: List[str]) -> float:
        """
        Evaluate an expression in Reverse Polish Notation (RPN).
        """
        stack = []
        for token in rpn:
            if self._is_number(token):
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
        if len(stack) != 1:
            raise ValueError("Invalid expression.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """
        Apply an operator to two operands and return the result.
        Handles division by zero.
        """
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero.")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {op}")

    def _is_number(self, token: str) -> bool:
        """
        Check if a token represents a valid number.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    # Example usage and basic tests (can be replaced with proper unit tests)
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",                # 7
        "(1 + 2) * 3",              # 9
        "2 * (3 + 4) / 2",          # 7
        "-3 + 5",                   # 2
        "4 + -2 * (6.5 - 3)",       # 4 + -2*3.5 = 4 - 7 = -3
        "-(2 + 3)",                 # -5
        "2 * -3",                   # -6
        "3.5 * 2",                  # 7
        "10 / 2.5",                 # 4
        "1 / 0",                    # Division by zero
        "((1 + 2)",                 # Unbalanced parentheses
        "2 ** 3",                   # Invalid character
        "3 +",                      # Invalid expression
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
