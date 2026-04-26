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

def safe_eval(expr):
    """Safely evaluate a mathematical expression using sympy."""
    try:
        # Convert string to sympy expression
        expr = parse_expr(expr, evaluate=False)
        
        # Check if expression contains only allowed symbols
        if not all(symbol in (x, y, z) for symbol in expr.atoms()):
            raise ValueError("Expression contains invalid symbols")
            
        # Evaluate expression with dummy variables
        return expr.evalf(subs={x: 0, y: 0, z: 0})
    except Exception as e:
        return str(e)

def main():
    print("Enter mathematical formulas (e.g., '2*x + 3') or 'quit' to exit.")
    
    while True:
        user_input = input("Enter formula: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        if not validate_input(user_input):
            print("Invalid input. Please use only alphanumeric characters, basic mathematical operators, spaces, and parentheses.")
            continue
        
        try:
            result = safe_eval(user_input)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()