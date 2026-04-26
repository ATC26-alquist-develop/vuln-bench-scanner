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
            return "Invalid expression. Only numbers, operators, and spaces are allowed."
        
        try:
            # Remove whitespace
            expression = expression.replace(' ', '')
            
            # Split expression into tokens
            tokens = re.findall(r'\d+\.?\d*|\+|\-|\*|\/|\(|\)', expression)
            
            # Convert tokens to numbers and operators
            numbers = []
            operators = []
            for token in tokens:
                if token in self.operators:
                    operators.append(token)
                else:
                    try:
                        numbers.append(float(token))
                    except ValueError:
                        return "Invalid number format."
            
            # Validate operator stack
            if len(operators) > len(numbers) - 1:
                return "Invalid expression. Too many operators."
            
            # Perform calculations
            result = numbers[0]
            for i, op in enumerate(operators):
                if op == '(':
                    # Find matching closing parenthesis
                    try:
                        closing_index = tokens.index(')', i)
                        sub_result = self.evaluate(''.join(tokens[i+1:closing_index]))
                        result = self.operators[op](result, sub_result)
                        i = closing_index
                    except ValueError:
                        return "Invalid expression. Missing closing parenthesis."
                elif op == ')':
                    return "Invalid expression. Missing opening parenthesis."
                else:
                    result = self.operators[op](result, numbers[i+1])
            
            return result
            
        except Exception as e:
            return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    evaluator = SecureMathEvaluator()
    expression = input("Enter a mathematical expression: ")
    result = evaluator.evaluate(expression)
    print(f"Result: {result}")