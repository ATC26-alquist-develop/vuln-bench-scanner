import re
from typing import Dict, Callable
import operator

class SecureMathEvaluator:
    def __init__(self):
        # Define allowed operators and their corresponding functions
        self.operators: Dict[str, Callable] = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
        }
        
        # Regex for validating numbers and operators
        self.number_pattern = re.compile(r'^-?\d+(\.\d+)?$')
        self.operator_pattern = re.compile(r'^[-+*/]$')

    def validate_input(self, expression: str) -> bool:
        """Validate the input expression."""
        if not expression or len(expression) > 100:  # Reasonable length limit
            return False
        
        # Split expression into parts
        parts = expression.split()
        
        # Check for operator usage
        if len(parts) < 3:
            return False
        
        # Validate each part
        for part in parts:
            if not self.number_pattern.match(part) and not self.operator_pattern.match(part):
                return False
            if not part.strip():  # Allow spaces but not empty parts
                return False
        
        return True

    def evaluate(self, expression: str) -> float:
        """Evaluate the mathematical expression securely."""
        if not self.validate_input(expression):
            raise ValueError("Invalid input format")

        # Split expression into parts
        parts = expression.split()
        
        # Convert to postfix notation
        postfix = self.infix_to_postfix(parts)
        
        # Evaluate postfix expression
        stack = []
        for token in postfix:
            if self.number_pattern.match(token):
                stack.append(float(token))
            else:
                if token not in self.operators:
                    raise ValueError(f"Unknown operator: {token}")
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = self.operators[token](operand1, operand2)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        
        return stack[0]

    def infix_to_postfix(self, infix: list) -> list:
        """Convert infix notation to postfix notation."""
        output = []
        operators = []
        
        for token in infix:
            if self.number_pattern.match(token):
                output.append(token)
            elif token in self.operators:
                while operators and operators[-1] != '(' and \
                      (self.operators[operators[-1]] precedence(token)):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if operators and operators[-1] == '(':
                    operators.pop()
                else:
                    raise ValueError("Mismatched parentheses")
        
        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operators.pop())
        
        return output

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    try:
        result = evaluator.evaluate("2 + 3 * 4")
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")