```python
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.sympify import SympifyError

def safe_evaluate(formula: str) -> str:
    """
    Safely evaluate a mathematical formula using sympy.
    Returns the result as a string or an error message if evaluation fails.
    """
    try:
        # Parse the formula into a sympy expression
        expr = parse_expr(formula, evaluate=False)
        
        # Safely evaluate the expression
        result = sp.simplify(expr)
        
        # Convert result to string and return
        return str(result)
    except SympifyError:
        return "Error: Invalid formula. Please enter a valid mathematical expression."
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Enter a mathematical formula to evaluate (or 'quit' to exit):")
    while True:
        formula = input("Formula: ").strip()
        if formula.lower() == 'quit':
            break
        result = safe_evaluate(formula)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
```