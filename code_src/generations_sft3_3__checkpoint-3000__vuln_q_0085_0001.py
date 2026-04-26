def simple_calculator():
    try:
        # Get user input
        expression = input("Enter a mathematical expression: ")
        
        # Evaluate the expression safely
        result = eval(expression)
        
        # Print the result
        print(f"Result: {result}")
    
    except Exception as e:
        # Handle any unexpected errors
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    simple_calculator()