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
        
        # Regex pattern for validating expressions
        self.pattern = re.compile(r'^[\d\s+\-*/().]+$')
        
        # Maximum expression length to prevent DoS
        self.MAX_LENGTH = 100
        
        # Maximum number of operations to prevent resource exhaustion
        self.MAX_OPERATIONS = 1000

    def evaluate(self, expression: str) -> float:
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression: A string containing a mathematical expression
            
        Returns:
            float: Result of the evaluation
            
        Raises:
            ValueError: If the expression is invalid or contains disallowed characters
        """
        # Validate input
        if not isinstance(expression, str):
            raise ValueError("Input must be a string")
            
        if len(expression) > self.MAX_LENGTH:
            raise ValueError(f"Expression too long (max {self.MAX_LENGTH} characters)")
            
        # Check for disallowed characters
        if not self.pattern.match(expression):
            raise ValueError("Invalid characters in expression")
            
        # Split expression into parts
        parts = re.findall(r'\d+|\+|\-|\*|/|\(|\)', expression)
        
        # Validate number of operations
        if len(parts) > self.MAX_OPERATIONS:
            raise ValueError(f"Too many operations (max {self.MAX_OPERATIONS})")
            
        # Evaluate expression using shunting yard algorithm
        output_queue = []
        operator_stack = []
        
        for token in parts:
            if token.isdigit():
                output_queue.append(float(token))
            elif token in self.operators:
                while (operator_stack and 
                       self.operators[operator_stack[-1]] precedence(token)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise ValueError("Mismatched parentheses")
                    
        # Process any remaining operators
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
            
        # Evaluate result
        result = output_queue[0]
        for i in range(1, len(output_queue), 2):
            result = self.operators[parts[i+1]](result, output_queue[i])
            
        return result

    def precedence(self, op1: str, op2: str) -> bool:
        """
        Compare operator precedence.
        
        Args:
            op1: First operator
            op2: Second operator
            
        Returns:
            bool: True if op1 has higher or equal precedence than op2
        """
        if op1 == '(' or op2 == '(':
            return False
        if op1 == ')':
            return True
        if op2 == ')':
            return False
        return self.operators[op1].__name__ >= self.operators[op2].__name__

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    try:
        result = evaluator.evaluate("3 + 5 * 2")
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")