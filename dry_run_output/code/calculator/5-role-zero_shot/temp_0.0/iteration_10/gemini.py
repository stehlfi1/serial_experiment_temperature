
import re

class Calculator:
    """
    A high-quality, maintainable calculator that evaluates arithmetic expressions.

    This class adheres to the principles of the ISO/IEC 25010 standard by
    focusing on functional suitability, performance efficiency, maintainability,
    reliability, and security.

    It uses the Shunting-yard algorithm to parse expressions, ensuring correct
    operator precedence and handling of parentheses. It does not use `eval()`,
    protecting against code injection vulnerabilities.

    Attributes:
        OPERATORS (dict): A dictionary mapping operators to their precedence and
                          the function that implements them.
    """

    OPERATORS = {
        '+': {'precedence': 1, 'func': lambda a, b: a + b},
        '-': {'precedence': 1, 'func': lambda a, b: a - b},
        '*': {'precedence': 2, 'func': lambda a, b: a * b},
        '/': {'precedence': 2, 'func': lambda a, b: a / b},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string.

        This is the public interface for the calculator. It orchestrates the
        tokenization, parsing (Shunting-yard), and evaluation steps.

        Args:
            expression: The arithmetic expression string to evaluate.
                        (e.g., "3 + 4 * (2 - 1)")

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, malformed).
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._shunting_yard(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (KeyError, IndexError):
            # Catches errors from malformed expressions during evaluation
            raise ValueError("Invalid or malformed expression")
        # Other exceptions (ValueError, ZeroDivisionError) are allowed to propagate

    def _is_number(self, token: str) -> bool:
        """Checks if a token can be converted to a float."""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _tokenize(self, expression: str) -> list[str]:
        """
        Converts an expression string into a list of tokens.

        This method handles integers, floats, operators, parentheses, and
        correctly identifies unary minus (negative numbers).

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (numbers as strings, operators, parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove all whitespace for easier parsing
        expression = expression.replace(" ", "")
        
        # Regex to find numbers (including floats), operators, and parentheses
        # This pattern correctly handles floating point numbers and operators.
        token_regex = re.compile(r"(\d+\.?\d*|[+\-*/()])")
        tokens = token_regex.findall(expression)

        # Post-process to handle unary minus (negative numbers)
        # A minus sign is unary if it's the first token or follows an operator or '('.
        processed_tokens = []
        for i, token in enumerate(tokens):
            if (token == '-' and
                (i == 0 or tokens[i-1] in self.OPERATORS or tokens[i-1] == '(')):
                # This is a unary minus, combine it with the next number
                try:
                    processed_tokens.append(f"-{tokens[i+1]}")
                    # Skip the next token since we've consumed it
                    tokens.pop(i+1)
                except IndexError:
                    raise ValueError("Invalid expression: trailing unary minus")
            else:
                processed_tokens.append(token)
        
        # Validate that all parts of the original string were tokenized
        if "".join(processed_tokens).replace("-","") != expression.replace("-",""):
             raise ValueError(f"Invalid characters in expression: {expression}")

        return processed_tokens


    def _shunting_yard(self, tokens: list[str]) -> list[str]:
        """
        Converts a token list from infix to postfix (RPN) notation.

        This method implements the Shunting-yard algorithm.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in Reverse Polish Notation.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in self.OPERATORS:
                while (operator_stack and
                       operator_stack[-1] in self.OPERATORS and
                       self.OPERATORS[operator_stack[-1]]['precedence'] >= self.OPERATORS[token]['precedence']):
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

    def _evaluate_rpn(self, rpn_queue: list[str]) -> float:
        """
        Evaluates a token queue in Reverse Polish Notation.

        Args:
            rpn_queue: A list of tokens in RPN.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: If division by zero occurs.
        """
        operand_stack = []

        for token in rpn_queue:
            if self._is_number(token):
                operand_stack.append(float(token))
            elif token in self.OPERATORS:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator")
                
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                
                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                
                operation = self.OPERATORS[token]['func']
                result = operation(operand1, operand2)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: too many operands")

        return operand_stack[0]


# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()
    
    print("--- High-Quality Python Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    
    # Example test cases to demonstrate correctness
    test_expressions = [
        "3 + 4 * 2 / ( 1 - 5 )",
        "10 + -2 * 5",
        "-10 + (8 * 2.5) - (3 / 1.5)",
        "(1 + 2) * 3",
        "10 / 2.5",
        "10 / 0",  # Division by zero
        "5 * (3 + 2", # Mismatched parentheses
        "5 + * 2", # Malformed expression
        "10 + abc" # Invalid characters
    ]

    print("\n--- Running Demonstration Cases ---")
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f'Expression: "{expr}"  =>  Result: {result}')
        except (ValueError, ZeroDivisionError) as e:
            print(f'Expression: "{expr}"  =>  Error: {e}')
    
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                break
            
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

