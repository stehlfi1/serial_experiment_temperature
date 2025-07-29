
import re
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This calculator adheres to standard operator precedence, supports parentheses,
    and handles integers, floating-point numbers, and negative values.

    The implementation uses the Shunting-yard algorithm to convert the infix
    expression to Reverse Polish Notation (RPN), which is then evaluated.
    This approach avoids the use of `eval()` and provides robust error handling.
    """

    # Operator precedence for the Shunting-yard algorithm.
    _PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, malformed).
            ZeroDivisionError: If the expression contains a division by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to provide a clean public API.
            raise e
        except Exception:
            # Catch any other unexpected errors during processing.
            raise ValueError("Malformed expression provided.")

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts an expression string into a list of tokens (numbers and operators).

        This method correctly handles floating-point numbers and distinguishes
        between binary subtraction and unary negation.

        Args:
            expression: The string expression.

        Returns:
            A list of tokens.

        Raises:
            ValueError: If an invalid character is found.
        """
        tokens = []
        # Regex to find numbers (int/float), operators, or parentheses.
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        
        last_token_was_operator_or_lparen = True

        for match in token_regex.finditer(expression):
            token = match.group(1)
            
            if token.isdigit() or '.' in token:
                tokens.append(float(token))
                last_token_was_operator_or_lparen = False
            elif token in self._PRECEDENCE:
                # Handle unary minus: if the '-' follows an operator or an opening
                # parenthesis, or is the first token, it's a negation.
                if token == '-' and last_token_was_operator_or_lparen:
                    # This is a special token to represent unary minus.
                    tokens.append('~') 
                else:
                    tokens.append(token)
                last_token_was_operator_or_lparen = True
            elif token in "()":
                tokens.append(token)
                last_token_was_operator_or_lparen = (token == '(')
        
        # A simple validation to check if all parts of the string were tokenized.
        # This catches invalid characters between valid tokens.
        if "".join(map(str, tokens)).replace('.', '').replace('~', '-') != expression.replace(" ", ""):
             raise ValueError(f"Invalid character in expression: '{expression}'")

        return tokens

    def _to_rpn(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If there are mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        # Add a unary minus operator with higher precedence
        precedence = self._PRECEDENCE.copy()
        precedence['~'] = 3 # Unary minus has high precedence

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0)):
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

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates a token queue in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                operand_stack.append(token)
            else: # Token is an operator
                try:
                    if token == '~': # Unary minus
                        operand = operand_stack.pop()
                        operand_stack.append(-operand)
                        continue

                    # Binary operators
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()

                    if token == '+':
                        operand_stack.append(operand1 + operand2)
                    elif token == '-':
                        operand_stack.append(operand1 - operand2)
                    elif token == '*':
                        operand_stack.append(operand1 * operand2)
                    elif token == '/':
                        if operand2 == 0:
                            raise ZeroDivisionError("Division by zero is not allowed.")
                        operand_stack.append(operand1 / operand2)
                except IndexError:
                    raise ValueError("Malformed expression: Invalid operator usage.")

        if len(operand_stack) != 1:
            raise ValueError("Malformed expression: Not enough operators.")

        return operand_stack[0]

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()
    print("--- Python Console Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")

    while True:
        try:
            expression_input = input(">>> ")
            if expression_input.lower() == 'exit':
                break
            
            if not expression_input.strip():
                continue

            result = calculator.calculate(expression_input)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

