
import re
from typing import List, Union

class Calculator:
    """
    A high-quality, maintainable calculator that evaluates arithmetic expressions.

    This class adheres to the principles of the ISO/IEC 25010 standard for
    software quality, focusing on functional suitability, reliability, performance
    efficiency, security, and maintainability.

    It safely evaluates string expressions containing integers, floating-point
    numbers, parentheses, and the four basic arithmetic operations (+, -, *, /),
    respecting standard operator precedence.

    Usage:
        calc = Calculator()
        result = calc.calculate("(3.5 + 1.5) * 2 - 5 / 2")
        print(result)  # Output: 7.5
    """

    def __init__(self):
        """Initializes the Calculator, setting up operator precedence."""
        self._operators = {
            '+': {'precedence': 1, 'association': 'Left'},
            '-': {'precedence': 1, 'association': 'Left'},
            '*': {'precedence': 2, 'association': 'Left'},
            '/': {'precedence': 2, 'association': 'Left'},
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string.

        This is the public interface for the calculator. It orchestrates the
        tokenization, parsing (Shunting-yard), and evaluation of the expression.

        Args:
            expression: The arithmetic expression string to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., invalid characters,
                        unbalanced parentheses, or misplaced operators).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions with a more user-friendly context if desired,
            # or let them propagate as is for clear error reporting.
            raise e
        except Exception:
            # Catch any other unexpected errors during processing.
            raise ValueError("Invalid or malformed expression provided.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an expression string into a list of tokens.

        This method handles negative numbers, floating-point numbers, operators,
        and parentheses. It also performs initial validation for invalid characters.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).
        
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        if not expression:
            raise ValueError("Expression cannot be empty.")
            
        # Regex to find numbers (including floats) or operators/parentheses.
        token_pattern = re.compile(r"(\d+\.?\d*|[\+\-\*\/\(\)])")
        tokens = token_pattern.findall(expression.replace(" ", ""))

        # Check for invalid characters not captured by the regex
        if "".join(tokens) != expression.replace(" ", ""):
            raise ValueError(f"Expression contains invalid characters.")

        # Handle unary minus: a '-' is unary if it's the first token,
        # or if it follows an operator or an opening parenthesis.
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._operators or tokens[i-1] == '('):
                # This is a unary minus. Combine it with the next token (number).
                if i + 1 < len(tokens) and tokens[i+1].replace('.', '', 1).isdigit():
                    # The token to be appended is handled in the next iteration.
                    continue
                else:
                    raise ValueError("Misplaced unary minus.")
            elif token.replace('.', '', 1).isdigit() and i > 0 and tokens[i-1] == '-':
                 if (i-1 == 0 or tokens[i-2] in self._operators or tokens[i-2] == '('):
                    processed_tokens.append('-' + token)
                 else:
                    processed_tokens.append(token)
            else:
                processed_tokens.append(token)
        
        return processed_tokens


    def _to_rpn(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts a list of infix tokens to a Reverse Polish Notation (RPN) queue.

        This method implements the Shunting-yard algorithm to correctly handle
        operator precedence and associativity.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list representing the RPN queue. Numbers are converted to floats.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('-', '', 1).replace('.', '', 1).isdigit():
                output_queue.append(float(token))
            elif token in self._operators:
                op1 = token
                while (operator_stack and operator_stack[-1] in self._operators and
                       (self._operators[operator_stack[-1]]['precedence'] > self._operators[op1]['precedence'] or
                        (self._operators[operator_stack[-1]]['precedence'] == self._operators[op1]['precedence'] and
                         self._operators[op1]['association'] == 'Left'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op1)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Discard the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates an RPN queue to produce the final result.

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero is attempted.
        """
        stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: Insufficient operands for operator.")
                
                operand2 = stack.pop()
                operand1 = stack.pop()

                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
            raise ValueError("Malformed expression provided.")

        return stack[0]

def main():
    """
    Main function to run the calculator in a simple console REPL.
    """
    print("Console Arithmetic Calculator")
    print("Enter an expression to evaluate or 'exit' to quit.")
    
    calculator = Calculator()

    while True:
        try:
            expression = input(">> ")
            if expression.lower() == 'exit':
                print("Exiting calculator.")
                break
            
            result = calculator.calculate(expression)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting calculator.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()
