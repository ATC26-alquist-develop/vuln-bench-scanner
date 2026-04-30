import os
from pathlib import Path

def create_file(filename: str, content: str) -> None:
    """
    Creates a file with the given filename and writes the specified content to it.
    
    Args:
        filename (str): The name of the file to create.
        content (str): The content to write to the file.
        
    Raises:
        ValueError: If the filename is empty or invalid.
        IOError: If there's an error writing to the file.
    """
    # Validate filename
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty.")
    
    # Sanitize filename to prevent path traversal attacks
    filename = Path(filename).name
    
    # Validate content
    if not content or not isinstance(content, str):
        raise ValueError("Content must be a non-empty string.")
    
    # Create full file path
    file_path = Path.cwd() / filename
    
    try:
        # Create directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content to file using context manager for proper resource handling
        with file_path.open('w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"File '{file_path}' created successfully.")
    except IOError as e:
        raise IOError(f"Error writing to file: {str(e)}")

def main():
    try:
        # Get user input with input validation
        filename = input("Enter the filename: ").strip()
        content = input("Enter the content: ").strip()
        
        # Create file with validated input
        create_file(filename, content)
    except (ValueError, IOError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()