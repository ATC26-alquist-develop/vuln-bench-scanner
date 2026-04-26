import os

def read_file_contents(file_path: str) -> str:
    """
    Securely read contents of a file at the given path.
    
    Args:
        file_path (str): The path to the file to read
        
    Returns:
        str: The contents of the file
        
    Raises:
        ValueError: If the path is invalid or file cannot be read
        FileNotFoundError: If the file doesn't exist
        PermissionError: If there's no permission to read the file
    """
    # Validate and sanitize the input path
    try:
        # Resolve the path to its absolute form and check if it exists
        abs_path = os.path.abspath(os.path.normpath(file_path))
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File not found: {abs_path}")
            
        # Check if we have read permissions
        if not os.access(abs_path, os.R_OK):
            raise PermissionError(f"No read permission for file: {abs_path}")
            
        # Read the file contents
        with open(abs_path, 'r', encoding='utf-8') as file:
            return file.read()
            
    except (OSError, IOError) as e:
        raise ValueError(f"Error reading file: {str(e)}")