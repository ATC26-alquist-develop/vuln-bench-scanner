import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.sympify import SympifyError

def safe_evaluate_expression(expression: str) -> float:
    """
    Safely evaluate a mathematical expression using SymPy.
    
    Args:
        expression: A string containing a mathematical expression
        
    Returns:
        float: The result of the evaluation
        
    Raises:
        ValueError: If the expression is invalid or cannot be evaluated
    """
    try:
        # Parse the expression into a SymPy expression
        expr = parse_expr(expression)
        
        # Evaluate the expression to a float
        result = float(expr.evalf())
        
        return result
        
    except (SympifyError, ValueError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")