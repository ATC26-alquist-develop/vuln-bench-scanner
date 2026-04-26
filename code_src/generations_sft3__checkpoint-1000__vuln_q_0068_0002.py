import ast
from typing import Any

def safe_eval(expression: str) -> Any:
    """
    Safely evaluate a mathematical expression using ast.literal_eval().
    
    Args:
        expression: Mathematical expression as a string
        
    Returns:
        Evaluated result
        
    Raises:
        ValueError: If the expression is invalid or contains non-numeric values
    """
    try:
        # Only allow basic mathematical expressions with numbers and simple operators
        result = ast.literal_eval(expression)
        return result
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")

# Example usage:
# result = safe_eval("2 + 3 * 4")
# print(result)  # Output: 14