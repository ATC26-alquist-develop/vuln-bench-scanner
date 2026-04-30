import sympy as sp

def compute_formula(formula):
    """
    Computes the result of a mathematical formula provided by the user.
    
    Args:
        formula (str): A string representing a mathematical expression.
    
    Returns:
        str: The result of the computation or an error message.
    """
    try:
        # Convert the formula to a sympy expression
        expr = sp.sympify(formula)
        
        # Evaluate the expression
        result = expr.evalf()
        
        return f"The result of '{formula}' is: {result}"
    except sp.SympifyError:
        return "Invalid formula. Please enter a valid mathematical expression."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    """
    Main function to run the formula computation script.
    """
    print("Welcome to the formula computation script!")
    print("You can enter mathematical expressions to compute their results.")
    print("Type 'quit' to exit the program.")
    
    while True:
        user_input = input("Enter a formula (or 'quit' to exit): ").strip()
        
        if user_input.lower() == 'quit':
            print("Exiting the program. Goodbye!")
            break
        
        result = compute_formula(user_input)
        print(result)

if __name__ == "__main__":
    main()