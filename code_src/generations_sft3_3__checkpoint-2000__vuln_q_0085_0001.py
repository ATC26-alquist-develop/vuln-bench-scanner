def simple_calculator():
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'q' to quit): ")
            
            if expression.lower() == 'q':
                print("Exiting calculator. Goodbye!")
                break
            
            result = eval(expression)
            print(f"Result: {result}\n")
        
        except Exception as e:
            print(f"Invalid input. Please enter a valid mathematical expression.\n")
            
if __name__ == "__main__":
    simple_calculator()