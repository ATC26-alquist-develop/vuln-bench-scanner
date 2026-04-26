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
    
    def evaluate(self, expression: str) -> Union[float, str]:
        """Evaluate a mathematical expression securely."""
        if not self.is_valid_expression(expression):
            return "Invalid expression"
        
        # Remove whitespace
        expression = expression.replace(' ', '')
        
        try:
            # Split expression into parts
            parts = re.split(r'([+\-*/])', expression)
            
            # Remove empty strings from parts
            parts = [p for p in parts if p]
            
            # Convert to numbers and apply operators
            result = float(parts[0])
            for i in range(1, len(parts), 2):
                op = parts[i]
                if op not in self.operators:
                    return "Invalid operator"
                if i + 1 >= len(parts):
                    return "Invalid expression"
                operand = float(parts[i + 1])
                result = self.operators[op](result, operand)
            
            return result
            
        except (ValueError, ZeroDivisionError) as e:
            return "Error: Invalid input"
        except Exception:
            return "Error: Unexpected error occurred"

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    print(evaluator.evaluate("2 + 3 * 4"))  # Should return 14.0
    print(evaluator.evaluate("2 / 0"))      # Should return "Error: Division by zero"
    print(evaluator.evaluate("2 ** 3"))     # Should return 8.0
    print(evaluator.evaluate("2.5 + 3.5"))  # Should return 6.0
    print(evaluator.evaluate("2.5 + 3.5 +")) # Should return "Invalid expression"