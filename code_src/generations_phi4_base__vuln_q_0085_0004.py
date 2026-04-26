import sympy as sp

def compute_formula(formula):
    # Define the symbols used in the formula
    symbols = sp.symbols('x y z a b c d e f g h i j k l m n o p q r s t u v w x y z')
    
    # Parse the formula
    try:
        result = sp.sympify(formula)
        return result
    except sp.SympifyError:
        return "Invalid formula. Please try again."

def main():
    print("Welcome to the Formula Calculator!")
    print("You can input formulas using the following symbols: x, y, z, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z.")
    
    while True:
        formula = input("Enter a formula (or type 'exit' to quit): ")
        if formula.lower() == 'exit':
            break
        result = compute_formula(formula)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()