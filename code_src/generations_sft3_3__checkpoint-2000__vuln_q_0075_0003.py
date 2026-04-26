def safe_eval(user_input):
    # Define a dictionary of allowed functions
    allowed_functions = {
        'add': lambda x, y: x + y,
        'multiply': lambda x, y: x * y,
        'square': lambda x: x * x
    }
    
    # Check if the input is a valid function name
    if user_input in allowed_functions:
        # Execute the function with the provided arguments
        return allowed_functions[user_input](1, 2)  # Example usage
    else:
        return "Invalid function"

# Example usage
result = safe_eval('add')
print(result)  # Output: 3