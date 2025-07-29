
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    and both integer and floating-point numbers (including negatives).
    Adheres to ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence
    OPERATORS = {
        '+': (1, lambda a, b: a + b),
        '-': (1, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: a / b),
    }

    # Token types
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid (syntax, unbalanced parentheses, invalid characters).
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[dict]:
        """
        Converts the input string into a list of tokens.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            List[dict]: List of token dictionaries.

        Raises:
            ValueError: If invalid characters are found or parentheses are unbalanced.
        """
        # Remove whitespace for easier processing
        expr = expression.replace(' ', '')
        tokens = []
        i = 0
        length = len(expr)
        paren_balance = 0

        # Regex for matching numbers (integers and floats, including negatives)
        number_regex = re.compile(r'^-?\d+(\.\d+)?')

        while i < length:
            char = expr[i]

            if char in '0123456789.':
                # Parse number (could be negative if at start or after '(' or operator)
                match = number_regex.match(expr[i:])
                if not match:
                    raise ValueError(f"Invalid number at position {i}")
                num_str = match.group(0)
                tokens.append({'type': self.NUMBER, 'value': float(num_str)})
                i += len(num_str)
            elif char in self.OPERATORS:
                # Handle unary minus (negative numbers)
                if char == '-' and (
                    i == 0 or
                    (tokens and tokens[-1]['type'] in {self.OPERATOR, self.LPAREN})
                ):
                    # It's a unary minus, parse as part of the number
                    match = number_regex.match(expr[i:])
                    if not match:
                        raise ValueError(f"Invalid negative number at position {i}")
                    num_str = match.group(0)
                    tokens.append({'type': self.NUMBER, 'value': float(num_str)})
                    i += len(num_str)
                else:
                    tokens.append({'type': self.OPERATOR, 'value': char})
                    i += 1
            elif char == '(':
                tokens.append({'type': self.LPAREN, 'value': char})
                paren_balance += 1
                i += 1
            elif char == ')':
                tokens.append({'type': self.RPAREN, 'value': char})
                paren_balance -= 1
                if paren_balance < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
                i += 1
            else:
                raise ValueError(f"Invalid character '{char}' at position {i}")

        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses: too many '('")

        return tokens

    def _to_rpn(self, tokens: List[dict]) -> List[Union[float, str]]:
        """
        Converts the list of tokens to Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

        Args:
            tokens (List[dict]): List of token dictionaries.

        Returns:
            List[Union[float, str]]: RPN output as a list.

        Raises:
            ValueError: If the expression is invalid.
        """
        output = []
        stack = []

        for token in tokens:
            if token['type'] == self.NUMBER:
                output.append(token['value'])
            elif token['type'] == self.OPERATOR:
                while (stack and stack[-1]['type'] == self.OPERATOR and
                       self.OPERATORS[stack[-1]['value']][0] >= self.OPERATORS[token['value']][0]):
                    output.append(stack.pop()['value'])
                stack.append(token)
            elif token['type'] == self.LPAREN:
                stack.append(token)
            elif token['type'] == self.RPAREN:
                while stack and stack[-1]['type'] != self.LPAREN:
                    output.append(stack.pop()['value'])
                if not stack or stack[-1]['type'] != self.LPAREN:
                    raise ValueError("Unbalanced parentheses")
                stack.pop()  # Remove '('
            else:
                raise ValueError("Unknown token type")

        while stack:
            if stack[-1]['type'] in {self.LPAREN, self.RPAREN}:
                raise ValueError("Unbalanced parentheses")
            output.append(stack.pop()['value'])

        return output

    def _evaluate_rpn(self, rpn: List[Union[float, str]]) -> float:
        """
        Evaluates the RPN expression.

        Args:
            rpn (List[Union[float, str]]): The RPN expression.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the RPN is invalid.
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
        "1 + 2 * 3",                # 7.0
        "(1 + 2) * 3",              # 9.0
        "10 / 2 + 3 * 2",           # 11.0
        "-5 + 3",                   # -2.0
        "4 + -2",                   # 2.0
        "3.5 * 2",                  # 7.0
        "10 / (5 - 5)",             # ZeroDivisionError
        "((2 + 3) * (4 - 1)) / 2",  # 7.5
        "2 + (3 * (4 - 1)",         # ValueError (unbalanced)
        "2 + 3 *",                  # ValueError (syntax)
        "abc + 1",                  # ValueError (invalid char)
        "-(2 + 3)",                 # -5.0
        "(-2) * (-3)",              # 6.0
        "2.5 + 3.1",                # 5.6
    ]

    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
