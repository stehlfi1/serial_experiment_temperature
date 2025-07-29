
import operator
from typing import List, Union, Dict, Callable

# Type alias for clarity
Token = Union[float, str]
OperatorDefinition = Dict[str, Union[int, Callable]]


class Calculator:
    """
    A console-based arithmetic calculator that safely evaluates mathematical
    expressions from a string.

    This class adheres to the principles of the ISO/IEC 25010 standard for
    software quality, emphasizing:
    - **Functional Suitability:** Correctly performs arithmetic operations with
      proper precedence and parenthesis support.
    - **Reliability:** Robustly handles invalid inputs, malformed expressions,
      and runtime errors like division by zero.
    - **Performance Efficiency:** Implements the efficient Shunting-yard algorithm
      for expression parsing and evaluation.
    - **Security:** Avoids the use of `eval()` to prevent code injection
      vulnerabilities.
    - **Maintainability:** Features a modular, object-oriented design with clear
      separation of concerns (tokenizing, parsing, evaluating), comprehensive
      documentation, and readable code.
    - **Testability:** The modular structure allows for individual components to be
      tested in isolation.
    """

    # --- Class Attributes for Configuration (Maintainability) ---
    OPERATORS: Dict[str, OperatorDefinition] = {
        "+": {"precedence": 1, "func": operator.add},
        "-": {"precedence": 1, "func": operator.sub},
        "*": {"precedence": 2, "func": operator.mul},
        "/": {"precedence": 2, "func": operator.truediv},
    }
    LEFT_PAREN: str = "("
    RIGHT_PAREN: str = ")"

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the Calculator. It orchestrates
        the tokenization, parsing (Shunting-yard), and RPN evaluation steps.

        Args:
            expression: The mathematical expression string to evaluate.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., invalid
                        characters, mismatched parentheses).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._shunting_yard(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raising with a more informative context if needed,
            # or simply propagating the clear, specific error.
            raise e
        except Exception as e:
            # Catch-all for unexpected errors, promoting reliability.
            raise ValueError(f"An unexpected error occurred: {e}") from e

    def _tokenize(self, expression: str) -> List[Token]:
        """
        Converts the input expression string into a list of tokens.

        This method handles numbers (integers, floats, negatives) and operators.
        It also performs initial validation for invalid characters.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (floats and strings for operators/parentheses).

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        tokens: List[Token] = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            # Handle numbers (integers and floats)
            if char.isdigit() or char == ".":
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                continue

            # Handle operators and parentheses
            if char in self.OPERATORS or char in [self.LEFT_PAREN, self.RIGHT_PAREN]:
                # Logic to correctly handle unary minus (negation) vs. binary minus (subtraction)
                if char == "-":
                    is_unary = (
                        not tokens or
                        isinstance(tokens[-1], str) and tokens[-1] in self.OPERATORS or
                        tokens[-1] == self.LEFT_PAREN
                    )
                    if is_unary:
                        # This is a negative number, not a subtraction operator.
                        # We find the number and prepend a minus sign.
                        i += 1
                        # Skip any whitespace after the unary minus
                        while i < len(expression) and expression[i].isspace():
                            i += 1
                        
                        if i == len(expression) or not (expression[i].isdigit() or expression[i] == "."):
                            raise ValueError("Invalid expression: unary minus must be followed by a number.")

                        num_str = "-"
                        while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                            num_str += expression[i]
                            i += 1
                        try:
                            tokens.append(float(num_str))
                        except ValueError:
                            raise ValueError(f"Invalid number format: '{num_str}'")
                        continue
                
                # If it's a binary operator or parenthesis
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Invalid character in expression: '{char}'")

        return tokens

    def _shunting_yard(self, tokens: List[Token]) -> List[Token]:
        """
        Converts a token list from infix to postfix notation (RPN).

        This method implements Dijkstra's Shunting-yard algorithm to handle
        operator precedence and associativity correctly.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in Reverse Polish Notation.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[Token] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and
                       operator_stack[-1] != self.LEFT_PAREN and
                       self.OPERATORS[operator_stack[-1]]["precedence"] >= self.OPERATORS[token]["precedence"]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == self.LEFT_PAREN:
                operator_stack.append(token)
            elif token == self.RIGHT_PAREN:
                while operator_stack and operator_stack[-1] != self.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != self.LEFT_PAREN:
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Discard the left parenthesis

        while operator_stack:
            op = operator_stack.pop()
            if op == self.LEFT_PAREN:
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Token]) -> float:
        """
        Evaluates a token queue in Reverse Polish Notation.

        Args:
            rpn_queue: A list of tokens in RPN format.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., insufficient
                        operands for an operator).
            ZeroDivisionError: If division by zero is attempted.
        """
        eval_stack: List[float] = []

        for token in rpn_queue:
            if isinstance(token, float):
                eval_stack.append(token)
            elif token in self.OPERATORS:
                if len(eval_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for an operator.")
                
                operand2 = eval_stack.pop()
                operand1 = eval_stack.pop()
                
                operation = self.OPERATORS[token]["func"]
                
                if token == "/" and operand2 == 0:
                    raise ZeroDivisionError("Error: Division by zero.")
                
                result = operation(operand1, operand2)
                eval_stack.append(result)

        if len(eval_stack) != 1:
            raise ValueError("Invalid expression: too many operands.")

        return eval_stack[0]


# --- Demonstration and Interactive Usage ---
if __name__ == "__main__":
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'quit' to exit.")

    calculator = Calculator()

    # --- Test Cases (Correctness) ---
    test_expressions = {
        "5 + 3": 8.0,
        "10 - 4": 6.0,
        "7 * 2": 14.0,
        "20 / 4": 5.0,
        "2 + 3 * 4": 14.0,
        "(2 + 3) * 4": 20.0,
        "10 / (2 + 3)": 2.0,
        "5.5 + 2.5 * 2": 10.5,
        "-3 * 4 + 2": -10.0,
        "3 * -4": -12.0,
        "5 - -3": 8.0,
        "(5 - (3 + 2)) * 3": 0.0,
        "100 / 10 * 2": 20.0
    }

    print("\n--- Running Automated Tests ---")
    all_passed = True
    for expr, expected in test_expressions.items():
        try:
            result = calculator.calculate(expr)
            if abs(result - expected) < 1e-9: # Floating point comparison
                print(f"[PASS] '{expr}' => {result}")
            else:
                print(f"[FAIL] '{expr}' => {result}, expected {expected}")
                all_passed = False
        except (ValueError, ZeroDivisionError) as e:
            print(f"[FAIL] '{expr}' => EXCEPTION: {e}")
            all_passed = False
    
    print("--- Test Summary ---")
    if all_passed:
        print("All automated tests passed successfully.")
    else:
        print("Some automated tests failed.")

    # --- Interactive Loop ---
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() == 'quit':
                break
            
            if not user_input.strip():
                continue

            result = calculator.calculate(user_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected system error occurred: {e}")

    print("Calculator exited.")
