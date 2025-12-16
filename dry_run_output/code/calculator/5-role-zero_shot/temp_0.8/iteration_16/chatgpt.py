
from typing import List, Union

class CalculatorError(Exception):
    """Custom exception class for Calculator errors."""
    pass

class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, /, parentheses,
    correct precedence, integer and floating-point numbers (including negatives).
    Follows ISO/IEC 25010 code quality requirements.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate the arithmetic expression.
        
        Args:
            expression (str): The arithmetic expression as a string.
        
        Returns:
            float: Result of evaluated expression.
        
        Raises:
            ValueError: On invalid input, unbalanced parentheses, invalid characters.
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        rpn = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(rpn)
        return result

    # --- Internal helpers ---

    def _tokenize(self, expression: str) -> List[str]:
        """
        Convert the input string into a list of tokens (numbers, operators, parentheses).

        Args:
            expression (str): User input arithmetic expression.

        Returns:
            List[str]: List of string tokens.

        Raises:
            ValueError: If unknown characters or invalid format is detected.
        """
        tokens = []
        num_buffer = []
        i = 0
        accepted_operators = {'+', '-', '*', '/', '(', ')'}
        prev_token = None

        def flush_number():
            nonlocal num_buffer
            if num_buffer:
                token = ''.join(num_buffer)
                # Validate that the number is correct
                try:
                    float(token)
                except ValueError:
                    raise ValueError(f"Invalid numeric token: '{token}'")
                tokens.append(token)
                num_buffer = []

        expression = expression.replace(' ', '')  # Remove spaces for simplicity
        while i < len(expression):
            char = expression[i]

            if char.isdigit() or char == '.':
                num_buffer.append(char)
                i += 1
                prev_token = 'number'
                continue

            if char in accepted_operators:
                # Handle unary minus for negative numbers
                if char == '-' and (prev_token in (None, 'operator', 'paren_l')):
                    num_buffer.append(char)
                    i += 1
                    prev_token = 'number'
                    continue
                flush_number()
                if char == '(':
                    tokens.append(char)
                    prev_token = 'paren_l'
                elif char == ')':
                    tokens.append(char)
                    prev_token = 'paren_r'
                else:
                    tokens.append(char)
                    prev_token = 'operator'
                i += 1
                continue

            raise ValueError(f"Invalid character in expression: '{char}'")
        
        flush_number()

        # Basic validation for parentheses balance
        if tokens.count('(') != tokens.count(')'):
            raise ValueError("Unbalanced parentheses in expression.")
        return tokens

    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Convert list of tokens from infix to postfix notation using Shunting Yard algorithm.

        Args:
            tokens (List[str]): List of tokens.

        Returns:
            List[str]: Postfix (RPN) token list.

        Raises:
            ValueError: If invalid syntax or unbalanced parentheses.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] in precedence and
                       precedence[token] <= precedence[operator_stack[-1]]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                found_left_paren = False
                while operator_stack:
                    op = operator_stack.pop()
                    if op == '(':
                        found_left_paren = True
                        break
                    output_queue.append(op)
                if not found_left_paren:
                    raise ValueError("Unbalanced parentheses detected during parsing.")
            else:
                raise ValueError(f"Unknown token during parsing: '{token}'")

        while operator_stack:
            op = operator_stack.pop()
            if op in '()':
                raise ValueError("Unbalanced parentheses remaining after parsing.")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, tokens: List[str]) -> float:
        """
        Evaluate an arithmetic expression in Reverse Polish Notation.

        Args:
            tokens (List[str]): Postfix token list.

        Returns:
            float: Evaluation result.

        Raises:
            ValueError: For bad format (e.g., too few operands).
            ZeroDivisionError: If division by zero is attempted.
        """
        stack: List[float] = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in {'+', '-', '*', '/'}:
                if len(stack) < 2:
                    raise ValueError(f"Insufficient operands for operator '{token}'")
                b, a = stack.pop(), stack.pop()
                result = None
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero.")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Unknown token in RPN evaluation: '{token}'")
        if len(stack) != 1:
            raise ValueError("Malformed expression: too many operands.")
        return stack[0]

    @staticmethod
    def _is_number(token: str) -> bool:
        """Helper to check if the token is a number."""
        try:
            float(token)
            return True
        except ValueError:
            return False

# --- Example tests (for demonstration) ---
# Remove or comment out below code when integrating into production or using in unit tests.

if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",
        "4.5 - 2.1 / (1 - 0.1)",
        "-2 + 3 * (4 - 1.5)",
        "10 / (2 - 2)",           # Should raise ZeroDivisionError
        "5 + * 2",                # Should raise ValueError
        "(((((3+1))))",           # Should raise ValueError
        "3.5 + (2.5 * -2)",       # Should handle negative numbers
        "1 + (2 * (3 + 4) - 5)",  # Nested parentheses
    ]

    for expr in test_expressions:
        try:
            print(f"Input: {expr}")
            result = calc.calculate(expr)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")
