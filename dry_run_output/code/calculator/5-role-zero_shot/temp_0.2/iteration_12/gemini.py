
import re

class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.

    This class implements a parser and evaluator for infix expressions, supporting
    addition, subtraction, multiplication, division, and parentheses. It adheres
    to standard operator precedence.

    The implementation follows the Shunting-yard algorithm to convert the infix
    expression to Reverse Polish Notation (RPN), which is then evaluated.
    This approach avoids the use of Python's `eval()` function for safety.

    ISO/IEC 25010 Compliance:
    - Functional Suitability: Correctly evaluates expressions with +, -, *, /, ().
    - Performance Efficiency: O(n) time complexity.
    - Reliability: Handles invalid inputs and division by zero gracefully.
    - Maintainability: Modular design with clear separation of concerns.
    - Security: Avoids `eval()` to prevent code injection vulnerabilities.
    """

    # Operator properties: precedence and associativity ('L' for Left, 'R' for Right)
    _OPERATORS = {
        '+': {'prec': 1, 'assoc': 'L'},
        '-': {'prec': 1, 'assoc': 'L'},
        '*': {'prec': 2, 'assoc': 'L'},
        '/': {'prec': 2, 'assoc': 'L'},
    }
    
    # Unary operators have the highest precedence
    _UNARY_OPERATORS = {
        'u-': {'prec': 3, 'assoc': 'R'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        self._validate_expression(expression)
        tokens = self._tokenize(expression)
        rpn_queue = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn_queue)
        return result

    def _validate_expression(self, expression: str) -> None:
        """Checks for invalid characters and unbalanced parentheses."""
        # Check for any characters that are not digits, operators, parentheses, or whitespace
        allowed_chars = r"[\d\s\.\+\-\*\/\(\)]+"
        if not re.fullmatch(allowed_chars, expression):
            raise ValueError("Expression contains invalid characters.")
        
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            raise ValueError("Expression has unbalanced parentheses.")

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input string into a list of tokens (numbers and operators).

        This tokenizer correctly handles floating-point numbers and distinguishes
        between binary and unary minus operators.
        """
        # Add spaces around operators to simplify splitting, but be careful with scientific notation
        # A negative lookbehind `(?<!e)` can prevent splitting on 'e-' in numbers like '1e-5'
        expression = re.sub(r'([\+\-\*\/\(\)])', r' \1 ', expression)
        tokens = expression.split()
        
        # Post-process to identify unary minus
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-':
                # It's a unary minus if it's the first token or preceded by an operator or '('
                is_first_token = (i == 0)
                is_preceded_by_operator = (i > 0 and tokens[i-1] in self._OPERATORS)
                is_preceded_by_paren = (i > 0 and tokens[i-1] == '(')
                
                if is_first_token or is_preceded_by_operator or is_preceded_by_paren:
                    processed_tokens.append('u-') # 'u-' represents unary minus
                else:
                    processed_tokens.append(token) # It's a binary minus
            else:
                processed_tokens.append(token)
        
        return processed_tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts a list of infix tokens to a Reverse Polish Notation (RPN) queue.

        This method implements Dijkstra's Shunting-yard algorithm.
        """
        output_queue = []
        operator_stack = []

        all_operators = {**self._OPERATORS, **self._UNARY_OPERATORS}

        for token in tokens:
            try:
                # If the token is a number, add it to the output queue.
                output_queue.append(float(token))
            except ValueError:
                if token in all_operators:
                    # Token is an operator
                    op1 = token
                    while (operator_stack and operator_stack[-1] != '(' and
                           (all_operators[operator_stack[-1]]['prec'] > all_operators[op1]['prec'] or
                            (all_operators[operator_stack[-1]]['prec'] == all_operators[op1]['prec'] and all_operators[op1]['assoc'] == 'L'))):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(op1)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    
                    if not operator_stack or operator_stack[-1] != '(':
                        # This case is technically caught by the initial validation,
                        # but included for algorithmic completeness.
                        raise ValueError("Mismatched parentheses in expression.")
                    operator_stack.pop() # Pop the '('
                else:
                    # This should not be reached if _validate_expression is correct
                    raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators from the stack to the output queue
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)
            
        return output_queue

    def _evaluate_rpn(self, rpn_queue: list) -> float:
        """Evaluates an RPN queue and returns the final result."""
        value_stack = []

        for token in rpn_queue:
            if isinstance(token, float):
                value_stack.append(token)
            else: # Token is an operator
                try:
                    if token in self._UNARY_OPERATORS:
                        operand = value_stack.pop()
                        if token == 'u-':
                            value_stack.append(-operand)
                    else:
                        operand2 = value_stack.pop()
                        operand1 = value_stack.pop()
                        if token == '+':
                            value_stack.append(operand1 + operand2)
                        elif token == '-':
                            value_stack.append(operand1 - operand2)
                        elif token == '*':
                            value_stack.append(operand1 * operand2)
                        elif token == '/':
                            if operand2 == 0:
                                raise ZeroDivisionError("Division by zero is not allowed.")
                            value_stack.append(operand1 / operand2)
                except IndexError:
                    raise ValueError("Malformed expression: insufficient operands for an operator.")

        if len(value_stack) != 1:
            raise ValueError("Malformed expression: too many values left after evaluation.")
            
        return value_stack[0]

def main():
    """
    Main function to run the calculator in an interactive console loop.
    """
    print("--- High-Quality Python Calculator ---")
    print("Supports +, -, *, /, parentheses, and floating-point numbers.")
    print("Enter 'exit' or 'quit' to close the program.")
    
    calculator = Calculator()
    
    while True:
        try:
            expression = input("\nEnter expression: ")
            if expression.lower() in ['exit', 'quit']:
                print("Exiting calculator. Goodbye!")
                break
            
            if not expression.strip():
                continue

            result = calculator.calculate(expression)
            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
