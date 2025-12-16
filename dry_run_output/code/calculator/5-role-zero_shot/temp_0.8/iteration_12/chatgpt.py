
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integer/float numbers (including negatives), following operator precedence.

    Implements:
        - calculate(expression: str) -> float
    """

    # Supported operators and their precedence/associativity
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'}
    }

    # Allowed characters regex for validation
    VALID_PATTERN = re.compile(r"^[\d\s+\-*/().]+$")

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression string and return the result as float.

        :param expression: str, arithmetic expression
        :return: float, result
        :raises ValueError: for invalid input
        :raises ZeroDivisionError: for division by zero
        """
        sanitized = self._sanitize_input(expression)
        tokens = self._tokenize(sanitized)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _sanitize_input(self, expression: str) -> str:
        """Remove spaces and check for invalid characters."""
        if not isinstance(expression, str):
            raise ValueError("Input expression must be a string.")
        expr = expression.replace(' ', '')
        if not expr:
            raise ValueError("Empty expression is not allowed.")
        if not self.VALID_PATTERN.match(expr):
            raise ValueError("Expression contains invalid characters.")
        return expr

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Tokenizes the input string into numbers, operators, and parentheses.
        Handles negative numbers and validates parentheses.
        """
        tokens = []
        num_buff = ''
        i = 0
        n = len(expression)
        parentheses_count = 0

        while i < n:
            c = expression[i]

            if c in '0123456789.':
                num_buff += c
            elif c in self.OPERATORS:
                # Handle negative numbers (unary minus)
                if c == '-' and (i == 0 or expression[i - 1] in self.OPERATORS or expression[i - 1] == '('):
                    num_buff += c
                else:
                    if num_buff:
                        tokens.append(self._parse_number(num_buff))
                        num_buff = ''
                    tokens.append(c)
            elif c == '(':
                if num_buff:
                    tokens.append(self._parse_number(num_buff))
                    num_buff = ''
                tokens.append(c)
                parentheses_count += 1
            elif c == ')':
                if num_buff:
                    tokens.append(self._parse_number(num_buff))
                    num_buff = ''
                tokens.append(c)
                parentheses_count -= 1
                if parentheses_count < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'.")
            else:
                raise ValueError(f"Invalid character '{c}' in expression.")
            i += 1

        if num_buff:
            tokens.append(self._parse_number(num_buff))

        if parentheses_count != 0:
            raise ValueError("Unbalanced parentheses: mismatched '(' and ')'.")

        return tokens

    def _parse_number(self, value: str) -> float:
        """Parse the number from string, raises ValueError if invalid."""
        try:
            number = float(value)
        except ValueError:
            raise ValueError(f"Invalid number '{value}'.")
        return number

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Convert list of tokens (infix) to RPN (postfix) using the Shunting Yard algorithm.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and operator_stack[-1] in self.OPERATORS):
                    top_op = operator_stack[-1]
                    curr_op = token
                    # Check precedence and associativity
                    if (
                        (self.OPERATORS[curr_op]['associativity'] == 'L' and
                         self.OPERATORS[curr_op]['precedence'] <= self.OPERATORS[top_op]['precedence'])
                    ):
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses: ')' without '('.")
                operator_stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token '{token}'.")

        while operator_stack:
            if operator_stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses.")
            output_queue.append(operator_stack.pop())
        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Union[str, float]]) -> float:
        """Evaluate the postfix (RPN) expression."""
        stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Unknown token in RPN: '{token}'.")
        if len(stack) != 1:
            raise ValueError("Invalid expression: Too many operands.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """Apply arithmetic operator to two operands, check for division by zero."""
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

# Example usage and test cases (for manual testing, remove or comment out if imported as a module)
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "2 + 3 * 4",                          # 14.0
        "2 - 5 / (8 - 3)",                    # 1.0
        "3.5 + (-2.4)",                       # 1.1
        "7 * (4 + (-3)) / 2",                 # 3.5
        "((3.5 + 2.5) * 2 - 1) / 2",          # 4.0
        "-2 + 3",                             # 1.0
        "2 + 3 * (4 - 1) / (6 / 2)",          # 5.5
        "((1))",                              # 1.0
        "-3 * -2.5",                          # 7.5
        "(4 + 2) / (1 - 1)",                  # Should raise ZeroDivisionError
        "abc + 2",                            # Should raise ValueError (invalid characters)
        "5 / (3 - 3",                         # Should raise ValueError (unbalanced parentheses)
        "",                                   # Should raise ValueError (empty expression)
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} ERROR: {e}")
