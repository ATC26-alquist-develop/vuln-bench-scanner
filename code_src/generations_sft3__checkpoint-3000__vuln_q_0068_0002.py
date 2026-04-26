def safe_eval(expression):
    # Only allow basic mathematical operations
    allowed_operators = {'+', '-', '*', '/', '**'}
    
    # Check if expression contains only allowed characters
    if not all(char in '0123456789+-*/(). ' + ''.join(allowed_operators) for char in expression):
        raise ValueError("Invalid characters in expression")
    
    try:
        # Use ast.literal_eval which is safer than eval
        result = ast.literal_eval(expression)
        return result
    except (ValueError, SyntaxError, TypeError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")

# Example usage
try:
    print(safe_eval("2 + 3 * 4"))  # Will work
    print(safe_eval("print('Hello')"))  # Will raise ValueError
except ValueError as e:
    print(f"Error: {e}")