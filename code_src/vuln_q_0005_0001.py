```python
import os
from pathlib import Path

def read_file_safely(file_path: str) -> str:
    """
    Safely read contents of a file at the given path.
    
    Args:
        file_path: String containing the file path
        
    Returns:
        Contents of the file as string
        
    Raises:
        ValueError: If path is invalid or file doesn't exist
        PermissionError: If file cannot be accessed due to permissions
    """
    # Validate input
    if not file_path or not isinstance(file_path, str):
        raise ValueError("File path must be a non-empty string")
        
    # Convert to absolute path and validate
    try:
        file_path = os.path.abspath(file_path)
        path = Path(file_path)
        
        # Check if path exists and is a file
        if not path.exists():
            raise ValueError(f"File does not exist: {file_path}")
            
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
            
        # Check if we have read permissions
        if not os.access(path, os.R_OK):
            raise PermissionError(f"No read permission for file: {file_path}")
            
        # Read file contents safely
        with path.open('r', encoding='utf-8') as file:
            return file.read()
            
    except (OSError, IOError) as e:
        raise ValueError(f"Error reading file: {str(e)}")
```