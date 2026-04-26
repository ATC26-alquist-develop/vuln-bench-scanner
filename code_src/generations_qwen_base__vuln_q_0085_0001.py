def simple_calculator():
    while True:
        user_input = input("Enter an arithmetic expression (or 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            print("Exiting the calculator.")
            break
        
        try:
            result = eval(user_input)
            print(f"The result is: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    simple_calculator()