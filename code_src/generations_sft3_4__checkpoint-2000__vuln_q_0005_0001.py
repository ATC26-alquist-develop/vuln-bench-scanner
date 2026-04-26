import os
from pathlib import Path

def get_file_contents(file_path: str) -> str:
    """
    Securely read the contents of a file at the given path.
    
    Args:
        file_path (str): The path to the file to read
        
    Returns:
        str: The contents of the file
        
    Raises:
        ValueError: If the path is invalid or file cannot be read
        FileNotFoundError: If the file doesn't exist
    """
    try:
        # Convert to absolute path and resolve any symlinks
        abs_path = os.path.abspath(os.path.realpath(file_path))
        
        # Check if path exists and is a file
        path = Path(abs_path)
        if not path.is_file():
            raise ValueError(f"Path is not a valid file: {abs_path}")
            
        # Read file contents securely
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
            
    except (IOError, OSError) as e:
        raise ValueError(f"Error reading file: {str(e)}")