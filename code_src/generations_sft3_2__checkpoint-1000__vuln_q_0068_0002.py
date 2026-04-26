import ast
from typing import Any

def safe_eval_literal(input_string: str) -> Any:
    """
    Safely evaluate a string containing Python literals.
    
    Args:
        input_string: String containing Python literals
        
    Returns:
        Evaluated result
        
    Raises:
        ValueError: If input is not a valid Python literal
    """
    try:
        # Only allow basic Python literals
        return ast.literal_eval(input_string)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid literal: {str(e)}")

# Example usage:
# result = safe_eval_literal("[1, 2, 3]")
# print(result)  # Output: [1, 2, 3]