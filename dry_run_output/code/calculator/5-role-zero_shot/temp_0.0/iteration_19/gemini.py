
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class adheres to the ISO/IEC 25010 standard by providing a reliable,
    efficient, and maintainable implementation. It supports addition, subtraction,
    multiplication, division, and parentheses, with correct operator precedence.

    The evaluation is performed using the Shunting-yard algorithm to convert
    the infix expression to Reverse Polish Notation (RPN), which is then evaluated.
    This approach avoids the use of `eval()` for safety and control.

    Attributes:
        _OPERATORS (dict): A dictionary mapping operators to their precedence and
                           associativity.
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

        This is the public interface for the Calculator. It orchestrates the
        tokenization, conversion to RPN, and final evaluation.

        Args:
            expression: The mathematical expression string to evaluate.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller.
            raise e
        except IndexError:
            # An IndexError during evaluation typically means a malformed expression
            # (e.g., "5 *") which results in an empty stack when an operand is needed.
            raise ValueError("Invalid or malformed expression.")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an expression string into a list of tokens (numbers, operators, parentheses).

        This method also handles unary minus (e.g., '-5' or '3 * -2').

        Args:
            expression: The expression string.

        Returns:
            A list of string tokens.

        Raises:
            ValueError: If an invalid character is found in the expression.
        """
        # Regex to find numbers (int/float), operators, or parentheses
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression)
        
        # Check for any characters that are not part of a valid token or whitespace
        if "".join(tokens) != re.sub(r'\s+', '', expression):
            raise ValueError("Expression contains invalid characters.")

        # Handle unary minus
        output_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('):
                # This is a unary minus. Combine it with the next token.
                try:
                    output_tokens.append(f"-{tokens[i+1]}")
                    # Skip the next token since we've consumed it
                    tokens.pop(i+1)
                except IndexError:
                    raise ValueError("Invalid expression: trailing unary minus.")
            else:
                output_tokens.append(token)
        
        return output_tokens

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of infix tokens from the _tokenize method.

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
            elif token in self._OPERATORS:
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       self._OPERATORS[operator_stack[-1]]['precedence'] >= self._OPERATORS[token]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
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

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the RPN expression is malformed.
        """
        stack: List[float] = []

        for token in rpn_tokens:
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                stack.append(float(token))
            elif token in self._OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator.")
                
                op2 = stack.pop()
                op1 = stack.pop()

                if token == '+':
                    stack.append(op1 + op2)
                elif token == '-':
                    stack.append(op1 - op2)
                elif token == '*':
                    stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    stack.append(op1 / op2)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")

        return stack[0]


def main():
    """
    Main function to run the calculator in an interactive console loop.
    """
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'quit' to exit.")
    
    calculator = Calculator()

    while True:
        try:
            expression = input(">>> ")
            if expression.lower() == 'quit':
                print("Exiting calculator. Goodbye!")
                break
            
            if not expression:
                continue

            result = calculator.calculate(expression)
            # Format to int if the result is a whole number
            if result == int(result):
                print(f"= {int(result)}")
            else:
                print(f"= {result:.4f}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
