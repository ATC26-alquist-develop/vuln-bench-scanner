import re
import operator
from typing import Dict, Callable

# Define supported operators and their corresponding functions
operators: Dict[str, Callable] = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

def is_safe_expression(expression: str) -> bool:
    """Validate the expression for safety."""
    # Only allow digits, operators, and spaces
    return bool(re.match(r'^[\d\s+\-*/().]+$', expression))

def evaluate_expression(expression: str) -> float:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: A string containing the mathematical expression to evaluate
        
    Returns:
        The result of the evaluation as a float
        
    Raises:
        ValueError: If the expression is invalid or contains unsafe characters
    """
    if not is_safe_expression(expression):
        raise ValueError("Invalid expression. Only digits, operators, and spaces are allowed.")
    
    # Tokenize the expression
    tokens = re.findall(r'\d+|\+|\-|\*|\/|\(|\)', expression)
    
    # Convert tokens to numbers and operators
    try:
        numbers = [float(token) for token in tokens if token.replace('.', '', 1).isdigit()]
        ops = [token for token in tokens if token in operators]
    except ValueError:
        raise ValueError("Invalid expression. Only numbers and operators are allowed.")
    
    # Shunting Yard algorithm for operator precedence
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output_queue = []
    operator_stack = []
    
    for token in tokens:
        if token.replace('.', '', 1).isdigit():
            output_queue.append(token)
        elif token in operators:
            while (operator_stack and operator_stack[-1] in operators and
                   precedence[operator_stack[-1]] >= precedence[token]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
    
    while operator_stack:
        output_queue.append(operator_stack.pop())
    
    # Evaluate the postfix expression
    stack = []
    for token in output_queue:
        if token.replace('.', '', 1).isdigit():
            stack.append(float(token))
        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            b, a = stack.pop(), stack.pop()
            try:
                result = operators[token](a, b)
            except ZeroDivisionError:
                raise ValueError("Division by zero is not allowed")
            stack.append(result)
    
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    
    return stack[0]

def main():
    while True:
        user_input = input("Enter a mathematical expression (or 'quit' to exit): ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        try:
            result = evaluate_expression(user_input)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()