
import operator
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator that evaluates string expressions.

    This class adheres to the ISO/IEC 25010 standard by providing a correct,
    efficient, secure, and maintainable implementation. It supports addition,
    subtraction, multiplication, division, and parentheses.

    It uses the Shunting-yard algorithm to convert infix expressions to
    Reverse Polish Notation (RPN), which is then evaluated. This approach
    avoids the use of the unsafe `eval()` function.
    """

    # Operator precedence and associativity definitions
    # Higher number means higher precedence.
    _OPERATORS = {
        '+': {'precedence': 1, 'func': operator.add},
        '-': {'precedence': 1, 'func': operator.sub},
        '*': {'precedence': 2, 'func': operator.mul},
        '/': {'precedence': 2, 'func': operator.truediv},
    }
    _PARENTHESES = '()'

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., invalid characters,
                        unbalanced parentheses, or incorrect operator usage).
            ZeroDivisionError: If the expression contains a division by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to provide a clean external interface
            raise e
        except Exception:
            # Catch any other unexpected errors during parsing/evaluation
            raise ValueError(f"Invalid or malformed expression: '{expression}'")

    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Converts the input string into a list of tokens (numbers and operators).
        This tokenizer correctly handles floating-point numbers and unary minuses.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i+1].isdigit()):
                num_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                continue

            if char in self._OPERATORS:
                # Handle unary minus: if it's the first token, or follows an operator or '('.
                if char == '-' and (not tokens or tokens[-1] in self._OPERATORS or tokens[-1] == '('):
                    # It's a unary minus. We'll read the subsequent number.
                    i += 1
                    # Skip any space between unary minus and number
                    while i < len(expression) and expression[i].isspace():
                        i += 1
                    
                    if i == len(expression):
                         raise ValueError("Expression ends with a unary operator")

                    num_str = ''
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    
                    if not num_str:
                        raise ValueError("Unary minus must be followed by a number")
                        
                    try:
                        tokens.append(-float(num_str))
                    except ValueError:
                        raise ValueError(f"Invalid number format after unary minus: '{num_str}'")
                    continue
                else:
                    tokens.append(char)
            
            elif char in self._PARENTHESES:
                tokens.append(char)
            
            else:
                raise ValueError(f"Invalid character in expression: '{char}'")
            
            i += 1
            
        return tokens

    def _to_rpn(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a token list from infix to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._OPERATORS:
                while (operator_stack and
                       operator_stack[-1] in self._OPERATORS and
                       self._OPERATORS[operator_stack[-1]]['precedence'] >= self._OPERATORS[token]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
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

    def _evaluate_rpn(self, rpn_tokens: List[Union[float, str]]) -> float:
        """Evaluates an RPN token list."""
        value_stack = []

        for token in rpn_tokens:
            if isinstance(token, float):
                value_stack.append(token)
            elif token in self._OPERATORS:
                if len(value_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands for operator")
                
                operand2 = value_stack.pop()
                operand1 = value_stack.pop()
                
                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero")
                
                operation = self._OPERATORS[token]['func']
                result = operation(operand1, operand2)
                value_stack.append(result)

        if len(value_stack) != 1:
            raise ValueError("Malformed expression resulting in invalid value stack")

        return value_stack[0]


if __name__ == '__main__':
    # This block demonstrates the calculator's usage and serves as a simple
    # interactive test harness.
    calculator = Calculator()

    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to evaluate or 'exit' to quit.")
    print("Supported operations: +, -, *, /, ()")
    print("Example: 3.5 * (2 + -1) / 2\n")

    while True:
        try:
            expression = input(">>> ")
            if expression.lower() == 'exit':
                break
            
            result = calculator.calculate(expression)
            print(f"= {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

