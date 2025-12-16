
from typing import List, Union

class CalculatorError(Exception):
    """Base exception class for Calculator errors."""
    pass

class InvalidCharacterError(CalculatorError, ValueError):
    """Raised when input contains invalid characters."""
    pass

class UnbalancedParenthesesError(CalculatorError, ValueError):
    """Raised when parentheses are unbalanced."""
    pass

class DivisionByZeroError(CalculatorError, ZeroDivisionError):
    """Raised when division by zero is attempted."""
    pass

class Calculator:
    """
    Console-based arithmetic calculator.

    Supports: +, -, *, /, parentheses, integers, floats, negatives.
    Adheres to ISO/IEC 25010 regarding correctness, robustness, and maintainability.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate the arithmetic expression.

        Args:
            expression (str): Arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            InvalidCharacterError: If the expression contains invalid characters.
            UnbalancedParenthesesError: If parentheses are unbalanced.
            DivisionByZeroError: If division by zero is attempted.
            ValueError: If the syntax is invalid.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    # ---- Tokenization ----

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Convert the input string into a list of tokens.

        Numbers are converted to float, operators and parentheses stay as strings.

        Args:
            expression (str): Arithmetic expression as a string.

        Returns:
            List[Union[str, float]]: List of tokens.

        Raises:
            InvalidCharacterError: On invalid characters.
            UnbalancedParenthesesError: On parenthesis errors.
        """
        VALID_CHARS = set('0123456789.+-*/() ')
        tokens = []
        i, length = 0, len(expression)
        last_token = None  # To distinguish unary/binary minus

        while i < length:
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char not in VALID_CHARS:
                raise InvalidCharacterError(f"Invalid character '{char}' in expression.")

            if char in '+*/':
                tokens.append(char)
                last_token = char
                i += 1
            elif char == '-':
                # Determine unary or binary minus
                if (
                    last_token is None or
                    (isinstance(last_token, str) and last_token in '+-*/(')
                ):
                    # Unary minus; scan number after the minus
                    j = i + 1
                    num_str = '-'
                    dot_count = 0
                    while j < length and (expression[j].isdigit() or expression[j] == '.'):
                        if expression[j] == '.':
                            dot_count += 1
                            if dot_count > 1:
                                break  # Only one dot allowed per number
                        num_str += expression[j]
                        j += 1
                    if num_str == '-':
                        raise InvalidCharacterError(f"Invalid unary minus at position {i}.")
                    try:
                        tokens.append(float(num_str))
                    except ValueError:
                        raise InvalidCharacterError(f"Invalid number: '{num_str}'")
                    last_token = num_str
                    i = j
                else:
                    # Binary minus
                    tokens.append('-')
                    last_token = '-'
                    i += 1
            elif char.isdigit() or char == '.':
                # Parse number (int/float)
                j = i
                num_str = ''
                dot_count = 0
                while j < length and (expression[j].isdigit() or expression[j] == '.'):
                    if expression[j] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            break  # Only one dot allowed per number
                    num_str += expression[j]
                    j += 1
                if not num_str or num_str == '.':
                    raise InvalidCharacterError(f"Invalid number at position {i}: '{num_str}'")
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise InvalidCharacterError(f"Invalid number: '{num_str}'")
                last_token = num_str
                i = j
            elif char in '()':
                tokens.append(char)
                last_token = char
                i += 1
            else:
                raise InvalidCharacterError(f"Unknown parsing error at position {i}.")
        # Parentheses balance check
        if tokens.count('(') != tokens.count(')'):
            raise UnbalancedParenthesesError("Parentheses are unbalanced.")
        return tokens

    # ---- Shunting Yard: Convert to Postfix (RPN) ----

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts infix token list to postfix (RPN) token list using Shunting Yard.

        Args:
            tokens (List[Union[str, float]]): Infix expression as token list.

        Returns:
            List[Union[str, float]]: RPN/postfix notation as token list.

        Raises:
            UnbalancedParenthesesError: For parenthesis mismatches.
            ValueError: For syntax errors.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        op_stack = []
        for token in tokens:
            if isinstance(token, float):  # Number
                output.append(token)
            elif token in '+-*/':
                while (
                    op_stack and
                    op_stack[-1] in '+-*/' and
                    precedence[op_stack[-1]] >= precedence[token]
                ):
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    output.append(op_stack.pop())
                if not op_stack or op_stack[-1] != '(':
                    raise UnbalancedParenthesesError("Mismatched parentheses.")
                op_stack.pop()  # Remove '('
            else:
                raise InvalidCharacterError(f"Unexpected token: {token}")
        while op_stack:
            if op_stack[-1] == '(' or op_stack[-1] == ')':
                raise UnbalancedParenthesesError("Mismatched parentheses at end of expression.")
            output.append(op_stack.pop())
        return output

    # ---- Evaluate RPN ----

    def _evaluate_rpn(self, tokens: List[Union[str, float]]) -> float:
        """
        Evaluates an RPN expression.

        Args:
            tokens (List[Union[str, float]]): RPN tokens.

        Returns:
            float: result

        Raises:
            DivisionByZeroError: For division by zero.
            ValueError: For syntax errors (e.g. stack underflow).
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in '+-*/':
                if len(stack) < 2:
                    raise ValueError("Insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    res = a + b
                elif token == '-':
                    res = a - b
                elif token == '*':
                    res = a * b
                elif token == '/':
                    if b == 0:
                        raise DivisionByZeroError("Division by zero.")
                    res = a / b
                stack.append(res)
            else:
                raise InvalidCharacterError(f"Invalid token in RPN: {token}.")
        if len(stack) != 1:
            raise ValueError("The expression is invalid or incomplete.")
        return stack.pop()

# ---- (Example usage & test) ----

if __name__ == "__main__":
    calculator = Calculator()
    expressions = [
        "3 + 4 * 2 / (1 - 5)",
        "-2.5 + (3 * (4 - 1.5))",
        "((3+2)*(-1.1))/2.0",
        "10 / 0",                         # Should raise DivisionByZeroError
        "5 + (2+3",                       # Should raise UnbalancedParenthesesError
        "abc + 2",                        # Should raise InvalidCharacterError
        "5 + * 3",                        # Should raise ValueError (syntax error)
        "-3.5",
        "1.5 + 2.5 * 3.5 - 4.5 / (-1.5)",
    ]
    for expr in expressions:
        try:
            result = calculator.calculate(expr)
            print(f"{expr} = {result}")
        except CalculatorError as e:
            print(f"{expr} -> Error: {e}")
