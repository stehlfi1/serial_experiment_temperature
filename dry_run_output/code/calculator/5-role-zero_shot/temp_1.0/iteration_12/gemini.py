
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that safely evaluates mathematical
    expressions from a string.

    This implementation adheres to the ISO/IEC 25010 standard by focusing on
    correctness, efficiency, security, and maintainability. It uses the
    Shunting-yard algorithm to handle operator precedence and parentheses
    without using the insecure `eval()` function.
    """

    # Operator precedence and associativity for the Shunting-yard algorithm.
    # Higher numbers indicate higher precedence.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'left'},
        '-': {'precedence': 1, 'assoc': 'left'},
        '*': {'precedence': 2, 'assoc': 'left'},
        '/': {'precedence': 2, 'assoc': 'left'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate (e.g., "3 + 4 * (2 - 1)").

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression contains invalid characters, unbalanced
                        parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        self._validate_expression(expression)
        tokens = self._tokenize(expression)
        rpn_queue = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn_queue)
        return float(result)

    def _validate_expression(self, expression: str) -> None:
        """
        Validates the entire expression for basic correctness.

        Args:
            expression: The expression string.

        Raises:
            ValueError: If invalid characters or unbalanced parentheses are found.
        """
        # Check for invalid characters
        allowed_chars = "0123456789.+-*/() "
        if any(char not in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters")

        # Check for unbalanced parentheses
        balance = 0
        for char in expression:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            if balance < 0:
                raise ValueError("Mismatched parentheses: ')' found before '('")
        if balance != 0:
            raise ValueError("Mismatched parentheses: Unbalanced number of '(' and ')'")

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Converts the input expression string into a list of tokens (numbers and operators).
        Handles unary minus correctly.

        Args:
            expression: The expression string.

        Returns:
            A list of tokens. For example, "-3.5 + 4" becomes [-3.5, '+', 4.0].
        """
        # Use regex to find all numbers (including floats) and operators
        # This regex robustly splits numbers, operators, and parentheses.
        token_pattern = re.compile(r'(\d+\.\d*|\.\d+|\d+|[+\-*/()])')
        raw_tokens = token_pattern.findall(expression.replace(" ", ""))

        tokens = []
        for i, token in enumerate(raw_tokens):
            if token == '-':
                # Check if '-' is a unary minus
                # It's unary if it's the first token, or if the preceding token
                # was an operator or an opening parenthesis.
                is_unary = (i == 0) or (raw_tokens[i - 1] in "+-*/(")
                if is_unary:
                    # Combine with the next number token to form a negative number
                    try:
                        next_token = raw_tokens[i + 1]
                        # This feels like mutation, but it is to create one token from two
                        # So we mark the original '-' to be skipped later
                        raw_tokens[i+1] = f"-{next_token}"
                        continue  # Skip appending the standalone '-'
                    except IndexError:
                        raise ValueError("Invalid expression: '-' at the end of expression")
                
            # If the current token was marked as part of a negative number, skip it.
            # This check is needed because we modified the list in-place.
            if token.startswith('-') and i > 0 and raw_tokens[i-1] == '-':
                 # This is the number part of a unary minus, has been merged.
                 # The prior element must be '-')
                 pass
            
            # Convert numeric strings to float, leave operators as strings
            try:
                tokens.append(float(token))
            except ValueError:
                tokens.append(token)
        
        # A filter to clear out the original '-' that were part of unary operations
        # This is a bit clumsy, but simpler than complex look-ahead logic above
        if '-' in raw_tokens:
             final_tokens = []
             for i, token in enumerate(tokens):
                 if token == '-' and isinstance(tokens[i+1], float) and tokens[i+1] < 0:
                     continue
                 final_tokens.append(token)
             return final_tokens

        return tokens


    def _shunting_yard(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts a list of tokens in infix notation to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of numbers (float) and operators (str).

        Returns:
            A list of tokens in RPN order.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._OPERATORS:
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       (self._OPERATORS[operator_stack[-1]]['precedence'] > self._OPERATORS[token]['precedence'] or
                        (self._OPERATORS[operator_stack[-1]]['precedence'] == self._OPERATORS[token]['precedence'] and
                         self._OPERATORS[token]['assoc'] == 'left'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                     # This should be caught by pre-validation, but serves as a safeguard.
                    raise ValueError("Mismatched parentheses in expression")
                operator_stack.pop()  # Discard the '('

        # Pop any remaining operators from the stack to the output queue
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                # This indicates a mismatch, guarded by pre-validation.
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[str, float]]) -> float:
        """
        Evaluates a queue of tokens in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of tokens in RPN.

        Returns:
            The final result of the calculation.
        """
        stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands for operator")
                
                op2 = stack.pop()
                op1 = stack.pop()

                if token == '+':
                    stack.append(op1 + op2)
                elif token == '-':
                    stack.append(op1 - op2)
                elif token == '*':
                    stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    stack.append(op1 / op2)

        if len(stack) != 1:
            raise ValueError("Invalid expression: The expression is incomplete or malformed")
        
        return stack[0]


if __name__ == "__main__":
    # This block demonstrates the usage of the Calculator class and serves as
    # a basic set of integration tests.
    calculator = Calculator()

    test_expressions = [
        "3 + 4 * 2 / ( 1 - 5 )",  # Precedence and parentheses
        "10 + -2 * 5",            # Unary minus
        "-5 * -2",                # Double unary minus
        "100 / 2 / 5",            # Left-associativity
        "2.5 * 4",                # Floating point numbers
        "(1 + 2) * 3",            # Basic parentheses
        "- (3 + 4)",              # Unary minus with parentheses
        "10",                     # Single number
    ]

    print("--- Running Calculator Tests ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}'\nResult: {result}\n")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}'\nError: {e}\n")

    print("\n--- Testing Error Cases ---")
    error_expressions = [
        "5 * (3 + 2",    # Unbalanced parentheses
        "5 +",          # Incomplete expression
        "1 / 0",        # Division by zero
        "5 & 4",        # Invalid character
        "5 5 +",        # Malformed expression (missing operator)
    ]
    for expr in error_expressions:
        try:
            calculator.calculate(expr)
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}'\nCaught Expected Error: {e}\n")
