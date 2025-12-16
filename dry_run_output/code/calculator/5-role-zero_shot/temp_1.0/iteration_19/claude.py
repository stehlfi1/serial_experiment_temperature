
"""
Arithmetic Calculator Module

A console-based calculator that evaluates arithmetic expressions with proper
operator precedence and parentheses support, following ISO/IEC 25010 standards.
"""

from typing import List, Union
import re


class CalculatorError(Exception):
    """Base exception class for calculator errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the expression contains invalid characters or syntax."""
    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are not properly balanced."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class Calculator:
    """
    A calculator class that evaluates arithmetic expressions using the Shunting Yard algorithm.
    
    Supports:
    - Basic operations: +, -, *, /
    - Parentheses for grouping
    - Integer and floating-point numbers (including negative values)
    - Proper operator precedence
    """
    
    # Operator precedence mapping (higher number = higher precedence)
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'left'},
        '-': {'precedence': 1, 'associativity': 'left'},
        '*': {'precedence': 2, 'associativity': 'left'},
        '/': {'precedence': 2, 'associativity': 'left'}
    }
    
    def __init__(self):
        """Initialize the calculator."""
        self._reset_state()
    
    def _reset_state(self) -> None:
        """Reset internal state for new calculation."""
        pass
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression (str): The arithmetic expression to evaluate
            
        Returns:
            float: The result of the evaluated expression
            
        Raises:
            InvalidExpressionError: If the expression contains invalid characters
            UnbalancedParenthesesError: If parentheses are not balanced
            DivisionByZeroError: If division by zero is attempted
            
        Example:
            >>> calc = Calculator()
            >>> calc.calculate("2 + 3 * 4")
            14.0
            >>> calc.calculate("(10 - 5) * 2")
            10.0
        """
        if not expression or not expression.strip():
            raise InvalidExpressionError("Empty expression")
        
        # Clean and validate the expression
        cleaned_expression = self._preprocess_expression(expression)
        self._validate_expression(cleaned_expression)
        
        # Tokenize the expression
        tokens = self._tokenize(cleaned_expression)
        
        # Convert to postfix notation using Shunting Yard algorithm
        postfix_tokens = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix_tokens)
        
        return float(result)
    
    def _preprocess_expression(self, expression: str) -> str:
        """
        Clean and preprocess the expression.
        
        Args:
            expression (str): Raw expression string
            
        Returns:
            str: Cleaned expression
        """
        # Remove whitespace
        expression = expression.replace(' ', '')
        
        # Handle negative numbers at the beginning or after operators/opening parentheses
        expression = re.sub(r'(?<=^|[+\-*/\(])-', '0-', expression)
        
        return expression
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the expression for correct syntax and balanced parentheses.
        
        Args:
            expression (str): The expression to validate
            
        Raises:
            InvalidExpressionError: If invalid characters are found
            UnbalancedParenthesesError: If parentheses are unbalanced
        """
        # Check for valid characters only
        valid_pattern = r'^[0-9+\-*/.()]+$'
        if not re.match(valid_pattern, expression):
            raise InvalidExpressionError("Invalid characters in expression")
        
        # Check for balanced parentheses
        paren_count = 0
        for char in expression:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        if paren_count != 0:
            raise UnbalancedParenthesesError("Unbalanced parentheses")
        
        # Check for consecutive operators (except for negative numbers)
        if re.search(r'[+*/]{2,}|[+*/]-[+*/]', expression):
            raise InvalidExpressionError("Consecutive operators not allowed")
        
        # Check for empty parentheses
        if '()' in expression:
            raise InvalidExpressionError("Empty parentheses not allowed")
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Split the expression into tokens (numbers, operators, parentheses).
        
        Args:
            expression (str): The expression to tokenize
            
        Returns:
            List[str]: List of tokens
        """
        # Pattern to match numbers (including decimals) and operators
        token_pattern = r'\d+\.?\d*|[+\-*/()]'
        tokens = re.findall(token_pattern, expression)
        
        # Filter out empty strings
        tokens = [token for token in tokens if token]
        
        return tokens
    
    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Convert infix notation to postfix notation using Shunting Yard algorithm.
        
        Args:
            tokens (List[str]): List of tokens in infix notation
            
        Returns:
            List[str]: List of tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop operators until opening parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # Remove the '('
            elif token in self.OPERATORS:
                # Pop operators with higher or equal precedence
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.OPERATORS and
                       self._should_pop_operator(token, operator_stack[-1])):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
        
        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def _should_pop_operator(self, current_op: str, stack_op: str) -> bool:
        """
        Determine if the operator on the stack should be popped.
        
        Args:
            current_op (str): Current operator being processed
            stack_op (str): Operator on top of the stack
            
        Returns:
            bool: True if stack operator should be popped
        """
        current_prec = self.OPERATORS[current_op]['precedence']
        stack_prec = self.OPERATORS[stack_op]['precedence']
        current_assoc = self.OPERATORS[current_op]['associativity']
        
        return (stack_prec > current_prec or 
                (stack_prec == current_prec and current_assoc == 'left'))
    
    def _evaluate_postfix(self, tokens: List[str]) -> Union[int, float]:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens (List[str]): List of tokens in postfix notation
            
        Returns:
            Union[int, float]: The result of the evaluation
            
        Raises:
            DivisionByZeroError: If division by zero is attempted
        """
        stack = []
        
        for token in tokens:
            if self._is_number(token):
                # Convert to appropriate numeric type
                if '.' in token:
                    stack.append(float(token))
                else:
                    stack.append(int(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise InvalidExpressionError("Invalid expression structure")
                
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                result = self._apply_operator(operand1, operand2, token)
                stack.append(result)
        
        if len(stack) != 1:
            raise InvalidExpressionError("Invalid expression structure")
        
        return stack[0]
    
    def _apply_operator(self, operand1: Union[int, float], 
                       operand2: Union[int, float], 
                       operator: str) -> Union[int, float]:
        """
        Apply an operator to two operands.
        
        Args:
            operand1: First operand
            operand2: Second operand
            operator: Operator to apply
            
        Returns:
            Union[int, float]: Result of the operation
            
        Raises:
            DivisionByZeroError: If attempting to divide by zero
        """
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise DivisionByZeroError("Division by zero is not allowed")
            return operand1 / operand2
        else:
            raise InvalidExpressionError(f"Unknown operator: {operator}")
    
    def _is_number(self, token: str) -> bool:
        """
        Check if a token represents a number.
        
        Args:
            token (str): Token to check
            
        Returns:
            bool: True if token is a number
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Supported operations: +, -, *, /, ()")
    print("Enter 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            expression = input("Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except CalculatorError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


calc = Calculator()
result = calc.calculate("2 + 3 * (4 - 1)")  # Returns 11.0
