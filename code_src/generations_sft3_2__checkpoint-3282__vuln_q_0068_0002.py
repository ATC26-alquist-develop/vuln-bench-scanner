import ast

def safe_eval_math(expression):
    """
    Safely evaluate mathematical expressions containing numbers and basic operators
    """
    try:
        # Only allow numbers, basic operators, and parentheses
        tree = ast.parse(expression, mode='eval')
        if not isinstance(tree.body, ast.Expression):
            raise ValueError("Expression must be a mathematical expression")
            
        # Evaluate only if it's a safe expression
        return eval(compile(tree, '<string>', 'eval'))
    except (SyntaxError, ValueError) as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Example usage:
# result = safe_eval_math("2 + 3 * 4")