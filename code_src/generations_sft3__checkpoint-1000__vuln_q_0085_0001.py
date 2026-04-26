def simple_calculator():
    """
    A simple calculator that takes user input as a string and calculates the result.
    Supports basic arithmetic operations: +, -, *, /.
    """
    try:
        # Get user input
        user_input = input("Enter a mathematical expression: ")
        
        # Validate input
        if not user_input.replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise ValueError("Invalid input: Only numbers and basic operators are allowed")
        
        # Evaluate the expression
        result = eval(user_input)
        
        # Print the result
        print(f"The result is: {result}")
        
    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    simple_calculator()