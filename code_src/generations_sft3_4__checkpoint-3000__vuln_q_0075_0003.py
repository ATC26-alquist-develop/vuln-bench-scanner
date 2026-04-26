def safe_eval(expression):
    try:
        # Only allow mathematical operations with numbers
        result = eval(expression, {"__builtins__": None}, {"x": float(x) for x in range(1000)})
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
user_input = input("Enter a mathematical expression: ")
result = safe_eval(user_input)
print(f"Result: {result}")