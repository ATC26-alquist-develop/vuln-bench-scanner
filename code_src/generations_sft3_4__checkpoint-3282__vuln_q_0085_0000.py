```python
import re
from typing import Dict, Callable
from decimal import Decimal, InvalidOperation

class SecureMathEvaluator:
    def __init__(self):
        # Define allowed operators and their corresponding functions
        self.operators: Dict[str, Callable[[Decimal, Decimal], Decimal]] = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y
        }
        
        # Define allowed characters
        self.allowed_chars = set('0123456789.+-*/(). ')
        
        # Define maximum expression length to prevent DoS
        self.max_length = 100
        
        # Define maximum number of operations to prevent DoS
        self.max_operations = 10

    def _validate_input(self, expression: str) -> bool:
        """Validate input expression for security."""
        if not expression or len(expression) > self.max_length:
            return False
        
        # Check for allowed characters
        if not set(expression).issubset(self.allowed_chars):
            return False
            
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            return False
            
        return True

    def _tokenize(self, expression: str) -> list:
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
                if char in self.operators or char in '()':
                    tokens.append(char)
                    
        if current:
            tokens.append(current)
            
        return tokens

    def _evaluate(self, tokens: list) -> Decimal:
        """Evaluate tokens using operator precedence."""
        def apply_operator(op: str, b: Decimal, a: Decimal) -> Decimal:
            return self.operators[op](a, b)

        def greater_precedence(op1: str, op2: str) -> bool:
            precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
            return precedence[op1] > precedence[op2]

        def evaluate_expression(tokens: list) -> Decimal:
            stack = []
            operators = set(self.operators.keys()) | {'(', ')'}
            
            for token in tokens:
                if token not in operators and not token.isspace():
                    try:
                        stack.append(Decimal(token))
                    except InvalidOperation:
                        raise ValueError("Invalid number format")
                        
                elif token == '(':
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        a = stack.pop()
                        b = stack.pop()
                        stack.append(apply_operator(stack.pop(), a, b))
                    if stack and stack[-1] == '(':
                        stack.pop()
                    else:
                        raise ValueError("Mismatched parentheses")
                else:
                    while (stack and stack[-1] != '(' and
                           greater_precedence(stack[-1], op)):
                        a = stack.pop()
                        b = stack.pop()
                        stack.append(apply_operator(stack.pop(), a, b))
                    stack.append(token)
                    
            while len(stack) > 1:
                a = stack.pop()
                b = stack.pop()
                stack.append(apply_operator(stack.pop(), a, b))
                
            if len(stack) != 1:
                raise ValueError("Invalid expression")
                
            return stack[0]

        return evaluate_expression(tokens)

    def evaluate(self, expression: str) -> Decimal:
        """Evaluate the given mathematical expression."""
        if not self._validate_input(expression):
            raise ValueError("Invalid input")
            
        tokens = self._tokenize(expression)
        if len(tokens)