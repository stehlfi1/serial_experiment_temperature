
import re
from typing import List, Union


class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.
    Adheres to ISO/IEC 25010 quality standards.
    """

    # Supported operators and their precedence and associativity
    _operators = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluate the given arithmetic expression string.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            float: The computed result.

        Raises:
            ValueError: For syntax errors, invalid characters, or unbalanced parentheses.
            ZeroDivisionError: Division by zero detected during evaluation.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Convert the input expression string to a list of tokens.

        Args:
            expression (str): Raw expression.

        Returns:
            List[Union[str, float]]: List of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: For invalid characters or malformed expressions.
        """
        # Remove spaces for easier parsing
        expr = expression.replace(' ', '')

        # Regular expression pattern for tokens
        token_pattern = r"""
            (?P<number>    # Integer or float (with optional unary minus)
                -?                # Possible unary minus
                (?:\d+\.\d*|\d*\.\d+|\d+)  # Digits, float formats
            )
            |(?P<op>[\+\-\*/])
            |(?P<paren>[()])
        """

        # Compile with VERBOSE mode for readability
        pattern = re.compile(token_pattern, re.VERBOSE)
        pos = 0
        tokens = []
        last_token_type = None  # To help distinguish unary minus from binary minus

        while pos < len(expr):
            match = pattern.match(expr, pos)
            if not match:
                raise ValueError(f"Invalid character in expression at position {pos}: '{expr[pos]}'")
            number = match.group('number')
            op = match.group('op')
            paren = match.group('paren')
            
            if number is not None:
                # Convert token to float (allows both integers and floats)
                try:
                    tokens.append(float(number))
                except ValueError:
                    raise ValueError(f"Invalid number: '{number}'")
                last_token_type = 'number'
            elif op is not None:
                # Detect unary minus
                if op == '-' and (last_token_type is None or last_token_type in {'op', 'paren_l'}):
                    # Check if next token is a number or left parenthesis
                    # Attach unary minus to number in the next iteration
                    # For cases like -3, -(2+1)
                    lookahead_match = pattern.match(expr, match.end())
                    if lookahead_match and lookahead_match.group('number') is not None:
                        # Will be parsed as a negative number in next iteration
                        pos += 1  # Skip this '-' since it will be part of the number
                        continue
                    elif lookahead_match and lookahead_match.group('paren') == '(':
                        # For -(...), insert -1 * (
                        tokens.append(float(-1))
                        tokens.append('*')
                        last_token_type = 'op'
                        pos += 1
                        continue
                tokens.append(op)
                last_token_type = 'op'
            elif paren is not None:
                if paren == '(':
                    tokens.append('(')
                    last_token_type = 'paren_l'
                else:
                    tokens.append(')')
                    last_token_type = 'paren_r'
            pos = match.end()

        self._validate_tokens(tokens)
        return tokens

    def _validate_tokens(self, tokens: List[Union[str, float]]) -> None:
        """
        Validate token stream for balanced parentheses and proper token arrangement.

        Args:
            tokens (List[Union[str, float]]): List of expression tokens.

        Raises:
            ValueError: If tokens are invalid or parentheses unbalanced.
        """
        paren_count = 0
        last = None
        for token in tokens:
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: ')' encountered before matching '('")
            elif isinstance(token, str) and token in self._operators:
                # Prevent operators at the start or two operators in a row
                if last is None or (isinstance(last, str) and last in self._operators and last != ')'):
                    raise ValueError(f"Syntax error: operator '{token}' at invalid position")
            last = token
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: Unmatched '(' in expression")

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Convert tokenized infix expression to Reverse Polish Notation (RPN) using Shunting Yard algorithm.

        Args:
            tokens (List[Union[str, float]]): List of input tokens.

        Returns:
            List[Union[str, float]]: RPN output as list.

        Raises:
            ValueError: Invalid operator sequence.
        """
        output = []
        stack = []

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self._operators:
                while (
                    stack and stack[-1] in self._operators and
                    (
                        (self._operators[token][1] == 'L' and self._operators[token][0] <= self._operators[stack[-1]][0])
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
                    raise ValueError("Unbalanced parentheses in expression")
                stack.pop()  # discard '('
            else:
                raise ValueError(f"Invalid token encountered: {token}")

        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses in expression")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluate an expression in Reverse Polish Notation (RPN).

        Args:
            rpn (List[Union[str, float]]): Expression as RPN.

        Returns:
            float: Computation result.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: For invalid RPN structure.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._operators:
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: insufficient values for operation")
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
                        raise ZeroDivisionError("Division by zero")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Invalid RPN token: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values left on stack")
        return stack[0]


if __name__ == "__main__":
    # Example usage and simple test cases for the Calculator.
    calc = Calculator()
    test_expressions = [
        "3 + 4 * 2 / (1 - 5)",
        "-3 + 4",
        "(2 + 3) * 4.5",
        "((1 + 2) * 3 - 4) / 5",
        "-(2+2*2)",
        " 2.5 * ( -2 + 4.1 ) ",
        "6 / 3 / 2",
        "-(-3)",
        "3 + -(-2)",
        "2 + 3 * (4 - 1.5)",
        "3 / 0",                # Division by zero.
        "2 + (3"                # Unbalanced parenthesis.
    ]
    for exp in test_expressions:
        try:
            result = calc.calculate(exp)
            print(f"{exp} = {result}")
        except Exception as e:
            print(f"{exp} raised an error: {e}")
