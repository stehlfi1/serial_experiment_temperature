
from typing import List, Union

class CalculatorError(Exception):
    """Custom exception class for Calculator-related errors."""
    pass

class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions
    containing +, -, *, /, parentheses, and numbers (integers or floats).
    Implements robust input validation and operator precedence without using eval().
    """

    # Define operator precedence and associativity
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'left'},
        '-': {'precedence': 1, 'associativity': 'left'},
        '*': {'precedence': 2, 'associativity': 'left'},
        '/': {'precedence': 2, 'associativity': 'left'}
    }
    VALID_CHARACTERS = set('0123456789.+-*/() ')
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: For syntax errors, invalid characters, or unbalanced parentheses.
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """
        Converts the expression string into a list of tokens (numbers, operators, or parentheses).
        Handles negative numbers, decimal numbers, and validates characters and parentheses.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            List[Union[str, float]]: List of tokens.

        Raises:
            ValueError: For invalid characters or unbalanced parentheses.
        """
        if not expression or not isinstance(expression, str):
            raise ValueError("Expression must be a non-empty string.")

        # Validate allowed characters
        if not set(expression).issubset(self.VALID_CHARACTERS):
            raise ValueError(f"Invalid character(s) in expression: {expression}")

        tokens = []
        num_buffer = []
        prev_token = None
        paren_balance = 0
        i = 0
        length = len(expression)

        while i < length:
            char = expression[i]

            if char.isspace():
                i += 1
                continue
            elif char in '0123456789.':
                # Build the current number (integer or float)
                num_buffer.append(char)
                i += 1
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    num_buffer.append(expression[i])
                    i += 1
                num_str = ''.join(num_buffer)
                if num_str.count('.') > 1:
                    raise ValueError(f"Invalid numeric format: {num_str}")
                tokens.append(float(num_str) if '.' in num_str else int(num_str))
                num_buffer = []
                prev_token = 'number'
            elif char in self.OPERATORS:
                # Handle unary minus (negative numbers)
                if char == '-' and (prev_token is None or (prev_token in ('operator', '(',))):
                    # Start of expression or follows '(' or another operator => unary minus
                    num_buffer.append('-')
                    i += 1
                else:
                    tokens.append(char)
                    prev_token = 'operator'
                    i += 1
            elif char == '(':
                tokens.append(char)
                paren_balance += 1
                prev_token = '('
                i += 1
            elif char == ')':
                tokens.append(char)
                paren_balance -= 1
                if paren_balance < 0:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses.")
                prev_token = ')'
                i += 1
            else:
                # Should never happen due to earlier character check
                raise ValueError(f"Unexpected character: '{char}'")

        if num_buffer:
            num_str = ''.join(num_buffer)
            if num_str.count('.') > 1:
                raise ValueError(f"Invalid numeric format: {num_str}")
            tokens.append(float(num_str) if '.' in num_str else int(num_str))

        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses in expression.")

        self._validate_tokens(tokens)
        return tokens

    def _validate_tokens(self, tokens: List[Union[str, float]]) -> None:
        """
        Performs syntactic validation on the token list (e.g., invalid operator sequences).

        Args:
            tokens (List[Union[str, float]]): The tokenized expression.

        Raises:
            ValueError: For invalid token sequences.
        """
        if not tokens:
            raise ValueError("Empty expression.")

        prev = None
        for i, token in enumerate(tokens):
            if isinstance(token, (int, float)):
                # Number following number/closing parenthesis is valid
                if prev in ('number', ')'):
                    pass
                prev = 'number'
            elif token in self.OPERATORS:
                if prev is None or prev in ('operator', '('):
                    # For binary operators, must not start after another operator or '(' unless unary minus
                    if not (token == '-' and (prev is None or prev == '(')):
                        raise ValueError(f"Invalid operator sequence near '{token}'.")
                prev = 'operator'
            elif token == '(':
                if prev in ('number', ')'):
                    # Should not be immediately preceded by a number or ')'
                    raise ValueError("Misplaced '('.")
                prev = '('
            elif token == ')':
                if prev in ('operator', '(') or prev is None:
                    raise ValueError("Misplaced ')'.")
                prev = ')'
            else:
                raise ValueError(f"Invalid token in expression: {token}")

        if prev == 'operator':
            raise ValueError("Expression cannot end with an operator.")

    def _to_postfix(self, tokens: List[Union[str, float]]) -> List[Union[str, float]]:
        """
        Converts an infix token list into a postfix (Reverse Polish Notation) token list
        using the Shunting Yard algorithm.

        Args:
            tokens (List[Union[str, float]]): Infix token list.

        Returns:
            List[Union[str, float]]: Postfix token list.

        Raises:
            ValueError: For syntactic errors.
        """
        output = []
        stack = []

        for token in tokens:
            if isinstance(token, (int, float)):
                output.append(token)
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                       ((self.OPERATORS[token]['associativity'] == 'left' and
                         self.OPERATORS[token]['precedence'] <= self.OPERATORS[stack[-1]]['precedence']))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses during conversion to postfix.")
                stack.pop()  # Remove '('
            else:
                raise ValueError(f"Invalid token: {token}")

        while stack:
            if stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses in expression.")
            output.append(stack.pop())

        return output

    def _evaluate_postfix(self, tokens: List[Union[str, float]]) -> float:
        """
        Evaluates a postfix (RPN) expression and returns the numeric result.

        Args:
            tokens (List[Union[str, float]]): Postfix token list.

        Returns:
            float: Computed result.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: For invalid syntax.
        """
        stack = []

        for token in tokens:
            if isinstance(token, (int, float)):
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError(f"Insufficient operands for operator '{token}'.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid syntax: too many values left after evaluation.")

        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operator to two operands.

        Args:
            a (float): Left operand.
            b (float): Right operand.
            operator (str): One of '+', '-', '*', '/'.

        Returns:
            float: Result of the operation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
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
            # Should never happen
            raise ValueError(f"Unknown operator: {operator}")

# Example test cases (for demonstration and testability)
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "2 + 2",
        "3 * (4 + 5)",
        "-7 + 2 * 3",
        "10 / (5 - 5)",
        "3.5 * (-2 + 4.2)",
        "2 + ((3.1 - 4.2) * 2) / 5",
        "((1 + 2) * (3 + 4)) / 2"
    ]

    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {str(e)}")
