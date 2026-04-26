import ast
from typing import Union

def safe_eval_math(expression: str) -> Union[int, float, None]:
    """
    Safely evaluate mathematical expressions using ast.literal_eval()
    Only allows basic mathematical operations and numbers
    
    Args:
        expression (str): Mathematical expression to evaluate
        
    Returns:
        Union[int, float, None]: Result of evaluation or None if invalid
    """
    try:
        # Only allows basic mathematical operations and numbers
        return ast.literal_eval(expression)
    except (ValueError, SyntaxError, TypeError):
        return None