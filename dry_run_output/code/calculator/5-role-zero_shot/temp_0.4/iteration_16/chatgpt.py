
"""
Console-based arithmetic calculator implemented according to ISO/IEC 25010 quality standards.

Features:
- Supports +, -, *, /, and parentheses.
- Respects operator precedence.
- Accepts integers and floating-point numbers, including negatives.
- Provides robust input validation and clear error messages.
- OOP design: Calculator class with calculate(expression: str) -> float.

Author: Senior Software Developer
"""
import re
from typing import List, Union

class CalculatorError(Exception):
    """Custom exception class for calculator errors."""
    pass


class Calculator:
    """
    Arithmetic calculator supporting basic operations and parentheses.

    Usage:
        calc = Calculator()
        result = calc.calculate("3 + (2 * 4) / 2")
    """

    # Allowed operators and their precedence and associativity
    _OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L'),
    }

    # Regex pattern: numbers, operators, parentheses, and whitespace
    _TOKEN_PATTERN = re.compile(r"""
        (?P<NUMBER>    -?\d+(\.\d+)?    ) |   # Integer or float number (with optional negative sign)
        (?P<OP>        [+\-*/]           ) |   # Operators
        (?P<LPAREN>    \(                ) |   # Left parenthesis
        (?P<RPAREN>    \)                ) |   # Right parenthesis
        (?P<SPACE>     \s+               )     # Whitespace
    """, re.VERBOSE)

    def calculate(self, expression: str) -> float:
        """
        Parses and evaluates the arithmetic expression.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If the input is invalid (e.g., syntax error, division by zero).
        """
        try:
            tokens = self._tokenize(expression)
            rpn = self._infix_to_rpn(tokens)
            result = self._evaluate_rpn(rpn)
            return result
        except CalculatorError as e:
            raise ValueError(f"Invalid input: {e}")

    # --------------------- Internal Methods ---------------------

    def _tokenize(self, expr: str) -> List[Union[str, float]]:
        """
        Tokenizes the input string into numbers, operators, and parentheses.

        Args:
            expr (str): The input expression.

        Returns:
            List[Union[str, float]]: List of tokens.

        Raises:
            CalculatorError: On unrecognized characters or malformed numbers.
        """
        tokens = []
        idx = 0
        length = len(expr)
        last_token = None
        while idx < length:
            match = self._TOKEN_PATTERN.match(expr, idx)
            if not match:
                raise CalculatorError(f"Invalid character at position {idx+1}: '{expr[idx]}'")
            # Process matched token
            if match.lastgroup == 'NUMBER':
                num_str = match.group('NUMBER')
                try:
                    num = float(num_str)
                except ValueError:
                    raise CalculatorError(f"Malformed number: {num_str}")
                tokens.append(num)
                last_token = 'NUMBER'
            elif match.lastgroup == 'OP':
                op = match.group('OP')
                # Detect unary minus: If first token or after '(', or another operator
                if op == '-' and (last_token is None or last_token in ('OP', 'LPAREN')):
                    # Look ahead to next number
                    num_match = self._TOKEN_PATTERN.match(expr, match.end())
                    if num_match and num_match.lastgroup == 'NUMBER':
                        num_str = '-' + num_match.group('NUMBER')
                        try:
                            num = float(num_str)
                        except ValueError:
                            raise CalculatorError(f"Malformed number: {num_str}")
                        tokens.append(num)
                        idx = num_match.end()
                        last_token = 'NUMBER'
                        continue  # skip standard idx update
                    else:
                        raise CalculatorError(f"Unexpected unary minus at position {idx+1}")
                tokens.append(op)
                last_token = 'OP'
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
                last_token = 'LPAREN'
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
                last_token = 'RPAREN'
            # Ignore spaces
            idx = match.end()
        self._validate_parentheses(tokens)
        self._validate_token_sequence(tokens)
        return tokens

    def _validate_parentheses(self, tokens: List[Union[str, float]]) -> None:
        """
        Validates that parentheses are balanced.

        Args:
            tokens: List of tokens.

        Raises:
            CalculatorError: If parentheses are unbalanced.
        """
        balance = 0
        for token in tokens:
            if token == '(':
                balance += 1
            elif token == ')':
                balance -= 1
                if balance < 0:
                    raise CalculatorError("Unbalanced parentheses: too many ')'")
        if balance != 0:
            raise CalculatorError("Unbalanced parentheses: too many '('")

    def _validate_token_sequence(self, tokens: List[Union[str, float]]) -> None:
        """
        Performs basic syntax checks (e.g., no consecutive operators, empty parentheses).

        Args:
            tokens: List of tokens.

        Raises:
            CalculatorError: On invalid token sequences.
        """
        types = []
        for t in tokens:
            if isinstance(t, float):
                types.append('NUMBER')
            elif t in self._OPERATORS:
                types.append('OP')
            elif t == '(':
                types.append('LPAREN')
            elif t == ')':
                types.append('RPAREN')
        prev = None
        for idx, t in enumerate(types):
            if t == 'OP' and (prev is None or prev in ('OP', 'LPAREN')):
                # Prevent consecutive operators (except unary minus handled in tokenizer)
                raise CalculatorError("Invalid operator sequence.")
            if t == 'RPAREN' and (prev is None or prev in ('OP', 'LPAREN')):
                # Prevent empty or invalid parentheses
                raise CalculatorError("Empty or misplaced parentheses.")
            if t == 'LPAREN' and prev == 'RPAREN':
                raise CalculatorError("Missing operator between ')('")
            prev = t

    def _infix_to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts infix expression to Reverse Polish Notation (RPN) using Shunting Yard.

        Args:
            tokens: List of tokens in infix order.

        Returns:
            List of tokens in RPN order.

        Raises:
            CalculatorError: On any logic error during conversion.
        """
        output = []
        stack = []
        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS and
                       ((self._OPERATORS[token][1] == 'L' and self._OPERATORS[token][0] <= self._OPERATORS[stack[-1]][0]) or
                        (self._OPERATORS[token][1] == 'R' and self._OPERATORS[token][0] < self._OPERATORS[stack[-1]][0]))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise CalculatorError("Mismatched parentheses during processing.")
                stack.pop()  # Remove '('
        while stack:
            if stack[-1] in ('(', ')'):
                raise CalculatorError("Mismatched parentheses at output.")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, tokens: List[Union[str, float]]) -> float:
        """
        Evaluates the RPN expression.

        Args:
            tokens: List of tokens in RPN order.

        Returns:
            float: Result.

        Raises:
            CalculatorError: For division by zero, or malformed expression.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise CalculatorError("Malformed expression.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise CalculatorError(f"Unexpected token in RPN: {token}")
        if len(stack) != 1:
            raise CalculatorError("Malformed input: too many values.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """
        Applies an operator to two operands.

        Args:
            a (float): Left operand.
            b (float): Right operand.
            op (str): Operator.

        Returns:
            float: The result.

        Raises:
            CalculatorError: On division by zero.
        """
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0.0:
                raise CalculatorError("Division by zero.")
            return a / b
        else:
            raise CalculatorError(f"Unsupported operator: {op}")

# ------------------------- Example Usage -------------------------

if __name__ == "__main__":
    calc = Calculator()
    # Simple console loop for demonstration purposes
    print("High-Quality Calculator (Type 'exit' to quit)")
    while True:
        expr = input("Enter an arithmetic expression: ").strip()
        if expr.lower() in {'exit', 'quit'}:
            break
        if not expr:
            continue
        try:
            result = calc.calculate(expr)
            print(f"= {result}")
        except ValueError as e:
            print(e)
