
from typing import List, Union

class Calculator:
    """
    Arithmetic Calculator that evaluates expressions containing +, -, *, /, parentheses,
    integer and floating-point numbers (supports negative values), with correct operator precedence.
    """

    # Supported operators and their precedence
    _OPERATORS = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression.
        
        :param expression: The string arithmetic expression to evaluate.
        :return: The computed result as a float.
        :raises ValueError: For invalid input, such as unbalanced parentheses or invalid characters.
        :raises ZeroDivisionError: When division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(rpn)

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Converts the input expression string into a list of tokens (numbers, operators, parentheses).
        
        :param expression: The string arithmetic expression.
        :return: List of tokens (floats for numbers, strings for operators/parentheses).
        :raises ValueError: If invalid characters or unbalanced parentheses are detected.
        """
        tokens = []
        num_buffer = ''
        i = 0
        n = len(expression)
        paren_balance = 0

        def flush_num_buffer():
            nonlocal num_buffer
            if num_buffer != '':
                try:
                    tokens.append(float(num_buffer))
                except ValueError:
                    raise ValueError(f"Invalid number: {num_buffer}")
                num_buffer = ''

        while i < n:
            char = expression[i]
            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                num_buffer += char
                i += 1
            elif char in self._OPERATORS:
                # Handle negative numbers (unary minus, possibly also unary plus)
                if (char == '-' or char == '+') and (
                    i == 0 or (expression[i-1] in self._OPERATORS or expression[i-1] == '(')
                ):
                    # It's a unary operator; attach to the number
                    num_buffer += char
                    i += 1
                else:
                    flush_num_buffer()
                    tokens.append(char)
                    i += 1
            elif char in ('(', ')'):
                flush_num_buffer()
                if char == '(':
                    paren_balance += 1
                else:
                    paren_balance -= 1
                    if paren_balance < 0:
                        raise ValueError("Unbalanced parentheses: too many closing parentheses")
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character in expression: '{char}'")
        flush_num_buffer()

        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses: mismatched opening/closing")
        if not tokens:
            raise ValueError("Expression is empty or invalid")
        return tokens

    def _infix_to_postfix(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts a list of infix tokens to postfix (Reverse Polish Notation) using the shunting yard algorithm.
        
        :param tokens: List of tokens.
        :return: List of tokens in postfix order.
        """
        output = []
        stack = []
        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in self._OPERATORS:
                while (stack and stack[-1] in self._OPERATORS and
                        self._OPERATORS[token] <= self._OPERATORS[stack[-1]]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Unbalanced parentheses detected during parsing")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Unknown token encountered: {token}")

        while stack:
            if stack[-1] == '(' or stack[-1] == ')':
                raise ValueError("Unbalanced parentheses detected at the end of parsing")
            output.append(stack.pop())
        return output

    def _evaluate_postfix(self, rpn: List[Union[str, float]]) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.
        
        :param rpn: List of tokens in postfix order.
        :return: Computed result as float.
        :raises ZeroDivisionError: On division by zero.
        :raises ValueError: If the expression is malformed.
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient values for operation")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Unknown token in evaluation: {token}")
        if len(stack) != 1:
            raise ValueError("Malformed expression: leftover values after evaluation")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Safely applies an operator to two numbers.
        :param a: Left operand
        :param b: Right operand
        :param operator: One of '+', '-', '*', '/'
        :return: The result of the operation
        :raises ZeroDivisionError: On division by zero
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero detected.")
            return a / b
        else:
            raise ValueError(f"Invalid operator: {operator}")

# Example usage (You can use these for simple tests):
if __name__ == "__main__":
    calc = Calculator()
    expressions = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-4 + (6/2) * 3",
        "10 / 0",     # Will raise ZeroDivisionError
        "7 + +5.0",   # Valid unary plus
        "(((1)))",    # Valid multiple parentheses
        "-3.5 * 2",   # Test negative float
        "2*-3",
        "5 + ((1 + 2) * 4) - 3",
    ]

    for expr in expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr}': {e}")
