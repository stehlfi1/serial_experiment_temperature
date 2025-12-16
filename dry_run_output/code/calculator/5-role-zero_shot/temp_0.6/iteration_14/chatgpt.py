
from typing import List, Union


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses, using correct operator precedence.
    Follows ISO/IEC 25010 software quality requirements.

    Methods:
        calculate(expression: str) -> float
            Evaluates a given arithmetic expression and returns the result as a float.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.

        :param expression: A string representing the arithmetic expression.
        :return: The computed result as a float.
        :raises ValueError: For invalid expressions or characters.
        :raises ZeroDivisionError: For division by zero cases.
        """
        tokens = self._tokenize(expression)
        rpn = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).

        :param expr: The input arithmetic expression.
        :return: A list of string tokens.
        :raises ValueError: For invalid characters or malformed numbers.
        """
        tokens = []
        i = 0
        length = len(expr)
        while i < length:
            char = expr[i]
            if char.isspace():
                i += 1
                continue
            elif char in '+-':  # Could be unary +/- or operator
                # Check if unary: Only at start or after '(' or operator
                if (
                    (i == 0) or
                    (tokens and tokens[-1] in '(*+/ -')
                ):
                    # Parse the unary number (possibly floating point)
                    num, num_chars = self._parse_number(expr[i:])
                    tokens.append(num)
                    i += num_chars
                else:
                    tokens.append(char)
                    i += 1
            elif char in '*/()':
                tokens.append(char)
                i += 1
            elif char.isdigit() or char == '.':
                num, num_chars = self._parse_number(expr[i:])
                tokens.append(num)
                i += num_chars
            else:
                raise ValueError(f"Invalid character found: '{char}'")
        return tokens

    def _parse_number(self, substr: str) -> (str, int):
        """
        Parses a number (integer or float, possibly negative) from the start of substr.

        :param substr: The string starting with the number.
        :return: Tuple of (number as string, length consumed).
        :raises ValueError: If the number format is invalid.
        """
        num_chars = 0
        has_decimal = False
        has_digit = False
        # Optional leading sign
        if substr and substr[0] in '+-':
            num_chars += 1
        while num_chars < len(substr):
            c = substr[num_chars]
            if c.isdigit():
                num_chars += 1
                has_digit = True
            elif c == '.':
                if has_decimal:
                    break  # Only one decimal allowed
                has_decimal = True
                num_chars += 1
            else:
                break
        if not has_digit:
            raise ValueError(f"Invalid number format in expression at: '{substr}'")
        return substr[:num_chars], num_chars

    def _shunting_yard(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts the list of tokens into Reverse Polish Notation using the Shunting Yard algorithm.

        :param tokens: Token list.
        :return: Tokens in RPN as list.
        :raises ValueError: For mismatched parentheses.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in precedence:
                while (stack and stack[-1] in precedence and
                       precedence[stack[-1]] >= precedence[token]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Invalid token: '{token}'")
        while stack:
            if stack[-1] in '()':
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, tokens: List[Union[str, float]]) -> float:
        """
        Evaluates the expression represented in Reverse Polish Notation.

        :param tokens: RPN token list.
        :return: Result as float.
        :raises ZeroDivisionError: For division by zero.
        :raises ValueError: For malformed RPN or invalid operations.
        """
        stack = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in {'+', '-', '*', '/'}:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: not enough operands.")
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
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(a / b)
            else:
                raise ValueError(f"Invalid token in RPN: '{token}'")
        if len(stack) != 1:
            raise ValueError("Malformed expression: leftover operands.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Determines if a string token is a number (integer or float).

        :param token: Token to check.
        :return: True if token represents a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    # Simple console interface for demonstration/testing
    calc = Calculator()
    print("Console Arithmetic Calculator (type 'exit' to quit)")
    while True:
        expr = input("\nEnter expression: ")
        if expr.strip().lower() == 'exit':
            break
        try:
            result = calc.calculate(expr)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
