```python
import os
from pathlib import Path
import stat

def read_file_safely(file_path: str, max_size: int = 1024 * 1024) -> str:
    """
    Safely read contents of a file from a trusted location.
    
    Args:
        file_path: Path to the file to read
        max_size: Maximum allowed file size in bytes (default 1MB)
    
    Returns:
        Contents of the file as a string
    
    Raises:
        ValueError: If the path is invalid or file is too large
        PermissionError: If the file cannot be accessed due to permissions
        OSError: For other OS-related errors
    """
    try:
        # Convert to absolute path and resolve any symlinks
        abs_path = Path(file_path).resolve()
        
        # Check if path is within allowed directory (adjust as needed)
        allowed_dir = Path('/path/to/allowed/directory').resolve()
        if not abs_path.is_relative_to(allowed_dir):
            raise ValueError("Access to this file is not allowed")
            
        # Check file size
        if abs_path.stat().st_size > max_size:
            raise ValueError(f"File size exceeds maximum allowed size of {max_size} bytes")
            
        # Check file permissions
        if not stat.S_ISREG(abs_path.stat().st_mode):
            raise ValueError("Invalid file type")
            
        # Read file contents safely
        with open(abs_path, 'r', encoding='utf-8') as file:
            return file.read()
            
    except (ValueError, PermissionError, OSError) as e:
        raise ValueError(f"Error accessing file: {str(e)}")
```