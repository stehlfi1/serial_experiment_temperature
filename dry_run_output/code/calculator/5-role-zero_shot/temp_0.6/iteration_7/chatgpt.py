
from typing import List, Union
import re

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    and both integer and floating-point numbers (including negative values).
    Implements ISO/IEC 25010 quality requirements.
    """

    # Supported operators with precedence and associativity
    _OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression string.

        :param expression: A string representing the arithmetic expression.
        :return: The result as a float.
        :raises ValueError: For malformed expressions or invalid characters.
        :raises ZeroDivisionError: For division by zero.
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")

        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Converts the input string to a list of tokens (numbers, operators, parentheses).

        :param expression: The arithmetic expression as a string.
        :return: List of tokens.
        :raises ValueError: If invalid or unsupported characters are found.
        """
        tokens = []
        position = 0
        length = len(expression)
        number_pattern = re.compile(r'\d+(\.\d+)?')

        # Allowed characters: digits, operators, parentheses, dot, spaces
        allowed_chars = set('0123456789.+-*/() \t')

        # Validation: invalid characters
        for ch in expression:
            if ch not in allowed_chars:
                raise ValueError(f"Invalid character '{ch}' in expression.")

        while position < length:
            ch = expression[position]

            if ch.isspace():
                position += 1
                continue

            # Number (possibly negative, integer or float)
            if ch.isdigit() or (ch == '.' and position + 1 < length and expression[position + 1].isdigit()):
                match = number_pattern.match(expression, position)
                if match:
                    num_str = match.group(0)
                    tokens.append(float(num_str))
                    position += len(num_str)
                    continue
                else:
                    raise ValueError(f"Invalid number at position {position}.")

            # Operator or Parenthesis
            if ch in '+-*/()':
                # Handle unary minus for negative numbers
                if ch == '-':
                    prev_token = tokens[-1] if tokens else None
                    # If at start, after '(', or after operator, treat as unary minus
                    if (prev_token in ('(', '+', '-', '*', '/', None)):
                        # Lookahead for a number or parenthesis
                        # Negative number
                        next_pos = position + 1
                        # Skip spaces
                        while next_pos < length and expression[next_pos].isspace():
                            next_pos += 1
                        if next_pos < length and (expression[next_pos].isdigit() or expression[next_pos] == '.'):
                            # Parse negative number
                            match = number_pattern.match(expression, next_pos)
                            if match:
                                num_str = '-' + match.group(0)
                                tokens.append(float(num_str))
                                position = next_pos + len(match.group(0))
                                continue
                            else:
                                raise ValueError(f"Invalid number after unary minus at position {position}.")
                        elif next_pos < length and expression[next_pos] == '(':
                            # Negative parenthesis expression: treat as '0 - ( ... )'
                            tokens.append(0.0)
                            tokens.append('-')
                            position += 1
                            continue
                        else:
                            raise ValueError(f"Invalid use of unary minus at position {position}.")
                    else:
                        tokens.append('-')
                        position += 1
                        continue
                else:
                    tokens.append(ch)
                    position += 1
                    continue

            raise ValueError(f"Invalid character '{ch}' at position {position}.")

        # Validation: check for unbalanced parentheses
        if tokens.count('(') != tokens.count(')'):
            raise ValueError("Unbalanced parentheses in expression.")

        return tokens

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts infix tokens to Reverse Polish Notation using the shunting yard algorithm.

        :param tokens: List of tokens in infix order.
        :return: List of tokens in RPN order.
        :raises ValueError: For syntax errors (e.g., mismatched parentheses).
        """
        output = []
        stack = []

        for token in tokens:
            if isinstance(token, float):
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
                if not stack or stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token '{token}' in expression.")

        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Mismatched parentheses in expression.")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, rpn_tokens: List[Union[str, float]]) -> float:
        """
        Evaluates a list of RPN tokens and returns the result.

        :param rpn_tokens: Tokens in RPN order.
        :return: Result as float.
        :raises ValueError: For syntax errors (e.g., insufficient operands).
        :raises ZeroDivisionError: For division by zero.
        """
        stack = []

        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Unknown token '{token}' in RPN evaluation.")

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")

        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies a binary operator to two operands.

        :param a: First operand.
        :param b: Second operand.
        :param operator: Operator as string.
        :return: Result as float.
        :raises ZeroDivisionError: For division by zero.
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero.")
            return a / b
        else:
            raise ValueError(f"Unsupported operator '{operator}'.")

if __name__ == "__main__":
    # Example usage and simple test cases
    calculator = Calculator()
    test_expressions = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-5 + 2",
        "4 / 2 + (6 - 3) * 2",
        "-(3 + 2) * 4.5",
        "3.5 + 2.5 * 2",
        "10 / (5 - 5)",  # Division by zero
        "((2 + 3) * 4",  # Unbalanced parentheses
        "2 + $",         # Invalid character
        "-(-2 + 3)"      # Nested unary minus
    ]

    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
