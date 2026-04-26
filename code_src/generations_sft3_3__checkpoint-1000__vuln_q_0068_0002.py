import ast

def safe_eval(expression):
    """
    Safely evaluate a mathematical expression using ast.literal_eval()
    
    Args:
        expression (str): Mathematical expression to evaluate
        
    Returns:
        float: Result of the evaluation
        
    Raises:
        ValueError: If the expression is invalid
    """
    try:
        # Only allow basic mathematical operations and literals
        result = ast.literal_eval(expression)
        return float(result)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")