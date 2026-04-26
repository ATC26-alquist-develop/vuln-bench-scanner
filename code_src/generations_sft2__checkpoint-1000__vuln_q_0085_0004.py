import sympy as sp

def compute_formula(formula):
    """
    Computes the result of a mathematical formula provided by the user.
    
    Args:
        formula (str): A string containing a mathematical formula with variables x and y.
    
    Returns:
        str: The result of the formula evaluation.
    """
    try:
        # Convert formula to sympy expression
        expr = sp.sympify(formula)
        
        # Define variables
        x, y = sp.symbols('x y')
        
        # Evaluate expression
        result = expr.subs({x: 1, y: 1})
        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """
    Main function to handle user input and display results.
    """
    print("Enter a formula with variables x and y (e.g., 'x + y'):")
    formula = input()
    result = compute_formula(formula)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()