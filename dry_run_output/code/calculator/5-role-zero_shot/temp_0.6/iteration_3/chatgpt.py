
import re
from typing import List, Union

class Calculator:
    """
    Console-based arithmetic calculator that supports +, -, *, /, parentheses,
    integers, floating-point numbers, and negative values.
    
    This class adheres to ISO/IEC 25010 requirements for correctness, performance,
    modularity, safety, testability, readability, and documentation.
    """
    
    # Define allowed operators and their precedence
    OPERATORS = {
        '+': (1, 'L'),  # (precedence, associativity)
        '-': (1, 'L'),
        '*': (2, 'L'),
        '/': (2, 'L')
    }
    
    TOKEN_REGEX = re.compile(r'\s*([-+*/()])|\s*([0-9]*\.?[0-9]+)')
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression string and returns the calculated result.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the evaluated expression.
        
        Raises:
            ValueError: If the input is invalid (e.g., unbalanced parentheses, invalid characters).
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input expression string into a list of tokens (numbers, operators, parentheses).
        Handles negative numbers appropriately.
        """
        tokens = []
        index = 0
        length = len(expression)
        prev_token = None

        while index < length:
            match = self.TOKEN_REGEX.match(expression, index)
            if not match:
                raise ValueError(f"Invalid character at position {index}: '{expression[index]}'")
            op, num = match.groups()
            if op:
                # Handle unary minus (negative numbers)
                if op == '-' and (prev_token is None or prev_token in self.OPERATORS or prev_token == '('):
                    # This is a unary minus, look ahead for a number
                    next_match = self.TOKEN_REGEX.match(expression, match.end())
                    if next_match and next_match.group(2):
                        tokens.append('-' + next_match.group(2))
                        index = next_match.end()
                        prev_token = 'num'
                        continue
                    else:
                        raise ValueError(f"Invalid unary minus at position {index}")
                tokens.append(op)
                prev_token = op
            elif num:
                tokens.append(num)
                prev_token = 'num'
            index = match.end()
        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the list of tokens for syntax errors such as unbalanced parentheses,
        invalid sequences, etc.
        """
        paren_count = 0
        prev_token = None
        for token in tokens:
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many ')'")
            elif token in self.OPERATORS:
                if prev_token is None or prev_token in self.OPERATORS or prev_token == '(':
                    raise ValueError("Invalid operator placement")
            else:
                # Must be a number
                try:
                    float(token)
                except ValueError:
                    raise ValueError(f"Invalid number: {token}")
            prev_token = token
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: too many '('")
        if prev_token in self.OPERATORS:
            raise ValueError("Expression cannot end with an operator")

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN) using the shunting yard algorithm.
        """
        output = []
        stack = []
        for token in tokens:
            if self._is_number(token):
                output.append(token)
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
                    raise ValueError("Unbalanced parentheses")
                stack.pop()
        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses")
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn: List[str]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation.
        """
        stack: List[float] = []
        for token in rpn:
            if self._is_number(token):
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Unknown token in RPN: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies the operator to two operands and returns the result.
        Raises ZeroDivisionError for division by zero.
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

    def _is_number(self, token: str) -> bool:
        """
        Checks if the token is a valid number.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    # Example usage and simple test cases
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-4 + 3",
        "3 + -4.5 * 2",
        "10 / 2 + 6 * (2 - 3.5)",
        "4 / 0",  # Should raise ZeroDivisionError
        "2 + (3 * 4",  # Should raise ValueError (unbalanced)
        "2 ++ 3",  # Should raise ValueError (invalid operator placement)
        "abc + 1",  # Should raise ValueError (invalid character)
    ]
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
