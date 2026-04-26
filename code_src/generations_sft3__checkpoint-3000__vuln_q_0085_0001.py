def simple_calculator():
    try:
        # Get user input
        expression = input("Enter a mathematical expression: ")
        
        # Evaluate the expression safely
        result = eval(expression)
        
        # Print the result
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error: Invalid input or calculation error - {str(e)}")

if __name__ == "__main__":
    simple_calculator()