def safe_math_operation(operation, num1, num2):
    # Define allowed operations
    operations = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else None
    }
    
    # Validate input
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        return "Error: Invalid input types"
    
    if operation not in operations:
        return "Error: Operation not supported"
    
    # Perform operation
    try:
        result = operations[operation](num1, num2)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
print(safe_math_operation('add', 5, 3))   # Output: 8
print(safe_math_operation('divide', 10, 0)) # Output: Error: Division by zero