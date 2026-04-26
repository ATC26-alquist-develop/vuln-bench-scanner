import os
from pathlib import Path

def read_file_contents(file_path: str) -> str:
    """
    Securely read contents of a file at the given path.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        str: Contents of the file
        
    Raises:
        ValueError: If path is invalid or file cannot be read
        FileNotFoundError: If file does not exist
    """
    try:
        # Convert to absolute path and resolve any symlinks
        abs_path = os.path.abspath(os.path.realpath(file_path))
        
        # Check if path exists and is a file
        path = Path(abs_path)
        if not path.is_file():
            raise ValueError(f"Path is not a valid file: {abs_path}")
            
        # Read file contents safely
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
            
    except (IOError, OSError) as e:
        raise ValueError(f"Error reading file: {e}")