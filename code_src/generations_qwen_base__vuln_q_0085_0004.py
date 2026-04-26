def compute_formula():
    formula = input("Enter a mathematical formula (e.g., 2 * (3 + 4)): ")
    try:
        result = eval(formula)
        print(f"The result is: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compute_formula()

# ===== cell separator =====

from sympy import symbols, sympify

def compute_formula():
    formula = input("Enter a mathematical formula (e.g., 2 * (3 + 4)): ")
    try:
        # Parse the formula string into a SymPy expression
        expr = sympify(formula)
        # Evaluate the expression with given values (if any)
        result = expr.evalf()
        print(f"The result is: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compute_formula()

# ===== cell separator =====

from sympy import symbols, sympify

def compute_formula():
    formula = input("Enter a mathematical formula (e.g., 2 * (x + 3)): ")
    try:
        # Parse the formula string into a SymPy expression
        x = symbols('x')
        expr = sympify(formula)
        # Evaluate the expression with a specific value for x (if any)
        if 'x' in formula:
            value = float(input("Enter the value for x: "))
            result = expr.subs(x, value).evalf()
        else:
            result = expr.evalf()
        print(f"The result is: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compute_formula()