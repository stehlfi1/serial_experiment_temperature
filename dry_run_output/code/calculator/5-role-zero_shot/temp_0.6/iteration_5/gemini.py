
import re

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class provides a safe and efficient way to compute mathematical
    expressions containing integers, floating-point numbers, addition,
    subtraction, multiplication, division, and parentheses. It adheres to
    standard operator precedence.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Correctly implements the required arithmetic
      operations, including operator precedence and parentheses.
    - Performance Efficiency: Uses a time-efficient O(n) algorithm (where n
      is the length of the expression) for parsing and evaluation.
    - Reliability: Robustly handles invalid inputs, syntax errors, and
      runtime errors like division by zero, raising specific exceptions.
    - Security: Avoids the use of `eval()` to prevent code injection
      vulnerabilities.
    - Maintainability: The code is modular, with responsibilities like
      tokenization, precedence logic, and evaluation separated into distinct
      methods. It is also highly readable and documented.
    - Portability: Uses only standard Python libraries, ensuring it can run
      on any system with a Python interpreter.
    """

    def __init__(self):
        """Initializes the Calculator, defining operator precedence."""
        self._precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        self._operators = set(self._precedence.keys())

    def _apply_operator(self, operators: list, values: list):
        """
        Applies an operator to the top two values on the value stack.

        Pops one operator and two operands, performs the calculation,
        and pushes the result back onto the value stack.

        Args:
            operators: A list (stack) of operators.
            values: A list (stack) of numeric values.

        Raises:
            ZeroDivisionError: If the operation is a division by zero.
            ValueError: If there are not enough values on the stack for an operation.
        """
        if len(values) < 2:
            raise ValueError("Invalid syntax: Not enough operands for an operator.")
        
        operator = operators.pop()
        right = values.pop()
        left = values.pop()

        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            values.append(left / right)

    def _tokenize(self, expression: str) -> list:
        """
        Converts an infix expression string into a list of tokens.

        This method handles integers, floats, and all valid operators.
        It also intelligently distinguishes between a unary minus (e.g., -5)
        and a binary subtraction operator.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens (numbers as floats, operators/parentheses as strings).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Add spaces around operators and parentheses to simplify splitting
        # Use regex to handle this robustly, especially around numbers
        expression = re.sub(r'([\+\-\*/\(\)])', r' \1 ', expression)
        tokens = expression.split()

        # Handle unary minus (e.g., "- 5" or "( - 5")
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._operators or tokens[i-1] == '('):
                # This is a unary minus. Combine it with the next number.
                if i + 1 < len(tokens):
                    try:
                        # Append the negative number directly
                        processed_tokens.append(f"-{tokens[i+1]}")
                        tokens[i+1] = '' # Mark next token as consumed
                    except (ValueError, IndexError):
                         raise ValueError(f"Invalid syntax: Dangling unary minus.")
                else:
                    raise ValueError(f"Invalid syntax: Dangling unary minus.")
            elif token: # Avoid appending empty strings from consumed tokens
                processed_tokens.append(token)
        
        # Final validation and type conversion
        final_tokens = []
        for token in processed_tokens:
            if token in self._operators or token in '()':
                final_tokens.append(token)
            else:
                try:
                    # Convert all numbers to float for consistent operations
                    final_tokens.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid character or number format: '{token}'")
        
        return final_tokens

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression string and returns the result.

        This is the main public method that orchestrates the tokenization
        and evaluation process using two stacks for values and operators.

        Args:
            expression: The arithmetic expression string.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: For syntax errors like mismatched parentheses or
                        invalid expression structure.
            ZeroDivisionError: For division by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Expression cannot be empty or non-string.")
            
        tokens = self._tokenize(expression)
        values = []
        operators = []

        for token in tokens:
            if isinstance(token, float):
                values.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                # Evaluate everything until we find the matching '('
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                if not operators or operators.pop() != '(':
                    raise ValueError("Mismatched parentheses: Unbalanced ')'")
            elif token in self._operators:
                # Apply operators with higher or equal precedence from the stack
                while (operators and operators[-1] != '(' and
                       self._precedence.get(operators[-1], 0) >= self._precedence.get(token, 0)):
                    self._apply_operator(operators, values)
                operators.append(token)

        # Apply any remaining operators
        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses: Unbalanced '('")
            self._apply_operator(operators, values)

        if len(values) != 1 or operators:
            raise ValueError("Invalid syntax: The expression is incomplete or malformed.")

        return values[0]


def main():
    """
    Main function to run the calculator in an interactive console loop.
    """
    calculator = Calculator()
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'quit' to exit.")
    print("Supported operations: +, -, *, / and parentheses ().")
    print("Example: 3.5 * (2 + -1) / 2")
    
    while True:
        try:
            expression = input(">>> ")
            if expression.lower() == 'quit':
                print("Exiting calculator. Goodbye!")
                break
            
            result = calculator.calculate(expression)
            # Format to int if the result is a whole number
            if result == int(result):
                print(f"= {int(result)}")
            else:
                print(f"= {result:.4f}") # Format floats to 4 decimal places

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting calculator. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
