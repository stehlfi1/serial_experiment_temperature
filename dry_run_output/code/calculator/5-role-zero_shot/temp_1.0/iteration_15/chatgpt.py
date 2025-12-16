
from typing import List, Union

class Calculator:
    """
    A console-based arithmetic calculator supporting +, -, *, /, parentheses,
    operator precedence, and both integers and floating-point numbers (including negatives).
    
    Adheres to high maintainability, code quality, and reliability requirements.
    """
        
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression string and returns its result as a float.
        
        Args:
            expression (str): Arithmetic expression to evaluate.
            
        Returns:
            float: The evaluated result.
        
        Raises:
            ValueError: If the input is invalid (unbalanced parentheses, invalid characters, etc.)
            ZeroDivisionError: In case of division by zero.
        """
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        rpn = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(rpn)
        
        
    def _tokenize(self, expr: str) -> List[str]:
        """
        Converts the input string into a list of valid tokens (numbers, operators, parentheses).
        Handles negative numbers and floating point numbers.
        
        Args:
            expr (str): Input expression.
        
        Returns:
            List[str]: Tokenized expression.
        
        Raises:
            ValueError: If invalid characters are found.
        """
        tokens = []
        i = 0
        length = len(expr)
        prev_token_type = None # "op" | "num" | "paren"
        
        while i < length:
            char = expr[i]

            if char.isspace():
                i += 1
                continue

            # number parsing (handles floats, negative numbers)
            if char.isdigit() or (char == '.' and i + 1 < length and expr[i+1].isdigit()):
                num_str = ''
                dot_seen = False
                while i < length and (expr[i].isdigit() or expr[i] == '.'):
                    if expr[i] == '.':
                        if dot_seen:
                            raise ValueError("Invalid number format: multiple decimal points.")
                        dot_seen = True
                    num_str += expr[i]
                    i += 1
                tokens.append(num_str)
                prev_token_type = "num"
                continue

            # handle negative number at the start or after '(' or operator
            if char == '-' and (
                prev_token_type is None or
                (prev_token_type == "op") or
                (prev_token_type == "paren" and tokens and tokens[-1] == '(')
            ):
                # look ahead for a number or decimal
                j = i + 1
                if j < length and (expr[j].isdigit() or expr[j] == '.'):
                    num_str = '-'
                    dot_seen = False
                    i += 1
                    while i < length and (expr[i].isdigit() or expr[i] == '.'):
                        if expr[i] == '.':
                            if dot_seen:
                                raise ValueError("Invalid number format: multiple decimal points.")
                            dot_seen = True
                        num_str += expr[i]
                        i += 1
                    tokens.append(num_str)
                    prev_token_type = "num"
                    continue
                else:
                    # Just a negative sign, treat as operator
                    tokens.append('-')
                    i += 1
                    prev_token_type = "op"
                    continue

            # handle operators
            if char in ('+', '-', '*', '/'):
                tokens.append(char)
                i += 1
                prev_token_type = "op"
                continue

            if char in ('(', ')'):
                tokens.append(char)
                i += 1
                prev_token_type = "paren"
                continue

            # invalid character
            raise ValueError(f"Invalid character in expression: '{char}'")

        return tokens

    def _validate_tokens(self, tokens: List[str]) -> None:
        """
        Validates the tokenized expression for basic errors.
        
        Checks:
         - Parentheses are balanced
         - No invalid sequences
        
        Args:
            tokens (List[str]): The tokenized expression.
        
        Raises:
            ValueError: If validation fails.
        """
        balance = 0
        prev_type = None
        for idx, token in enumerate(tokens):
            if token == '(':
                balance += 1
                prev_type = "paren"
            elif token == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Unbalanced parentheses: more ')' than '('.")
                prev_type = "paren"
            elif token in ('+', '-', '*', '/'):
                if prev_type is None or prev_type == "op":
                    # Prevent two consecutive operators (except negative numbers, handled in tokenizer)
                    raise ValueError("Invalid operator sequence.")
                prev_type = "op"
            else:
                # token is a number
                try:
                    float(token)
                except ValueError:
                    raise ValueError(f"Invalid number token: {token}")
                prev_type = "num"
        if balance != 0:
            raise ValueError("Unbalanced parentheses in expression.")

    def _infix_to_postfix(self, tokens: List[str]) -> List[Union[str, float]]:
        """
        Transforms infix tokens into postfix (RPN) using the Shunting Yard algorithm.
        
        Args:
            tokens (List[str]): The tokenized infix expression.
            
        Returns:
            List[Union[str, float]]: The tokens in postfix (RPN) order.
        """
        output = []
        op_stack = []
        # Operator precedence map
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        # Both + and - are left-associative
        left_assoc = {'+': True, '-': True, '*': True, '/': True}
        
        for token in tokens:
            if self._is_number(token):
                output.append(float(token))
            elif token in precedence:
                while (op_stack and op_stack[-1] in precedence and
                       (precedence[op_stack[-1]] > precedence[token] or
                        (precedence[op_stack[-1]] == precedence[token] and left_assoc[token]))):
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    output.append(op_stack.pop())
                if not op_stack:
                    raise ValueError("Unbalanced parentheses during infix-to-postfix conversion.")
                op_stack.pop() # remove '('
            else:
                raise ValueError(f"Unexpected token: {token}")
        
        while op_stack:
            if op_stack[-1] in ('(', ')'):
                raise ValueError("Unbalanced parentheses at end of processing.")
            output.append(op_stack.pop())
        
        return output
        
    def _evaluate_postfix(self, postfix: List[Union[str, float]]) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            postfix (List[Union[str, float]]): The postfix (RPN) token list.
            
        Returns:
            float: Result of expression
        
        Raises:
            ZeroDivisionError: On division by zero.
            ValueError: If the postfix is invalid.
        """
        stack = []
        for token in postfix:
            if isinstance(token, float):
                stack.append(token)
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in postfix: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid expression: leftover operands in stack.")
        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operation.
        
        Args:
            a (float): Left operand.
            b (float): Right operand.
            operator (str): Operator ('+', '-', '*', '/')
        
        Returns:
            float: Result
        
        Raises:
            ZeroDivisionError: For division by zero.
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero.")
            return a / b
        else:
            raise ValueError(f"Invalid operator: {operator}")

    def _is_number(self, token: str) -> bool:
        """
        Check if a string token represents a valid number.
        
        Args:
            token (str): Token string.
        
        Returns:
            bool: True if number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

# Example test cases (demonstrating easy testability)
if __name__ == "__main__":
    calc = Calculator()
    test_expressions = [
        "1 + 2 * 3",            # 7
        "(1 + 2) * 3",          # 9
        "-2 + 3 * 4",           # 10
        "3 + 4 * 2 / (1 - 5)",  # 1
        "3.5 + (-2.1)",         # 1.4
        "-(2 + 3) * 4",         # -20
        "5 / 0.5",              # 10
        "((2+3)*5.5-6)/2",      # 10.25
        "-0.75 * (4+2) / -3",   # 1.5
    ]

    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} => ERROR: {e}")
