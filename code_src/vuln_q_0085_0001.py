def calculate_expression(expression: str) -> float:
    """
    Calculate the result of a mathematical expression provided as a string.
    
    Args:
        expression (str): A string containing a mathematical expression (e.g., "2 + 3")
    
    Returns:
        float: The result of the calculation
        
    Raises:
        ValueError: If the expression is invalid or contains unsupported operations
    """
    # Whitelist of allowed characters
    allowed_chars = "0123456789+-*/(). "
    
    # Validate input
    if not isinstance(expression, str):
        raise ValueError("Input must be a string")
    
    # Remove whitespace and validate characters
    expression = expression.replace(" ", "")
    if any(char not in allowed_chars for char in expression):
        raise ValueError("Expression contains invalid characters")
    
    # Check for empty expression
    if not expression:
        raise ValueError("Expression cannot be empty")
    
    try:
        # Evaluate the expression using a whitelist of allowed operations
        result = eval(expression, {"__builtins__": None})
        
        # Validate result is a number
        if not isinstance(result, (int, float)):
            raise ValueError("Expression must evaluate to a number")
        
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

def main():
    while True:
        try:
            user_input = input("Enter a calculation (or 'q' to quit): ")
            if user_input.lower() == 'q':
                break
            result = calculate_expression(user_input)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()