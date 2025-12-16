
from typing import List, Union


class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, / and parentheses.
    Adheres to ISO/IEC 25010: Maintainable, Reliable, Safe, and Testable.
    """

    # Allowed characters for validation
    _valid_characters = set("0123456789.+-*/() ")

    def calculate(self, expression: str) -> float:
        """
        Parse and evaluate the given arithmetic expression string.
        :param expression: str, the arithmetic expression to evaluate.
        :return: float, the result of the evaluation.
        :raises ValueError: If the expression is invalid.
        :raises ZeroDivisionError: If division by zero occurs.
        """
        # Preliminary validation and cleaning
        self._validate_input(expression)
        expression = expression.replace(" ", "")  # Remove all spaces

        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _validate_input(self, expression: str) -> None:
        """
        Validate that the input expression has only permitted characters and balanced parentheses.
        :param expression: The input arithmetic expression.
        :raises ValueError: If invalid characters or unbalanced parentheses are found.
        """
        # Character check
        for ch in expression:
            if ch not in self._valid_characters:
                raise ValueError(f"Invalid character found: '{ch}'")

        # Parentheses balance check
        depth = 0
        for ch in expression:
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth < 0:
                    raise ValueError("Unbalanced parentheses: too many closing ')'")
        if depth != 0:
            raise ValueError("Unbalanced parentheses: missing closing ')'")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Convert the expression string into a list of tokens: numbers, operators, parentheses.
        Handles negative numbers and floating-point numbers.
        """
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            ch = expression[i]
            if ch in '0123456789.':
                # Parse number (int or float)
                num, i = self._parse_number(expression, i)
                tokens.append(num)
            elif ch in '+-*/()':
                # Handle leading negative or negative after '(' or operator (unary minus)
                if ch == '-' and (i == 0 or expression[i - 1] in '(-+*/'):
                    # This is a unary minus: parse negative number
                    if i + 1 < n and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        num, i = self._parse_number(expression, i)
                        tokens.append(num)
                    else:
                        raise ValueError(f"Invalid unary '-' at position {i}")
                else:
                    tokens.append(ch)
                    i += 1
            else:
                raise ValueError(f"Invalid token '{ch}' at position {i}")
        return tokens

    def _parse_number(self, s: str, i: int) -> (str, int):
        """
        Parses a number (including negative and floating point) starting at index i.
        Returns the parsed number as string (to be converted to float/int), and the next index.
        """
        n = len(s)
        num_str = ''
        if s[i] == '-':
            num_str += '-'
            i += 1
        dot_seen = False
        digit_seen = False
        while i < n and (s[i].isdigit() or s[i] == '.'):
            if s[i] == '.':
                if dot_seen:
                    raise ValueError(f"Invalid number with multiple decimal points starting at position {i-len(num_str)}")
                dot_seen = True
            else:
                digit_seen = True
            num_str += s[i]
            i += 1
        if not digit_seen:
            raise ValueError(f"Expected digit in number at position {i}")
        return num_str, i

    def _to_rpn(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts token list (in infix notation) to Reverse Polish Notation (postfix) using the Shunting Yard algorithm.
        :param tokens: list of str, the infix tokens.
        :return: list of tokens (numbers as floats and operators as str) in postfix order.
        """
        prec = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in prec:
                while stack and stack[-1] in prec and prec[token] <= prec[stack[-1]]:
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Mismatched parentheses during parsing")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token '{token}' during parsing")
        while stack:
            if stack[-1] in '()':
                raise ValueError("Unbalanced parentheses in expression")
            output.append(stack.pop())
        return output

    def _is_number(self, token: str) -> bool:
        """
        Checks if a string token represents a valid number.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _evaluate_rpn(self, rpn: List[Union[float, str]]) -> float:
        """
        Evaluate the expression given in Reverse Polish Notation.
        :param rpn: List of tokens (numbers as floats, operators as str).
        :return: The final result (float).
        :raises ZeroDivisionError: If division by zero occurs.
        :raises ValueError: For invalid RPN expressions.
        """
        stack: List[float] = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: insufficient operands for operator")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Unknown token '{token}' in evaluation")
        if len(stack) != 1:
            raise ValueError("Invalid syntax: too many operands remain")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Safely apply an arithmetic operator to two operands.
        :param a: first operand
        :param b: second operand
        :param operator: one of +, -, *, /
        :return: result (float)
        :raises ZeroDivisionError: if division by zero
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        else:
            raise ValueError(f"Unsupported operator: {operator}")


if __name__ == "__main__":
    # Simple CLI driver for manual testing
    calc = Calculator()
    print("Console Arithmetic Calculator (type 'exit' or Ctrl+C to quit)")
    while True:
        try:
            expr = input("Enter expression: ").strip()
            if expr.lower() in ('exit', 'quit'):
                break
            result = calc.calculate(expr)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
