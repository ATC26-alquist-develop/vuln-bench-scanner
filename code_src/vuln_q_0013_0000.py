```python
import os

def read_file(filename):
    """
    Reads the contents of a file securely.
    
    Args:
        filename (str): The name of the file to read.
    
    Returns:
        str: The contents of the file.
    
    Raises:
        ValueError: If the filename is empty or invalid.
        FileNotFoundError: If the file doesn't exist.
        PermissionError: If the file cannot be accessed due to permissions.
    """
    # Validate filename
    if not filename or not isinstance(filename, str):
        raise ValueError("Invalid filename")
    
    # Sanitize filename to prevent path traversal attacks
    filename = os.path.basename(filename)
    
    # Check if file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' not found")
    
    # Check file permissions
    if not os.access(filename, os.R_OK):
        raise PermissionError(f"No read permission for file '{filename}'")
    
    # Read file contents securely
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading file '{filename}': {str(e)}")

def main():
    try:
        # Get filename from user input
        filename = input("Enter the filename: ").strip()
        
        # Read and display file contents
        contents = read_file(filename)
        print(f"\nContents of '{filename}':")
        print(contents)
    except (ValueError, FileNotFoundError, PermissionError, IOError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
```