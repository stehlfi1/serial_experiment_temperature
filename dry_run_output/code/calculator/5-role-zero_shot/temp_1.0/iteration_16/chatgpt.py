
import re
from typing import List, Union


class CalculatorError(Exception):
    """Base class for calculator exceptions."""
    pass


class InvalidCharacterError(CalculatorError, ValueError):
    """Exception raised for invalid characters in the expression."""
    pass


class UnbalancedParenthesesError(CalculatorError, ValueError):
    """Exception raised for unbalanced parentheses."""
    pass


class DivisionByZeroError(CalculatorError, ZeroDivisionError):
    """Exception raised for division by zero."""
    pass


class Calculator:
    """
    Arithmetic Calculator that evaluates mathematical expressions containing
    +, -, *, / operators and parentheses, with correct precedence.
    """

    # Regular expression for tokenizing the arithmetic expression
    TOKEN_REGEX = re.compile(
        r'\s*('
        r'(?:\d+\.\d+|\d+\.\d*|\.\d+|\d+)'  # numbers (int/float)
        r'|[+\-*/()]'                       # operators and parentheses
        r')\s*'
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result as float.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of evaluating the expression.

        Raises:
            InvalidCharacterError: If the expression contains invalid characters.
            UnbalancedParenthesesError: If the expression has unbalanced parentheses.
            DivisionByZeroError: If division by zero is attempted.
            ValueError: For other value-related errors.
        """
        # Tokenize expression
        tokens = self._tokenize(expression)
        # Convert infix to postfix using the Shunting Yard algorithm
        rpn = self._to_postfix(tokens)
        # Evaluate the postfix expression
        result = self._evaluate_postfix(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Splits the input string into tokens, while checking for invalid characters
        and correctness of parentheses.

        Args:
            expression (str): The expression string.

        Returns:
            List[str]: List of tokens (numbers, operators, parentheses).
        
        Raises:
            InvalidCharacterError: If the expression contains invalid characters.
            UnbalancedParenthesesError: If parentheses are unbalanced.
        """
        tokens = []
        pos = 0
        paren_balance = 0

        while pos < len(expression):
            match = self.TOKEN_REGEX.match(expression, pos)
            if not match:
                raise InvalidCharacterError(
                    f"Invalid character at position {pos}: '{expression[pos]}'")
            token = match.group(1)
            pos = match.end()
            if token in ('(', ')'):
                if token == '(':
                    paren_balance += 1
                else:
                    paren_balance -= 1
                    if paren_balance < 0:
                        raise UnbalancedParenthesesError(
                            "Parentheses are unbalanced: too many ')'")
            tokens.append(token)

        if paren_balance != 0:
            raise UnbalancedParenthesesError(
                "Parentheses are unbalanced: mismatched '(' and ')'")

        # Handle unary minus tokens (convert to 'u-' for easier processing)
        tokens = self._handle_unary_operators(tokens)
        return tokens

    def _handle_unary_operators(self, tokens: List[str]) -> List[str]:
        """
        Processes unary minus to distinguish negative numbers from subtraction.

        Args:
            tokens (List[str]): The tokenized input.

        Returns:
            List[str]: Tokens with unary minus marked as 'u-'.
        """
        result = []
        prev_token = None
        for idx, token in enumerate(tokens):
            if token == '-' and (prev_token is None or prev_token in ('+', '-', '*', '/', '(')):
                # Unary minus detected
                result.append('u-')
            else:
                result.append(token)
            prev_token = result[-1]
        return result

    def _to_postfix(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts tokens from infix to postfix (Reverse Polish Notation) for evaluation.

        Args:
            tokens (List[str]): The tokenized input.

        Returns:
            List[Union[str, float]]: List of postfix tokens.

        Raises:
            ValueError: If the expression contains syntactic errors.
        """
        output = []
        stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        right_associative = {'u-'}
        operators = set(precedence) | {'u-'}

        def is_number(tok):
            try:
                float(tok)
                return True
            except (ValueError, TypeError):
                return False

        for token in tokens:
            if is_number(token):
                output.append(float(token))
            elif token == 'u-':
                stack.append(token)
            elif token in precedence:
                while (stack and stack[-1] in operators and
                       ((stack[-1] not in right_associative and
                         precedence.get(stack[-1], 3) >= precedence[token])
                        or
                        (stack[-1] in right_associative and
                         precedence.get(stack[-1], 3) > precedence[token]))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise UnbalancedParenthesesError("Unmatched ')'")
                stack.pop()  # Remove '('
            else:
                raise InvalidCharacterError(f"Unknown token: {token}")

        while stack:
            if stack[-1] in ('(', ')'):
                raise UnbalancedParenthesesError("Unbalanced parentheses detected at the end of expression")
            output.append(stack.pop())
        return output

    def _evaluate_postfix(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates a postfix (RPN) expression.

        Args:
            rpn (List[Union[str, float]]): The postfix token list.

        Returns:
            float: The result.

        Raises:
            DivisionByZeroError: If a division by zero occurs.
            ValueError: For malformed expression.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token == 'u-':
                if not stack:
                    raise ValueError("Malformed expression: unary minus lacks operand.")
                stack.append(-stack.pop())
            elif token in ('+', '-', '*', '/'):
                try:
                    b = stack.pop()
                    a = stack.pop()
                except IndexError:
                    raise ValueError("Malformed expression: insufficient operands.")
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise InvalidCharacterError(f"Unknown token in evaluation: {token}")
        if len(stack) != 1:
            raise ValueError("Malformed expression: leftover operands.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """
        Applies a binary arithmetic operation.

        Args:
            a (float): Left operand.
            b (float): Right operand.
            op (str): Operator.

        Returns:
            float: Result.

        Raises:
            DivisionByZeroError: If division by zero is attempted.
        """
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0.0:
                raise DivisionByZeroError("Division by zero.")
            return a / b
        else:
            raise InvalidCharacterError(f"Unsupported operator: {op}")


# Example Usage and Testability:
if __name__ == "__main__":
    calc = Calculator()
    test_cases = [
        "2 + 3 * 4",                  # 14.0
        "-2 + 3",                     # 1.0
        "(2 + 3) * 4",                # 20.0
        "3 + 4 * 2 / (1 - 5)",        # 1.0
        "2.5 * (2 - 0.75)",           # 3.125
        "-3 + 4 * -2",                # -11.0
        "((2+3)*2)-3/(1+2)",          # 9.0
        "-(3 + 5) * 2",               # -16.0
        "2 / 0",                      # Division by zero (error)
        "5++2",                       # Malformed expression (error)
        "(2+3",                       # Unbalanced parentheses (error)
        "abc + 3"                     # Invalid character (error)
    ]

    for expr in test_cases:
        print(f"Expression: {expr}")
        try:
            result = calc.calculate(expr)
            print(f"Result: {result}\n")
        except CalculatorError as e:
            print(f"Error: {e}\n")
