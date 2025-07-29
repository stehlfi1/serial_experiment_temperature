
import re
from typing import List, Union

class Calculator:
    """
    A safe and efficient arithmetic expression evaluator.

    This class provides functionality to parse and evaluate mathematical expressions
    containing integers, floating-point numbers, addition, subtraction,
    multiplication, division, and parentheses.

    It implements the Shunting-yard algorithm to ensure correct operator
    precedence and associativity without using the unsafe `eval()` function.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Correctly evaluates expressions.
    - Performance Efficiency: Uses an O(n) algorithm.
    - Reliability: Handles invalid inputs and mathematical errors gracefully.
    - Security: Avoids `eval()` to prevent code injection.
    - Maintainability: Modular, documented, and readable code.
    - Testability: Internal logic is separated into testable private methods.
    """

    def __init__(self):
        """Initializes the Calculator, setting up operator precedence."""
        self._precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        self._operators = set(self._precedence.keys())

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an infix expression string into a list of tokens.

        This method handles negative numbers, floating-point numbers, and
        ensures all characters in the expression are valid.

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to find numbers (including floats/negatives) or operators/parentheses
        # It correctly handles cases like '5*-2' or '-5+2'
        token_regex = r"(-?\d+\.?\d*)|([+\-*/()])"
        tokens = re.findall(token_regex, expression)
        
        # re.findall with groups returns tuples, e.g., ('-5', '') or ('', '+')
        # We need to flatten and filter the list.
        processed_tokens = [group[0] or group[1] for group in tokens]

        # Validate that the entire string was consumed by our regex
        if "".join(processed_tokens).replace(" ", "") != expression.replace(" ", ""):
            raise ValueError(f"Expression contains invalid characters: '{expression}'")
            
        return processed_tokens

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of tokens from infix to Reverse Polish Notation (RPN).

        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[str] = []
        operator_stack: List[str] = []

        for token in tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                output_queue.append(token)
            elif token in self._operators:
                while (operator_stack and operator_stack[-1] in self._operators and
                       self._precedence.get(operator_stack[-1], 0) >= self._precedence.get(token, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression")
                operator_stack.pop()  # Discard the '('

        while operator_stack:
            operator = operator_stack.pop()
            if operator == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(operator)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluates a token list in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero is attempted.
        """
        value_stack: List[float] = []

        for token in rpn_tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                value_stack.append(float(token))
            elif token in self._operators:
                if len(value_stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands for operator")
                
                op2 = value_stack.pop()
                op1 = value_stack.pop()

                if token == '+':
                    value_stack.append(op1 + op2)
                elif token == '-':
                    value_stack.append(op1 - op2)
                elif token == '*':
                    value_stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    value_stack.append(op1 / op2)
            else:
                # This case should ideally not be reached with proper tokenization
                raise ValueError(f"Unknown token during evaluation: {token}")

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: too many values left after evaluation")

        return value_stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression string.

        This is the main public method that orchestrates the tokenization,
        conversion to RPN, and final evaluation.

        Args:
            expression: The mathematical expression to evaluate.
                        Example: "3 + 4 * (2 - 1) / 5"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: For invalid characters or malformed expressions.
            ZeroDivisionError: For division by zero.
        """
        # Pre-process to handle unary minus at the beginning of the expression
        # e.g., "-5 + 2" becomes "0 - 5 + 2" for easier tokenization
        # Note: The regex in _tokenize now handles this, but this is a good
        # defensive measure for simpler tokenizers. We'll keep it clean.
        expression = expression.strip()
        if not expression:
            raise ValueError("Cannot calculate an empty expression")
            
        tokens = self._tokenize(expression)
        rpn_tokens = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn_tokens)
        
        return result

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    print("--- High-Quality Python Calculator ---")
    print("Supports +, -, *, /, parentheses, floats, and negative numbers.")
    print("Enter 'exit' or 'quit' to close.")
    
    calculator = Calculator()
    
    while True:
        try:
            user_input = input("\nEnter expression: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting calculator. Goodbye!")
                break
            
            if not user_input:
                continue

            result = calculator.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")

