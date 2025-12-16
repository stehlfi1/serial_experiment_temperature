
import re
from typing import List, Union

class CalculatorError(Exception):
    """Custom exception for Calculator errors."""
    pass

class Calculator:
    """
    A robust arithmetic calculator adhering to ISO/IEC 25010 software quality attributes.
    Supports +, -, *, /, parentheses, integer and floating point numbers (including negatives).
    """

    # Regular expression for tokenizing
    TOKEN_REGEX = re.compile(
        r'''
        (?P<NUMBER>   -?\d+(\.\d+)? ) |  # Integer or float with optional unary minus
        (?P<LPAREN>   \(           ) |  # Opening parenthesis
        (?P<RPAREN>   \)           ) |  # Closing parenthesis
        (?P<OP>       [+\-*/]      ) |  # Arithmetic operators
        (?P<WS>       \s+          )    # Whitespace
        ''', re.VERBOSE
    )

    # Operator precedences and associativity
    OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return a float result.
        Raises:
            ValueError: for invalid expressions (unbalanced parentheses, invalid tokens, etc.)
            ZeroDivisionError: for division by zero
        """
        # Step 1: Tokenization and validation
        tokens = self._tokenize(expression)
        # Step 2: Parse to Reverse Polish Notation (RPN) using the shunting yard algorithm
        rpn = self._to_rpn(tokens)
        # Step 3: Evaluate RPN
        result = self._eval_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """Tokenizes the expression string into numbers, operators, and parentheses."""
        tokens = []
        pos = 0
        last_token = None

        while pos < len(expression):
            match = self.TOKEN_REGEX.match(expression, pos)
            if not match:
                raise ValueError(f"Invalid character at position {pos}: '{expression[pos]}'")

            kind = match.lastgroup
            value = match.group(kind)

            if kind == 'NUMBER':
                # Ensure literals are well-formed
                number = float(value)
                tokens.append(number)
                last_token = 'NUMBER'
            elif kind == 'OP':
                # Handle unary minus
                if value == '-' and (last_token is None or last_token in ('OP', 'LPAREN')):
                    # Lookahead to see the negative number
                    num_match = self.TOKEN_REGEX.match(expression, match.end())
                    if num_match and num_match.lastgroup == 'NUMBER':
                        num_value = num_match.group('NUMBER')
                        full_num = '-' + num_value
                        number = float(full_num)
                        tokens.append(number)
                        pos = num_match.end()
                        last_token = 'NUMBER'
                        continue
                    else:
                        raise ValueError(f"Invalid unary minus at position {pos}")
                else:
                    tokens.append(value)
                    last_token = 'OP'
            elif kind == 'LPAREN':
                tokens.append('(')
                last_token = 'LPAREN'
            elif kind == 'RPAREN':
                tokens.append(')')
                last_token = 'RPAREN'
            # Ignore whitespace
            pos = match.end()

        self._validate_parentheses(tokens)
        return tokens

    def _validate_parentheses(self, tokens: List[Union[str, float]]):
        """Checks for balanced parentheses."""
        count = 0
        for token in tokens:
            if token == '(':
                count += 1
            elif token == ')':
                count -= 1
                if count < 0:
                    raise ValueError("Unbalanced parentheses: too many closing ')'")
        if count != 0:
            raise ValueError("Unbalanced parentheses: unmatched '(' remaining")

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts the token list into Reverse Polish Notation (RPN) using the shunting yard algorithm.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and operator_stack[-1] in self.OPERATORS):
                    top_op = operator_stack[-1]
                    if (
                        (self.OPERATORS[token][1] == 'L' and self.OPERATORS[token][0] <= self.OPERATORS[top_op][0])
                        or
                        (self.OPERATORS[token][1] == 'R' and self.OPERATORS[token][0] < self.OPERATORS[top_op][0])
                    ):
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unmatched parenthesis detected.")
                operator_stack.pop()  # Pop '('
            else:
                raise ValueError(f"Unexpected token: {token}")

        while operator_stack:
            top = operator_stack.pop()
            if top in ('(', ')'):
                raise ValueError("Unmatched parenthesis detected on remaining stack")
            output_queue.append(top)
        return output_queue

    def _eval_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates the expression in Reverse Polish Notation.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient values for operation")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: leftover items in evaluation stack")
        return stack[0]

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """
        Applies an arithmetic operator to two operands.
        """
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {op}")


if __name__ == "__main__":
    # Example interactive session
    calc = Calculator()
    print("Console Arithmetic Calculator (type 'quit' to exit)")
    while True:
        try:
            expr = input(">>> ")
            if expr.strip().lower() in {'quit', 'exit'}:
                break
            result = calc.calculate(expr)
            print(result)
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
