import ast
from typing import Union

def safe_eval_math(expression: str) -> Union[int, float]:
    """
    Safely evaluate mathematical expressions using ast.literal_eval()
    Only allows basic arithmetic operations and numbers
    
    Args:
        expression (str): Mathematical expression to evaluate
        
    Returns:
        Union[int, float]: Result of the evaluation
        
    Raises:
        ValueError: If expression is invalid or contains unsupported operations
    """
    try:
        # Use ast.literal_eval instead of eval for safer expression evaluation
        result = ast.literal_eval(expression)
        # Ensure the result is either int or float
        if not isinstance(result, (int, float)):
            raise ValueError("Evaluation resulted in non-numeric type")
        return result
    except (ValueError, SyntaxError, TypeError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")