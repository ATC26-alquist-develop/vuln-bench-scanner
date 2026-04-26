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

    def validate_input(self, expression: str) -> bool:
        """Validate the input expression."""
        if not expression or len(expression) > 100:  # Limit input length
            return False
        
        # Split expression into parts
        parts = expression.split()
        
        # Check for valid operators
        for part in parts:
            if not self.operator_pattern.match(part):
                return False
                
        # Check for valid numbers
        for part in parts:
            if not self.number_pattern.match(part):
                return False
                
        return True

    def evaluate(self, expression: str) -> float:
        """Evaluate the mathematical expression safely."""
        if not self.validate_input(expression):
            raise ValueError("Invalid input format")

        # Replace spaces with empty strings
        expression = expression.replace(' ', '')
        
        # Split expression into parts
        parts = expression.split()
        
        # Convert to postfix notation
        postfix = self.infix_to_postfix(parts)
        
        # Evaluate postfix expression
        return self.evaluate_postfix(postfix)

    def infix_to_postfix(self, infix: list) -> list:
        """Convert infix notation to postfix notation."""
        output = []
        operators = []
        
        for token in infix:
            if self.number_pattern.match(token):
                output.append(token)
            elif token in self.operators:
                while operators and operators[-1] != '(' and \
                      self.operators[operators[-1]] >= self.operators[token]:
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if not operators or operators[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                operators.pop()
                
        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operators.pop())
            
        return output

    def evaluate_postfix(self, postfix: list) -> float:
        """Evaluate postfix notation."""
        stack = []
        
        for token in postfix:
            if self.number_pattern.match(token):
                stack.append(float(token))
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                b, a = stack.pop(), stack.pop()
                result = self.operators[token](a, b)
                stack.append(result)
                
        if len(stack) != 1:
            raise ValueError("Invalid expression")
            
        return stack[0]

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    try:
        result = evaluator.evaluate("5 + 3 * 2 / 4")
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")