import re
from sympy import sympify, sympify, sympify, sympify, sympify
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.sympify import SympifyError

def safe_eval_formula(formula):
    """
    Safely evaluate a mathematical formula string.
    
    Args:
        formula (str): The mathematical formula to evaluate
        
    Returns:
        float: The result of the evaluation
        
    Raises:
        ValueError: If the formula is invalid or contains unsupported operations
    """
    # Remove all whitespace from the formula
    formula = ''.join(formula.split())
    
    # Check if the formula is a valid expression
    try:
        expr = parse_expr(formula)
    except SympifyError:
        raise ValueError("Invalid formula format")
    
    # Check for unsupported operations
    if not re.match(r'^[\d\s\+\-\*\/\(\)\.\,]+$', str(expr)):
        raise ValueError("Unsupported operation in formula")
    
    # Evaluate the expression
    result = float(expr.evalf(subs={}))
    
    return result

def main():
    print("Enter mathematical formulas (press Enter twice to submit)")
    print("Examples: 2+2, sin(pi), (2+2)*3")
    
    while True:
        try:
            formula = input()
            if not formula.strip():
                continue
                
            result = safe_eval_formula(formula)
            print(f"Result: {result}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print("An unexpected error occurred")
        finally:
            print()

if __name__ == "__main__":
    main()