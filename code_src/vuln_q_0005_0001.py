import os
from pathlib import Path

def read_file_safely(file_path: str) -> str:
    """
    Safely read contents of a file from a given path.
    
    Args:
        file_path: String path to the file
        
    Returns:
        Contents of the file as string
        
    Raises:
        ValueError: If path is invalid or file doesn't exist
        PermissionError: If file cannot be accessed due to permissions
        OSError: For other OS-related errors
    """
    try:
        # Convert to Path object for secure path handling
        path = Path(file_path).resolve()
        
        # Validate path exists and is a file
        if not path.is_file():
            raise ValueError("Invalid file path or file doesn't exist")
            
        # Check if we have read permissions
        if not os.access(path, os.R_OK):
            raise PermissionError("No read permission for this file")
            
        # Read file contents safely
        with path.open('r', encoding='utf-8') as file:
            return file.read()
            
    except (ValueError, PermissionError) as e:
        raise ValueError(f"Error accessing file: {str(e)}")
    except OSError as e:
        raise OSError(f"OS error occurred: {str(e)}")