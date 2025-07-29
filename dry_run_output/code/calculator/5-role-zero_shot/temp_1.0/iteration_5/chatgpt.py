
"""
A console-based arithmetic calculator that follows the ISO/IEC 25010 quality standards.

- Supports +, -, *, /, parentheses, integers, floats, and negative numbers.
- Validates input, handles errors explicitly, and enforces correct operator precedence.
- Uses object-oriented design.
"""

import re
from typing import List, Union

class Calculator:
    """
    Arithmetic Calculator supporting +, -, *, /, parentheses, and floating-point numbers.
    Usage:
        calc = Calculator()
        result = calc.calculate("1 + 2 * (3 - 4)")
    """

    # Allowed operators and their precedences
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'left'},
        '-': {'precedence': 1, 'associativity': 'left'},
        '*': {'precedence': 2, 'associativity': 'left'},
        '/': {'precedence': 2, 'associativity': 'left'}
    }

    # Regular expression for tokenization
    TOKEN_PATTERN = re.compile(
        r'\s*('
        r'(?P<NUMBER>(?:-)?\d+(?:\.\d+)?)|'      # Integer or float, possibly negative
        r'(?P<OPERATOR>[\+\-\*/])|'              # Arithmetic operators
        r'(?P<PAREN>[\(\)])|'                    # Parentheses
        r'(?P<INVALID>.)'                        # Any other character
        r')'
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The evaluated result.

        Raises:
            ValueError: If the expression is invalid (syntax error, unbalanced parentheses, etc).
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._infix_to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List[str]:
        """
        Converts input string into a list of tokens.

        Handles negative numbers properly.
        """
        tokens = []
        last_token = None
        idx = 0

        while idx < len(expr):
            match = self.TOKEN_PATTERN.match(expr, idx)
            if not match:
                raise ValueError(f"Unable to parse at position {idx}: '{expr[idx:]}'")

            token = match.group()
            idx = match.end()
            
            if match.lastgroup == 'NUMBER':
                tokens.append(match.group('NUMBER'))
                last_token = 'NUMBER'
            elif match.lastgroup == 'OPERATOR':
                # Handle unary minus (negative numbers)
                if match.group('OPERATOR') == '-' and (
                    last_token is None or last_token in {'OPERATOR', 'PAREN_OPEN'}
                ):
                    # Next token may be a negative number; look ahead
                    next_match = self.TOKEN_PATTERN.match(expr, idx)
                    if next_match and next_match.lastgroup == 'NUMBER':
                        idx = next_match.end()
                        tokens.append('-' + next_match.group('NUMBER'))
                        last_token = 'NUMBER'
                    else:
                        tokens.append('-')
                        last_token = 'OPERATOR'
                else:
                    tokens.append(match.group('OPERATOR'))
                    last_token = 'OPERATOR'
            elif match.lastgroup == 'PAREN':
                if token == '(':
                    tokens.append('(')
                    last_token = 'PAREN_OPEN'
                else:
                    tokens.append(')')
                    last_token = 'PAREN_CLOSE'
            elif match.lastgroup == 'INVALID':
                raise ValueError(f"Invalid character: {token.strip()}")
        
        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates token list for syntax.
        Checks:
        - Balanced parentheses
        - Valid token ordering (no two operators in a row, etc)
        """
        balance = 0
        prev_token_type = None

        for idx, token in enumerate(tokens):
            if token == '(':
                balance += 1
                prev_token_type = 'PAREN_OPEN'
            elif token == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Unbalanced parentheses")
                prev_token_type = 'PAREN_CLOSE'
            elif token in self.OPERATORS:
                if prev_token_type in (None, 'OPERATOR', 'PAREN_OPEN'):
                    # Only allow unary minus handled during tokenization
                    raise ValueError(f"Operator '{token}' cannot follow '{prev_token_type or 'start'}'")
                prev_token_type = 'OPERATOR'
            else:  # NUMBER
                if prev_token_type == 'PAREN_CLOSE':
                    raise ValueError("Missing operator before number")
                prev_token_type = 'NUMBER'

        if balance != 0:
            raise ValueError("Unbalanced parentheses")

        if prev_token_type == 'OPERATOR':
            raise ValueError("Expression cannot end with an operator")

    def _infix_to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts infix tokens to Reverse Polish Notation using the shunting-yard algorithm.
        """
        output = []
        stack = []

        for token in tokens:
            if token not in self.OPERATORS and token not in {'(', ')'}:
                # Token is a number
                output.append(token)
            elif token in self.OPERATORS:
                while (
                    stack and stack[-1] in self.OPERATORS and
                    (
                        (self.OPERATORS[token]['associativity'] == 'left' and
                         self.OPERATORS[token]['precedence'] <= self.OPERATORS[stack[-1]]['precedence'])
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
                    raise ValueError("Unbalanced parentheses")
                stack.pop()  # Remove '('

        # Drain stack
        while stack:
            if stack[-1] in {'(', ')'}:
                raise ValueError("Unbalanced parentheses")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, rpn: List[str]) -> float:
        """
        Evaluates a list of Reverse Polish Notation tokens and returns the result.
        """
        stack = []

        for token in rpn:
            if token not in self.OPERATORS:
                try:
                    num = float(token)
                except ValueError:
                    raise ValueError(f"Invalid number: {token}")
                stack.append(num)
            else:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
        if len(stack) != 1:
            raise ValueError("Too many operands.")

        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Safely applies an arithmetic operator to two numbers, checks for division by zero.
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0.0:
                raise ZeroDivisionError("Division by zero.")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {operator}")


if __name__ == "__main__":
    # Example usage & basic test harness
    calc = Calculator()
    expressions = [
        "1 + 2 * 3",               # 7
        "(1 + 2) * 3",             # 9
        "4 + -5 * (2.5-3.5)",      # 9
        "10 / 2 + 6 * (4-1)",      # 22
        "7 + ((3 + 2) * (8 / 4))",  # 17
        "-3 + 4",                  # 1
        "((2 + 3) * 4.5) / -1",    # -22.5
        "5 / (2 - 2)",             # Division by zero
        "2.5.6 + 4",               # Invalid number
        "4 + (3 * 2"               # Unbalanced parentheses
    ]
    for expr in expressions:
        try:
            result = calc.calculate(expr)
            print(f"Expression: {expr}  -->  Result: {result}")
        except Exception as ex:
            print(f"Expression: {expr}  -->  Error: {ex}")
