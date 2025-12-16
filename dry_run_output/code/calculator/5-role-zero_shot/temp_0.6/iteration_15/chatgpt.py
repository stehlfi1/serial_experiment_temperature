
import re
from typing import List, Union

class CalculatorError(Exception):
    """Custom exception class for calculator errors."""
    pass

class Calculator:
    """
    Arithmetic Calculator that supports +, -, *, / with parenthesis and correct operator precedence.
    """

    # Allowed operators, their precedence, and associativity
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'}
    }

    # Token regular expression (supporting negative numbers and decimal points)
    TOKEN_REGEX = re.compile(r"""
        (?P<NUMBER>      -?\d+(\.\d+)? ) |     # Integer or decimal (optionally negative)
        (?P<OPERATOR>    [\+\-\*/]    ) |     # Operators +, -, *, /
        (?P<LPAREN>      \(           ) |     # Left parenthesis
        (?P<RPAREN>      \)           ) |     # Right parenthesis
        (?P<SPACE>       \s+          )       # Whitespace
    """, re.VERBOSE)

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
        
        Raises:
            CalculatorError, ValueError, ZeroDivisionError, SyntaxError
        
        Returns:
            float: The result of the evaluated expression.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input expression into a list of tokens.
        Supports negative numbers.

        Args:
            expression (str): The expression string to tokenize.

        Raises:
            ValueError: For invalid tokens/characters.
        
        Returns:
            List[str]: List of tokens.
        """
        tokens = []
        idx = 0
        last_token = None

        while idx < len(expression):
            match = self.TOKEN_REGEX.match(expression, idx)
            if match is None:
                raise ValueError(f"Invalid character at position {idx}: '{expression[idx]}'")
            if match.lastgroup == 'NUMBER':
                tokens.append(match.group().replace(' ', ''))
                last_token = 'NUMBER'
            elif match.lastgroup == 'OPERATOR':
                op = match.group()
                # Handle unary minus (negative numbers)
                if op == '-' and (last_token is None or last_token in ('OPERATOR', 'LPAREN')):
                    # Scan forward for a number after unary minus
                    next_match = self.TOKEN_REGEX.match(expression, match.end())
                    if next_match and next_match.lastgroup == 'NUMBER':
                        num_token = '-' + next_match.group().replace(' ', '')
                        tokens.append(num_token)
                        idx = next_match.end()
                        last_token = 'NUMBER'
                        continue
                    else:
                        tokens.append('-1')
                        tokens.append('*')
                        last_token = 'OPERATOR'
                else:
                    tokens.append(op)
                    last_token = 'OPERATOR'
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
                last_token = 'LPAREN'
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
                last_token = 'RPAREN'
            # Ignore spaces
            idx = match.end()
        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts list of tokens from infix to postfix (Reverse Polish Notation)
        using the Shunting Yard Algorithm.

        Args:
            tokens (List[str]): Infix tokens

        Raises:
            SyntaxError: On unbalanced parentheses or malformed expressions

        Returns:
            List[str]: RPN tokens
        """
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in self.OPERATORS:
                while (
                    stack and stack[-1] in self.OPERATORS and
                    ((self.OPERATORS[token]['associativity'] == 'L' and
                      self.OPERATORS[token]['precedence'] <= self.OPERATORS[stack[-1]]['precedence'])
                     or
                     (self.OPERATORS[token]['associativity'] == 'R' and
                      self.OPERATORS[token]['precedence'] < self.OPERATORS[stack[-1]]['precedence']))
                ):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                found_left = False
                while stack:
                    top = stack.pop()
                    if top == '(':
                        found_left = True
                        break
                    output.append(top)
                if not found_left:
                    raise SyntaxError("Unbalanced parentheses: Extra ')'")
            else:
                raise ValueError(f"Unsupported token: {token}")

        # Pop any remaining operators from the stack
        while stack:
            top = stack.pop()
            if top in ('(', ')'):
                raise SyntaxError("Unbalanced parentheses: Extra '('")
            output.append(top)
        return output

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluates a list of RPN tokens and returns the computed result.

        Args:
            rpn_tokens (List[str]): The RPN expression tokens.

        Raises:
            ZeroDivisionError: On division by zero.
            SyntaxError: On malformed expression.

        Returns:
            float: The calculation result.
        """
        stack = []
        for token in rpn_tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise SyntaxError("Malformed expression: insufficient values for operation")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
            else:
                raise ValueError(f"Unknown RPN token: {token}")

        if len(stack) != 1:
            raise SyntaxError("Malformed expression: leftover operands in stack after evaluation")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if the token is a number (integer or float).

        Args:
            token (str): The token to check.

        Returns:
            bool: True if token is number else False.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example usage & manual testing
if __name__ == "__main__":
    calc = Calculator()

    test_cases = [
        "1 + 2 * 3",                 # 7.0
        "(1 + 2) * 3",               # 9.0
        "5 / 2",                     # 2.5
        "5 / (2 + 3)",               # 1.0
        "-4 + 3",                    # -1.0
        "2 * -3",                    # -6.0
        "-(4 + 5) * 2",              # -18.0
        "3 + 4 * 2 / (1 - 5)",       # 1.0
        "2.5 * (3.2 + -1.2)",        # 5.0
        "--3 + 2",                   # 5.0 (interpreted as -(-3) + 2)
        "((2))",                     # 2.0
        "1 + (2 * (3 + 4))",         # 15.0
        "-5 * -(3 + 2)",             # 25.0
        "0 / 1",                     # 0.0
        "5 / 0",                     # ZeroDivisionError
        "5 *",                       # SyntaxError
        "abc",                       # ValueError
        "((1+2)",                    # SyntaxError
        "3 + )2("                    # SyntaxError
    ]

    for expr in test_cases:
        print(f"Expression: {expr}")
        try:
            result = calc.calculate(expr)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {e.__class__.__name__}: {e}\n")
