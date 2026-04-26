import re
from sympy import sympify, sympify, sympify, sympify, sympify
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_mode
from sympy.core.sympify import SympifyError

def safe_eval_formula(formula):
    """
    Safely evaluate a mathematical formula string.
    
    Args:
        formula (str): The mathematical formula to evaluate
        
    Returns:
        float: The result of the evaluation
        
    Raises:
        ValueError: If the formula is invalid or contains dangerous operations
    """
    # Remove all whitespace
    formula = ''.join(formula.split())
    
    # Check for dangerous operations
    dangerous_ops = ['eval', 'exec', 'import', 'open', 'eval', 'compile', '__']
    if any(op in formula for op in dangerous_ops):
        raise ValueError("Dangerous operations are not allowed")
        
    # Parse the formula
    try:
        expr = parse_expr(formula, transformations=(standard_transformations + (implicit_multiplication_mode,)))
    except SympifyError:
        raise ValueError("Invalid mathematical formula")
        
    # Evaluate the expression
    try:
        result = float(expr.evalf())
    except (TypeError, ValueError):
        raise ValueError("Unable to evaluate the formula")
        
    return result

def main():
    print("Enter mathematical formulas (type 'exit' to quit)")
    
    while True:
        try:
            formula = input("Enter formula: ")
            if formula.lower() == 'exit':
                break
                
            result = safe_eval_formula(formula)
            print(f"Result: {result}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print("An unexpected error occurred")
            
if __name__ == "__main__":
    main()