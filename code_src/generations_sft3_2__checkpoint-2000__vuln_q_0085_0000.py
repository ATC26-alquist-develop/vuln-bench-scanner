```python
import re
from typing import Dict, List
import operator
from decimal import Decimal, InvalidOperation

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
        # Maximum number of operations to prevent DoS
        self.MAX_OPERATIONS = 10

    def _validate_input(self, expression: str) -> bool:
        """Validate input expression for security."""
        if not expression or len(expression) > self.MAX_LENGTH:
            return False
        
        # Only allow digits, operators, spaces, decimal points, and parentheses
        if not re.match(r'^[\d\s\+\-\*\/\.()]+$', expression):
            return False
        
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            return False
        
        return True

    def _tokenize(self, expression: str) -> List[str]:
        """Convert expression to tokens."""
        tokens = []
        current = ''
        
        for char in expression:
            if char in self.operators or char in '()':
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append(char)
            else:
                current += char
        
        if current:
            tokens.append(current)
        
        return tokens

    def _evaluate(self, tokens: List[str]) -> Decimal:
        """Evaluate tokens using operator precedence."""
        def apply_operator(operators: List[str], values: List[Decimal]) -> Decimal:
            op = operators.pop()
            right = values.pop()
            left = values.pop()
            values.append(self.operators[op](left, right))
            operators.append(op)
            return values[-1]

        def parse_expression(tokens: List[str], values: List[Decimal], operators: List[str]) -> Decimal:
            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token in self.operators:
                    while operators and operators[-1] != '(' and self.operators[token] >= self.operators[operators[-1]]:
                        apply_operator(operators, values)
                    operators.append(token)
                elif token == '(':
                    j = i + 1
                    depth = 1
                    while depth > 0:
                        i += 1
                        if tokens[i] == '(':
                            depth += 1
                        elif tokens[i] == ')':
                            depth -= 1
                    values.append(parse_expression(tokens[i+1:], [], operators))
                    i = i + 1
                elif token == ')':
                    raise ValueError("Mismatched parentheses")
                else:
                    values.append(Decimal(token))
                i += 1
            
            while len(operators) > 1:
                apply_operator(operators, values)
            
            return values[0]

        tokens = [t if t in self.operators or t == '(' or t == ')' else f"Decimal('{t}')" for t in tokens]
        values = []
        operators = []
        
        try:
            result = parse_expression(tokens, values, operators)
            return result.quantize(Decimal('0.0001'))
        except (ValueError, InvalidOperation) as e:
            raise ValueError(f"Invalid expression: {str(e)}")

    def evaluate(self, expression: str) -> Decimal:
        """Evaluate a mathematical expression."""
        if not self._validate_input(expression):
            raise ValueError("Invalid input")
        
        tokens = self._tokenize(expression)
        if len(tokens) > self.MAX_OPERATIONS:
            raise ValueError("Expression too complex")
        
        return self._evaluate(tokens)

# Example usage
if __name__ == "__main__":