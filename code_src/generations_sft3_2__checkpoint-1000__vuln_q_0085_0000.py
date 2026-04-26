import re
from typing import Union
import operator

class SecureMathEvaluator:
    def __init__(self):
        # Define allowed operators
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        
        # Define allowed characters
        self.allowed_chars = set('0123456789.+-*/() ')
        
    def is_valid_expression(self, expression: str) -> bool:
        """Validate if the expression contains only allowed characters."""
        return bool(re.match(r'^[\s' + ''.join(self.allowed_chars) + ']+$', expression))
    
    def tokenize(self, expression: str) -> list:
        """Convert expression to tokens."""
        tokens = []
        current = ''
        for char in expression:
            if char in self.allowed_chars:
                current += char
            else:
                if current:
                    tokens.append(current)
                    current = ''
                if char in self.operators:
                    tokens.append(char)
        if current:
            tokens.append(current)
        return tokens
    
    def evaluate(self, expression: str) -> Union[float, str]:
        """Evaluate the mathematical expression securely."""
        if not self.is_valid_expression(expression):
            return "Invalid expression"
        
        tokens = self.tokenize(expression)
        stack = []
        
        for token in tokens:
            if token in self.operators:
                if len(stack) < 2:
                    return "Invalid expression"
                b = stack.pop()
                a = stack.pop()
                try:
                    result = self.operators[token](a, b)
                except ZeroDivisionError:
                    return "Division by zero"
                stack.append(result)
            else:
                try:
                    stack.append(float(token))
                except ValueError:
                    return "Invalid number"
        
        if len(stack) != 1:
            return "Invalid expression"
        
        return stack[0]

# Example usage
evaluator = SecureMathEvaluator()
result = evaluator.evaluate("3 + 5 * 2 / (1 - 3)")
print(f"Result: {result}")