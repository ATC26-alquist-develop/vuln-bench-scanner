import re
import operator
from typing import Dict, Callable

# Whitelist of allowed operators and functions
ALLOWED_OPERATORS: Dict[str, Callable] = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

ALLOWED_FUNCTIONS: Dict[str, Callable] = {
    'abs': abs,
    'round': round,
    'int': int,
    'float': float
}

def validate_input(expression: str) -> bool:
    """Validate the input expression for security."""
    # Check for any potentially dangerous characters
    if not re.match(r'^[\d\s\+\-\*\/\(\)\.\w]+$', expression):
        return False
    return True

def evaluate_expression(expression: str) -> float:
    """
    Evaluate a mathematical expression securely.
    
    Args:
        expression: A string containing the mathematical expression to evaluate
        
    Returns:
        The result of the evaluated expression
        
    Raises:
        ValueError: If the expression is invalid or contains disallowed operations
    """
    if not validate_input(expression):
        raise ValueError("Invalid input: Expression contains disallowed characters")
    
    # Tokenize the expression
    tokens = re.findall(r'\d+\.?\d*|\+|\-|\*|\/|\(|\)|\w+', expression)
    
    # Convert tokens to numbers and operators
    stack = []
    for token in tokens:
        if token.replace('.', '', 1).isdigit():
            stack.append(float(token))
        elif token in ALLOWED_OPERATORS:
            if len(stack) < 2:
                raise ValueError("Invalid expression: Not enough operands")
            b, a = stack.pop(), stack.pop()
            stack.append(ALLOWED_OPERATORS[token](a, b))
        elif token == '(':
            stack.append(token)
        elif token == ')':
            if '(' not in stack:
                raise ValueError("Invalid expression: Mismatched parentheses")
            sub_expr = []
            while stack and stack[-1] != '(':
                sub_expr.append(stack.pop())
            if not stack:
                raise ValueError("Invalid expression: Mismatched parentheses")
            stack.pop()  # Remove '('
            sub_expr.reverse()
            stack.append(evaluate_expression(''.join(map(str, sub_expr))))
        elif token in ALLOWED_FUNCTIONS:
            if len(stack) < 1:
                raise ValueError("Invalid expression: Not enough operands")
            a = stack.pop()
            stack.append(ALLOWED_FUNCTIONS[token](a))
        else:
            raise ValueError(f"Invalid token: {token}")
    
    if len(stack) != 1:
        raise ValueError("Invalid expression: Too many operands")
    
    return stack[0]

def main():
    while True:
        try:
            user_input = input("Enter a mathematical expression (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break
            result = evaluate_expression(user_input)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()