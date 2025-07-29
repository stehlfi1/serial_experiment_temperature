
import operator

class Calculator:
    """
    A high-quality, console-based arithmetic calculator.

    This class implements a calculator that evaluates arithmetic expressions
    from a string. It adheres to the ISO/IEC 25010 standard for software
    quality by emphasizing correctness, performance, safety, and maintainability.

    Features:
    - Supports addition (+), subtraction (-), multiplication (*), division (/).
    - Correctly handles operator precedence.
    - Supports parentheses for grouping.
    - Accepts integers and floating-point numbers, including negative values.
    - Provides robust validation and clear error messages.
    - Does NOT use the unsafe `eval()` function.

    The implementation uses the Shunting-yard algorithm to convert the infix
    expression to Reverse Polish Notation (RPN), which is then evaluated.
    """

    # --- Constants for defining operator properties ---
    _OPERATORS = {
        '+': {'precedence': 1, 'func': operator.add},
        '-': {'precedence': 1, 'func': operator.sub},
        '*': {'precedence': 2, 'func': operator.mul},
        '/': {'precedence': 2, 'func': operator.truediv}
    }
    _PARENTHESES = {'(', ')'}

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the main public interface for the Calculator.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., mismatched
                        parentheses, invalid characters).
            ZeroDivisionError: If the expression contains a division by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raise exceptions to be handled by the caller,
            # maintaining a clear chain of responsibility.
            raise e
        except Exception as e:
            # Catch any other unexpected errors and wrap them for clarity.
            raise ValueError(f"An unexpected error occurred: {e}") from e

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input string into a list of tokens (numbers and operators).
        This process is also known as lexical analysis.

        Args:
            expression: The string expression to tokenize.

        Returns:
            A list of tokens (floats and strings).

        Raises:
            ValueError: For invalid characters or number formats.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                continue

            # Handle operators and parentheses
            if char in self._OPERATORS or char in self._PARENTHESES:
                # Handle unary minus (e.g., -5 or 3 * -5)
                if char == '-' and (not tokens or isinstance(tokens[-1], str) and tokens[-1] != ')'):
                    num_str = "-"
                    i += 1
                    # Skip any whitespace after the unary minus
                    while i < len(expression) and expression[i].isspace():
                        i += 1
                    
                    if i == len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                        raise ValueError("Invalid use of unary minus")
                        
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    try:
                        tokens.append(float(num_str))
                    except ValueError:
                        raise ValueError(f"Invalid number format: '{num_str}'")
                    continue
                
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Invalid character in expression: '{char}'")
        
        return tokens

    def _to_rpn(self, tokens: list) -> list:
        """
        Converts a token list from infix to Reverse Polish Notation (RPN)
        using the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: For mismatched parentheses or invalid expression structure.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._OPERATORS:
                while (operator_stack and
                       operator_stack[-1] != '(' and
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
                operator_stack.pop()  # Discard the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: list) -> float:
        """
        Evaluates a token list in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack = []

        for token in rpn_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            elif token in self._OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator")
                
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                
                if token == '/' and op2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                
                operation_func = self._OPERATORS[token]['func']
                result = operation_func(op1, op2)
                operand_stack.append(result)
        
        if len(operand_stack) != 1:
            raise ValueError("Invalid expression format")

        return operand_stack[0]


if __name__ == "__main__":
    # --- Demonstration of the Calculator ---
    # This block runs only when the script is executed directly.
    
    calc = Calculator()
    
    print("--- High-Quality Python Calculator ---")
    print("Enter an arithmetic expression or 'exit' to quit.")
    print("Example: 3.5 + 4 * (2 - 1) / 2")
    
    while True:
        try:
            expression_input = input("\n> ")
            if expression_input.lower() == 'exit':
                print("Exiting calculator.")
                break
            
            result = calc.calculate(expression_input)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected system error occurred: {e}")

