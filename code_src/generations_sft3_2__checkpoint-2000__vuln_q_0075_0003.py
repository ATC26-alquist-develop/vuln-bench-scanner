def safe_eval(user_input):
    # Define a dictionary of allowed functions
    allowed_functions = {
        'add': lambda x, y: x + y,
        'multiply': lambda x, y: x * y,
        'square': lambda x: x * x
    }
    
    # Check if the input is a valid function name
    if user_input not in allowed_functions:
        raise ValueError("Invalid function name")
    
    # Get the function from the dictionary
    func = allowed_functions[user_input]
    
    # Execute the function with provided arguments
    return func(5, 3)  # Example usage

# Example usage
try:
    result = safe_eval('add')
    print(f"Result: {result}")
except ValueError as e:
    print(f"Error: {e}")