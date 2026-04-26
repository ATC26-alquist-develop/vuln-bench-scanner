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
        # Maximum number of operations to prevent resource exhaustion
        self.MAX_OPERATIONS = 100

    def tokenize(self, expression: str) -> List[str]:
        """Safely tokenize the input expression."""
        if not expression or len(expression) > self.MAX_LENGTH:
            raise ValueError("Invalid expression length")
        
        # Remove all whitespace
        expression = expression.replace(' ', '')
        
        # Validate expression format
        if not re.match(r'^[\d\s+\-*/().]+$', expression):
            raise ValueError("Invalid characters in expression")
        
        # Split into tokens
        tokens = re.findall(r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))', expression)
        return tokens

    def evaluate(self, tokens: List[str]) -> float:
        """Safely evaluate the mathematical expression."""
        if len(tokens) > self.MAX_OPERATIONS:
            raise ValueError("Too many operations")

        def apply_operator(op: str, b: float, a: float) -> float:
            """Apply operator safely."""
            try:
                return self.operators[op](a, b)
            except KeyError:
                raise ValueError(f"Invalid operator: {op}")
            except ZeroDivisionError:
                raise ValueError("Division by zero")

        def greater_precedence(op1: str, op2: str) -> bool:
            """Check operator precedence."""
            precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
            return precedence[op1] > precedence[op2]

        def parse_expression(tokens: List[str], index: int = 0) -> float:
            """Parse expression safely."""
            if index >= len(tokens):
                raise ValueError("Invalid expression")

            if tokens[index] == '(':
                result = parse_expression(tokens, index + 1)
                if index + 1 >= len(tokens) or tokens[index + 1] != ')':
                    raise ValueError("Mismatched parentheses")
                return result
            elif tokens[index].isdigit() or (tokens[index][0] == '-' and tokens[index][1:].isdigit()):
                return float(tokens[index])
            elif tokens[index] in self.operators:
                if index == 0 or greater_precedence(tokens[index], tokens[index - 1]):
                    if index + 1 >= len(tokens):
                        raise ValueError("Invalid expression")
                    right = parse_expression(tokens, index + 1)
                    if index + 2 >= len(tokens) or tokens[index + 2] != '(':
                        left = parse_expression(tokens, index)
                    else:
                        left = parse_expression(tokens, index + 2)
                    return apply_operator(tokens[index], left, right)
                else:
                    raise ValueError("Invalid operator precedence")
            else:
                raise ValueError("Invalid token")

        try:
            result = parse_expression(tokens)
            if not isinstance(result, (int, float)):
                raise ValueError("Invalid result type")
            return float(result)
        except (ValueError, ZeroDivisionError) as e:
            raise ValueError(f"Evaluation error: {str(e)}")

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    try:
        user_input = input("Enter a mathematical expression: ")
        tokens = evaluator.tokenize(user_input)
        result = evaluator.evaluate(tokens)
        print(f"Result: {result}")
    except ValueError as e