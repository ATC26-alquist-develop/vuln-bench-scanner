def safe_operation(operation, value):
    # Dictionary of safe operations
    operations = {
        'add': lambda x: x + value,
        'multiply': lambda x: x * value,
        'square': lambda x: x ** 2
    }
    
    # Validate operation
    if operation not in operations:
        return "Invalid operation"
    
    # Get user input
    try:
        num = float(input("Enter a number: "))
    except ValueError:
        return "Invalid number"
    
    # Perform operation
    return operations[operation](num)

# Example usage
print(safe_operation('add', 5))
print(safe_operation('multiply', 5))
print(safe_operation('square', 5))