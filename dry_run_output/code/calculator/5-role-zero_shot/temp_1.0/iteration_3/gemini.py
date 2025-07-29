
import collections

class Calculator:
    """
    A high-quality, maintainable calculator that evaluates arithmetic expressions.

    This class provides a safe and efficient way to evaluate string-based
    mathematical expressions containing integers, floating-point numbers,
    parentheses, and the four basic arithmetic operators (+, -, *, /).

    It adheres to ISO/IEC 25010 principles by focusing on correctness,
    performance, reliability, security, and maintainability. It uses the
    Shunting-yard algorithm to safely parse expressions without using the
    dangerous `eval()` function.

    Attributes:
        _OPERATORS (set): A set of supported binary operators.
        _PRECEDENCE (dict): A mapping of operators to their precedence level.
        _UNARY_MINUS (str): A special token to represent unary minus internally.
    """

    _OPERATORS = {'+', '-', '*', '/'}
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    # Internal token for unary minus to distinguish from binary subtraction
    _UNARY_MINUS = '~'

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public method that orchestrates the tokenization, parsing,
        and evaluation of the expression.

        Args:
            expression: The mathematical expression string to evaluate.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid characters,
                        or has unbalanced parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            postfix_queue = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to provide a clean, user-facing error.
            raise e
        except Exception as e:
            # Catch any other unexpected errors and wrap them in a ValueError.
            raise ValueError(f"Invalid or malformed expression: {e}") from e

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts the input string expression into a list of tokens.

        This method handles numbers (integers and floats), operators,
        parentheses, and correctly identifies unary minus.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens.

        Raises:
            ValueError: If an unrecognized character is found.
        """
        tokens = []
        num_buffer = ""
        # The previous token is used to correctly identify unary minus.
        # A minus is unary if it's at the start or follows an operator or '('.
        prev_token = None

        for char in expression:
            if char.isspace():
                continue

            if char.isdigit() or char == '.':
                num_buffer += char
            else:
                if num_buffer:
                    tokens.append(num_buffer)
                    prev_token = num_buffer
                    num_buffer = ""

                if char == '-' and (prev_token is None or prev_token in self._OPERATORS or prev_token == '('):
                    # This is a unary minus for negation.
                    tokens.append(self._UNARY_MINUS)
                elif char in self._OPERATORS or char in '()':
                    tokens.append(char)
                else:
                    raise ValueError(f"Invalid character in expression: '{char}'")
                prev_token = char

        if num_buffer:
            tokens.append(num_buffer)

        return tokens

    def _infix_to_postfix(self, tokens: list[str]) -> collections.deque:
        """
        Converts a token list from infix to postfix (RPN) notation.

        This implementation uses the Shunting-yard algorithm. It correctly
        handles operator precedence and associativity.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A deque containing tokens in postfix (RPN) order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = collections.deque()
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                output_queue.append(token)
            elif token == self._UNARY_MINUS:
                 operator_stack.append(token)
            elif token in self._OPERATORS:
                while (operator_stack and
                       operator_stack[-1] in self._OPERATORS and
                       self._PRECEDENCE.get(operator_stack[-1], 0) >= self._PRECEDENCE.get(token, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression")
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            operator = operator_stack.pop()
            if operator == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(operator)

        return output_queue

    def _evaluate_postfix(self, postfix_queue: collections.deque) -> float:
        """
        Evaluates a postfix (RPN) expression.

        Args:
            postfix_queue: A deque of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., insufficient operands).
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack = []

        for token in postfix_queue:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                operand_stack.append(float(token))
            elif token == self._UNARY_MINUS:
                if not operand_stack:
                    raise ValueError("Invalid expression: unary minus requires an operand")
                operand_stack.append(-operand_stack.pop())
            elif token in self._OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError(f"Invalid expression: operator '{token}' requires two operands")
                
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
                        raise ZeroDivisionError("Division by zero")
                    operand_stack.append(op1 / op2)
        
        if len(operand_stack) != 1:
            raise ValueError("Malformed expression: invalid number of operands and operators")

        return operand_stack[0]


if __name__ == '__main__':
    """
    Example usage of the Calculator class.
    
    This block demonstrates how to instantiate and use the calculator,
    showcasing both valid calculations and error handling.
    """
    calculator = Calculator()

    print("Welcome to the High-Quality Python Calculator!")
    print("Enter 'exit' to quit.\n")

    # --- Test Cases ---
    print("--- Running Built-in Test Cases ---")
    test_expressions = {
        "Basic Addition": "5 + 3",
        "Basic Subtraction": "10 - 4",
        "Basic Multiplication": "6 * 7",
        "Basic Division": "20 / 4",
        "Operator Precedence": "2 + 3 * 4",
        "Parentheses": "(2 + 3) * 4",
        "Floating Point Numbers": "3.5 * (2.1 - 1.1)",
        "Negative Numbers": "-5 * (-2 + 8)",
        "Complex Expression": "10 + (4 - 2) * 3 / (1 + 1) - -1",
        "Division by Zero": "10 / (5 - 5)",
        "Invalid Character": "5_ + 3",
        "Mismatched Parentheses": "(5 + 3",
        "Malformed Expression": "5 * + 3"
    }

    for name, expr in test_expressions.items():
        try:
            result = calculator.calculate(expr)
            print(f"✅ {name}: '{expr}' = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"❌ {name}: '{expr}' -> Error: {e}")
    
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("Enter expression: ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
        
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

