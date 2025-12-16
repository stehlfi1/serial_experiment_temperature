
from typing import List, Union


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions
    containing +, -, *, / operators, parentheses, integers, and floating-point numbers.
    Compliant with ISO/IEC 25010 software quality model.
    """

    # Supported operators and their precedence
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'L'},
        '-': {'precedence': 1, 'associativity': 'L'},
        '*': {'precedence': 2, 'associativity': 'L'},
        '/': {'precedence': 2, 'associativity': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string and returns the result as a float.

        :param expression: str - The arithmetic expression to evaluate.
        :return: float - The result of the evaluation.
        :raises ValueError: For invalid input expressions.
        :raises ZeroDivisionError: For division by zero.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List[Union[str, float]]:
        """
        Converts an input string into a list of tokens (numbers, operators, parentheses).

        :param expr: str - The expression to tokenize.
        :return: List of tokens.
        :raises ValueError: For invalid input (e.g., invalid characters, unbalanced parentheses).
        """
        tokens = []
        num_buffer = ''
        idx = 0
        length = len(expr)
        parentheses_stack = []

        def flush_number():
            nonlocal num_buffer
            if num_buffer != '':
                try:
                    number = float(num_buffer)
                    tokens.append(number)
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_buffer}'")
                num_buffer = ''

        while idx < length:
            char = expr[idx]
            if char.isspace():
                idx += 1
                continue

            # Start of number / float, including negative sign
            if char in '+-' and (
                idx == 0 or expr[idx - 1] in '()+-*/'
            ):
                # Support for negative/positive numbers
                num_buffer += char
                idx += 1
                continue

            if char.isdigit() or char == '.':
                num_buffer += char
                idx += 1
                continue

            flush_number()

            if char in self.OPERATORS:
                tokens.append(char)
            elif char == '(':
                tokens.append(char)
                parentheses_stack.append(char)
            elif char == ')':
                if not parentheses_stack:
                    raise ValueError("Unbalanced parentheses: extra ')'")
                parentheses_stack.pop()
                tokens.append(char)
            else:
                raise ValueError(f"Invalid character found: '{char}'")
            idx += 1

        flush_number()
        if parentheses_stack:
            raise ValueError("Unbalanced parentheses: extra '('")
        return tokens

    def _to_rpn(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts the list of tokens to Reverse Polish Notation (RPN) using the Shunting Yard Algorithm.

        :param tokens: List of tokens from tokenizer.
        :return: List of tokens in RPN order.
        :raises ValueError: For malformed expressions.
        """
        output = []
        stack = []

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                       ((self.OPERATORS[token]['associativity'] == 'L' and
                         self.OPERATORS[token]['precedence'] <= self.OPERATORS[stack[-1]]['precedence']))):
                    output.append(stack.pop())
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
                    raise ValueError("Unbalanced parentheses encountered during RPN conversion")
            else:
                raise ValueError(f"Unknown token during RPN conversion: '{token}'")

        while stack:
            top = stack.pop()
            if top in ('(', ')'):
                raise ValueError("Unbalanced parentheses encountered at end of RPN conversion")
            output.append(top)
        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates the Reverse Polish Notation token list and computes the result.

        :param rpn: List of tokens in RPN order.
        :return: The computed float result.
        :raises ValueError: For malformed expressions.
        :raises ZeroDivisionError: For division by zero.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: insufficient values for operation")
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
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Unknown token during RPN evaluation: '{token}'")
        if len(stack) != 1:
            raise ValueError("Invalid syntax: too many values after evaluation")
        return stack[0]


if __name__ == "__main__":
    import sys

    calc = Calculator()

    print("Simple Arithmetic Calculator (type 'exit' to quit)")
    print("Supports +, -, *, /, parentheses, integers, floats, negative numbers\n")

    while True:
        try:
            expr = input("Enter expression: ")
            if expr.lower() == 'exit':
                print("Goodbye!")
                break
            result = calc.calculate(expr)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
