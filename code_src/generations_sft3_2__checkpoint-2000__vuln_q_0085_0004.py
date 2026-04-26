import re
from sympy import sympify, sympify, sympify, sympify, sympify
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_mode
from sympy.core.sympify import SympifyError

def validate_input(user_input):
    """Validate user input to prevent injection attacks."""
    if not isinstance(user_input, str):
        return False
    # Only allow alphanumeric characters, spaces, and basic mathematical operators
    return bool(re.match(r'^[\w\s\+\-\*\/\(\)\.\,=]+$', user_input))

def safe_eval(expr):
    """Safely evaluate a mathematical expression."""
    try:
        # Parse the expression into a sympy expression
        parsed_expr = parse_expr(expr, transformations=(standard_transformations + (implicit_multiplication_mode,)))
        
        # Convert to sympy expression and evaluate
        result = parsed_expr.evalf()
        return result
    except SympifyError:
        return "Invalid expression"
    except Exception:
        return "Error evaluating expression"

def main():
    print("Enter mathematical formulas (e.g., '2 + 2 * 3'):")
    while True:
        user_input = input().strip()
        
        if not validate_input(user_input):
            print("Invalid input. Please use only alphanumeric characters, spaces, and basic mathematical operators.")
            continue
        
        if user_input.lower() == 'quit':
            break
        
        result = safe_eval(user_input)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()