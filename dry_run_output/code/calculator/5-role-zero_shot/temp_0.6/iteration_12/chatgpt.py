
from typing import List, Union


class Calculator:
    """
    A console-based arithmetic calculator that supports +, -, *, /, (), integers and floats.
    It parses and evaluates expressions with correct operator precedence and validation.
    
    Methods
    -------
    calculate(expression: str) -> float
        Evaluates the arithmetic expression and returns the result as a float.
    """

    def __init__(self):
        # Define supported operators and their precedence
        self.operators = {
            '+': {'precedence': 1, 'associativity': 'left'},
            '-': {'precedence': 1, 'associativity': 'left'},
            '*': {'precedence': 2, 'associativity': 'left'},
            '/': {'precedence': 2, 'associativity': 'left'},
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result as a float.
        
        Parameters
        ----------
        expression : str
            The arithmetic expression to evaluate.
        
        Returns
        -------
        float
            The result of the evaluated expression.
        
        Raises
        ------
        ValueError
            If the expression is invalid (e.g., unbalanced parentheses, illegal character).
        ZeroDivisionError
            If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).
        
        Parameters
        ----------
        expression : str
            The input arithmetic expression.

        Returns
        -------
        List[str]
            List of string tokens.

        Raises
        ------
        ValueError
            For invalid characters or malformed numbers.
        """
        tokens = []
        i = 0
        n = len(expression)
        last_token_type = 'operator'  # For unary minus detection

        while i < n:
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            # Number (integer, float), possibly negative
            if char.isdigit() or (char == '.' and i + 1 < n and expression[i+1].isdigit()) or \
               (char == '-' and (last_token_type in ['operator', 'lparen']) \
                and (i + 1 < n and (expression[i+1].isdigit() or expression[i+1] == '.'))):
                num_str = ''
                if char == '-':
                    num_str += '-'
                    i += 1
                    char = expression[i] if i < n else ''

                dot_count = 0
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError(f"Invalid number with multiple decimal points at position {i}.")
                    num_str += expression[i]
                    i += 1
                try:
                    float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number: {num_str}")
                tokens.append(num_str)
                last_token_type = 'number'

            # Parentheses
            elif char == '(':
                tokens.append(char)
                i += 1
                last_token_type = 'lparen'
            elif char == ')':
                tokens.append(char)
                i += 1
                last_token_type = 'rparen'

            # Operators
            elif char in self.operators:
                tokens.append(char)
                i += 1
                last_token_type = 'operator'

            else:
                raise ValueError(f"Invalid character '{char}' at position {i}.")

        if not tokens:
            raise ValueError("Expression is empty or contains only whitespace.")

        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of tokens from infix to Reverse Polish Notation using Shunting Yard Algorithm.

        Parameters
        ----------
        tokens : List[str]
            List of tokens in infix notation.

        Returns
        -------
        List[str]
            Tokens in RPN order.

        Raises
        ------
        ValueError
            For unbalanced parentheses or malformed expressions.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in self.operators:
                while operator_stack:
                    top = operator_stack[-1]
                    if top in self.operators and (
                            (self.operators[token]['associativity'] == 'left' and
                             self.operators[token]['precedence'] <= self.operators[top]['precedence']) or
                            (self.operators[token]['associativity'] == 'right' and
                             self.operators[token]['precedence'] < self.operators[top]['precedence'])
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
                    raise ValueError("Unbalanced parentheses: ')' found without matching '('")
                operator_stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token: {token}")

        while operator_stack:
            top = operator_stack.pop()
            if top in ('(', ')'):
                raise ValueError("Unbalanced parentheses: missing '(' or ')'")
            output_queue.append(top)
        return output_queue

    def _evaluate_rpn(self, tokens: List[str]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation.

        Parameters
        ----------
        tokens : List[str]
            Tokens in RPN order.

        Returns
        -------
        float
            The result of the evaluation.

        Raises
        ------
        ZeroDivisionError
            If division by zero is attempted.
        ValueError
            For malformed RPN expressions.
        """
        stack: List[float] = []

        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN: {token}")

        if len(stack) != 1:
            raise ValueError("Malformed expression: leftover operands.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operation on operands a and b.

        Parameters
        ----------
        a : float
            First operand
        b : float
            Second operand
        operator : str
            Operator ('+', '-', '*', '/')

        Returns
        -------
        float
            Result of the operation
        
        Raises
        ------
        ZeroDivisionError
            If division by zero is attempted.
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero.")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def _is_number(self, token: str) -> bool:
        """
        Checks if the given token is a number.

        Parameters
        ----------
        token : str
            Token to check

        Returns
        -------
        bool
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    # Demo/test: Uncomment block below to test with manual input or test cases.
    import sys
    calc = Calculator()

    def test_expressions():
        test_cases = [
            # Valid
            ("2 + 3 * 4", 14.0),
            ("(2 + 3) * 4", 20.0),
            ("-2 + 4.5 * (-3)", -15.5),
            ("2 + 3 * 4 - 5 / 2", 11.5),
            ("((2+3)*4.0)-(7/2)", 15.5),
            ("-3.5", -3.5),
            ("-2 * (4 + -3)", -2.0),
            ("3.2 + 2.8", 6.0),
            ("-2*-2", 4.0),
            # Invalid: Uncomment these lines to see raised exceptions
            # ("2 +* 2", None),
            # ("(((2 + 2)", None),
            # ("2 / 0", None),
            # ("foo + 1", None),
        ]
        for expr, expected in test_cases:
            try:
                result = calc.calculate(expr)
                print(f"{expr} = {result} (expected: {expected})")
                assert expected is None or abs(result - expected) < 1e-9
            except Exception as e:
                print(f"{expr} raised {e}")

    # test_expressions()
    while True:
        try:
            input_expr = input("Enter expression (or 'exit'): ").strip()
            if input_expr.lower() == 'exit':
                print("Exiting calculator.")
                break
            res = calc.calculate(input_expr)
            print("Result:", res)
        except Exception as ex:
            print(f"Error: {ex}", file=sys.stderr)
