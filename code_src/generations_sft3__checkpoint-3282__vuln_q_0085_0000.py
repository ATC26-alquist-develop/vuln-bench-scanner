import re
from typing import Dict, Callable
from decimal import Decimal, InvalidOperation

class SecureMathEvaluator:
    def __init__(self):
        # Define allowed operators and their corresponding functions
        self.operators: Dict[str, Callable[[Decimal, Decimal], Decimal]] = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else Decimal('inf')
        }
        
        # Regex pattern for validating expressions
        self.pattern = re.compile(r'^[\d\s+\-*/().]+$')
        
        # Maximum expression length to prevent DoS
        self.MAX_LENGTH = 100
        
        # Maximum number of operations to prevent resource exhaustion
        self.MAX_OPERATIONS = 100
        
    def _validate_input(self, expression: str) -> bool:
        """Validate expression input."""
        if not expression or len(expression) > self.MAX_LENGTH:
            return False
        if not self.pattern.fullmatch(expression):
            return False
        return True
    
    def _tokenize(self, expression: str) -> list:
        """Convert expression to tokens."""
        tokens = []
        current = ''
        
        for char in expression:
            if char.isspace():
                if current:
                    tokens.append(current)
                    current = ''
            elif char in self.operators.keys():
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append(char)
            else:
                current += char
                
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
            
        stack = []
        operators = set(self.operators.keys())
        
        for token in tokens:
            if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                stack.append(Decimal(token))
            elif token in operators:
                while stack and stack[-1] in operators and greater_precedence(stack[-1], token):
                    stack.append(apply_operator(stack.pop(), stack.pop(), stack.pop() if stack else Decimal('0')))
                stack.append(token)
            else:
                raise ValueError(f"Invalid token: {token}")
                
        while stack:
            token = stack.pop()
            if token not in operators:
                raise ValueError(f"Invalid expression: {expression}")
                
        result = stack[0]
        while stack:
            result = stack.pop() if stack[-1] in operators else result
            if not stack:
                break
            result = apply_operator(stack.pop(), result, stack.pop() if stack else Decimal('0'))
            
        return result
    
    def evaluate(self, expression: str) -> Decimal:
        """Evaluate the given mathematical expression."""
        if not self._validate_input(expression):
            raise ValueError("Invalid input expression")
            
        tokens = self._tokenize(expression)
        if len(tokens) > self.MAX_OPERATIONS:
            raise ValueError("Expression too complex")
            
        try:
            return self._evaluate(tokens)
        except (InvalidOperation, ValueError) as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")