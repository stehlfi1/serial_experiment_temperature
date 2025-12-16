
"""
A console-based arithmetic calculator class adhering to ISO/IEC 25010 quality standards.
Features:
- Supports +, -, *, /, parentheses, operator precedence, negative numbers, floats, and ints.
- Input validation: balanced parentheses, valid tokens, division by zero, etc.
- OOP design: all interaction via Calculator.calculate()
- No eval(), safe parsing and evaluation.
- Comprehensive documentation.
"""

import re

class CalculatorError(Exception):
    """Custom exception for calculator-specific errors."""
    pass


class Calculator:
    """
    Arithmetic calculator supporting +, -, *, /, parentheses, and precedence.
    Provides input validation and safe, modular parsing and evaluation.
    """
    # Allowed operators with their precedence and associativity (for Shunting Yard)
    OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L'),
    }
    # Pattern to match valid tokens: numbers, operators, parentheses, whitespace
    TOKEN_PATTERN = re.compile(
        r'\s*(?:(?P<number>-?\d*\.?\d+)|(?P<operator>[\+\-\*/])|(?P<paren>[()]))'
    )
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression string and returns the result as float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The evaluated result.

        Raises:
            ValueError: For invalid syntax (e.g., bad tokens, unbalanced parentheses).
            ZeroDivisionError: If division by zero occurs in any subexpression.
        """
        try:
            tokens = self._tokenize(expression)
            rpn = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn)
            return result
        except CalculatorError as ce:
            raise ValueError(str(ce))
        except ZeroDivisionError as zde:
            raise zde

    def _tokenize(self, expr: str):
        """
        Tokenizes the input expression string. Supports negative numbers, decimals, operators, and parentheses.

        Args:
            expr (str): The expression to tokenize.

        Returns:
            list[str]: List of tokens as strings.

        Raises:
            CalculatorError: For any invalid or extra/unrecognized tokens.
        """
        tokens = []
        pos = 0
        last_token = None
        while pos < len(expr):
            match = self.TOKEN_PATTERN.match(expr, pos)
            if not match:
                raise CalculatorError(f"Invalid character at position {pos}: '{expr[pos]}'")
            # Extract token
            if match.group('number'):
                tokens.append(match.group('number'))
                last_token = 'number'
            elif match.group('operator'):
                # Handle unary minus (negative numbers), only if preceded by (beginning, operator, or open paren)
                if match.group('operator') == '-' and (last_token is None or last_token in ('operator', 'lparen')):
                    # Try to parse as part of the following number
                    num_match = self.TOKEN_PATTERN.match(expr, match.end())
                    if num_match and num_match.group('number'):
                        tokens.append('-' + num_match.group('number'))
                        pos = num_match.end()
                        last_token = 'number'
                        continue
                    else:
                        tokens.append('0')  # Interpret as '0 - expr'
                        tokens.append('-')
                        last_token = 'operator'
                else:
                    tokens.append(match.group('operator'))
                    last_token = 'operator'
            elif match.group('paren'):
                if match.group('paren') == '(':
                    tokens.append('(')
                    last_token = 'lparen'
                else:
                    tokens.append(')')
                    last_token = 'rparen'
            pos = match.end()
        # Validate tokens
        self._validate_tokens(tokens)
        return tokens

    def _validate_tokens(self, tokens):
        """
        Performs basic syntactic validation of token stream.

        Args:
            tokens (list[str]): The token list from `_tokenize`.

        Raises:
            CalculatorError: If any error is found.
        """
        # Check for invalid arrangement (e.g., two binary operators in a row, etc.)
        open_paren = 0
        last_type = None
        for i, tok in enumerate(tokens):
            if tok == '(':
                open_paren += 1
                last_type = 'lparen'
            elif tok == ')':
                open_paren -= 1
                if open_paren < 0:
                    raise CalculatorError("Unbalanced parentheses.")
                last_type = 'rparen'
            elif tok in self.OPERATORS:
                if last_type in (None, 'operator', 'lparen'):
                    raise CalculatorError("Invalid operator placement or missing operand.")
                last_type = 'operator'
            else:
                # Assume it's a number (float/int)
                if last_type == 'rparen':
                    raise CalculatorError("Missing operator between closing parenthesis and number.")
                try:
                    float(tok)
                except ValueError:
                    raise CalculatorError(f"Invalid token '{tok}'.")
                last_type = 'number'
        if open_paren != 0:
            raise CalculatorError("Unbalanced parentheses.")

    def _to_rpn(self, tokens):
        """
        Converts the list of tokens from infix to Reverse Polish Notation (RPN)
        using Dijkstra's Shunting Yard algorithm.

        Args:
            tokens (list[str]): Token list.

        Returns:
            list[str]: RPN token list.

        Raises:
            CalculatorError: On invalid syntax.
        """
        output = []
        op_stack = []
        for tok in tokens:
            if tok in self.OPERATORS:
                while op_stack and op_stack[-1] in self.OPERATORS:
                    prev_prec, prev_assoc = self.OPERATORS[op_stack[-1]]
                    curr_prec, curr_assoc = self.OPERATORS[tok]
                    if (curr_assoc == 'L' and curr_prec <= prev_prec) or (curr_assoc == 'R' and curr_prec < prev_prec):
                        output.append(op_stack.pop())
                    else:
                        break
                op_stack.append(tok)
            elif tok == '(':
                op_stack.append(tok)
            elif tok == ')':
                while op_stack and op_stack[-1] != '(':
                    output.append(op_stack.pop())
                if not op_stack or op_stack[-1] != '(':
                    raise CalculatorError("Mismatched parentheses.")
                op_stack.pop()  # Remove '('
            else:
                # Numbers
                output.append(tok)
        while op_stack:
            if op_stack[-1] in ('(', ')'):
                raise CalculatorError("Mismatched parentheses.")
            output.append(op_stack.pop())
        return output

    def _evaluate_rpn(self, tokens):
        """
        Evaluates a Reverse Polish Notation (RPN) token list.

        Args:
            tokens (list[str]): RPN token list.

        Returns:
            float: The result of the expression.

        Raises:
            ZeroDivisionError: On division by zero.
            CalculatorError: For invalid syntax or operations.
        """
        stack = []
        for tok in tokens:
            if tok in self.OPERATORS:
                if len(stack) < 2:
                    raise CalculatorError("Insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                if tok == '+':
                    res = a + b
                elif tok == '-':
                    res = a - b
                elif tok == '*':
                    res = a * b
                elif tok == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero.")
                    res = a / b
                else:
                    raise CalculatorError(f"Unknown operator '{tok}'.")
                stack.append(res)
            else:
                try:
                    n = float(tok)
                    stack.append(n)
                except ValueError:
                    raise CalculatorError(f"Invalid number '{tok}'.")
        if len(stack) != 1:
            raise CalculatorError("Malformed expression.")
        return stack[0]


if __name__ == "__main__":
    # Example console app interface for testability
    calc = Calculator()
    print("Console Arithmetic Calculator")
    print("Enter arithmetic expressions (or 'exit' to quit).")
    while True:
        try:
            expr = input("> ").strip()
            if expr.lower() in ("exit", "quit"):
                break
            result = calc.calculate(expr)
            print(f"= {result}")
        except Exception as e:
            print(f"Error: {e}")
