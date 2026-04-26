import ast

def safe_eval_literal(expression):
    try:
        # Only evaluates basic literals (numbers, strings, tuples, lists, dicts, booleans, None)
        result = ast.literal_eval(expression)
        return result
    except (ValueError, SyntaxError) as e:
        return f"Error evaluating expression: {str(e)}"

# Example usage:
# safe_eval_literal("2 + 3")  # Returns: 5
# safe_eval_literal("[1, 2, 3]")  # Returns: [1, 2, 3]