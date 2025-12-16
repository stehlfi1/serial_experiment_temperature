
import operator

class Calculator:
    """
    A high-quality, maintainable calculator that evaluates arithmetic expressions.

    This class adheres to the principles of the ISO/IEC 25010 standard by providing
    a solution that is correct, efficient, modular, safe, and well-documented.

    It uses the Shunting-Yard algorithm to parse and evaluate expressions, 
    supporting addition, subtraction, multiplication, division, parentheses, and
    correct operator precedence for integers and floating-point numbers.
    """

    # --- Constants for Modularity and Readability ---
    _OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    _PRECEDENCE = {
        '(': 0,
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression from a string and returns the result.

        Args:
            expression: A string containing the mathematical expression to be evaluated.
                        The expression can contain integers, floats, parentheses, and
                        the operators +, -, *, /.

        Returns:
            The floating-point result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, malformed structure).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        # --- Safety and Reliability: Input Validation ---
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Input expression must be a non-empty string.")

        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except ZeroDivisionError:
            # Re-raise with a consistent, user-friendly message for fault tolerance.
            raise ZeroDivisionError("Evaluation error: Division by zero is not allowed.")
        except (ValueError, IndexError) as e:
            # Catch internal processing errors and frame them as invalid expression errors.
            # IndexError can occur from pop() on empty stacks for malformed expressions.
            raise ValueError(f"Invalid expression provided. Details: {e}")

    # --- Modularity: Private Helper Methods for Single Responsibilities ---

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts an expression string into a list of tokens (numbers and operators).

        This tokenizer correctly handles multi-digit numbers, floating-point numbers,
        and unary minus (e.g., '-5' or '3 * -2').

        Args:
            expression: The raw expression string.

        Returns:
            A list of string tokens.
        
        Raises:
            ValueError: If an unrecognized character is found.
        """
        # Remove all whitespace for easier parsing
        expression = expression.replace(" ", "")
        
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isdigit() or char == '.':
                num_str = ""
                # Consume all parts of a number (digits and a single decimal point)
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
                continue # Continue to the next loop iteration

            if char in self._OPERATORS or char in '()':
                # --- Correctness: Handle Unary Minus ---
                # A minus sign is unary if it's the first token, or if it follows
                # an operator or an opening parenthesis.
                if char == '-' and (i == 0 or expression[i-1] in self._OPERATORS or expression[i-1] == '('):
                    num_str = "-"
                    i += 1
                    # Find the number following the unary minus
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    
                    if len(num_str) == 1: # Case where '-' is followed by non-digit
                         raise ValueError("Invalid use of operator '-'")

                    tokens.append(num_str)
                    continue

                tokens.append(char)
                i += 1
                continue
            
            # --- Safety: Invalid Character Handling ---
            raise ValueError(f"Invalid character in expression: '{char}'")
        
        return tokens

    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """
        Converts a list of infix tokens to postfix (RPN) using Shunting-Yard.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in postfix order.
        
        Raises:
            ValueError: For mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            try:
                # If token is a number, add it to the output queue.
                float(token)
                output_queue.append(token)
            except ValueError:
                if token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    # Pop operators until an opening parenthesis is found.
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    
                    if not operator_stack or operator_stack.pop() != '(':
                        raise ValueError("Mismatched parentheses: more ')' than '('")
                    
                elif token in self._OPERATORS:
                    # Pop operators with higher or equal precedence.
                    while (operator_stack and 
                           self._PRECEDENCE.get(operator_stack[-1], 0) >= self._PRECEDENCE.get(token, 0)):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)

        # Pop any remaining operators from the stack to the output.
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                # --- Safety: Mismatched Parentheses Check ---
                raise ValueError("Mismatched parentheses: more '(' than ')'")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, postfix_tokens: list[str]) -> float:
        """
        Evaluates a postfix (RPN) expression.

        Args:
            postfix_tokens: A list of tokens in postfix order.

        Returns:
            The final calculated result.
        
        Raises:
            ValueError: If the expression is malformed (e.g., insufficient operands).
            ZeroDivisionError: For division by zero.
        """
        value_stack = []

        for token in postfix_tokens:
            try:
                # If token is a number, convert and push to stack.
                value_stack.append(float(token))
            except ValueError:
                # Token must be an operator.
                if len(value_stack) < 2:
                    raise ValueError(f"Insufficient operands for operator '{token}'")
                
                # --- Correctness: Operand Order ---
                operand2 = value_stack.pop()
                operand1 = value_stack.pop()
                
                operation = self._OPERATORS[token]
                
                # --- Safety: Division by Zero Check ---
                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError()
                
                result = operation(operand1, operand2)
                value_stack.append(result)

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: check operator and operand balance.")

        return value_stack[0]


if __name__ == '__main__':
    # --- Example Usage and Demonstration ---
    # This section demonstrates the calculator's functionality and serves as
    # an informal test suite, showcasing its testability.
    
    calculator = Calculator()
    
    expressions_to_test = [
        "3 + 5 * (10 - 4)",          # Expected: 33.0 (Precedence and Parentheses)
        "10 / 2 - 3",                # Expected: 2.0 (Order of Operations)
        "5.5 + 2.5",                 # Expected: 8.0 (Floating Point Support)
        "-5 + 10",                   # Expected: 5.0 (Unary Minus at Start)
        "10 * -2",                   # Expected: -20.0 (Unary Minus after Operator)
        "10 / (2 - 2)",              # Expected: ZeroDivisionError
        "5 + (3 * 2",               # Expected: ValueError (Mismatched Parentheses)
        "5 + 3 # 2",                 # Expected: ValueError (Invalid Character)
        "5 + * 3",                   # Expected: ValueError (Malformed Expression)
        "((20 - 10) * 3) / 5 + 1"     # Expected: 7.0 (Complex Expression)
    ]
    
    print("--- Running Calculator Tests ---")
    
    for i, expr in enumerate(expressions_to_test):
        try:
            result = calculator.calculate(expr)
            print(f"Test {i+1}: '{expr}' = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Test {i+1}: '{expr}' -> Handled error: {e}")

    print("\n--- Interactive Calculator ---")
    print("Enter 'quit' to exit.")
    while True:
        try:
            user_input = input("Calculate: ")
            if user_input.lower() == 'quit':
                break
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
