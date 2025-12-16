
import re
from typing import List, Union

class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, /, parentheses, 
    and both integers and floating-point numbers, including negatives.
    
    Adheres to ISO/IEC 25010 quality attributes: correctness, performance, 
    modularity, safety, testability, readability.
    """

    # Allowed operators with precedence and associativity
    OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }

    # Valid characters: digits, decimal points, operators, parentheses, whitespaces
    TOKEN_REGEX = re.compile(
        r"""
        (?P<NUMBER>   -?\d+(\.\d+)? ) |      # Integer or decimal number (with optional negative sign)
        (?P<LPAREN>   \(          ) |        # Left parenthesis
        (?P<RPAREN>   \)          ) |        # Right parenthesis
        (?P<OP>       [+\-*/]     ) |        # Operator
        (?P<SPACE>    \s+         )          # Whitespace
        """,
        re.VERBOSE
    )

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression string.

        Parameters:
            expression (str): The input arithmetic expression.

        Returns:
            float: Result of the evaluated expression.

        Raises:
            ValueError: For invalid input or syntax errors.
            ZeroDivisionError: For division by zero.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string to a list of tokens.
        Handles negative numbers carefully.

        Parameters:
            expression (str): Input arithmetic expression.

        Returns:
            List[str]: List of tokens as strings.

        Raises:
            ValueError: If unknown characters are present.
        """

        tokens: List[str] = []
        pos = 0
        length = len(expression)

        while pos < length:
            match = self.TOKEN_REGEX.match(expression, pos)
            if not match:
                raise ValueError(f"Invalid character at position {pos}: '{expression[pos]}'")

            if match.lastgroup == 'NUMBER':
                tokens.append(match.group('NUMBER'))
            elif match.lastgroup == 'OP':
                # Special handling for unary minus (negative numbers)
                op = match.group('OP')
                # If it's a '-' and either at start, or after an operator or left parenthesis, treat as unary
                if (op == '-' and
                    (len(tokens) == 0 or
                     tokens[-1] in ('+', '-', '*', '/', '('))):
                    # Look ahead for number (unary minus) 
                    num_match = self.TOKEN_REGEX.match(expression, match.end())
                    if num_match and num_match.lastgroup == 'NUMBER':
                        neg_number = '-' + num_match.group('NUMBER')
                        tokens.append(neg_number)
                        pos = num_match.end()
                        continue
                    else:
                        # Standalone '-', treat as unary minus for zero
                        tokens.append('0')
                        tokens.append('-')
                else:
                    tokens.append(op)
            elif match.lastgroup == 'LPAREN':
                tokens.append('(')
            elif match.lastgroup == 'RPAREN':
                tokens.append(')')
            # Ignore spaces
            pos = match.end()

        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the list of tokens for balanced parentheses and valid sequence.

        Parameters:
            tokens (List[str]): Token list to validate.

        Raises:
            ValueError: For unbalanced parentheses or invalid token sequences.
        """
        paren_count = 0
        prev = None
        for token in tokens:
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
            elif token in self.OPERATORS and prev in self.OPERATORS:
                raise ValueError("Invalid expression: consecutive operators.")
            prev = token

        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: too many '('")

    def _to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts token list to Reverse Polish Notation (Shunting Yard Algorithm).

        Parameters:
            tokens (List[str]): List of input tokens.

        Returns:
            List[Union[str, float]]: RPN as list.
        """
        output: List[Union[str, float]] = []
        stack: List[str] = []

        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                       ((self.OPERATORS[token][1] == 'L' and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]) or
                        (self.OPERATORS[token][1] == 'R' and self.OPERATORS[token][0] < self.OPERATORS[stack[-1]][0]))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    # Should be caught during validation, but double check
                    raise ValueError("Unbalanced parentheses during conversion.")
                stack.pop()
            else:
                # Should never get here due to tokenize/validate
                raise ValueError(f"Invalid token: {token}")

        while stack:
            if stack[-1] == '(' or stack[-1] == ')':
                raise ValueError("Unbalanced parentheses at the end.")
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates an RPN expression.

        Parameters:
            rpn (List[Union[str, float]]): RPN token list.

        Returns:
            float: Result value.

        Raises:
            ZeroDivisionError: For division by zero.
            ValueError: For invalid RPN.
        """
        stack: List[float] = []

        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: insufficient operands.")

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
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(a / b)
            else:
                raise ValueError(f"Invalid RPN token: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid syntax after RPN evaluation.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """
        Checks if token is a valid number.

        Parameters:
            token (str): Token to check.

        Returns:
            bool: True if token is number.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

# --- Optional: Main function for demonstration and basic testing ---
if __name__ == "__main__":
    calculator = Calculator()
    example_expressions = [
        "1 + 2 * 3",
        "(2 + 3) * 4.5 - -2.5",
        "-6 / 2",
        "(-2.3 + 4) * (7 - 5) / 2",
        "3.14 + (1 - (2 + (3*4))) / 5",
        "10 / (5 - 5)",  # Should raise ZeroDivisionError
        "((1+2)*(3-4)",  # Should raise ValueError: Unbalanced
        "3 + + 4",       # Should raise ValueError
    ]
    for expr in example_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
