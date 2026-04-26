import os
from pathlib import Path
import stat

def read_file_contents(file_path: str) -> str:
    """
    Securely read contents of a file from a given path.
    
    Args:
        file_path: String path to the file
        
    Returns:
        Contents of the file as string
        
    Raises:
        ValueError: If path is invalid or file doesn't exist
        PermissionError: If file cannot be accessed due to permissions
    """
    try:
        # Convert to Path object and resolve to absolute path
        path = Path(file_path).resolve()
        
        # Verify path exists and is a file
        if not path.is_file():
            raise ValueError("Invalid file path or file doesn't exist")
            
        # Verify file has read permissions
        if not os.access(path, os.R_OK):
            raise PermissionError("File cannot be accessed due to permissions")
            
        # Read file contents
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except (OSError, ValueError) as e:
        raise ValueError(f"Error accessing file: {str(e)}")