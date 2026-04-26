def calculate_expression(expression):
    # Split the expression by spaces to handle multi-digit numbers and multiple operations
    tokens = expression.split()
    
    # Initialize the result with the first number
    result = float(tokens[0])
    
    # Initialize an index to keep track of the current token
    i = 1
    
    # Iterate through the tokens starting from the second token
    while i < len(tokens):
        # Get the current operator
        operator = tokens[i]
        
        # Get the next number
        next_number = float(tokens[i + 1])
        
        # Perform the operation based on the operator
        if operator == '+':
            result += next_number
        elif operator == '-':
            result -= next_number
        elif operator == '*':
            result *= next_number
        elif operator == '/':
            # Check for division by zero
            if next_number == 0:
                return "Error: Division by zero"
            result /= next_number
        else:
            return "Error: Unsupported operator"
        
        # Move to the next token
        i += 2
    
    return result

# Main program
if __name__ == "__main__":
    # Take input from the user
    user_input = input("Enter a mathematical expression (e.g., '3 + 5'): ")
    
    # Calculate the result
    result = calculate_expression(user_input)
    
    # Print the result
    print("Result:", result)