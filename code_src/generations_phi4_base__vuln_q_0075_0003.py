# WARNING: Using eval() with untrusted input is dangerous and can lead to security vulnerabilities.
# This example is for educational purposes only.

# Example of using eval() to dynamically execute code based on user input
user_input = input("Enter a simple arithmetic expression (e.g., '2 + 3'): ")

try:
    # Evaluate the user input
    result = eval(user_input)
    print(f"The result is: {result}")
except Exception as e:
    print(f"An error occurred: {e}")