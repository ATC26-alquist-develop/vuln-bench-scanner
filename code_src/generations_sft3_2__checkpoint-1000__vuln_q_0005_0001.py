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
        FileNotFoundError: If the file does not exist
    """
    try:
        # Convert to Path object for secure path handling
        path = Path(file_path).resolve()
        
        # Check if path is a file and exists
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Read file contents securely
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
            
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")