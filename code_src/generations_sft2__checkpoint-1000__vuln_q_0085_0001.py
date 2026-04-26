import re

def is_valid_number(s):
    """Validate if the input string is a valid number."""
    return bool(re.match(r'^-?\d+(\.\d+)?$', s))

def calculate(expression):
    """Safely evaluate a mathematical expression."""
    if not is_valid_number(expression):
        raise ValueError("Invalid input: must be a number")
    
    try:
        return eval(expression)
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}")

def main():
    """Main function to run the calculator."""
    while True:
        user_input = input("Enter a number or expression (or 'quit' to exit): ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        try:
            result = calculate(user_input)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()