import os

def read_file(file_path: str) -> None:
    """
    Securely read and print the contents of a file.
    
    Args:
        file_path: Path to the file to be read
        
    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be accessed due to permission issues
        OSError: For other OS-related errors
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")
        
    if not file_path:
        raise ValueError("file_path cannot be empty")
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Permission denied: Unable to read file {file_path}")
        
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except OSError as e:
        raise OSError(f"Error reading file: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        read_file(file_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)