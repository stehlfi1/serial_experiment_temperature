
"""
A high-quality, console-based arithmetic calculator adhering to ISO/IEC 25010.

This module provides a Calculator class capable of evaluating arithmetic
expressions from strings, including support for parentheses and operator precedence.

ISO/IEC 25010 Characteristics Adherence:
- Functional Suitability: Correctly implements addition, subtraction,
  multiplication, division, and parentheses.
- Performance Efficiency: Utilizes the efficient Shunting-yard algorithm for
  expression parsing and evaluation.
- Compatibility: Written in standard Python 3, compatible with major platforms.
- Usability: Provides clear error messages for invalid input.
- Reliability: Includes robust error handling for malformed expressions,
  invalid characters, and division by zero.
- Security: Avoids the use of `eval()` to prevent code injection vulnerabilities.
- Maintainability: Code is modular, well-documented, and uses clear naming
  conventions, making it easy to understand, modify, and test.
- Portability: No platform-specific dependencies are used.
"""

import re
from typing import List, Union

# A type alias for tokens to improve readability.
Token = Union[float, str]


class Calculator:
    """
    A class to evaluate arithmetic expressions from a string.

    This calculator parses and evaluates expressions containing integers,
    floating-point numbers, and the operators +, -, *, /, and parentheses.
    It follows standard operator precedence.
    """

    # --- Class Attributes for Configuration ---
    # Defines the supported operators and their properties.
    # This centralized configuration enhances maintainability.
    OPERATORS = {
        '+': {'precedence': 1, 'func': lambda a, b: a + b},
        '-': {'precedence': 1, 'func': lambda a, b: a - b},
        '*': {'precedence': 2, 'func': lambda a, b: a * b},
        '/': {'precedence': 2, 'func': lambda a, b: a / b},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string.

        This is the main public interface of the calculator. It orchestrates
        the tokenization, parsing (Shunting-yard), and evaluation steps.

        Args:
            expression: The arithmetic expression string to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is malformed, contains invalid
                        characters, or has mismatched parentheses.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._to_rpn(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return result
        except (ValueError, ZeroDivisionError) as e:
            # Re-raising exceptions to be handled by the caller,
            # preserving the original error type and message.
            raise e
        except Exception:
            # Catch any other unexpected errors during parsing/evaluation.
            raise ValueError(f"Invalid or malformed expression: '{expression}'")

    def _tokenize(self, expression: str) -> List[Token]:
        """
        Converts the input string into a list of numbers and operators.

        This method uses regular expressions for efficient and accurate tokenization.
        It correctly handles integers, floats, and all supported operators,
        while also detecting and flagging any invalid characters. It also handles
        unary minus at the beginning of an expression or after an operator/parenthesis.

        Args:
            expression: The raw expression string.

        Returns:
            A list of tokens (float numbers and string operators).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to find numbers (int/float) or operators/parentheses.
        # This is a robust way to split the string into meaningful parts.
        token_regex = re.compile(r"(\d+\.?\d*|\.\d+|[+\-*/()])")
        
        # Remove whitespace to simplify parsing
        expression = expression.replace(" ", "")
        
        raw_tokens = token_regex.findall(expression)

        # Validate that the regex captured the entire string. If not, there
        # are invalid characters.
        if "".join(raw_tokens) != expression:
            raise ValueError("Expression contains invalid characters.")

        tokens: List[Token] = []
        for i, token in enumerate(raw_tokens):
            if token in self.OPERATORS or token in "()":
                # Handle unary minus: a '-' is unary if it's the first token,
                # or if it follows an operator or an opening parenthesis.
                if token == '-' and (i == 0 or raw_tokens[i-1] in self.OPERATORS or raw_tokens[i-1] == '('):
                    # This is a unary minus. We prepend '0' to treat it as a binary op.
                    # e.g., "-5" becomes "0-5", "( -5 )" becomes "( 0 - 5 )"
                    tokens.append(0.0)
                tokens.append(token)
            else:
                # Convert numeric strings to float
                tokens.append(float(token))

        return tokens


    def _to_rpn(self, tokens: List[Token]) -> List[Token]:
        """
        Converts a token list from infix to postfix (RPN) using Shunting-yard.

        This algorithm correctly processes operators and parentheses to produce
        an output queue in Reverse Polish Notation, which is easy to evaluate.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list of tokens in RPN order.

        Raises:
            ValueError: If the expression has mismatched parentheses.
        """
        output_queue: List[Token] = []
        operator_stack: List[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self.OPERATORS:
                # While there's an operator on the stack with higher or equal precedence
                while (operator_stack and operator_stack[-1] != '(' and
                       self.OPERATORS[operator_stack[-1]]['precedence'] >= self.OPERATORS[token]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop operators from the stack to the queue until a '(' is found
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                # If the stack is empty, parentheses are mismatched
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop() # Discard the '('

        # Pop any remaining operators from the stack to the queue
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                # If a '(' is found here, it's a mismatch
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: List[Token]) -> float:
        """
        Evaluates a token queue in Reverse Polish Notation (RPN).

        Args:
            rpn_queue: A list of tokens in RPN order.

        Returns:
            The final calculated result as a float.

        Raises:
            ValueError: If the expression is malformed (e.g., not enough operands).
            ZeroDivisionError: For division by zero.
        """
        value_stack: List[float] = []

        for token in rpn_queue:
            if isinstance(token, float):
                value_stack.append(token)
            elif token in self.OPERATORS:
                if len(value_stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands for operator.")
                
                # Pop operands in reverse order
                operand2 = value_stack.pop()
                operand1 = value_stack.pop()
                
                # For division, check for division by zero
                if token == '/' and operand2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                
                # Apply the operator and push the result back to the stack
                result = self.OPERATORS[token]['func'](operand1, operand2)
                value_stack.append(result)

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: too many values left after evaluation.")

        return value_stack[0]


# --- Main execution block for demonstration and manual testing ---
if __name__ == "__main__":
    # This block demonstrates the Calculator's usage and serves as a
    # simple, interactive test harness. It showcases the code's testability.
    
    calc = Calculator()
    
    print("--- Console Arithmetic Calculator ---")
    print("Enter an expression to calculate or 'exit' to quit.")
    
    # Example expressions to showcase functionality and correctness
    test_expressions = [
        "3 + 5 * (10 - 4)",
        "10 / 2 - 3",
        "2.5 * 4 + 1.1",
        "-5 + 10",
        "5 * -2",
        "(4 + 6) * (3 - 1) / 5",
        "100 / (10 * (2 + 3))",
        "3 +",  # Invalid expression
        "5 * (10 - 2",  # Mismatched parentheses
        "10 / 0",  # Division by zero
        "5 & 4",  # Invalid character
    ]
    
    print("\n--- Running Pre-defined Test Cases ---")
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"'{expr}' = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"'{expr}' -> Error: {e}")
    
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_input = input(">> ")
            if user_input.lower() == 'exit':
                break
            if not user_input:
                continue
            
            result = calc.calculate(user_input)
            print(f"= {result}")
        
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

