import os
from pathlib import Path
import tempfile

def secure_file_operation(operation, file_path, content=None):
    """
    Securely perform file operations (read/write) with proper error handling.
    
    Args:
        operation (str): 'read' or 'write'
        file_path (str): Path to the file
        content (str, optional): Content to write if operation is 'write'
    
    Returns:
        str: File content if operation is 'read', None if operation is 'write'
    """
    try:
        # Convert to Path object for secure path handling
        path = Path(file_path).resolve()
        
        # Ensure path is within allowed directory (adjust 'allowed_dir' as needed)
        allowed_dir = Path.cwd() / 'secure_files'
        if not path.is_relative_to(allowed_dir):
            raise ValueError("Access denied: File path is outside allowed directory")
            
        if operation == 'read':
            # Use 'x' mode to prevent accidental overwriting
            with path.open('x') as f:
                return f.read()
        elif operation == 'write':
            # Use temporary file for atomic write
            with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=str(allowed_dir)) as temp_file:
                temp_path = Path(temp_file.name)
                temp_file.write(content)
                temp_path.replace(path)
            return None
        else:
            raise ValueError("Invalid operation. Use 'read' or 'write'.")
    except (IOError, OSError, ValueError) as e:
        print(f"Error: {e}")
        return None

# Example usage:
# content = secure_file_operation('read', 'secure_files/example.txt')
# secure_file_operation('write', 'secure_files/example.txt', 'New content')