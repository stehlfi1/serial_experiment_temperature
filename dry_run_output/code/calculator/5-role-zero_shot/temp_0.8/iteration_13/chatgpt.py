
import re
from typing import List

class CalculatorError(Exception):
    """Custom exception type for calculator errors."""
    pass

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /,
    parentheses, correct operator precedence, and both integer and
    floating-point numbers (including negatives).

    Adheres to ISO/IEC 25010 for software quality models.
    """

    # Operator precedence map
    _precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }

    # Valid characters for input validation
    _valid_characters_pattern = re.compile(r'^[\d\s\.\+\-\*\/\(\)]+$')

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result.

        :param expression: A string representing the arithmetic expression.
        :return: The result as a float.
        :raises CalculatorError: On invalid syntax, unbalanced parentheses, division by zero, or invalid characters.
        """
        sanitized = self._sanitize(expression)
        tokens = self._tokenize(sanitized)
        rpn = self._infix_to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _sanitize(self, expression: str) -> str:
        """
        Removes spaces and validates characters.

        :param expression: The input expression string.
        :return: Sanitized string.
        :raises CalculatorError: On invalid characters.
        """
        expr = expression.replace(' ', '')
        if not expr:
            raise CalculatorError("Empty expression is not allowed.")
        if not self._valid_characters_pattern.fullmatch(expr):
            raise CalculatorError("Invalid characters in expression.")
        return expr

    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenizes the arithmetic expression to numbers and operators.

        :param expression: The sanitized expression string.
        :return: List of tokens.
        :raises CalculatorError: On unbalanced parentheses or invalid syntax.
        """
        tokens = []
        i = 0
        length = len(expression)
        while i < length:
            char = expression[i]

            if char in '+-*/()':
                # Negative number detection (unary minus)
                if char == '-' and (i == 0 or expression[i - 1] in '+-*/('):
                    # Start of number
                    number = '-'
                    i += 1
                    while i < length and (expression[i].isdigit() or expression[i] == '.'):
                        number += expression[i]
                        i += 1
                    if number == '-':
                        raise CalculatorError("Invalid use of '-' operator.")
                    tokens.append(number)
                    continue
                else:
                    tokens.append(char)
                    i += 1
            elif char.isdigit() or char == '.':
                number = ''
                dot_count = 0
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise CalculatorError("Invalid numeric format: multiple decimals.")
                    number += expression[i]
                    i += 1
                tokens.append(number)
            else:
                raise CalculatorError(f"Invalid character in expression: '{char}'")

        # Parenthesis balance check
        balance = 0
        for token in tokens:
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
            if balance < 0:
                raise CalculatorError("Unbalanced parentheses detected.")
        if balance != 0:
            raise CalculatorError("Unbalanced parentheses detected.")

        return tokens

    def _infix_to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN) using the Shunting Yard Algorithm.

        :param tokens: List of infix tokens.
        :return: List of RPN tokens.
        :raises CalculatorError: On syntax errors.
        """
        output = []
        stack = []

        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in self._precedence:
                while (stack and stack[-1] in self._precedence and
                       ((self._precedence[token] < self._precedence[stack[-1]]) or
                        (self._precedence[token] == self._precedence[stack[-1]] and token in '+-*/'))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise CalculatorError("Unbalanced parentheses during RPN conversion.")
                stack.pop()  # Discard '('
            else:
                raise CalculatorError(f"Unknown token during RPN conversion: {token}")

        while stack:
            if stack[-1] in '()':
                raise CalculatorError("Unbalanced parentheses in expression.")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, tokens: List[str]) -> float:
        """
        Evaluates a postfix (RPN) expression.

        :param tokens: RPN tokens.
        :return: Computed result as float.
        :raises CalculatorError: On computation errors such as division by zero or invalid syntax.
        """
        stack = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self._precedence:
                if len(stack) < 2:
                    raise CalculatorError("Invalid syntax: not enough operands.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise CalculatorError(f"Unknown token during evaluation: {token}")

        if len(stack) != 1:
            raise CalculatorError("Invalid expression: leftover operands or insufficient operations.")

        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """Checks if a token is a number."""
        try:
            float(token)
            return True
        except ValueError:
            return False

    @staticmethod
    def _apply_operator(a: float, b: float, operator: str) -> float:
        """Applies the arithmetic operator to two operands."""
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise CalculatorError("Division by zero detected.")
            return a / b
        else:
            raise CalculatorError(f"Unknown operator: {operator}")

# Example Usage (Uncomment for testing):
# calc = Calculator()
# try:
#     expr = input("Enter an arithmetic expression: ")
#     result = calc.calculate(expr)
#     print(f"Result: {result}")
# except CalculatorError as ce:
#     print(f"Error: {ce}")
