
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    operator precedence, and both integers and floating-point numbers (including negatives).

    This class follows ISO/IEC 25010 quality standards:
      - Correctness: Produces accurate results for valid expressions.
      - Performance: Uses efficient algorithms (shunting yard & stack-based evaluation).
      - Modularity: Separates tokenization, parsing, and evaluation.
      - Safety: Validates input, handles errors, avoids unsafe operations.
      - Testability: Well-structured for unit testing.
      - Readability: Well-documented and readable code.
    """

    # Define allowed operators and their precedence
    OPERATORS = {
        '+': (1, 'left'),
        '-': (1, 'left'),
        '*': (2, 'left'),
        '/': (2, 'left'),
    }

    # Token regex patterns
    TOKEN_SPEC = [
        ('NUMBER',   r'-?\d+(\.\d+)?'),  # Integer or decimal number (with optional negative sign)
        ('OP',       r'[+\-*/]'),        # Arithmetic operators
        ('LPAREN',   r'\('),             # Left parenthesis
        ('RPAREN',   r'\)'),             # Right parenthesis
        ('SKIP',     r'[ \t]+'),         # Skip spaces and tabs
        ('MISMATCH', r'.'),              # Any other character
    ]
    TOKEN_REGEX = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC))

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression.

        Args:
            expression (str): The arithmetic expression as a string.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid, contains unbalanced parentheses or invalid characters.
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Convert the input string into a list of tokens (numbers, operators, parentheses).

        Args:
            expression (str): The arithmetic expression.

        Returns:
            List[Union[str, float]]: List of tokens.

        Raises:
            ValueError: If the input contains invalid characters or malformed numbers.
        """
        tokens = []
        prev_token = None

        # Preprocessing: remove leading/trailing whitespace
        expression = expression.strip()
        pos = 0
        while pos < len(expression):
            match = self.TOKEN_REGEX.match(expression, pos)
            if not match:
                raise ValueError(f"Invalid token at position {pos}")

            kind = match.lastgroup
            value = match.group()

            if kind == 'NUMBER':
                # Accept negative numbers only if at the start or after '(' or operator
                if (prev_token in (None, 'LPAREN', 'OP')) or (
                    prev_token == 'NUMBER' and value.startswith('-') and not value[1:].replace('.', '', 1).isdigit()
                ):
                    try:
                        num = float(value)
                    except Exception:
                        raise ValueError(f"Malformed number: {value}")
                    tokens.append(num)
                    prev_token = 'NUMBER'
                else:
                    # Handle missing operator (e.g., "2 3"), which is invalid
                    raise ValueError(f"Missing operator before number at position {pos}: '{value}'")
            elif kind == 'OP':
                # Handle unary minus for negative numbers
                if value == '-' and (prev_token in (None, 'LPAREN', 'OP')):
                    # Look ahead for a number
                    num_match = re.match(r'-?\d+(\.\d+)?', expression[match.end():])
                    if num_match:
                        num_value = value + num_match.group()
                        try:
                            num = float(num_value)
                        except Exception:
                            raise ValueError(f"Malformed number: {num_value}")
                        tokens.append(num)
                        pos = match.end() + num_match.end()
                        prev_token = 'NUMBER'
                        continue
                    else:
                        raise ValueError(f"Invalid unary minus usage at position {pos}")
                else:
                    tokens.append(value)
                    prev_token = 'OP'
            elif kind == 'LPAREN':
                tokens.append('(')
                prev_token = 'LPAREN'
            elif kind == 'RPAREN':
                tokens.append(')')
                prev_token = 'RPAREN'
            elif kind == 'SKIP':
                pass  # Ignore whitespace
            elif kind == 'MISMATCH':
                raise ValueError(f"Invalid character '{value}' at position {pos}")
            pos = match.end()
        self._validate_parentheses(tokens)
        self._validate_token_sequence(tokens)
        return tokens

    def _validate_parentheses(self, tokens: List[Union[str, float]]) -> None:
        """
        Validates that parentheses are balanced.

        Args:
            tokens (List[Union[str, float]]): List of tokens.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: too many ')'")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: too many '('")

    def _validate_token_sequence(self, tokens: List[Union[str, float]]) -> None:
        """
        Validate token order for obvious syntax errors.

        Args:
            tokens (List[Union[str, float]]): List of tokens.

        Raises:
            ValueError: On invalid token order.
        """
        if not tokens:
            raise ValueError("Empty expression")

        prev_token_type = None
        for idx, token in enumerate(tokens):
            if isinstance(token, float):
                token_type = 'NUMBER'
            elif token in self.OPERATORS:
                token_type = 'OP'
            elif token == '(':
                token_type = 'LPAREN'
            elif token == ')':
                token_type = 'RPAREN'
            else:
                raise ValueError(f"Unknown token: {token}")

            # No two adjacent numbers or adjacent operators (except unary - handled earlier)
            if prev_token_type == 'NUMBER' and token_type == 'NUMBER':
                raise ValueError(f"Missing operator between numbers at position {idx}")
            if prev_token_type == 'OP' and token_type == 'OP':
                raise ValueError(f"Missing operand between operators at position {idx}")
            if prev_token_type == 'LPAREN' and token_type == 'RPAREN':
                raise ValueError(f"Empty parentheses at position {idx}")
            prev_token_type = token_type

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Convert a list of tokens in infix notation to Reverse Polish Notation (RPN)
        using the shunting yard algorithm.

        Args:
            tokens (List[Union[str, float]]): List of tokens.

        Returns:
            List[Union[str, float]]: RPN token list.

        Raises:
            ValueError: On invalid operator or parentheses usage.
        """
        output_queue: List[Union[str, float]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and operator_stack[-1] in self.OPERATORS):
                    top_op = operator_stack[-1]
                    token_prec, token_assoc = self.OPERATORS[token]
                    top_prec, _ = self.OPERATORS[top_op]
                    if (token_assoc == 'left' and token_prec <= top_prec) or \
                       (token_assoc == 'right' and token_prec < top_prec):
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
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop '('
            else:
                raise ValueError(f"Unknown token during parsing: {token}")

        while operator_stack:
            if operator_stack[-1] in ('(', ')'):
                raise ValueError("Mismatched parentheses at end")
            output_queue.append(operator_stack.pop())
        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Union[str, float]]) -> float:
        """
        Evaluate a list of RPN tokens.

        Args:
            rpn_tokens (List[Union[str, float]]): List of tokens in RPN order.

        Returns:
            float: The result of the calculation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: For invalid operations.
        """
        stack: List[float] = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: left extra operands")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Apply an operator to two operands.

        Args:
            a (float): Left operand.
            b (float): Right operand.
            operator (str): Operator symbol.

        Returns:
            float: Result.

        Raises:
            ZeroDivisionError: On division by zero.
            ValueError: On unknown operator.
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {operator}")


if __name__ == "__main__":
    # Example usage and simple tests
    calc = Calculator()
    test_cases = [
        "1 + 2",
        "2 * (3 + 4)",
        "(2 + 3) * 4.5",
        "7 / 2",
        "-3.5 + 2",
        "3 + 4 * 2 / (1 - 5)",
        "((1 + 2.5) * 3) - 4 / 2",
        "1 + (2 * (3 + (4 * (5 - 6))))",
        "1 / 0",  # Should raise ZeroDivisionError
        "2 + (3", # Should raise ValueError (unbalanced parenthesis)
        "abc + 1", # Should raise ValueError (invalid character)
        "2 ** 3",  # Should raise ValueError (unsupported operator)
    ]
    for expr in test_cases:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
