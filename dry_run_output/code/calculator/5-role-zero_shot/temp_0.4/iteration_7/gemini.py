
import operator
from typing import List, Union, Dict, Any

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class implements a robust calculator using the Shunting-yard algorithm
    to handle standard arithmetic operations with correct operator precedence and
    parentheses. It is designed with a focus on quality attributes from the
    ISO/IEC 25010 standard, including correctness, efficiency, safety,
    and maintainability.

    Attributes:
        OPERATORS (Dict[str, Dict[str, Any]]): A dictionary defining the
            supported operators, their precedence, and associated functions.
    """

    # Using a class attribute for operators makes it easy to extend.
    # For example, to add exponentiation: '**': {'prec': 3, 'func': operator.pow}
    OPERATORS: Dict[str, Dict[str, Any]] = {
        '+': {'prec': 1, 'func': operator.add},
        '-': {'prec': 1, 'func': operator.sub},
        '*': {'prec': 2, 'func': operator.mul},
        '/': {'prec': 2, 'func': operator.truediv},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface of the calculator. It orchestrates
        the tokenization, parsing (to RPN), and evaluation of the expression.

        Args:
            expression: The mathematical expression string to evaluate.
                        e.g., "3 + 4 * (2 - 1)"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        tokens = self._tokenize(expression)
        rpn_tokens = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn_tokens)
        return result

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts the expression string into a list of tokens.

        This method handles numbers (integers, floats, negatives) and operators.
        It correctly distinguishes between a binary subtraction and a unary negative.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens, where numbers are floats and operators/parentheses
            are strings.

        Raises:
            ValueError: If an unrecognized character is found.
        """
        tokens: List[Union[float, str]] = []
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

            if char in self.OPERATORS or char in '()':
                # Handle unary minus: check if it's the start of the expression
                # or if it follows an operator or an opening parenthesis.
                if char == '-' and (not tokens or isinstance(tokens[-1], str) and tokens[-1] in self.OPERATORS or tokens[-1] == '('):
                    # This is a unary minus, not a subtraction.
                    # Look ahead for the number.
                    i += 1
                    if i >= len(expression):
                        raise ValueError("Invalid expression: '-' at the end")
                    
                    num_str = "-"
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    
                    if len(num_str) == 1: # Just a '-' without a number
                        raise ValueError("Invalid expression: standalone '-'")
                    
                    try:
                        tokens.append(float(num_str))
                    except ValueError:
                        raise ValueError(f"Invalid negative number format: '{num_str}'")
                    continue

                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Invalid character in expression: '{char}'")

        return tokens

    def _to_rpn(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to Reverse Polish Notation (RPN).

        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[Union[float, str]] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and operator_stack[-1] != '(' and
                       self.OPERATORS[operator_stack[-1]]['prec'] >= self.OPERATORS[token]['prec']):
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
        Evaluates a token list in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        stack: List[float] = []

        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                operation = self.OPERATORS[token]
                
                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                
                result = operation['func'](operand1, operand2)
                stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")

        return stack[0]

# --- Main execution block for interactive console usage ---
if __name__ == "__main__":
    print("High-Quality Python Arithmetic Calculator")
    print("Enter 'quit' to exit.")
    
    calculator = Calculator()

    while True:
        try:
            expression_input = input("calc> ")
            if expression_input.lower() == 'quit':
                break
            if not expression_input:
                continue

            result = calculator.calculate(expression_input)
            # Format to int if the result is a whole number
            if result == int(result):
                print(f"= {int(result)}")
            else:
                print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

