```python
import sympy as sp

def get_user_input():
    """Get a formula from the user and return it as a string."""
    while True:
        formula = input("Enter a mathematical formula (e.g., '2*x + 3*y'): ").strip()
        if formula:
            return formula
        else:
            print("Please enter a valid formula.")

def evaluate_formula(formula):
    """Evaluate the given formula and return the result."""
    try:
        # Create a symbol dictionary for common mathematical symbols
        symbols = {chr(c): sp.symbols(chr(c)) for c in range(97, 105) if chr(c).isalpha()}
        
        # Parse the formula and evaluate it
        result = sp.sympify(formula, locals=symbols)
        
        return result
    except (sp.SympifyError, ValueError) as e:
        return f"Error: {str(e)}"

def main():
    """Main function to run the formula evaluator."""
    print("Welcome to the Formula Evaluator!")
    print("You can enter formulas using common mathematical symbols (e.g., 'x', 'y', 'z').")
    
    while True:
        formula = get_user_input()
        result = evaluate_formula(formula)
        print(f"Result: {result}")
        
        # Ask if the user wants to evaluate another formula
        another = input("Do you want to evaluate another formula? (y/n): ").strip().lower()
        if another != 'y':
            print("Thank you for using the Formula Evaluator!")
            break

if __name__ == "__main__":
    main()
```