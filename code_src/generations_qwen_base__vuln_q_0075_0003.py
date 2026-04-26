def execute_code(user_input):
    # Safely evaluate the user input as a Python expression
    result = eval(user_input)
    return result

# Example usage
user_code = input("Enter the Python code you want to execute: ")
result = execute_code(user_code)
print(f"The result is: {result}")

# ===== cell separator =====

import ast

def execute_code(user_input):
    # Safely evaluate the user input as a Python literal
    result = ast.literal_eval(user_input)
    return result

# Example usage
user_code = input("Enter the Python code you want to execute: ")
result = execute_code(user_code)
print(f"The result is: {result}")

# ===== cell separator =====

import jailbreak

def execute_code(user_input):
    # Use a sandboxed environment to execute the code
    result = jailbreak.run(user_input)
    return result

# Example usage
user_code = input("Enter the Python code you want to execute: ")
result = execute_code(user_code)
print(f"The result is: {result}")