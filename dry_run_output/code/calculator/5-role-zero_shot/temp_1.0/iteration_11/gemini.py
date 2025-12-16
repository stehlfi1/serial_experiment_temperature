
import operator
from typing import List, Dict, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions from a string.

    This calculator supports addition, subtraction, multiplication, and division,
    as well as parentheses for grouping. It correctly handles operator precedence
    and supports both integer and floating-point numbers, including negative values.

    The implementation uses the Shunting-yard algorithm to convert the infix
    expression to Reverse Polish Notation (RPN), which is then evaluated. This
    approach avoids the use of Python's `eval()` function, ensuring safety
    and providing a solid algorithmic foundation.

    Adheres to ISO/IEC 25010 principles:
    - Functional Suitability: Correctly evaluates complex expressions.
    - Performance Efficiency: Uses an O(n) algorithm for evaluation.
    - Maintainability: Code is modular, readable, and well-documented.
    - Reliability: Robustly handles invalid inputs and operational errors.
    - Security: Avoids `eval()`, preventing code injection vulnerabilities.
    """

    # Operator properties: precedence and the corresponding function
    _OPERATORS: Dict[str, tuple[int, callable]] = {
        '+': (1, operator.add),
        '-': (1, operator.sub),
        '*': (2, operator.mul),
        '/': (2, operator.truediv),
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., invalid characters,
                        unbalanced parentheses).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._infix_to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return float(result)
        except (KeyError, IndexError):
            # Catches errors from popping from empty stacks or invalid operators,
            # which indicates a malformed expression.
            raise ValueError("Invalid or malformed expression.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input expression string into a list of tokens.

        This private method handles numbers (integers, floats, negatives)
        and operators. It also performs initial validation for invalid characters.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: For characters that are not part of a valid number or
                        a recognized operator/parenthesis.
        """
        tokens: List[str] = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            # Handle numbers (including floats and leading negatives)
            if char.isdigit() or (char == '.'):
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                
                if num_str.count('.') > 1:
                    raise ValueError(f"Invalid number format: {num_str}")
                tokens.append(num_str)
                continue

            # Handle unary minus (negative numbers)
            # A minus is unary if it's the first token or follows an operator or an open parenthesis.
            if char == '-' and (not tokens or tokens[-1] in self._OPERATORS or tokens[-1] == '('):
                # Start of a negative number
                i += 1
                num_str = "-"
                # Find the end of the number
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1

                if len(num_str) == 1: # Just a '-' followed by non-digit
                    raise ValueError("Invalid use of unary minus.")
                if num_str.count('.') > 1:
                    raise ValueError(f"Invalid number format: {num_str}")
                tokens.append(num_str)
                continue

            # Handle operators and parentheses
            if char in self._OPERATORS or char in '()':
                tokens.append(char)
                i += 1
                continue
            
            raise ValueError(f"Invalid character in expression: '{char}'")
        
        return tokens

    def _infix_to_rpn(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Converts a list of infix tokens to a postfix (RPN) list.

        This implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue: List[Union[str, float]] = []
        operator_stack: List[str] = []

        for token in tokens:
            # If the token is a number, add it to the output queue.
            try:
                output_queue.append(float(token))
                continue
            except ValueError:
                # Token is an operator or parenthesis
                pass

            # If the token is an operator
            if token in self._OPERATORS:
                op1_prec = self._OPERATORS[token][0]
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       self._OPERATORS[operator_stack[-1]][0] >= op1_prec):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            
            # If the token is a left parenthesis
            elif token == '(':
                operator_stack.append(token)

            # If the token is a right parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                # If stack runs out without finding '(', parentheses are mismatched.
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop() # Pop the left parenthesis '('

        # Pop any remaining operators from the stack to the output
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)
            
        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Union[str, float]]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression is malformed, leading to an
                        invalid stack state.
        """
        operand_stack: List[float] = []

        for token in rpn_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            else: # Token is an operator string
                if len(operand_stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands for operator.")
                
                # Pop operands in reverse order
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()

                _, operation = self._OPERATORS[token]

                if token == '/' and op2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                result = operation(op1, op2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression: too many operands.")
            
        return operand_stack[0]


# --- Main execution block for demonstrating the Calculator ---
if __name__ == "__main__":
    print("Console Arithmetic Calculator")
    print("Enter an expression to calculate or 'exit' to quit.")
    print("-" * 30)

    calculator = Calculator()

    # --- Self-testing with various cases ---
    test_cases = {
        "1 + 1": 2.0,
        "2 - 3": -1.0,
        "4 * 5": 20.0,
        "10 / 2": 5.0,
        "3 + 4 * 2": 11.0,
        "(3 + 4) * 2": 14.0,
        "10 / (2.5 * 2)": 2.0,
        "-5 + 10": 5.0,
        "10 * -2": -20.0,
        "1 - -1": 2.0,
        "(4 + 6) / (-2 + 4)": 5.0,
        "3.14 * 2": 6.28
    }

    print("Running self-tests...")
    all_tests_passed = True
    for expr, expected in test_cases.items():
        try:
            result = calculator.calculate(expr)
            if abs(result - expected) < 1e-9: # Compare floats with tolerance
                print(f"  PASS: '{expr}' -> {result}")
            else:
                print(f"  FAIL: '{expr}' -> {result} (Expected: {expected})")
                all_tests_passed = False
        except (ValueError, ZeroDivisionError) as e:
            print(f"  ERROR on test '{expr}': {e}")
            all_tests_passed = False

    if all_tests_passed:
        print("All self-tests passed successfully!\n")
    else:
        print("Some self-tests failed.\n")
    
    # --- Interactive Loop ---
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() == 'exit':
                break
            if not user_input.strip():
                continue
            
            result = calculator.calculate(user_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

