import os
from pathlib import Path

def secure_file_operation(operation: str, file_path: str, content: str = None) -> str:
    """
    Securely perform file operations (read or write) on a specified file.
    
    Args:
        operation: 'read' or 'write'
        file_path: Path to the file
        content: Content to write (None for read operation)
    
    Returns:
        File content as string if operation is 'read'
    
    Raises:
        ValueError: If operation is invalid or file path is invalid
        IOError: If file operation fails
    """
    # Validate operation
    if operation not in ['read', 'write']:
        raise ValueError("Operation must be 'read' or 'write'")

    # Convert to Path object for secure path handling
    file_path = Path(file_path).resolve()

    # Validate file path
    if not file_path.is_file():
        raise ValueError("Invalid file path")

    try:
        if operation == 'read':
            # Securely read file content
            with file_path.open('r', encoding='utf-8') as file:
                return file.read()
        elif operation == 'write':
            # Securely write content to file
            with file_path.open('w', encoding='utf-8') as file:
                file.write(content)
    except IOError as e:
        raise IOError(f"File operation failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

# ===== cell separator =====

# Reading a file
content = secure_file_operation('read', '/path/to/file.txt')
print(content)

# Writing to a file
secure_file_operation('write', '/path/to/file.txt', 'Hello, World!')