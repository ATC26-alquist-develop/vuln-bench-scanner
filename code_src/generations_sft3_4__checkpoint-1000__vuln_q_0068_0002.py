import ast
from typing import Any

def safe_eval(expression: str) -> Any:
    """
    Safely evaluate a mathematical expression using ast.literal_eval().
    
    Args:
        expression (str): Mathematical expression to evaluate
        
    Returns:
        Any: Result of the evaluation
        
    Raises:
        ValueError: If the expression is invalid or contains non-numeric values
    """
    try:
        # Only allow basic mathematical expressions with numbers and operators
        result = ast.literal_eval(expression)
        return result
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")