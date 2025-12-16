
from typing import List, Union
import re

class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass

class Calculator:
    """
    Console-based arithmetic calculator supporting +, -, *, /, parentheses, 
    and correct operator precedence with integer and floating point numbers.
    
    Adheres to ISO/IEC 25010 on correctness, safety, and quality principles.
    """
    
    # Supported operators and their precedences
    OPERATORS = {
        '+': (1, 'left'),
        '-': (1, 'left'),
        '*': (2, 'left'),
        '/': (2, 'left'),
    }
    
    TOKEN_PATTERN = re.compile(
        r'\s*('
        r'-?\d+(?:\.\d+)?'      # numbers, possibly negative, integer or decimal
        r'|[+\-*/()]'           # operators and parentheses
        r')\s*'
    )
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.

        :param expression: Expression string (e.g., "3 + (2 * 5) / 4")
        :return: Evaluation result as float
        :raises CalculatorError: On invalid input or math errors
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expr: str) -> List[str]:
        """
        Splits and validates the input into a list of tokens.

        :param expr: Raw infix expression string
        :return: List of token strings
        """
        if not expr or not isinstance(expr, str):
            raise CalculatorError("Input must be a non-empty string.")

        tokens = []
        position = 0
        while position < len(expr):
            match = self.TOKEN_PATTERN.match(expr, position)
            if not match:
                raise CalculatorError(f"Invalid character at position {position}: '{expr[position]}'")
            token = match.group(1)
            tokens.append(token)
            position = match.end()
        
        self._validate_tokens(tokens)
        return tokens

    def _validate_tokens(self, tokens: List[str]):
        """
        Validates token list for correct sequence and characters.

        :param tokens: List of tokens
        :raises CalculatorError: On invalid sequencing or character usage
        """
        # Check for balanced parentheses
        paren_count = 0
        prev_token = None
        for i, token in enumerate(tokens):
            if token == '(':
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise CalculatorError("Unbalanced parentheses in expression.")
            elif token in self.OPERATORS:
                if prev_token is None or prev_token in self.OPERATORS or prev_token == '(':
                    # Allow unary minus, e.g., "-3"
                    if token == '-' and (prev_token is None or prev_token == '('):
                        pass
                    else:
                        raise CalculatorError(f"Operator '{token}' at invalid position.")
            else:
                # Should be a valid number
                try:
                    float(token)
                except ValueError:
                    raise CalculatorError(f"Invalid number: {token}")
            prev_token = token
        if paren_count != 0:
            raise CalculatorError("Unbalanced parentheses in expression.")

    def _to_rpn(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN)
        using the shunting-yard algorithm.

        :param tokens: List of infix tokens
        :return: List of tokens in RPN order
        """
        output_queue = []
        operator_stack = []
        i = 0

        while i < len(tokens):
            token = tokens[i]
            # Number (operand)
            if self._is_number(token):
                output_queue.append(float(token))
            # Operator
            elif token in self.OPERATORS:
                # Handle unary minus as negative numbers
                if token == '-' and (i == 0 or tokens[i-1] in self.OPERATORS or tokens[i-1] == '('):
                    # Merge unary minus with number
                    if i + 1 < len(tokens) and self._is_number(tokens[i+1]):
                        output_queue.append(-float(tokens[i+1]))
                        i += 1
                    else:
                        raise CalculatorError("Invalid use of unary minus.")
                else:
                    while (operator_stack and 
                           operator_stack[-1] in self.OPERATORS and
                           (
                               (self.OPERATORS[token][1] == 'left' and self.OPERATORS[token][0] <= self.OPERATORS[operator_stack[-1]][0]) or
                               (self.OPERATORS[token][1] == 'right' and self.OPERATORS[token][0] < self.OPERATORS[operator_stack[-1]][0])
                           )):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise CalculatorError("Mismatched parentheses encountered.")
                operator_stack.pop()  # Remove '('
            else:
                raise CalculatorError(f"Invalid token: {token}")
            i += 1
        
        # Empty remaining operators
        while operator_stack:
            op = operator_stack.pop()
            if op in ('(', ')'):
                raise CalculatorError("Unbalanced parentheses at end of expression.")
            output_queue.append(op)
        
        return output_queue

    def _is_number(self, s: str) -> bool:
        """
        Checks if the string represents a number.

        :param s: Input string
        :return: True if number, False otherwise
        """
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def _evaluate_rpn(self, rpn: List[Union[float, str]]) -> float:
        """
        Evaluates an RPN (Reverse Polish Notation) token list.

        :param rpn: List of RPN tokens
        :return: Computed float result
        :raises CalculatorError: On math errors (e.g., division by zero)
        """
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise CalculatorError("Not enough operands for operator.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise CalculatorError(f"Unknown token in RPN evaluation: {token}")
        
        if len(stack) != 1:
            raise CalculatorError("Too many operands left after evaluation.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operator to two float operands.

        :param a: Left operand
        :param b: Right operand
        :param operator: Operator string (+, -, *, /)
        :return: Result float
        :raises CalculatorError: On division by zero
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise CalculatorError("Division by zero is not allowed.")
            return a / b
        else:
            raise CalculatorError(f"Unsupported operator '{operator}'.")

# --- Example Usage and Test Cases ---

if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "3 + 4 * 2 / (1 - 5)",          # Simple precedence
        "10 + 2 * 6",                   # Order of operations
        "100 * (2 + 12)",               # Parentheses
        "100 * (2 + 12) / 14",          # Combined ops & parentheses
        "-2.5 + 1.5 * (4 - 2)",         # Negative, float, parentheses
        "((2 + 3.1) * (7-4.1)) / -2",   # Nested parentheses, negative divisor
        "1 - -2",                       # Double negative
        "42",                           # Single number
        "3 +",                          # Invalid (missing operand)
        "(4 + 5",                       # Invalid (unbalanced)
        "2 ** 5",                       # Invalid (unsupported op)
        "3.14 / 0",                     # Division by zero
    ]

    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except CalculatorError as ce:
            print(f"{expr} -> Error: {ce}")
