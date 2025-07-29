
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.

    Adheres to ISO/IEC 25010 for quality requirements.
    """

    # Allowed operators and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        :param expression: The arithmetic expression as a string.
        :return: The result of the evaluated expression.
        :raises ValueError: For invalid syntax or characters.
        :raises ZeroDivisionError: For division by zero.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).

        :param expression: The arithmetic expression as a string.
        :return: List of tokens.
        :raises ValueError: For invalid characters or unbalanced parentheses.
        """
        tokens = []
        num_buffer = ''
        i = 0
        length = len(expression)
        parentheses_balance = 0

        while i < length:
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char in '0123456789.':
                num_buffer += char
                i += 1
                continue

            # Handle negative numbers (unary minus)
            if char == '-' and (not tokens or tokens[-1] in self.OPERATORS or tokens[-1] == '('):
                num_buffer += char
                i += 1
                continue

            # Flush number buffer
            if num_buffer:
                try:
                    num = float(num_buffer)
                except ValueError:
                    raise ValueError(f"Invalid number: {num_buffer}")
                tokens.append(num)
                num_buffer = ''

            if char in self.OPERATORS:
                tokens.append(char)
            elif char == '(':
                tokens.append(char)
                parentheses_balance += 1
            elif char == ')':
                tokens.append(char)
                parentheses_balance -= 1
                if parentheses_balance < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
            else:
                raise ValueError(f"Invalid character: '{char}'")
            i += 1

        # Flush last number buffer
        if num_buffer:
            try:
                num = float(num_buffer)
            except ValueError:
                raise ValueError(f"Invalid number: {num_buffer}")
            tokens.append(num)

        if parentheses_balance != 0:
            raise ValueError("Unbalanced parentheses: too many '('")

        return tokens

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts the list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        :param tokens: List of tokens in infix notation.
        :return: List of tokens in RPN.
        :raises ValueError: For invalid syntax.
        """
        output = []
        stack = []

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                       self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]):
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
                raise ValueError(f"Unknown token: {token}")

        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation.

        :param rpn: List of tokens in RPN.
        :return: The result as a float.
        :raises ZeroDivisionError: For division by zero.
        :raises ValueError: For invalid syntax.
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
                raise ValueError(f"Unknown token in RPN: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid syntax: too many operands")

        return stack[0]

# Example usage and test cases
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",            # 7.0
        "(1 + 2) * 3",          # 9.0
        "10 / 2 + 3 * 2",       # 11.0
        "-5 + 3",               # -2.0
        "4 + -2 * (3 - 5.5)",   # 9.0
        "3.5 * 2 - 1 / (2 + 2)",# 6.0
        "((2))",                # 2.0
        "-(2 + 3)",             # -5.0
        "1 / 0",                # ZeroDivisionError
        "2 + (3 * 4",           # ValueError (unbalanced parentheses)
        "2 + $",                # ValueError (invalid character)
    ]

    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
