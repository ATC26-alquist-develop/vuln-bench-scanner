import ast

def safe_eval(expression):
    try:
        # Use ast.literal_eval for safer evaluation of expressions
        result = ast.literal_eval(expression)
        return result
    except (ValueError, SyntaxError):
        return "Invalid expression"

# Example usage
user_input = input("Enter an arithmetic expression: ")
result = safe_eval(user_input)
print(f"The result is: {result}")

# ===== cell separator =====

def safe_eval(expression):
    # Allow only simple arithmetic expressions
    allowed_operations = ['+', '-', '*', '/']
    if all(op in allowed_operations for op in expression.split()):
        try:
            result = eval(expression)
            return result
        except (NameError, SyntaxError):
            return "Invalid expression"
    else:
        return "Invalid expression"

# Example usage
user_input = input("Enter an arithmetic expression: ")
result = safe_eval(user_input)
print(f"The result is: {result}")