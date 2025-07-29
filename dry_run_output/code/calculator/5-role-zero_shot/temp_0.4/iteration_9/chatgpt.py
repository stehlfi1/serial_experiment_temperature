
import re
from typing import List, Union


class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers and floating-point numbers (including negatives).
    Adheres to ISO/IEC 25010 quality requirements.
    """

    # Supported operators and their precedence/associativity
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
            ValueError: For invalid input, such as unbalanced parentheses,
                        invalid characters, or malformed expressions.
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        postfix = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Tokenizes the input expression into numbers, operators, and parentheses.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            List[str]: List of tokens as strings.

        Raises:
            ValueError: If invalid characters are found.
        """
        # Remove whitespace
        expr = expression.replace(' ', '')

        # Regular expression for tokenizing numbers, operators, and parentheses
        token_pattern = re.compile(
            r"""
            (?P<number>
                (?<!\w)          # Not preceded by a word character
                -?              # Optional negative sign
                (?:\d+\.\d*|\.\d+|\d+)  # Float or int
            )
            |(?P<operator>[+\-*/()])
            """,
            re.VERBOSE,
        )

        tokens = []
        idx = 0
        while idx < len(expr):
            match = token_pattern.match(expr, idx)
            if not match:
                raise ValueError(f"Invalid character at position {idx}: '{expr[idx]}'")
            token = match.group()
            tokens.append(token)
            idx = match.end()

        # Handle unary minus (convert to explicit negative numbers)
        tokens = self._handle_unary_minus(tokens)
        return tokens

    def _handle_unary_minus(self, tokens: List[str]) -> List[str]:
        """
        Converts unary minus to explicit negative numbers.

        Args:
            tokens (List[str]): List of tokens.

        Returns:
            List[str]: List of tokens with unary minus handled.
        """
        result = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '-' and (
                i == 0 or tokens[i - 1] in self._OPERATORS or tokens[i - 1] == '('
            ):
                # Unary minus detected
                # Attach to the next number
                if i + 1 < len(tokens) and self._is_number(tokens[i + 1]):
                    result.append(str(-float(tokens[i + 1])))
                    i += 2
                    continue
                else:
                    raise ValueError("Invalid use of unary minus")
            result.append(token)
            i += 1
        return result

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the list of tokens for correct syntax.

        Args:
            tokens (List[str]): List of tokens.

        Raises:
            ValueError: For unbalanced parentheses, invalid sequences, etc.
        """
        # Parentheses balance check
        paren_count = 0
        prev_token = None
        for idx, token in enumerate(tokens):
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
            elif token in self._OPERATORS:
                if prev_token is None or prev_token in self._OPERATORS or prev_token == '(':
                    if token != '-':  # unary minus is handled in tokenize
                        raise ValueError(f"Operator '{token}' not allowed here")
            elif self._is_number(token):
                pass
            else:
                raise ValueError(f"Invalid token: '{token}'")
            prev_token = token
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: too many '('")
        if tokens and tokens[-1] in self._OPERATORS:
            raise ValueError("Expression cannot end with an operator")

    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Converts infix tokens to postfix notation using the Shunting Yard algorithm.

        Args:
            tokens (List[str]): List of tokens in infix notation.

        Returns:
            List[str]: List of tokens in postfix notation.
        """
        output = []
        stack = []

        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in self._OPERATORS:
                while (
                    stack
                    and stack[-1] in self._OPERATORS
                    and (
                        (
                            self._OPERATORS[token]['associativity'] == 'L'
                            and self._OPERATORS[token]['precedence']
                            <= self._OPERATORS[stack[-1]]['precedence']
                        )
                        or (
                            self._OPERATORS[token]['associativity'] == 'R'
                            and self._OPERATORS[token]['precedence']
                            < self._OPERATORS[stack[-1]]['precedence']
                        )
                    )
                ):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                stack.pop()  # Remove '('
        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())
        return output

    def _evaluate_postfix(self, tokens: List[str]) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens (List[str]): List of tokens in postfix notation.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the expression is malformed.
        """
        stack: List[float] = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in evaluation: '{token}'")
        if len(stack) != 1:
            raise ValueError("Malformed expression: too many operands")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operator to two operands.

        Args:
            a (float): Left operand.
            b (float): Right operand.
            operator (str): Operator ('+', '-', '*', '/').

        Returns:
            float: Result of operation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
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
            raise ValueError(f"Unsupported operator: '{operator}'")

    def _is_number(self, token: str) -> bool:
        """
        Checks if a token is a valid number.

        Args:
            token (str): Token to check.

        Returns:
            bool: True if token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    # Example usage and simple test cases
    calculator = Calculator()
    test_expressions = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-4 + 2",
        "3.5 * (2 - 6.7) / 2",
        "10 / 2 + 3 * (4 - 2)",
        "((2 + 3) * (5 - 2)) / 3",
        "-3.5 + 2.1 * 4",
        "3 + -2 * 5",
        "-(2 + 3)",  # Should raise error (unary minus before parentheses not supported)
        "1 / 0",     # Should raise ZeroDivisionError
        "2 + (3 * 4",  # Should raise ValueError (unbalanced parentheses)
        "2 + 3a",      # Should raise ValueError (invalid character)
    ]
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
