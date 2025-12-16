
import re
from collections import deque
from typing import List, Union

class Calculator:
    """
    A robust, console-based arithmetic calculator that evaluates string expressions.

    This class is designed with the principles of the ISO/IEC 25010 standard
    for software quality in mind, emphasizing correctness, performance, security,
    and maintainability.

    It uses the Shunting-Yard algorithm to parse expressions, supporting:
    - Basic arithmetic operations: +, -, *, /
    - Parentheses for grouping: ()
    - Correct operator precedence.
    - Integer and floating-point numbers (including negative values).

    The implementation explicitly avoids the use of `eval()` to prevent
    code injection vulnerabilities.
    """

    # Operator properties: precedence and associativity.
    # Higher precedence value means it's evaluated first.
    _OPERATORS = {
        '+': {'precedence': 1, 'assoc': 'left'},
        '-': {'precedence': 1, 'assoc': 'left'},
        '*': {'precedence': 2, 'assoc': 'left'},
        '/': {'precedence': 2, 'assoc': 'left'},
    }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a given arithmetic expression string and returns the result.

        Args:
            expression: The arithmetic expression string to evaluate.

        Returns:
            The result of the calculation as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        tokens = self._tokenize(expression)
        rpn_queue = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn_queue)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).
        Also handles unary minus by converting it to a binary operation (e.g., "-5" -> "0 - 5").
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")
            
        # Regex to capture numbers (int/float), operators, and parentheses.
        token_regex = re.compile(r'(\d+(?:\.\d*)?|\.\d+|[+\-*/()])')
        
        # Remove whitespace and find all tokens
        clean_expression = expression.replace(" ", "")
        tokens = token_regex.findall(clean_expression)

        # Validate that all characters were tokenized
        if "".join(tokens) != clean_expression:
            raise ValueError("Expression contains invalid characters.")

        # Handle unary minus: if '-' is at the start or after an operator/opening parenthesis,
        # insert a '0' before it.
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self._OPERATORS or tokens[i-1] == '('):
                processed_tokens.append('0')
            processed_tokens.append(token)
            
        return processed_tokens

    def _shunting_yard(self, tokens: List[str]) -> deque[Union[float, str]]:
        """
        Converts a list of infix tokens to a Reverse Polish Notation (RPN) queue
        using the Shunting-Yard algorithm.
        """
        output_queue: deque[Union[float, str]] = deque()
        operator_stack: deque[str] = deque()

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                output_queue.append(float(token))
            elif token in self._OPERATORS:
                op1 = token
                while (operator_stack and operator_stack[-1] in self._OPERATORS and
                       (self._OPERATORS[operator_stack[-1]]['precedence'] > self._OPERATORS[op1]['precedence'] or
                        (self._OPERATORS[operator_stack[-1]]['precedence'] == self._OPERATORS[op1]['precedence'] and
                         self._OPERATORS[op1]['assoc'] == 'left'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op1)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop() # Discard the '('

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: deque[Union[float, str]]) -> float:
        """
        Evaluates a Reverse Polish Notation (RPN) queue.
        """
        operand_stack: deque[float] = deque()

        for token in rpn_queue:
            if isinstance(token, float):
                operand_stack.append(token)
            else: # Token is an operator
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression format (operator without enough operands).")
                
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
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    operand_stack.append(op1 / op2)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression format (too many operands).")

        return operand_stack[0]

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    calculator = Calculator()
    
    print("--- Welcome to the High-Quality Python Calculator ---")
    print("This demonstration shows various valid and invalid expressions.")
    
    expressions = [
        # Correctness and Precedence
        "3 + 5 * (10 - 4)",
        # Floating point numbers
        "1.5 * 2.5 + 3.5 / 1.0",
        # Negative numbers and unary minus
        "-5 + 10",
        "10 * -2",
        "5 - -3",
        "( -1 + 2 ) * 3",
        # Complex expression
        "100 / ( 2 + 3 ) * 2 - 5.5",
        # Invalid expressions for error handling
        "5 * (10 - 4",      # Mismatched parentheses
        "5 +",              # Incomplete expression
        "10 / 0",           # Division by zero
        "5 @ 2",            # Invalid character
        "3 4 +",            # Malformed (too many operands)
    ]
    
    for expr in expressions:
        print(f"\nEvaluating expression: '{expr}'")
        try:
            result = calculator.calculate(expr)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")

