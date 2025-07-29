
import re
from typing import List, Union

class Calculator:
    """
    A safe, maintainable, and efficient arithmetic expression evaluator.

    This class implements a calculator that can parse and evaluate strings
    containing mathematical expressions. It adheres to standard operator
    precedence and supports parentheses.

    The implementation follows the ISO/IEC 25010 standard for software quality,
    focusing on reliability, security, maintainability, and performance.

    It uses the Shunting-yard algorithm to convert infix expressions to
    Reverse Polish Notation (RPN), which is then evaluated. This avoids the
    use of the insecure `eval()` function.
    """

    # Operator precedence and associativity definitions.
    # Higher number means higher precedence.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'L'},
        '-': {'precedence': 1, 'assoc': 'L'},
        '*': {'precedence': 2, 'assoc': 'L'},
        '/': {'precedence': 2, 'assoc': 'L'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: A string containing the mathematical expression.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., invalid characters,
                        unbalanced parentheses, malformed expression).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raising exceptions to be handled by the caller,
            # preserving the original error type and message.
            raise e
        except Exception:
            # Catch any other unexpected errors during processing.
            raise ValueError("Invalid or malformed expression")

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an expression string into a list of tokens.

        This method handles numbers (integers, floats), operators, parentheses,
        and whitespace. It also correctly identifies unary minus operators.

        Returns:
            A list of tokens (as strings).

        Raises:
            ValueError: If an unrecognized character is found.
        """
        # Regex to find numbers, operators, or parentheses
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        tokens = token_regex.findall(expression)
        
        # Check for any characters not matched by the regex (excluding whitespace)
        if "".join(tokens) != re.sub(r"\s+", "", expression):
            raise ValueError("Expression contains invalid characters")

        # Handle unary minus: a '-' is unary if it's the first token or
        # if it follows an operator or an opening parenthesis.
        output_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('):
                # This is a unary minus. Combine it with the next number.
                # We prepend a '0' to the RPN logic to handle it as '0 - number'.
                output_tokens.append('0')
            output_tokens.append(token)
            
        return output_tokens

    def _to_rpn(self, tokens: List[str]) -> List[str]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If parentheses are mismatched.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
                # Token is a number
                output_queue.append(token)
            elif token in self._OPERATORS:
                # Token is an operator
                op1 = token
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       (self._OPERATORS[operator_stack[-1]]['precedence'] > self._OPERATORS[op1]['precedence'] or
                        (self._OPERATORS[operator_stack[-1]]['precedence'] == self._OPERATORS[op1]['precedence'] and self._OPERATORS[op1]['assoc'] == 'L'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op1)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression")
                operator_stack.pop() # Discard the '('

        # Pop any remaining operators from the stack to the queue
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: List[str]) -> float:
        """
        Evaluates a list of tokens in Reverse Polish Notation (RPN).

        Returns:
            The final result of the calculation.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack: List[float] = []

        for token in rpn_tokens:
            if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
                operand_stack.append(float(token))
            elif token in self._OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator")
                
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                
                if token == '+':
                    operand_stack.append(op1 + op2)
                elif token == '-':
                    operand_stack.append(op1 - op2)
                elif token == '*':
                    operand_stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    operand_stack.append(op1 / op2)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: operands remaining after evaluation")

        return operand_stack[0]


if __name__ == "__main__":
    """
    Main execution block to demonstrate the Calculator class.
    This provides a simple command-line interface for testing.
    """
    calculator = Calculator()
    print("Welcome to the Console Calculator!")
    print("Enter 'quit' to exit.")
    
    while True:
        expression = input(">> ")
        if expression.lower() == 'quit':
            break
        
        if not expression.strip():
            continue
            
        try:
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")

    print("Calculator exited.")

