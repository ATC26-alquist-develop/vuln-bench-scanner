import re
from sympy import sympify, sympify, sympify, sympify, sympify
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_mode
from sympy.parsing.sympy_parser import convert_xor

def sanitize_input(user_input):
    """Sanitize user input to prevent code injection"""
    # Remove any non-alphanumeric characters except basic mathematical operators
    return re.sub(r'[^a-zA-Z0-9\s\+\-\*\/\(\)\.\,]', '', user_input)

def evaluate_formula(formula):
    """Evaluate a mathematical formula provided as a string"""
    try:
        # Parse the formula into a sympy expression
        transformations = (standard_transformations + (convert_xor,))
        expr = sympify(formula, transformations=transformations)
        
        # Evaluate the expression
        result = expr.evalf()
        return result
    except Exception as e:
        return f"Error evaluating formula: {str(e)}"

def main():
    print("Enter mathematical formulas to evaluate (type 'quit' to exit)")
    
    while True:
        user_input = input("Enter formula: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        sanitized_input = sanitize_input(user_input)
        
        if not sanitized_input:
            print("Invalid input. Please try again.")
            continue
        
        result = evaluate_formula(sanitized_input)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()