
from typing import List, Union


class Calculator:
    """
    Console-based arithmetic calculator.

    Supports +, -, *, /, parentheses, floating-point/integer numbers, and negative values.
    Evaluates expressions in string form.
    Ensures input validation and operator precedence without using eval().
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression.

        Args:
            expression (str): Arithmetic expression to evaluate

        Returns:
            float: Result of the evaluation

        Raises:
            ValueError: For syntax errors, invalid input, or math errors (e.g., division by zero)
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._infix_to_rpn(tokens)
        return self._evaluate_rpn(rpn)

    # ------------------------------- Tokenizer -------------------------------

    def _tokenize(self, expr: str) -> List[str]:
        """
        Convert input string into a list of tokens.

        Args:
            expr (str): Input expression

        Returns:
            List[str]: List of tokens

        Raises:
            ValueError: For invalid characters
        """
        tokens = []
        i = 0
        length = len(expr)
        while i < length:
            char = expr[i]

            # Skip whitespace
            if char.isspace():
                i += 1
                continue

            # Number token (supports unary minus)
            if char.isdigit() or char == '.':
                num, n = self._read_number(expr, i)
                tokens.append(num)
                i = n
                continue

            # Operator or parenthesis
            if char in '+-*/()':
                # Check for unary minus (negative numbers)
                if char == '-':
                    if self._is_unary_minus(tokens, i, expr):
                        num, n = self._read_number(expr, i)
                        tokens.append(num)
                        i = n
                        continue
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Invalid character found: '{char}'")

        return tokens

    def _read_number(self, expr: str, i: int) -> (str, int):
        """
        Parse a number, possibly a floating point or negative.

        Args:
            expr (str): Expression string
            i (int): Current cursor position

        Returns:
            Tuple[str, int]: (number_token, new_cursor_pos)
        """
        num = ""
        if expr[i] == '-':
            num += '-'
            i += 1

        dot_seen = False
        digit_seen = False
        while i < len(expr):
            c = expr[i]
            if c.isdigit():
                num += c
                digit_seen = True
            elif c == '.':
                if dot_seen:
                    break
                dot_seen = True
                num += c
            else:
                break
            i += 1

        if not digit_seen:
            raise ValueError("Invalid number format.")
        return (num, i)

    def _is_unary_minus(self, tokens: List[str], idx: int, expr: str) -> bool:
        """
        Determine whether a '-' is unary (negative sign) or binary (subtraction).

        Args:
            tokens (List[str]): Current tokens parsed
            idx (int): Index in input string
            expr (str): Input string

        Returns:
            bool: True if unary minus, else False
        """
        if not tokens:
            return True  # Start of expression
        prev_token = tokens[-1]
        if prev_token in "(*+/-":
            return True
        # Also check previous chars in string (whitespace might be in between)
        j = idx - 1
        while j >= 0 and expr[j].isspace():
            j -= 1
        if j < 0 or expr[j] in "(*+/-":
            return True
        return False

    # --------------------------- Token Validation ----------------------------

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validate tokens for correct parenthesis, structure, and allowable elements.

        Args:
            tokens (List[str]): Expression tokens

        Raises:
            ValueError: For unbalanced parentheses or consecutive operator errors
        """
        paren_count = 0
        prev_token = None
        for idx, t in enumerate(tokens):
            if t == '(':
                paren_count += 1
            elif t == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: Too many ')'")
            elif t in '+-*/':
                if prev_token is None or prev_token in '+-*/(':
                    # Allow unary minus, but not other operators
                    if t != '-':
                        raise ValueError("Operator used without left-hand operand.")
            else:
                # Should be a number; validate using float conversion
                try:
                    float(t)
                except ValueError:
                    raise ValueError(f"Invalid number token: {t}")
            prev_token = t
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: Too many '('")
        if prev_token in '+-*/':
            raise ValueError("Expression cannot end with an operator.")

    # ------------------------------- Parsing ---------------------------------

    def _infix_to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Convert the infix token list to Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

        Args:
            tokens (List[str]): Infix tokens

        Returns:
            List[Union[str, float]]: RPN output tokens
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operators = []

        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in '+-*/':
                while (operators and operators[-1] != '(' and
                       precedence.get(operators[-1], 0) >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if not operators:
                    raise ValueError("Mismatched parentheses detected.")
                operators.pop()  # Remove '('
        while operators:
            if operators[-1] in '()':
                raise ValueError("Mismatched parentheses detected.")
            output.append(operators.pop())

        return output

    def _is_number(self, token: str) -> bool:
        """Check if a string token is a valid number."""
        try:
            float(token)
            return True
        except Exception:
            return False

    # --------------------------- RPN Evaluation ------------------------------

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluate an expression in Reverse Polish Notation.

        Args:
            rpn (List[Union[str, float]]): RPN tokens

        Returns:
            float: Computed result

        Raises:
            ZeroDivisionError: Division by zero
            ValueError: Invalid syntax (e.g. stack size mismatch)
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in '+-*/':
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: Not enough values for operation.")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero not allowed.")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Unexpected token in evaluation: {token}")
        if len(stack) != 1:
            raise ValueError("The user input has too many values and not enough operators.")
        return stack[0]


# ------------------- Example Usage & Simple Test Cases ------------------------

if __name__ == "__main__":
    calc = Calculator()
    expressions = [
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "-4 + 5.5 * (3 - 2.5) / 2",
        "3 / (3 - 3)",             # Should raise ZeroDivisionError
        "12 + * 2",                # Invalid
        "((2 + 2) * 3",            # Unbalanced
        "1.23 + -4.56"
    ]

    for expr in expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {str(e)}")
