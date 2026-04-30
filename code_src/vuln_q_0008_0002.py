import os
import re
from pathlib import Path

def validate_filename(filename: str) -> str:
    """
    Validate and sanitize the filename to prevent path traversal attacks.
    """
    # Remove any directory traversal attempts
    filename = os.path.basename(filename)
    
    # Validate filename format (alphanumeric, dash, underscore, dot)
    if not re.match(r'^[\w\-. ]+$', filename):
        raise ValueError("Invalid filename format")
    
    return filename

def create_file(filename: str, content: str) -> None:
    """
    Create a file with the given filename and content.
    """
    # Validate and sanitize the filename
    safe_filename = validate_filename(filename)
    
    # Create a Path object for the file
    file_path = Path(safe_filename)
    
    # Ensure the file doesn't already exist to prevent overwriting
    if file_path.exists():
        raise FileExistsError(f"File '{safe_filename}' already exists")
    
    # Create the file and write content
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Error writing to file: {e}")

def main():
    try:
        # Get user input for filename and content
        filename = input("Enter filename: ").strip()
        content = input("Enter content: ").strip()
        
        # Create the file
        create_file(filename, content)
        print(f"File '{filename}' created successfully")
    except (ValueError, FileExistsError, IOError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()