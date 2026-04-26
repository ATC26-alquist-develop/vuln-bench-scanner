def simple_calculator():
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'q' to quit): ")
            
            if expression.lower() == 'q':
                print("Exiting calculator. Goodbye!")
                break
            
            # Remove whitespace and split the expression
            expression = expression.replace(" ", "")
            tokens = expression.split()
            
            # Validate input
            if len(tokens) != 3:
                raise ValueError("Invalid expression. Please enter three numbers and an operator.")
            
            # Validate operators
            if tokens[1] not in ('+', '-', '*', '/'):
                raise ValueError("Invalid operator. Please use +, -, *, or /")
            
            # Convert tokens to numbers
            num1 = float(tokens[0])
            num2 = float(tokens[2])
            
            # Perform calculation
            if tokens[1] == '+':
                result = num1 + num2
            elif tokens[1] == '-':
                result = num1 - num2
            elif tokens[1] == '*':
                result = num1 * num2
            elif tokens[1] == '/':
                if num2 == 0:
                    raise ValueError("Division by zero is not allowed.")
                result = num1 / num2
            
            print(f"Result: {result}\n")
        
        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print("An unexpected error occurred. Please try again.\n")

if __name__ == "__main__":
    simple_calculator()