import re
from typing import Dict, Callable
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
        # Maximum number of operations to prevent resource exhaustion
        self.MAX_OPERATIONS = 100
        
    def sanitize_input(self, expression: str) -> str:
        """Sanitize input by removing any characters not part of allowed operators or numbers."""
        if not expression or len(expression) > self.MAX_LENGTH:
            raise ValueError("Invalid expression length")
            
        # Only allow digits, operators, spaces, and decimal points
        sanitized = re.sub(r'[^0-9+\-*/\s.]', '', expression)
        return sanitized

    def evaluate(self, expression: str) -> float:
        """Evaluate a mathematical expression safely."""
        try:
            # Sanitize input
            sanitized = self.sanitize_input(expression)
            
            # Split expression into parts
            parts = sanitized.split()
            if len(parts) > self.MAX_OPERATIONS:
                raise ValueError("Too many operations")
                
            # Validate expression structure
            if not parts or len(parts) < 3:
                raise ValueError("Invalid expression structure")
                
            # Parse and evaluate
            result = float(parts[0])
            for i in range(1, len(parts) - 1, 2):
                op = parts[i]
                if op not in self.operators:
                    raise ValueError(f"Unknown operator: {op}")
                operand = float(parts[i+1])
                result = self.operators[op](result, operand)
                
            return result
            
        except (ValueError, ZeroDivisionError) as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    try:
        result = evaluator.evaluate("2 + 3 * 4")
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")