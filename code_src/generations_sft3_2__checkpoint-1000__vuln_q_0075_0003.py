import ast

def safe_eval_literal(user_input):
    try:
        # Only allow basic Python literals
        result = ast.literal_eval(user_input)
        return result
    except (ValueError, SyntaxError) as e:
        print(f"Error: {e}")
        return None

# Example usage
user_input = input("Enter a Python literal: ")
result = safe_eval_literal(user_input)
if result is not None:
    print(f"Evaluated result: {result}")