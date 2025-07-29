
import operator
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class implements a parser and evaluator for arithmetic expressions,
    adhering to standard operator precedence and supporting parentheses. It is
    designed for robustness, maintainability, and security, avoiding the use of
    `eval()`.

    The evaluation process follows two main steps:
    1.  The infix expression is tokenized and converted to Reverse Polish
        Notation (RPN) using the Shunting-yard algorithm.
    2.  The RPN expression is evaluated using a stack-based approach.
    """

    # Supported operators with their corresponding function and precedence
    # Lower number means lower precedence.
    _OPERATORS = {
        '+': {'func': operator.add, 'prec': 1},
        '-': {'func': operator.sub, 'prec': 1},
        '*': {'func': operator.mul, 'prec': 2},
        '/': {'func': operator.truediv, 'prec': 2},
    }

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an expression string into a list of tokens.

        This method handles numbers (integers, floats, negatives) and operators.
        It intelligently distinguishes between a subtraction operator and a
        unary negative sign.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of string tokens (numbers, operators, parentheses).

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

            # Handle numbers (integers and floats)
            if char.isdigit() or char == '.':
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
                continue

            # Handle operators and parentheses
            if char in self._OPERATORS or char in '()':
                # Logic to handle unary minus
                if char == '-':
                    is_unary = (
                        not tokens or
                        tokens[-1] in self._OPERATORS or
                        tokens[-1] == '('
                    )
                    if is_unary:
                        # It's a unary minus, bundle it with the next number
                        i += 1
                        num_str = "-"
                        while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                            num_str += expression[i]
                            i += 1
                        if num_str == '-':
                            raise ValueError("Invalid expression: hanging minus sign")
                        tokens.append(num_str)
                        continue
                
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Invalid character in expression: '{char}'")
        
        return tokens

    def _to_rpn(self, tokens: List[str]) -> List[Union[float, str]]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN).

        This method uses the Shunting-yard algorithm.

        Args:
            tokens: A list of string tokens from the _tokenize method.

        Returns:
            A list representing the RPN expression, with numbers as floats.

        Raises:
            ValueError: If there are mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            try:
                # If the token is a number, add it to the output queue.
                output_queue.append(float(token))
            except ValueError:
                # The token is an operator or parenthesis
                if token in self._OPERATORS:
                    op1 = token
                    while (operator_stack and
                           operator_stack[-1] != '(' and
                           self._OPERATORS[operator_stack[-1]]['prec'] >= self._OPERATORS[op1]['prec']):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(op1)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    
                    if not operator_stack or operator_stack[-1] != '(':
                        raise ValueError("Mismatched parentheses in expression")
                    operator_stack.pop()  # Pop the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)
            
        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Union[float, str]]) -> float:
        """
        Evaluates an RPN expression.

        Args:
            rpn_queue: A list representing the RPN expression.

        Returns:
            The final result of the calculation as a float.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero is attempted.
        """
        operand_stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                operand_stack.append(token)
            else:  # Token is an operator
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator")
                
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                
                operation = self._OPERATORS[token]['func']

                if token == '/' and op2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                
                result = operation(op1, op2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        
        return operand_stack[0]

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the public interface for the Calculator class. It orchestrates
        the tokenization, parsing, and evaluation of the expression.

        Args:
            expression: The arithmetic expression to evaluate.
                        e.g., "3 + 4 * (2 - 1) / 5"

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: For invalid expressions, syntax errors, or
                        mismatched parentheses.
            ZeroDivisionError: For division by zero.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Expression must be a non-empty string.")

        tokens = self._tokenize(expression)
        rpn_queue = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn_queue)

        return result


if __name__ == "__main__":
    """
    An interactive command-line interface to demonstrate the Calculator.
    """
    print("Welcome to the Python Calculator!")
    print("Enter an expression to calculate or 'exit' to quit.")
    
    calculator = Calculator()

    while True:
        try:
            expr = input(">> ")
            if expr.lower() == 'exit':
                print("Goodbye!")
                break
            
            result = calculator.calculate(expr)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

