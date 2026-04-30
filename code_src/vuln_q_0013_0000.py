```python
import os
from pathlib import Path

def read_file_safely(filename: str) -> str:
    """
    Safely read the contents of a file with proper validation.
    
    Args:
        filename: The name of the file to read
        
    Returns:
        The contents of the file as a string
        
    Raises:
        ValueError: If the filename is invalid or the file doesn't exist
        PermissionError: If the file cannot be accessed due to permission issues
    """
    # Normalize and validate the filename
    safe_filename = os.path.normpath(filename).lstrip(os.sep)
    if not safe_filename or safe_filename.startswith('.'):
        raise ValueError("Invalid filename")
    
    # Convert to absolute path and check if it exists and is a file
    file_path = Path(safe_filename).resolve()
    if not file_path.is_file():
        raise ValueError("File does not exist or is not a regular file")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except PermissionError:
        raise PermissionError("Permission denied: Unable to read the file")

# Example usage
try:
    user_input = input("Enter the filename to read: ").strip()
    content = read_file_safely(user_input)
    print("File contents:")
    print(content)
except (ValueError, PermissionError) as e:
    print(f"Error: {e}")
```