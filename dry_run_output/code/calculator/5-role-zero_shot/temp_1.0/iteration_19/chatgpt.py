
import re
from typing import List


class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    integer and floating point numbers. Input is validated and errors
    are reported using built-in Python exceptions.

    Methods
    -------
    calculate(expression: str) -> float
        Evaluates the mathematical expression and returns the result as float.
    """

    # Supported operators with precedence and associativity
    OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluate the arithmetic expression.

        Parameters
        ----------
        expression : str
            The input arithmetic expression.

        Returns
        -------
        float
            The result of the evaluated expression.

        Raises
        ------
        ValueError
            If the expression contains invalid tokens or unbalanced parentheses.
        ZeroDivisionError
            If division by zero is attempted.
        """

        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Convert expression string into a list of tokens

        Returns
        -------
        List[str]
            List of tokens (number/operator/parenthesis)
        """

        # -- Validate and tokenize input
        # Regex: match numbers, decimal numbers, operators, or parentheses
        # Supports negative and floating point numbers
        token_spec = r'''
            (?P<NUMBER>    (?<![\d.])  -? \d+(?:\.\d+)? )    |  # number/int/float, allow negative sign if at start or after '(' or operator
            (?P<OPERATOR>  [+\-*/])                        |  # operator
            (?P<LPAREN>    \()                              |  # left parenthesis
            (?P<RPAREN>    \))                              |  # right parenthesis
            (?P<SPACE>     \s+)                                # whitespace (ignore)
        '''

        token_regex = re.compile(token_spec, re.VERBOSE)

        tokens = []
        position = 0
        prev_token = None
        while position < len(expression):
            match = token_regex.match(expression, position)
            if not match:
                raise ValueError(f"Invalid character at position {position}: '{expression[position]}'")

            kind = match.lastgroup
            value = match.group(match.lastgroup)
            if kind == 'NUMBER':
                tokens.append(value)
            elif kind == 'OPERATOR':
                # Distinguish between subtraction and negative number
                if value == '-' and (prev_token is None or prev_token in '([' + '+-*/'):
                    # This '-' is a unary sign for number (negative number)
                    # Let it be handled by number regex (which already allows negative)
                    # So, don't append, just continue
                    pass
                else:
                    tokens.append(value)
            elif kind == 'LPAREN':
                tokens.append('(')
            elif kind == 'RPAREN':
                tokens.append(')')
            # skip spaces
            prev_token = tokens[-1] if tokens else None
            position = match.end()

        # Check for consecutive operators or invalid token placement is handled in _to_rpn
        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Shunting Yard algorithm to convert tokens to Reverse Polish Notation.

        Parameters
        ----------
        tokens : List[str]

        Returns
        -------
        List[str]
            RPN (postfix notation) list

        Raises
        ------
        ValueError if parentheses are unbalanced or the expression is invalid.
        """
        output = []
        stack = []
        prev_token = None
        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in self.OPERATORS:
                # validate operator placement (e.g. no '**', '+*', etc.)
                if prev_token in self.OPERATORS or prev_token is None or prev_token == '(':
                    raise ValueError(f"Operator '{token}' used without preceding number or parenthesis.")
                while (stack and stack[-1] in self.OPERATORS):
                    top_op = stack[-1]
                    token_precedence, token_assoc = self.OPERATORS[token]
                    top_precedence, _ = self.OPERATORS[top_op]
                    if ((token_assoc == 'L' and token_precedence <= top_precedence) or
                        (token_assoc == 'R' and token_precedence < top_precedence)):
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                # Pop until '(' is found
                found_lparen = False
                while stack:
                    top = stack.pop()
                    if top == '(':
                        found_lparen = True
                        break
                    output.append(top)
                if not found_lparen:
                    raise ValueError("Unbalanced parentheses detected: ')' found without matching '('")
                # no output append for parenthesis
            prev_token = token

        # Check for invalid trailing operator
        if prev_token in self.OPERATORS:
            raise ValueError(f"Expression cannot end with operator: '{prev_token}'")
        # Pop any remaining operators
        while stack:
            top = stack.pop()
            if top in '()':
                raise ValueError("Unbalanced parentheses detected.")
            output.append(top)

        return output

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluate Reverse Polish Notation list.

        Parameters
        ----------
        rpn_tokens : List[str]

        Returns
        -------
        float

        Raises
        ------
        ZeroDivisionError if division by zero.
        ValueError if invalid expression.
        """
        stack = []
        for token in rpn_tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator.")
                b = stack.pop()
                a = stack.pop()
                result = None
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0.0:
                        raise ZeroDivisionError("Division by zero.")
                    result = a / b
                stack.append(result)
        if len(stack) != 1:
            raise ValueError("Invalid expression: leftover operands found.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Determines if a token is a valid number.

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
    import sys

    calc = Calculator()
    print("Console Arithmetic Calculator (type 'exit' to quit)")
    while True:
        try:
            expr = input("Enter expression: ")
            if expr.strip().lower() == 'exit':
                break
            result = calc.calculate(expr)
            print("Result:", result)
        except Exception as e:
            print("Error:", type(e).__name__, '-', str(e))
