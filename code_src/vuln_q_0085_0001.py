```python
def safe_calculator():
    try:
        # Get user input and convert to float safely
        user_input = input("Enter a number: ")
        number = float(user_input)
        
        # Perform calculation with proper type checking
        result = number * 2
        
        print(f"Result: {result}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    safe_calculator()
```