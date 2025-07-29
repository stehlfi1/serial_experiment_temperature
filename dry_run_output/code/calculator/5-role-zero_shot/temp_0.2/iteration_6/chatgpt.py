
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.

    Implements ISO/IEC 25010 quality requirements:
    - Correctness: Accurate evaluation of expressions with proper precedence.
    - Performance: Efficient parsing and evaluation (O(n) time).
    - Modularity: Tokenization, parsing, and evaluation are separated.
    - Safety: Robust input validation and error handling.
    - Testability: Methods are logically separated and easily testable.
    - Readability: Clear naming, docstrings, and comments.
    """

    # Allowed operators and their precedence
    OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression string and returns the result as a float.

        :param expression: The arithmetic expression to evaluate.
        :type expression: str
        :return: The result of the evaluated expression.
        :rtype: float
        :raises ValueError: If the expression is invalid.
        :raises ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).

        :param expression: The input arithmetic expression.
        :return: List of tokens.
        :raises ValueError: If invalid characters or malformed numbers are found.
        """
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            elif char in '()+-*/':
                # Handle unary minus (negative numbers)
                if char == '-' and (i == 0 or expression[i-1] in ' (*/+-'):
                    # Start of expression or after operator/parenthesis: unary minus
                    j = i + 1
                    # Accept numbers like -3.5 or -2
                    num_str = '-'
                    decimal_found = False
                    while j < n and (expression[j].isdigit() or (expression[j] == '.' and not decimal_found)):
                        if expression[j] == '.':
                            decimal_found = True
                        num_str += expression[j]
                        j += 1
                    if len(num_str) > 1:
                        try:
                            num = float(num_str) if '.' in num_str else int(num_str)
                        except ValueError:
                            raise ValueError(f"Invalid number: {num_str}")
                        tokens.append(num)
                        i = j
                        continue
                    else:
                        # It's just a unary minus before something else, treat as 0 - expr
                        tokens.append(0)
                        tokens.append('-')
                        i += 1
                        continue
                tokens.append(char)
                i += 1
            elif char.isdigit() or char == '.':
                # Parse number (integer or float)
                j = i
                decimal_found = False
                while j < n and (expression[j].isdigit() or (expression[j] == '.' and not decimal_found)):
                    if expression[j] == '.':
                        if decimal_found:
                            raise ValueError(f"Invalid number: multiple decimals in {expression[i:j+1]}")
                        decimal_found = True
                    j += 1
                num_str = expression[i:j]
                try:
                    num = float(num_str) if '.' in num_str else int(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number: {num_str}")
                tokens.append(num)
                i = j
            else:
                raise ValueError(f"Invalid character: '{char}'")
        self._validate_parentheses(tokens)
        return tokens

    def _validate_parentheses(self, tokens: List[Union[str, float]]) -> None:
        """
        Validates that parentheses are balanced in the token list.

        :param tokens: List of tokens.
        :raises ValueError: If parentheses are unbalanced.
        """
        balance = 0
        for token in tokens:
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
        if balance != 0:
            raise ValueError("Unbalanced parentheses: too many '('")

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts the list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        :param tokens: List of tokens in infix notation.
        :return: List of tokens in RPN.
        :raises ValueError: If the expression is malformed.
        """
        output = []
        stack = []
        for token in tokens:
            if isinstance(token, (int, float)):
                output.append(token)
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                       ((self.OPERATORS[token][1] == 'L' and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]) or
                        (self.OPERATORS[token][1] == 'R' and self.OPERATORS[token][0] < self.OPERATORS[stack[-1]][0]))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Invalid token: {token}")
        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates a Reverse Polish Notation (RPN) expression.

        :param rpn: List of tokens in RPN.
        :return: The result as a float.
        :raises ZeroDivisionError: If division by zero occurs.
        :raises ValueError: If the expression is malformed.
        """
        stack = []
        for token in rpn:
            if isinstance(token, (int, float)):
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Malformed expression: too many operands")
        return stack[0]

# Example usage and test cases
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",                # 7
        "(1 + 2) * 3",              # 9
        "10 / 2 + 3 * 2",           # 11
        "-5 + 3",                   # -2
        "4 + -2",                   # 2
        "3.5 * 2",                  # 7.0
        "2 * (3 + 4.5)",            # 15.0
        "((2+3)*4)-5/2",            # 17.5
        "-(2 + 3) * 4",             # -20
        "3 + 4 * 2 / (1 - 5)",      # 1.0
        "3 + (4 * 2) / (1 - 5)",    # 1.0
        "3 + ((4 * 2) / (1 - 5))",  # 1.0
        "0.1 + 0.2",                # 0.3
        "5 / 0",                    # ZeroDivisionError
        "2 + (3 * 4",               # ValueError (unbalanced)
        "2 + 3 ** 4",               # ValueError (invalid char)
        "abc + 1",                  # ValueError (invalid char)
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
