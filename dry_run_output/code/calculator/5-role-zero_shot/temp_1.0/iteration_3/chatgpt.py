
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, / operations,
    parentheses, and correct precedence for integer/float numbers.

    The Calculator class adheres to ISO/IEC 25010 quality requirements.
    It provides modularity, input safety, maintainable OOP design, and testability.
    """

    # Token types
    NUMBER   = 'NUMBER'
    OPERATOR = 'OPERATOR'
    LPAREN   = 'LPAREN'
    RPAREN   = 'RPAREN'

    # Operator precedence map
    _precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }

    # Supported operators
    _operators = set(_precedence.keys())

    # Allowed characters (for safety)
    _allowed_re = re.compile(r'^[\d\.\+\-\*/\(\)\s]+$')

    class Token:
        """
        Represents a single token in an arithmetic expression.
        """
        def __init__(self, type_: str, value: Union[float, str]):
            self.type = type_
            self.value = value

        def __repr__(self):
            return f"Token({self.type}, {self.value})"

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression.

        Args:
            expression (str): The arithmetic expression as a string.

        Returns:
            float: The evaluated result.

        Raises:
            ValueError: If the input is invalid (e.g., illegal characters, bad syntax).
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._eval_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List['Calculator.Token']:
        """
        Converts the input string into a list of tokens.
        Handles negative numbers and floating-point parsing.

        Args:
            expr (str): The input expression.

        Returns:
            List[Token]: Tokenized list of tokens.
        
        Raises:
            ValueError: When unallowed characters or invalid syntax present.
        """
        expr = expr.strip()
        if not expr:
            raise ValueError("Empty expression")

        # Safety: Only allow allowed characters
        if not self._allowed_re.match(expr):
            raise ValueError("Invalid character in expression")

        tokens: List[Calculator.Token] = []
        i = 0
        last_token_type = None
        length = len(expr)

        while i < length:
            ch = expr[i]
            if ch.isspace():
                i += 1
                continue
            elif ch in '()+-*/':
                # Handle negative numbers (unary minus)
                if ch == '-' and (last_token_type is None or
                                  last_token_type in {self.OPERATOR, self.LPAREN}):
                    # negative number
                    num_match = re.match(r'-?\d+(\.\d+)?', expr[i:])
                    if num_match:
                        num_str = num_match.group()
                        tokens.append(self.Token(self.NUMBER, float(num_str)))
                        i += len(num_str)
                        last_token_type = self.NUMBER
                        continue
                    else:
                        raise ValueError(f"Invalid syntax at position {i}")
                elif ch == '+':
                    # unary plus - skip, or treat as binary plus if appropriate
                    if (last_token_type is None or
                        last_token_type in {self.OPERATOR, self.LPAREN}):
                        # e.g. "+2", "(+2)", just skip unary plus
                        i += 1
                        continue
                if ch == '(':
                    tokens.append(self.Token(self.LPAREN, ch))
                    last_token_type = self.LPAREN
                elif ch == ')':
                    tokens.append(self.Token(self.RPAREN, ch))
                    last_token_type = self.RPAREN
                else:
                    tokens.append(self.Token(self.OPERATOR, ch))
                    last_token_type = self.OPERATOR
                i += 1
            elif ch.isdigit() or ch == '.':
                num_match = re.match(r'\d+(\.\d+)?', expr[i:])
                if num_match:
                    num_str = num_match.group()
                    tokens.append(self.Token(self.NUMBER, float(num_str)))
                    i += len(num_str)
                    last_token_type = self.NUMBER
                else:
                    raise ValueError(f"Invalid number at position {i}")
            else:
                raise ValueError(f"Invalid character: '{ch}'")
        # Parentheses balance check
        self._check_parentheses(tokens)
        return tokens

    def _check_parentheses(self, tokens: List['Calculator.Token']) -> None:
        """
        Checks if parentheses are balanced in token list.
        Raises ValueError if not balanced.

        Args:
            tokens (List[Token]): The list of tokens.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        count = 0
        for tok in tokens:
            if tok.type == self.LPAREN:
                count += 1
            elif tok.type == self.RPAREN:
                count -= 1
            if count < 0:
                raise ValueError("Unbalanced parentheses: too many )")
        if count != 0:
            raise ValueError("Unbalanced parentheses: too many (")

    def _to_rpn(self, tokens: List['Calculator.Token']) -> List['Calculator.Token']:
        """
        Converts the token list to Reverse Polish Notation (RPN)
        using the shunting yard algorithm.

        Args:
            tokens (List[Token]): List of tokens.

        Returns:
            List[Token]: RPN token list.

        Raises:
            ValueError: For invalid syntax or misplaced parentheses/operators.
        """
        output: List[Calculator.Token] = []
        stack: List[Calculator.Token] = []

        for token in tokens:
            if token.type == self.NUMBER:
                output.append(token)
            elif token.type == self.OPERATOR:
                while (stack and stack[-1].type == self.OPERATOR and
                       self._precedence[token.value] <= self._precedence[stack[-1].value]):
                    output.append(stack.pop())
                stack.append(token)
            elif token.type == self.LPAREN:
                stack.append(token)
            elif token.type == self.RPAREN:
                found_lparen = False
                while stack:
                    top = stack.pop()
                    if top.type == self.LPAREN:
                        found_lparen = True
                        break
                    else:
                        output.append(top)
                if not found_lparen:
                    raise ValueError("Unbalanced parentheses: ')' without '('")
            else:
                raise ValueError(f"Invalid token type: {token.type}")

        while stack:
            if stack[-1].type in {self.LPAREN, self.RPAREN}:
                raise ValueError("Unbalanced parentheses in expression")
            output.append(stack.pop())
        return output

    def _eval_rpn(self, tokens: List['Calculator.Token']) -> float:
        """
        Evaluates a list of tokens in RPN (postfix) order.

        Args:
            tokens (List[Token]): RPN token list.

        Returns:
            float: Final result.

        Raises:
            ValueError: If there are missing operands or other errors.
            ZeroDivisionError: On division by zero.
        """
        stack: List[float] = []
        for token in tokens:
            if token.type == self.NUMBER:
                stack.append(token.value)
            elif token.type == self.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Insufficient values for operation")
                b = stack.pop()
                a = stack.pop()
                if token.value == '+':
                    stack.append(a + b)
                elif token.value == '-':
                    stack.append(a - b)
                elif token.value == '*':
                    stack.append(a * b)
                elif token.value == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
                else:
                    raise ValueError(f"Unsupported operator: {token.value}")
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: leftover values after evaluation")
        return stack[0]


if __name__ == "__main__":
    calc = Calculator()
    expressions = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-4.5 + 2.5 * (3 - 1.5)",
        "4 / 0",
        "2 + (3 * (2-5) / 3.0)",
        "5 +",
        "a + 1",
        "",
        "((7+3)/2)*(5-2)"
    ]
    for expr in expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr!r} -> Error: {e}")
