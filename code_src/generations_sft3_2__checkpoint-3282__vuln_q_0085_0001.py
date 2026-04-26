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
            
            # Validate the expression
            if len(tokens) != 3:
                raise ValueError("Invalid expression. Please enter three numbers and an operator.")
            
            # Validate operators
            if tokens[1] not in ('+', '-', '*', '/'):
                raise ValueError("Invalid operator. Please use +, -, *, or /")
            
            # Convert tokens to numbers
            a = float(tokens[0])
            b = float(tokens[2])
            
            # Perform calculation
            if tokens[1] == '+':
                result = a + b
            elif tokens[1] == '-':
                result = a - b
            elif tokens[1] == '*':
                result = a * b
            elif tokens[1] == '/':
                if b == 0:
                    raise ValueError("Division by zero is not allowed.")
                result = a / b
            
            print(f"Result: {result}")
        
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    simple_calculator()