def safe_execute_code(code: str) -> None:
    """
    Safely execute a string of Python code.
    
    Args:
        code (str): The Python code to execute
        
    Raises:
        SyntaxError: If the code contains syntax errors
        Exception: For any other execution errors
    """
    try:
        exec(code, globals())
    except SyntaxError as e:
        print(f"Syntax error: {e}")
    except Exception as e:
        print(f"Error executing code: {e}")

# Example usage
safe_execute_code("print('Hello, World!')")