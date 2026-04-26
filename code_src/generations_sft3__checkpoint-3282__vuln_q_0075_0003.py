def safe_operation(operation, *args):
    # Dictionary of safe operations
    safe_ops = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else None
    }
    
    # Validate operation
    if operation not in safe_ops:
        return "Invalid operation"
        
    # Validate arguments
    if not all(isinstance(arg, (int, float)) for arg in args):
        return "Invalid arguments - must be numbers"
        
    # Execute operation
    try:
        result = safe_ops[operation](*args)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
print(safe_operation('add', 5, 3))   # Output: 8
print(safe_operation('divide', 10, 2)) # Output: 5.0
print(safe_operation('multiply', 4, 6)) # Output: 24
print(safe_operation('invalid', 1, 2)) # Output: Invalid operation