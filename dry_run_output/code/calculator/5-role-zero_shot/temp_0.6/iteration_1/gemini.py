
import re

class Calculator:
    """
    A high-quality, maintainable calculator that evaluates arithmetic expressions.

    This class implements a calculator that can parse and evaluate string-based
    arithmetic expressions, supporting addition, subtraction, multiplication,
    division, and parentheses. It adheres to standard operator precedence.

    The implementation uses a classic two-stack algorithm for direct evaluation
    of infix expressions, ensuring both correctness and efficiency. It does not
    use `eval()` or similar functions, providing protection against code
    injection vulnerabilities.

    Attributes:
        _OPERATORS (dict): A dictionary mapping operators to their precedence level.
                           This design makes it easy to extend with new operators.
    """

    # Class attribute for defining operators and their precedence.
    # Higher number means higher precedence.
    _OPERATORS = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string.

        This is the public interface for the Calculator. It orchestrates the
        tokenization and evaluation of the expression.

        Args:
            expression: The arithmetic expression string to evaluate.
                        Example: "3 + 5 * (2 - 8)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is otherwise malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            result = self._evaluate(tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions with a clear, user-facing message.
            raise type(e)(f"Error evaluating expression: {e}") from e
        except IndexError:
            # An IndexError during evaluation typically indicates a malformed
            # expression (e.g., "5 *").
            raise ValueError("Malformed expression.") from None

    def _tokenize(self, expression: str) -> list[str | float]:
        """
        Converts the input string into a list of numbers and operators (tokens).

        This method handles integers, floating-point numbers, and negative values.
        It also validates for any characters that are not part of a valid
        expression.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens, where numbers are floats and operators/parentheses
            are strings.

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        # Regex to find numbers (int/float), operators, or parentheses.
        # This is a robust way to split the string while keeping delimiters.
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        
        # Remove all whitespace for easier parsing
        expression = "".join(expression.split())
        
        tokens = token_regex.findall(expression)
        
        # Validate that the entire string was tokenized
        if "".join(tokens) != expression:
            raise ValueError("Expression contains invalid characters.")

        # Process tokens to handle unary minus and convert numbers
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('):
                # This is a unary minus (e.g., "-5" or "3 * -5")
                # We represent it as a multiplication by -1.
                # This simplifies the evaluation logic significantly.
                processed_tokens.extend([float(-1), '*'])
            elif token.replace('.', '', 1).isdigit():
                processed_tokens.append(float(token))
            else:
                processed_tokens.append(token)
                
        return processed_tokens

    def _apply_operator(self, operators: list, values: list) -> None:
        """
        Applies the top operator from the stack to the top two values.

        Pops one operator and two values, performs the calculation, and pushes
        the result back onto the values stack.

        Args:
            operators: The stack of operators (list of strings).
            values: The stack of numerical values (list of floats).

        Raises:
            ZeroDivisionError: If the operation is division by zero.
            ValueError: If the stacks are in an invalid state.
        """
        if not operators or not len(values) >= 2:
            raise ValueError("Malformed expression or mismatched operators/values.")

        operator = operators.pop()
        right_operand = values.pop()
        left_operand = values.pop()

        if operator == '+':
            values.append(left_operand + right_operand)
        elif operator == '-':
            values.append(left_operand - right_operand)
        elif operator == '*':
            values.append(left_operand * right_operand)
        elif operator == '/':
            if right_operand == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            values.append(left_operand / right_operand)

    def _evaluate(self, tokens: list[str | float]) -> float:
        """
        Evaluates a list of tokens using a two-stack algorithm.

        Args:
            tokens: A list of numbers (floats) and operators (strings).

        Returns:
            The final calculated result.

        Raises:
            ValueError: For unbalanced parentheses or malformed expressions.
        """
        values: list[float] = []
        operators: list[str] = []

        for token in tokens:
            if isinstance(token, float):
                values.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                if not operators or operators.pop() != '(':
                    raise ValueError("Mismatched or unbalanced parentheses.")
            elif token in self._OPERATORS:
                while (operators and operators[-1] in self._OPERATORS and
                       self._OPERATORS[operators[-1]] >= self._OPERATORS[token]):
                    self._apply_operator(operators, values)
                operators.append(token)

        # Apply any remaining operators
        while operators:
            # If a '(' is found here, it means there was an unclosed parenthesis
            if operators[-1] == '(':
                raise ValueError("Mismatched or unbalanced parentheses.")
            self._apply_operator(operators, values)

        if len(values) != 1 or operators:
            raise ValueError("Malformed expression.")

        return values[0]


# --- Main Execution Block for Demonstration ---
if __name__ == "__main__":
    """
    Provides a simple command-line interface to demonstrate the Calculator.
    """
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'exit' to quit.")
    
    calculator = Calculator()

    while True:
        try:
            expression_input = input(">> ")
            if expression_input.lower() == 'exit':
                print("Exiting calculator.")
                break
            
            if not expression_input.strip():
                continue

            result = calculator.calculate(expression_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            # Catch any unexpected errors
            print(f"An unexpected error occurred: {e}")

