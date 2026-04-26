```python
import re
from typing import Dict, Callable
import operator

class SecureMathEvaluator:
    def __init__(self):
        # Define allowed operators with their corresponding functions
        self.operators: Dict[str, Callable] = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        
        # Regex for validating numbers and operators
        self.number_pattern = re.compile(r'^-?\d+(\.\d+)?$')
        self.operator_pattern = re.compile(r'^[-+*/]$')

    def _validate_number(self, value: str) -> float:
        """Validate and convert number input."""
        if not self.number_pattern.match(value):
            raise ValueError("Invalid number format")
        return float(value)

    def _validate_operator(self, operator: str) -> None:
        """Validate operator input."""
        if not self.operator_pattern.match(operator):
            raise ValueError("Invalid operator")

    def _tokenize(self, expression: str) -> list:
        """Split expression into tokens."""
        tokens = []
        current = ''
        
        for char in expression:
            if char.isspace():
                continue
            if char in self.operators or char in {'(', ')'}:
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append(char)
            else:
                current += char
        
        if current:
            tokens.append(current)
        
        return tokens

    def evaluate(self, expression: str) -> float:
        """Evaluate mathematical expression securely."""
        try:
            # Validate input
            if not expression.strip():
                raise ValueError("Empty expression")

            # Tokenize expression
            tokens = self._tokenize(expression)
            
            # Validate operators
            for token in tokens:
                self._validate_operator(token)
            
            # Handle parentheses
            stack = []
            for token in tokens:
                if token == '(':
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        stack.pop()
                    if not stack:
                        raise ValueError("Mismatched parentheses")
                    stack.pop()  # Remove '('
                else:
                    stack.append(token)
            
            if stack:
                raise ValueError("Mismatched parentheses")

            # Evaluate tokens
            result = self._evaluate_tokens(tokens)
            if not isinstance(result, float):
                raise ValueError("Invalid expression")
            return result

        except (ValueError, ZeroDivisionError) as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")

    def _evaluate_tokens(self, tokens: list) -> float:
        """Recursively evaluate tokens."""
        stack = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if isinstance(token, float):
                stack.append(token)
            elif token in self.operators:
                if i == 0 or tokens[i-1] != '(':
                    raise ValueError("Invalid operator position")
                if token == '/':
                    if not stack:
                        raise ValueError("Division by zero")
                    if not isinstance(stack[-1], (int, float)):
                        raise ValueError("Invalid division")
                    if stack[-1] == 0:
                        raise ValueError("Division by zero")
                    result = stack.pop() / self.operators[token](stack.pop())
                else:
                    result = self.operators[token](stack.pop(), stack.pop())
                stack.append(result)
            elif token == '(':
                raise ValueError("Mismatched parentheses")
            elif token == ')':
                raise ValueError("Mismatched parentheses")
            else:
                raise ValueError("Invalid token")
            
            i += 1

        if len(stack) != 1:
            raise ValueError("Invalid expression")
        
        return stack[0]

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    try:
        result =