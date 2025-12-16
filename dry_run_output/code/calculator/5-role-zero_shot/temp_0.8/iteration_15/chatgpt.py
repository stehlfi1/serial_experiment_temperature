
"""
Calculator Module
-----------------
A console-based arithmetic calculator adhering to ISO/IEC 25010 quality standards.
Implements addition, subtraction, multiplication, division, and supports parentheses,
integer and floating-point numbers (including negatives). Validates input expression and handles errors.

Author: [Your Name]
Date: [Current Date]
"""

import re
from typing import List, Union

class Calculator:
    """
    Calculator class providing arithmetic expression evaluation.
    Expression is parsed, validated, and evaluated according to operator precedence
    without using eval().
    """

    # Define operator precedence and associativity
    _OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }

    # Regex for tokenizing numbers (integers, floats), operators, and parentheses
    _TOKEN_PATTERN = re.compile(r"""
        (?P<NUMBER>   -?\d+(\.\d+)?   )   # Integer or Float (may be negative)
        |(?P<OP>      [+\-*/]         )   # Operator
        |(?P<LPAREN>  [(]             )   # Left Parenthesis
        |(?P<RPAREN>  [)]             )   # Right Parenthesis
        |(?P<SPACE>   [ \t]+          )   # Ignore whitespace
        |(?P<INVALID> .               )   # Any other character (invalid)
    """, re.VERBOSE)

    def calculate(self, expression: str) -> float:
        """
        Parse, validate, and evaluate the arithmetic expression.

        :param expression: The arithmetic expression as a string
        :return: The evaluated result as a float
        :raises ValueError, ZeroDivisionError, SyntaxError: On various input errors
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Tokenizes the input string into numbers, operators, and parentheses.

        :param expression: The arithmetic expression as a string
        :return: List of tokens (float, or str for operators/parentheses)
        :raises ValueError: If invalid characters are present
        """
        tokens = []
        prev_token = None
        idx = 0
        while idx < len(expression):
            match = self._TOKEN_PATTERN.match(expression, idx)
            if not match:
                raise ValueError(f"Invalid syntax at position {idx}.")
            if match.lastgroup == 'NUMBER':
                number_str = match.group('NUMBER')
                tokens.append(float(number_str))
                prev_token = 'NUMBER'
            elif match.lastgroup == 'OP':
                op = match.group('OP')

                # Interpret unary '-' (negative number) if appropriate
                if op == '-' and (prev_token is None or prev_token in {'OP', 'LPAREN'}):
                    # Look ahead for a number (possibly negative)
                    next_match = self._TOKEN_PATTERN.match(expression, match.end())
                    if next_match and next_match.lastgroup == 'NUMBER':
                        number_str = '-' + next_match.group('NUMBER')
                        tokens.append(float(number_str))
                        idx = next_match.end() - 1  # skip next token since it's now part of the number
                        prev_token = 'NUMBER'
                    else:
                        tokens.append(op)
                        prev_token = 'OP'
                else:
                    tokens.append(op)
                    prev_token = 'OP'
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
                prev_token = 'LPAREN'
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
                prev_token = 'RPAREN'
            elif match.lastgroup == 'SPACE':
                pass  # Ignore spaces
            elif match.lastgroup == 'INVALID':
                raise ValueError(f"Invalid character '{match.group()}' at position {idx}.")
            idx = match.end()
        return tokens

    def _validate_tokens(self, tokens: List[Union[float, str]]) -> None:
        """
        Validate tokens: balanced parentheses, correct token sequences.

        :param tokens: List of tokens
        :raises SyntaxError: On parentheses mismatch, invalid ordering, empty input, etc.
        """
        paren_stack = []
        prev_token_type = None

        if not tokens:
            raise SyntaxError("Empty expression.")

        for i, token in enumerate(tokens):
            if token == '(':
                paren_stack.append(token)
                prev_token_type = 'LPAREN'
            elif token == ')':
                if not paren_stack:
                    raise SyntaxError("Unmatched closing parenthesis.")
                paren_stack.pop()
                prev_token_type = 'RPAREN'
            elif isinstance(token, float):
                if prev_token_type == 'RPAREN':
                    raise SyntaxError("Unexpected number after ')'.")
                prev_token_type = 'NUMBER'
            elif token in self._OPERATORS:
                if prev_token_type in {None, 'OP', 'LPAREN'}:
                    if token != '-':
                        raise SyntaxError(f"Operator '{token}' can't start an expression or follow another operator/left parenthesis.")
                prev_token_type = 'OP'
            else:
                raise SyntaxError(f"Invalid token encountered: {token}")

        if paren_stack:
            raise SyntaxError("Unmatched opening parenthesis.")

        if prev_token_type == 'OP':
            raise SyntaxError("Expression cannot end with an operator.")

    def _to_rpn(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Convert infix expression (token list) to Reverse Polish Notation (RPN) using shunting-yard algorithm.

        :param tokens: List of tokens in infix notation
        :return: List of tokens in RPN
        """
        output = []
        stack = []

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS):
                    top_op = stack[-1]
                    curr_prec, curr_assoc = self._OPERATORS[token]
                    top_prec, _ = self._OPERATORS[top_op]
                    if (curr_assoc == 'L' and curr_prec <= top_prec) or (curr_assoc == 'R' and curr_prec < top_prec):
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise SyntaxError("Mismatched parentheses during RPN conversion.")
                stack.pop()
            else:
                raise SyntaxError(f"Invalid token in RPN conversion: {token}")

        while stack:
            if stack[-1] in {'(', ')'}:
                raise SyntaxError("Mismatched parentheses in expression.")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, rpn: List[Union[float, str]]) -> float:
        """
        Evaluate the Reverse Polish Notation (RPN) token list to compute the result.

        :param rpn: List of tokens in RPN
        :return: Result as float
        :raises ZeroDivisionError: On division by zero
        """
        stack = []

        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise SyntaxError(f"Not enough operands for operator '{token}'.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise SyntaxError(f"Invalid token during RPN evaluation: {token}")

        if len(stack) != 1:
            raise SyntaxError("Invalid expression - processing ended with more than one result on stack.")

        return stack[0]

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """
        Applies arithmetic operation for two operands.

        :param a: Left operand
        :param b: Right operand
        :param op: Operator string
        :return: Computation result
        :raises ZeroDivisionError: On division by zero
        """
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero is undefined.")
            return a / b
        else:
            raise ValueError(f"Unsupported operator '{op}'.")

# Example usage & minimal test cases (for manual testing purposes)

if __name__ == '__main__':
    calc = Calculator()
    expressions = [
        "1 + 2 * 3",
        "(2 + 3) * (4 - 5.5)",
        "-3 + 4 * 2 / ( 1 - 5 )",
        "3.5 + (-2.7)",
        "4 / 0",                  # Division by zero test
        "2 + (3 * 4",             # Unbalanced parenthesis
        "2 ++ 3",                 # Invalid operator sequence
        "2 + #",                  # Invalid character
    ]

    for expr in expressions:
        try:
            result = calc.calculate(expr)
            print(f"Input: {expr}\nResult: {result}\n")
        except Exception as e:
            print(f"Input: {expr}\nError: {type(e).__name__}: {e}\n")
