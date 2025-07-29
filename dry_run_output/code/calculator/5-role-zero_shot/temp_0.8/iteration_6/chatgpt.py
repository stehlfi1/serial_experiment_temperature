
import re
from typing import List, Union


class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integer and floating-point numbers (including negatives).
    Implements calculate(expression: str) -> float.

    Adheres to ISO/IEC 25010 guidelines:
    - Correctness: Produces accurate results
    - Performance: Efficient via Shunting Yard Algorithm
    - Modularity: Separated tokenization, parsing, evaluation
    - Safety: Validates inputs, handles division by zero, etc.
    - Testability: Modular and documented
    """

    # Supported operators and their precedence/associativity
    _OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L'),
    }
    _VALID_CHARS = re.compile(r'^[\d\s\.\+\-\*\/\(\)]*$')

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        :param expression: A string representing the arithmetic expression.
        :return: Result as a float.
        :raises ValueError, ZeroDivisionError, SyntaxError
        """
        tokens = self._tokenize(expression)
        postfix = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(postfix)

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Tokenizes the input expression into numbers, operators, and parentheses.
        Handles negative numbers and validates syntax.

        :param expression: Input string expression
        :return: List of tokens (floats, operators, parentheses)
        :raises ValueError, SyntaxError
        """
        # Input validation
        expr = expression.replace(' ', '')
        if not expr:
            raise ValueError("Input expression is empty.")
        if not self._VALID_CHARS.match(expr):
            raise ValueError("Invalid characters in expression.")

        tokens: List[Union[float, str]] = []
        i = 0
        n = len(expr)

        def is_operator(c: str) -> bool:
            return c in self._OPERATORS

        while i < n:
            c = expr[i]
            if c in '0123456789.':  # Number or decimal
                num_match = re.match(r'\d+(\.\d*)?|\.\d+', expr[i:])
                if not num_match:
                    raise SyntaxError(f"Invalid number at position {i}")
                num_str = num_match.group()
                num_val = float(num_str)
                tokens.append(num_val)
                i += len(num_str)
            elif c in self._OPERATORS:
                # Handle unary minus
                if c == '-' and (
                    (i == 0) or (expr[i - 1] in self._OPERATORS or expr[i - 1] == '(')
                ):
                    # It's a unary minus, look ahead to parse the number
                    num_match = re.match(r'-\d+(\.\d*)?|-?\.\d+', expr[i:])
                    if not num_match:
                        tokens.append('-')  # It's just minus operator
                        i += 1
                        continue
                    num_str = num_match.group()
                    num_val = float(num_str)
                    tokens.append(num_val)
                    i += len(num_str)
                else:
                    tokens.append(c)
                    i += 1
            elif c in '()':
                tokens.append(c)
                i += 1
            else:
                raise ValueError(f"Invalid character '{c}' at position {i}")

        # Validate parentheses balance
        if tokens.count('(') != tokens.count(')'):
            raise SyntaxError("Unbalanced parentheses in expression.")

        return tokens

    def _infix_to_postfix(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts infix token list to postfix (RPN) using the Shunting Yard algorithm.

        :param tokens: List of tokens (from _tokenize)
        :return: Postfix token list
        :raises SyntaxError
        """
        output: List[Union[float, str]] = []
        stack: List[str] = []
        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self._OPERATORS:
                while stack and stack[-1] in self._OPERATORS:
                    top = stack[-1]
                    curr_prec, curr_assoc = self._OPERATORS[token]
                    top_prec, _ = self._OPERATORS[top]
                    if (curr_assoc == 'L' and curr_prec <= top_prec) or \
                       (curr_assoc == 'R' and curr_prec < top_prec):
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                found_left_paren = False
                while stack:
                    top = stack.pop()
                    if top == '(':
                        found_left_paren = True
                        break
                    output.append(top)
                if not found_left_paren:
                    raise SyntaxError("Mismatched parentheses in expression.")
            else:
                raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators
        while stack:
            top = stack.pop()
            if top in '()':
                raise SyntaxError("Mismatched parentheses in expression.")
            output.append(top)

        return output

    def _evaluate_postfix(self, tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a postfix (RPN) token list.

        :param tokens: List of tokens in postfix order
        :return: Computed result as float
        :raises ZeroDivisionError, SyntaxError
        """
        stack: List[float] = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                try:
                    b = stack.pop()
                    a = stack.pop()
                except IndexError:
                    raise SyntaxError("Invalid syntax in expression.")
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(a / b)
            else:
                raise ValueError(f"Unknown token in postfix: {token}")

        if len(stack) != 1:
            raise SyntaxError("Invalid syntax in expression.")

        return stack[0]


# Example Usage and Test Cases (Uncomment to test)
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",                   # 7.0
        "4 / 2 + 6",                   # 8.0
        "-3.5 + (2 * 4.5)",            # 6.5
        "2 * (3 + 4)",                 # 14.0
        "((1+2)*3)/4",                 # 2.25
        "-5 + 2",                      # -3.0
        "10 / (5 - 5)",                # Division by zero
        "2 * -3",                      # -6.0
        "3 +",                         # SyntaxError
        "3 + 4 * (2 - 1.5)",           # 5.0
        "2.5 * 2.0",                   # 5.0
        "",                            # ValueError
        "7 + ((3)",                    # SyntaxError (unbalanced)
        "a + 2",                       # ValueError (invalid char)
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as ex:
            print(f"{expr} => Error: {ex}")
