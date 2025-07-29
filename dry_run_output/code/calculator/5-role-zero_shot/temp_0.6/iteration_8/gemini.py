
import operator

class Calculator:
    """
    A high-quality, maintainable calculator that evaluates arithmetic expressions.

    This class implements a calculator that can parse and evaluate strings
    containing mathematical expressions. It adheres to standard operator precedence,
    supports parentheses, and handles integers, floating-point numbers, and
    negative values.

    The evaluation is performed using the Shunting-yard algorithm to convert
    the infix expression to Reverse Polish Notation (RPN), which is then
    evaluated safely without using Python's `eval()` function.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Correctly computes expressions.
    - Performance Efficiency: Uses an efficient O(n) algorithm.
    - Maintainability: Modular design with clear, documented methods.
    - Reliability: Robust error handling for invalid input and math errors.
    - Security: Avoids `eval()` to prevent code injection vulnerabilities.
    - Testability: Logic is separated into testable units.
    """
    
    # Define operators, their precedence, and their corresponding functions
    _OPERATORS = {
        '+': (operator.add, 1),
        '-': (operator.sub, 1),
        '*': (operator.mul, 2),
        '/': (operator.truediv, 2),
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        This is the public interface for the calculator. It orchestrates the
        tokenization, parsing (infix to RPN), and evaluation of the expression.

        Args:
            expression: The mathematical expression string to evaluate.
                        Example: "3 + 4 * (2 - 1)"

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_tokens = self._infix_to_rpn(tokens)
            result = self._evaluate_rpn(rpn_tokens)
            return result
        except KeyError as e:
            raise ValueError(f"Invalid character in expression: {e}")
        except IndexError:
            raise ValueError("Malformed expression or invalid operator usage")

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts the input expression string into a list of tokens.

        This method handles numbers (integers, floats, negatives) and operators.
        It correctly distinguishes between a binary subtraction and a unary negation.

        Args:
            expression: The raw expression string.

        Returns:
            A list of string tokens. e.g., "5 * -2" -> ['5', '*', '-2'].

        Raises:
            ValueError: If an unrecognized character is found.
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
                tokens.append(num_str)
                continue

            if char in self._OPERATORS or char in '()':
                # Handle unary minus (negation)
                if char == '-' and (not tokens or tokens[-1] in self._OPERATORS or tokens[-1] == '('):
                    # This is a unary minus, not subtraction
                    i += 1
                    # Find the number it applies to
                    num_str = "-"
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    if num_str == "-":
                        raise ValueError("Invalid use of unary minus")
                    tokens.append(num_str)
                    continue
                
                tokens.append(char)
                i += 1
                continue
            
            raise ValueError(f"Invalid character in expression: '{char}'")
        
        return tokens

    def _infix_to_rpn(self, tokens: list[str]) -> list[str]:
        """
        Converts a tokenized infix expression to Reverse Polish Notation (RPN).

        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            try:
                # If the token is a number, add it to the output queue.
                float(token)
                output_queue.append(token)
            except ValueError:
                if token in self._OPERATORS:
                    # Token is an operator.
                    op1_precedence = self._OPERATORS[token][1]
                    while (operator_stack and 
                           operator_stack[-1] in self._OPERATORS and
                           self._OPERATORS[operator_stack[-1]][1] >= op1_precedence):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    
                    if not operator_stack or operator_stack[-1] != '(':
                        raise ValueError("Mismatched parentheses in expression")
                    operator_stack.pop() # Pop the '('

        # Pop any remaining operators from the stack to the output
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression")
            output_queue.append(op)
            
        return output_queue

    def _evaluate_rpn(self, rpn_tokens: list[str]) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            rpn_tokens: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression is malformed.
        """
        value_stack = []

        for token in rpn_tokens:
            try:
                # If the token is a number, push it to the stack.
                value_stack.append(float(token))
            except ValueError:
                # Token is an operator.
                if len(value_stack) < 2:
                    raise ValueError("Malformed expression: insufficient values for an operator.")
                
                operand2 = value_stack.pop()
                operand1 = value_stack.pop()
                
                operation, _ = self._OPERATORS[token]
                
                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                result = operation(operand1, operand2)
                value_stack.append(result)
        
        if len(value_stack) != 1:
            raise ValueError("Malformed expression: too many values left.")
            
        return value_stack[0]

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()
    
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'quit' to exit.")
    
    # Example expressions for demonstration
    expressions_to_test = [
        "3 + 5 * 2",                   # Precedence
        "10 / 2 - 3",                  # Precedence
        "(3 + 5) * 2",                 # Parentheses
        "10 / (2 - 3)",                # Negative result
        "5 * -2",                      # Unary minus
        "-5 + 10",                     # Unary minus at start
        "3.5 * (1.2 + 8.8)",           # Floating point numbers
        "100 / 3",                     # Floating point division
        "-(5 + 2) * 3",                # Unary minus on parenthesis
        # Error cases
        "5 * (2 + 3",                  # Mismatched parentheses
        "5 / 0",                       # Division by zero
        "5 & 2",                       # Invalid character
        "5 + * 2",                     # Malformed expression
    ]

    print("\n--- Running Automated Tests ---")
    for expr in expressions_to_test:
        try:
            result = calculator.calculate(expr)
            print(f"Expression: '{expr}' -> Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: '{expr}' -> Error: {e}")

    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'quit':
                break
            if not user_input:
                continue
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
        
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

