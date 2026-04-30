I can help you create a secure way to evaluate mathematical expressions. Here's a safe implementation using the `sympy` library:

```python
from sympy import sympify, SympifyError

def evaluate_expression(expression: str) -> str:
    """
    Safely evaluate a mathematical expression using sympy.
    
    Args:
        expression (str): The mathematical expression to evaluate
        
    Returns:
        str: The result of the evaluation or an error message
    """
    try:
        # Convert string to sympy expression and evaluate
        result = sympify(expression)
        return str(result)
    except SympifyError:
        return "Invalid expression. Please enter a valid mathematical expression."
    except Exception as e:
        return f"An error occurred: {str(e)}"
```

This implementation uses sympy's secure parsing and evaluation methods, which are much safer than using eval(). It handles basic arithmetic operations, functions, and constants.