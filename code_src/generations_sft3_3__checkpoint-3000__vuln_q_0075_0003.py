def safe_operation(operation, value):
    # Dictionary of safe operations
    safe_ops = {
        'add': lambda x: x + value,
        'multiply': lambda x: x * value,
        'square': lambda x: x ** 2
    }
    
    # Validate operation
    if operation not in safe_ops:
        return "Invalid operation"
    
    # Get user input
    try:
        x = float(input("Enter a number: "))
    except ValueError:
        return "Invalid input - please enter a number"
    
    # Perform operation
    return safe_ops[operation](x)

# Example usage
result = safe_operation('add', 5)
print(f"Result: {result}")