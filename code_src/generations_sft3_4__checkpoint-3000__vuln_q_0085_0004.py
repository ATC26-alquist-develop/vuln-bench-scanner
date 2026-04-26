import re
from sympy import sympify, sympify, sympify, sympify, sympify
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import x, y, z

def validate_input(user_input):
    """Validate user input to ensure it only contains allowed characters."""
    if not isinstance(user_input, str):
        return False
    # Only allow alphanumeric characters, basic mathematical operators, spaces, and parentheses
    return bool(re.match(r'^[\w\s\+\-\*\/\(\)\.\,]*$', user_input))

def calculate_expression(user_input):
    """Calculate the result of a mathematical expression entered by the user."""
    if not validate_input(user_input):
        return "Invalid input. Please use only numbers, letters, spaces, and basic mathematical operators."
    
    try:
        # Use sympy to parse and evaluate the expression
        expr = parse_expr(user_input)
        result = expr.evalf()
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Enter a mathematical expression (e.g., '2 + 2 * 3'):")
    user_input = input().strip()
    
    if not user_input:
        print("No input provided.")
        return
    
    result = calculate_expression(user_input)
    print(result)

if __name__ == "__main__":
    main()