
import collections

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class implements a calculator that adheres to standard operator precedence,
    supports parentheses, and handles both integer and floating-point numbers.
    The implementation uses the Shunting-yard algorithm to convert infix
    expressions to postfix (RPN) for safe and efficient evaluation,
    explicitly avoiding the use of `eval()`.

    The design emphasizes modularity, testability, and robust error handling,
    aligning with the principles of the ISO/IEC 25010 standard for
    software quality.

    Attributes:
        _OPERATORS (dict): A dictionary mapping operators to their precedence and
                           associativity ('L' for left, 'R' for right).
    """

    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'L'},
        '-': {'precedence': 1, 'assoc': 'L'},
        '*': {'precedence': 2, 'assoc': 'L'},
        '/': {'precedence': 2, 'assoc': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate. It can
                        contain numbers, operators (+, -, *, /), and
                        parentheses.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., malformed,
                        contains unknown characters, unbalanced parentheses).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")
        if not expression:
            raise ValueError("Expression cannot be empty.")

        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (IndexError, KeyError):
            # IndexError from pop() on empty list or KeyError on operator lookup
            # indicates a malformed expression (e.g., "5 *", "++2").
            raise ValueError("Invalid or malformed expression.")

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts the input string expression into a list of tokens.

        This private method handles numbers (including floats and negatives),
        operators, and parentheses. It correctly distinguishes between binary
        subtraction and unary negation.

        Returns:
            A list of tokens (e.g., ['-3.5', '*', '(', '4', '+', '2', ')']).

        Raises:
            ValueError: If an unrecognized character is found.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
                continue

            if char in self._OPERATORS or char in '()':
                # Handle unary minus (negation) vs. binary minus (subtraction)
                if char == '-':
                    is_unary = (
                        not tokens or
                        tokens[-1] in self._OPERATORS or
                        tokens[-1] == '('
                    )
                    if is_unary:
                        # It's a unary minus, find the number it applies to
                        i += 1
                        # Skip any whitespace after the minus sign
                        while i < len(expression) and expression[i].isspace():
                            i += 1
                        
                        if i == len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                            raise ValueError("Invalid use of unary minus.")
                        
                        num_str = "-"
                        while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                            num_str += expression[i]
                            i += 1
                        tokens.append(num_str)
                        continue
                
                # It's a binary operator or parenthesis
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Unrecognized character in expression: '{char}'")
        
        return tokens

    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """
        Converts a tokenized infix expression to postfix (RPN) using Shunting-yard.

        Returns:
            A list of tokens in postfix order.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue = collections.deque()
        operator_stack = []

        for token in tokens:
            try:
                # If token is a number, add it to the output queue
                float(token)
                output_queue.append(token)
            except ValueError:
                # Token is an operator or parenthesis
                if token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if not operator_stack or operator_stack[-1] != '(':
                        raise ValueError("Mismatched parentheses in expression.")
                    operator_stack.pop()  # Discard the '('
                else:  # Token is an operator
                    op1_info = self._OPERATORS[token]
                    while (operator_stack and operator_stack[-1] != '(' and
                           (self._OPERATORS[operator_stack[-1]]['precedence'] > op1_info['precedence'] or
                            (self._OPERATORS[operator_stack[-1]]['precedence'] == op1_info['precedence'] and op1_info['assoc'] == 'L'))):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)

        # Pop any remaining operators from the stack to the output
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return list(output_queue)

    def _evaluate_postfix(self, postfix_tokens: list[str]) -> float:
        """
        Evaluates a postfix (RPN) expression.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: For division by zero.
        """
        operand_stack = []

        for token in postfix_tokens:
            try:
                operand_stack.append(float(token))
            except ValueError:  # Token is an operator
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator.")
                
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                
                if token == '+':
                    operand_stack.append(op1 + op2)
                elif token == '-':
                    operand_stack.append(op1 - op2)
                elif token == '*':
                    operand_stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    operand_stack.append(op1 / op2)
        
        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: too many operands.")
            
        return operand_stack[0]


if __name__ == '__main__':
    # This block demonstrates the usage of the Calculator class
    # and serves as a simple integration test.
    
    calculator = Calculator()
    
    print("--- Console Arithmetic Calculator ---")
    print("Enter 'exit' to quit.")
    
    # Example expressions for demonstration
    test_expressions = [
        "3 + 5 * 2",              # Expected: 13.0
        "(3 + 5) * 2",            # Expected: 16.0
        "10 / 2 - 3",             # Expected: 2.0
        "10 / (2 - 3)",           # Expected: -10.0
        "-5.5 * (2 + 1)",         # Expected: -16.5
        "2 * -3",                 # Expected: -6.0 (Handled)
        "100 / 10 * 2",           # Expected: 20.0
        "1 + 2 * (3 - 4 / 2) + 5",# Expected: 8.0
        "10 / 0",                 # Expected: ZeroDivisionError
        "(3 + 5",                 # Expected: ValueError (Mismatched parentheses)
        "3 + 5)",                 # Expected: ValueError (Mismatched parentheses)
        "3 & 4",                  # Expected: ValueError (Unrecognized character)
        "3 + * 4",                # Expected: ValueError (Malformed expression)
    ]
    
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: {expr:<25} | Result: {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Expression: {expr:<25} | Error: {e}")
            
    # Interactive loop
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("Enter expression: ")
            if user_input.lower() == 'exit':
                break
            result = calculator.calculate(user_input)
            print(f"Result: {result}\n")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}\n")

