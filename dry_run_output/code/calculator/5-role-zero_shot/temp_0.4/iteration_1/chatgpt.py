
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.
    Adheres to ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'left'},
        '-': {'precedence': 1, 'associativity': 'left'},
        '*': {'precedence': 2, 'associativity': 'left'},
        '/': {'precedence': 2, 'associativity': 'left'}
    }

    # Pattern for valid tokens: numbers, operators, parentheses, and whitespace
    TOKEN_PATTERN = re.compile(
        r"""
        (?P<number>    -?\d+(\.\d+)? ) |   # Integer or decimal, possibly negative
        (?P<operator>  [+\-*/]        ) |   # Operators
        (?P<paren>     [()]           ) |   # Parentheses
        (?P<space>     \s+            )     # Whitespace
        """,
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        :param expression: The arithmetic expression as a string.
        :return: The evaluated result as a float.
        :raises ValueError: If the expression is invalid.
        :raises ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Tokenizes the input expression into numbers, operators, and parentheses.

        :param expression: The arithmetic expression as a string.
        :return: List of tokens.
        :raises ValueError: If invalid characters or unbalanced parentheses are found.
        """
        tokens = []
        position = 0
        last_token = None

        while position < len(expression):
            match = self.TOKEN_PATTERN.match(expression, position)
            if not match:
                raise ValueError(f"Invalid character at position {position}: '{expression[position]}'")

            if match.lastgroup == 'number':
                number_str = match.group('number')
                tokens.append(float(number_str))
                last_token = 'number'
            elif match.lastgroup == 'operator':
                op = match.group('operator')
                # Handle unary minus for negative numbers
                if op == '-' and (last_token is None or last_token in ('operator', 'paren_open')):
                    # Look ahead for a number
                    next_match = self.TOKEN_PATTERN.match(expression, match.end())
                    if next_match and next_match.lastgroup == 'number':
                        # Merge '-' with the number
                        number_str = '-' + next_match.group('number')
                        tokens.append(float(number_str))
                        position = next_match.end() - 1  # -1 because position will be incremented at end
                        last_token = 'number'
                    else:
                        # It's a standalone unary minus (e.g., "-(3+4)")
                        tokens.append(op)
                        last_token = 'operator'
                else:
                    tokens.append(op)
                    last_token = 'operator'
            elif match.lastgroup == 'paren':
                paren = match.group('paren')
                tokens.append(paren)
                last_token = 'paren_open' if paren == '(' else 'paren_close'
            # Ignore whitespace
            position = match.end()

        # Validate parentheses balance
        if not self._parentheses_balanced(tokens):
            raise ValueError("Unbalanced parentheses in expression.")

        return tokens

    def _parentheses_balanced(self, tokens: List[Union[str, float]]) -> bool:
        """
        Checks if parentheses are balanced in the token list.

        :param tokens: List of tokens.
        :return: True if balanced, False otherwise.
        """
        balance = 0
        for token in tokens:
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts the list of tokens from infix to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        :param tokens: List of tokens.
        :return: List of tokens in RPN order.
        :raises ValueError: If the expression is invalid.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and operator_stack[-1] in self.OPERATORS and
                       ((self.OPERATORS[token]['associativity'] == 'left' and
                         self.OPERATORS[token]['precedence'] <= self.OPERATORS[operator_stack[-1]]['precedence']) or
                        (self.OPERATORS[token]['associativity'] == 'right' and
                         self.OPERATORS[token]['precedence'] < self.OPERATORS[operator_stack[-1]]['precedence']))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Remove '('
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            op = operator_stack.pop()
            if op in ('(', ')'):
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Union[str, float]]) -> float:
        """
        Evaluates the expression in Reverse Polish Notation.

        :param rpn_tokens: List of tokens in RPN order.
        :return: The evaluated result as a float.
        :raises ZeroDivisionError: If division by zero occurs.
        :raises ValueError: If the expression is invalid.
        """
        stack = []

        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")

        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operator to two operands.

        :param a: Left operand.
        :param b: Right operand.
        :param operator: Operator as a string.
        :return: Result of the operation.
        :raises ZeroDivisionError: If division by zero occurs.
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
            raise ValueError(f"Unsupported operator: {operator}")

# Example usage and simple test cases
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",               # 7.0
        "(1 + 2) * 3",             # 9.0
        "-5 + 3 * (2 - 4.5)",      # -12.5
        "10 / 2 + 3 * 4 - 7",      # 9.0
        "((2.5 + 2.5) * 2) / 2",   # 5.0
        "-(3 + 4) * 2",            # -14.0
        "3 + -2 * 4",              # -5.0
        "3 + (-2) * 4",            # -5.0
        "3.5 + 2.1",               # 5.6
        "4 / 0",                   # ZeroDivisionError
        "2 + (3 * 4",              # ValueError (unbalanced parentheses)
        "2 + a",                   # ValueError (invalid character)
    ]

    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
