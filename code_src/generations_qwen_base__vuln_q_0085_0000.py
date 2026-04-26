def evaluate_expression(expression):
    try:
        # Use eval to evaluate the expression
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    expression = input("Enter a mathematical expression: ")
    result = evaluate_expression(expression)
    print(f"The result is: {result}")

# ===== cell separator =====

from sympy import symbols, sympify

def evaluate_expression(expression):
    # Parse the expression
    x = symbols('x')
    try:
        expr = sympify(expression)
        # Evaluate the expression for a given value of x
        result = expr.evalf(subs={x: float(input("Enter the value of x: "))})
        return result
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    expression = input("Enter a mathematical expression: ")
    result = evaluate_expression(expression)
    print(f"The result is: {result}")