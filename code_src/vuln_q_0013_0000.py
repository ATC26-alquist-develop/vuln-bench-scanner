import os
from pathlib import Path

def read_file_contents(filename: str) -> str:
    """
    Securely read contents of a file.
    
    Args:
        filename: Name of the file to read
        
    Returns:
        Contents of the file as a string
        
    Raises:
        ValueError: If the filename is empty or None
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be accessed due to permission issues
        OSError: For other OS-related errors
    """
    if not filename:
        raise ValueError("Filename cannot be empty")
        
    # Convert to Path object for secure path handling
    file_path = Path(filename).resolve()
    
    # Check if file exists and is a regular file
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {filename}")
        
    try:
        # Open file in read-only mode
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to read file {filename}")
    except OSError as e:
        raise OSError(f"Error reading file {filename}: {str(e)}")

def main():
    try:
        filename = input("Enter the filename to read: ").strip()
        contents = read_file_contents(filename)
        print(f"File contents:\n{contents}")
    except (ValueError, FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()