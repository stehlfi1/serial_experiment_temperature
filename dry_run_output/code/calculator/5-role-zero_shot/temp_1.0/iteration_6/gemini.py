
import operator

class Calculator:
    """
    A high-quality, maintainable calculator that evaluates arithmetic expressions.

    This class provides a safe and efficient way to compute the result of
    string-based arithmetic expressions, supporting addition, subtraction,
    multiplication, division, and parentheses. It adheres to standard operator
    precedence.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Correctly evaluates expressions with operator precedence.
    - Performance Efficiency: Uses an O(n) algorithm (Shunting-Yard).
    - Reliability: Handles invalid inputs gracefully with specific exceptions.
    - Security: Avoids `eval()` to prevent code injection vulnerabilities.
    - Maintainability: The logic is modularly separated into tokenization,
      RPN conversion, and RPN evaluation for clarity and ease of modification.
    - Testability: Each internal method can be unit-tested independently.
    """

    # Define supported operators, their implementing functions, and precedence
    _OPERATORS = {
        '+': {'func': operator.add, 'prec': 1},
        '-': {'func': operator.sub, 'prec': 1},
        '*': {'func': operator.mul, 'prec': 2},
        '/': {'func': operator.truediv, 'prec': 2},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string.

        Args:
            expression: The arithmetic expression to evaluate.
                        e.g., "3 + 5 * (2 - 8)"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid
                        characters, or has unbalanced parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions with clear context for the user.
            raise e
        except IndexError:
            # Catches errors from popping from empty stacks, indicating a bad expression.
            raise ValueError("Invalid expression format or operator usage.")
        except Exception as e:
            # Catch any other unexpected errors during processing.
            raise RuntimeError(f"An unexpected error occurred: {e}")


    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts the expression string into a list of tokens.

        This tokenizer correctly handles floating-point numbers, negative numbers,
        and operators/parentheses. It also validates character usage.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        tokens = []
        num_buffer = []
        
        # Pre-process to handle unary minus correctly, e.g., turning "-5" to "0-5"
        # or "(-5)" to "(0-5)". This simplifies the main tokenizer logic.
        processed_expr = expression.replace(" ", "")
        
        for i, char in enumerate(processed_expr):
            if char.isdigit() or char == '.':
                num_buffer.append(char)
            elif char in self._OPERATORS or char in '()':
                # Flush the number buffer if it's not empty
                if num_buffer:
                    tokens.append("".join(num_buffer))
                    num_buffer = []
                
                # Handle unary minus by checking the preceding token
                if char == '-' and (i == 0 or processed_expr[i-1] in '(*/+-'):
                    tokens.append('0') # Implicit zero for unary operation
                
                tokens.append(char)
            else:
                raise ValueError(f"Invalid character in expression: '{char}'")
        
        # Add any remaining number in the buffer to the tokens list
        if num_buffer:
            tokens.append("".join(num_buffer))
            
        return tokens

    def _to_rpn(self, tokens: list[str]) -> list[str]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN)
        using the Shunting-Yard algorithm.

        Args:
            tokens: A list of tokens from the tokenizer.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit(): # Handles floats and negatives
                output_queue.append(token)
            elif token in self._OPERATORS:
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       self._OPERATORS[operator_stack[-1]]['prec'] >= self._OPERATORS[token]['prec']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Discard the left parenthesis

        # Pop any remaining operators from the stack to the queue
        while operator_stack:
            operator = operator_stack.pop()
            if operator == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(operator)
            
        return output_queue

    def _evaluate_rpn(self, rpn_tokens: list[str]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: For malformed RPN expressions.
        """
        operand_stack = []

        for token in rpn_tokens:
            if token in self._OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for an operator.")
                
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                operator_info = self._OPERATORS[token]
                
                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                result = operator_info['func'](operand1, operand2)
                operand_stack.append(result)
            else:
                try:
                    operand_stack.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid number token: {token}")

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression format.")
        
        return operand_stack[0]

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()

    # --- Test Cases ---
    expressions_to_test = [
        ("Simple addition", "5 + 3", 8.0),
        ("Simple subtraction", "10 - 4", 6.0),
        ("Simple multiplication", "6 * 7", 42.0),
        ("Simple division", "20 / 4", 5.0),
        ("Floating point numbers", "2.5 * 4 + 1.5", 11.5),
        ("Operator precedence", "3 + 5 * 2", 13.0),
        ("Parentheses", "(3 + 5) * 2", 16.0),
        ("Complex expression", "100 / (2 + 3) * 2 - 5", 35.0),
        ("Negative numbers", "-5 * (-2 + 8)", -30.0),
        ("Leading negative", "-10 + 20", 10.0),
        ("Division with float result", "10 / 3", 10/3),
        ("Edge case with zero", "0 * 10 - 0", 0.0),
    ]

    print("--- Running Standard Test Cases ---")
    for description, expr, expected in expressions_to_test:
        try:
            result = calculator.calculate(expr)
            status = "PASSED" if abs(result - expected) < 1e-9 else f"FAILED (Got {result})"
            print(f"- {description:<25} | Expression: {expr:<25} | Expected: {expected:<10} | Result: {result:<10.4f} | Status: {status}")
        except (ValueError, ZeroDivisionError, RuntimeError) as e:
            print(f"- {description:<25} | Expression: {expr:<25} | FAILED with error: {e}")

    # --- Error Handling Test Cases ---
    error_expressions = [
        ("Division by zero", "10 / 0"),
        ("Mismatched parentheses (extra left)", "((5 + 2) * 3"),
        ("Mismatched parentheses (extra right)", "(5 + 2) * 3)"),
        ("Invalid character", "5 # 4"),
        ("Invalid operator placement", "5 * + 3"),
    ]
    
    print("\n--- Running Error Handling Test Cases ---")
    for description, expr in error_expressions:
        try:
            calculator.calculate(expr)
            print(f"- {description:<30} | Expression: {expr:<20} | Status: FAILED (No exception was raised)")
        except Exception as e:
            print(f"- {description:<30} | Expression: {expr:<20} | Status: PASSED (Caught expected error: {e})")
            
    # --- Interactive Mode ---
    print("\n--- Interactive Calculator Mode ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    while True:
        user_input = input(">>> ")
        if user_input.lower() == 'exit':
            break
        try:
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError, RuntimeError) as e:
            print(f"Error: {e}")

