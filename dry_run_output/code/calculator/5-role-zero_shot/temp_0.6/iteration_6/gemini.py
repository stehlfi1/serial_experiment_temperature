
import operator
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that safely evaluates mathematical
    expressions.

    This class adheres to the principles of the ISO/IEC 25010 standard,
    prioritizing correctness, reliability, efficiency, and maintainability.

    It implements a standard two-pass approach:
    1.  Tokenization and parsing (Shunting-yard algorithm) to convert the infix
        expression to a postfix (RPN) queue.
    2.  Evaluation of the RPN queue to compute the final result.

    This approach avoids the use of `eval()` for security and control.

    Attributes:
        _operators (dict): A mapping of operator symbols to their precedence,
                           associativity, and corresponding function.
    """

    def __init__(self):
        """Initializes the Calculator with operator definitions."""
        self._operators = {
            '+': (1, operator.add),
            '-': (1, operator.sub),
            '*': (2, operator.mul),
            '/': (2, operator.truediv),
        }

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts an expression string into a list of tokens (numbers and operators).

        This method handles integers, floats, and unary minuses (e.g., '-5' or '3 * -2').
        It also performs initial validation for invalid characters.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens, where numbers are converted to floats.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or (char == '.'):
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                continue

            if char in self._operators or char in '()':
                # Handle unary minus: a '-' is unary if it's the first token
                # or if it follows another operator or an opening parenthesis.
                if char == '-' and (not tokens or tokens[-1] in self._operators or tokens[-1] == '('):
                    num_str = "-"
                    i += 1
                    # Skip any whitespace after the unary minus
                    while i < len(expression) and expression[i].isspace():
                        i += 1
                    # Check if expression ends unexpectedly
                    if i == len(expression):
                        raise ValueError("Invalid expression: unexpected end after unary minus")
                    
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    
                    if len(num_str) == 1: # Just a '-' was found, not followed by a number
                        raise ValueError("Invalid expression: isolated unary minus")
                        
                    try:
                        tokens.append(float(num_str))
                    except ValueError:
                        raise ValueError(f"Invalid negative number format: '{num_str}'")
                    continue
                else:
                    tokens.append(char)
                    i += 1
                    continue

            raise ValueError(f"Invalid character in expression: '{char}'")
        
        return tokens

    def _shunting_yard(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to postfix (RPN) notation using the
        Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the `_tokenize` method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._operators:
                op1_precedence = self._operators[token][0]
                while (operator_stack and operator_stack[-1] in self._operators and
                       self._operators[operator_stack[-1]][0] >= op1_precedence):
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
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates a token list in RPN order.

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero is attempted.
        """
        stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            else:  # Token is an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                op_func = self._operators[token][1]

                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")

                result = op_func(operand1, operand2)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
            
        return stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public method that orchestrates the tokenization,
        parsing, and evaluation of the expression.

        Args:
            expression: The mathematical expression string.
                        Example: "3 + 4 * (2 - 1)"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: For invalid expressions, characters, or parentheses.
            ZeroDivisionError: For division by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression cannot be empty")
            
        tokens = self._tokenize(expression)
        rpn_tokens = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn_tokens)
        
        return result

# --- Demonstration ---
if __name__ == "__main__":
    calc = Calculator()
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() == 'exit':
                break
            
            result = calc.calculate(user_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

