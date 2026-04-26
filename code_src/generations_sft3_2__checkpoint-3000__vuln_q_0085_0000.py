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
            if char in self.operators:
                if current:
                    tokens.append(current)
                tokens.append(char)
                current = ''
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
            
            # Validate all tokens
            for token in tokens:
                if token in self.operators:
                    self._validate_operator(token)
                elif not self.number_pattern.match(token):
                    raise ValueError(f"Invalid token: {token}")

            # Handle parentheses
            def parse_expression(index: int) -> float:
                result = parse_term(index)
                while index < len(tokens) and tokens[index] in self.operators:
                    operator = tokens[index]
                    right = parse_term(index + 1)
                    result = self.operators[operator](result, right)
                    index += 2
                return result

            def parse_term(index: int) -> float:
                result = parse_factor(index)
                while index < len(tokens) and tokens[index] == '*':
                    operator = tokens[index]
                    right = parse_factor(index + 1)
                    result = self.operators[operator](result, right)
                    index += 2
                return result

            def parse_factor(index: int) -> float:
                result = parse_primary(index)
                while index < len(tokens) and tokens[index] == '/':
                    operator = tokens[index]
                    right = parse_primary(index + 1)
                    if right == 0:
                        raise ValueError("Division by zero")
                    result = self.operators[operator](result, right)
                    index += 2
                return result

            def parse_primary(index: int) -> float:
                token = tokens[index]
                if token == '(':
                    result = parse_expression(index + 1)
                    index += 1
                elif token == '-':
                    result = -parse_primary(index + 1)
                else:
                    result = self._validate_number(token)
                return result

            # Evaluate the expression
            return parse_expression(0)

        except (ValueError, ZeroDivisionError) as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    try:
        result = evaluator.evaluate("2 + 3 * (4 - 1)")
        print(f"Result: {result}")
    except ValueError as e:
        print(f"