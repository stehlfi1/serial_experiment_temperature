
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    and both integer and floating-point numbers (including negatives).
    Adheres to ISO/IEC 25010 quality attributes: correctness, performance,
    modularity, safety, testability, readability, and documentation.
    """

    # Supported operators and their precedence
    _OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid syntax or characters.
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input expression string into a list of tokens.

        Args:
            expression (str): The arithmetic expression.

        Returns:
            List[str]: List of tokens.

        Raises:
            ValueError: If invalid characters are found or parentheses are unbalanced.
        """
        tokens = []
        i = 0
        length = len(expression)
        paren_balance = 0
        while i < length:
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char in '()+-*/':
                # Handle unary minus (negative numbers)
                if char == '-' and (
                    i == 0 or (tokens and tokens[-1] in '(*+/ -')
                ):
                    # Start of expression or after operator/parenthesis: unary minus
                    num, num_len = self._read_number(expression, i)
                    tokens.append(num)
                    i += num_len
                    continue

                if char == '(':
                    paren_balance += 1
                elif char == ')':
                    paren_balance -= 1
                    if paren_balance < 0:
                        raise ValueError("Unbalanced parentheses: too many ')'")
                tokens.append(char)
                i += 1
            elif char.isdigit() or char == '.':
                num, num_len = self._read_number(expression, i)
                tokens.append(num)
                i += num_len
            else:
                raise ValueError(f"Invalid character in expression: '{char}'")

        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses: too many '('")
        return tokens

    def _read_number(self, expr: str, start: int) -> (str, int):
        """
        Reads a number (integer or float, possibly negative) from expr starting at index start.

        Args:
            expr (str): The expression string.
            start (int): Start index.

        Returns:
            (str, int): Tuple of (number string, length of number).
        """
        i = start
        num_str = ''
        decimal_found = False

        # Handle leading minus for negative numbers
        if expr[i] == '-':
            num_str += '-'
            i += 1

        while i < len(expr):
            if expr[i].isdigit():
                num_str += expr[i]
            elif expr[i] == '.':
                if decimal_found:
                    break  # Second decimal point, stop number
                decimal_found = True
                num_str += '.'
            else:
                break
            i += 1

        # Validate number format
        if num_str in ('-', '') or num_str == '-.':
            raise ValueError(f"Invalid number format near: '{expr[start:i+1]}'")
        return num_str, i - start

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN) using the shunting yard algorithm.

        Args:
            tokens (List[str]): List of tokens in infix notation.

        Returns:
            List[str]: List of tokens in RPN.

        Raises:
            ValueError: If the expression is invalid.
        """
        output = []
        stack = []

        for token in tokens:
            if self._is_number(token):
                output.append(token)
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
                if not stack:
                    raise ValueError("Unbalanced parentheses: missing '('")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token: '{token}'")

        while stack:
            if stack[-1] in '()':
                raise ValueError("Unbalanced parentheses")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, rpn: List[str]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation.

        Args:
            rpn (List[str]): List of tokens in RPN.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the expression is invalid.
        """
        stack: List[float] = []

        for token in rpn:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values for operation")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Unknown token in evaluation: '{token}'")

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values")
        return stack[0]

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


# Example usage and simple tests
if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        ("1 + 2", 3.0),
        ("2 * (3 + 4)", 14.0),
        ("2 * 3 + 4", 10.0),
        ("2 * (3 + 4 * (2 - 1))", 14.0),
        ("-5 + 3", -2.0),
        ("-5 * -3", 15.0),
        ("(1 + 2) * (3 + 4)", 21.0),
        ("3.5 + 2.1", 5.6),
        ("3 / 2", 1.5),
        ("10 / 0", ZeroDivisionError),
        ("2 + (3 * 4", ValueError),  # Unbalanced parentheses
        ("2 + a", ValueError),       # Invalid character
        ("", ValueError),            # Empty expression
        ("-3.5 * (2 + 4.2)", -21.7),
    ]

    for expr, expected in test_cases:
        try:
            result = calc.calculate(expr)
            assert abs(result - expected) < 1e-8, f"Test failed: {expr} = {result}, expected {expected}"
            print(f"PASS: {expr} = {result}")
        except Exception as e:
            if isinstance(expected, type) and isinstance(e, expected):
                print(f"PASS: {expr} raised {e.__class__.__name__}")
            else:
                print(f"FAIL: {expr} raised {e.__class__.__name__}: {e}")
