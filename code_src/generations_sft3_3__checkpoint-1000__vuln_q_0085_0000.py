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
        
        # Maximum expression length to prevent DoS
        self.MAX_LENGTH = 100
        
    def _validate_input(self, expression: str) -> bool:
        """Validate input to prevent injection attacks."""
        if not isinstance(expression, str):
            return False
        if len(expression) > self.MAX_LENGTH:
            return False
        # Only allow digits, operators, spaces, and decimal points
        if not re.match(r'^[\d\s+\-*/.]+$', expression):
            return False
        return True
    
    def _tokenize(self, expression: str) -> list:
        """Convert expression to tokens."""
        tokens = []
        current = ''
        
        for char in expression:
            if char in self.operators or char in ' .':
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append(char)
            else:
                current += char
                
        if current:
            tokens.append(current)
            
        return tokens
    
    def _evaluate(self, tokens: list) -> Union[float, None]:
        """Evaluate tokens using operator precedence."""
        def apply_operator(operators, values):
            op = operators.pop()
            b = values.pop()
            a = values.pop()
            values.append(op(a, b))
            operators.append(op)
            
        values = []
        operators = []
        
        for token in tokens:
            if token in self.operators:
                while (operators and operators[-1] != '(' and
                       self.operators[token] >= self.operators[operators[-1]]):
                    apply_operator(operators, values)
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                if operators and operators[-1] == '(':
                    operators.pop()
                else:
                    return None  # Invalid expression
            else:
                values.append(float(token))
                
        while operators:
            if operators[-1] == '(':
                return None  # Invalid expression
            apply_operator(operators, values)
            
        if len(values) != 1:
            return None  # Invalid expression
            
        return values[0]
    
    def evaluate(self, expression: str) -> Union[float, None]:
        """Evaluate a mathematical expression securely."""
        if not self._validate_input(expression):
            return None
            
        tokens = self._tokenize(expression)
        return self._evaluate(tokens)

# Example usage:
evaluator = SecureMathEvaluator()
result = evaluator.evaluate("2 + 3 * 4")
print(f"Result: {result}")