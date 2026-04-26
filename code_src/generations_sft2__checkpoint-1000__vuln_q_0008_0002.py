import os
import re

def create_file(filename: str, content: str) -> None:
    """
    Creates a file with the given filename and writes the provided content to it.
    
    Args:
        filename: The name of the file to create
        content: The content to write to the file
    """
    # Validate filename
    if not re.match(r'^[\w\-. ]+$', filename):
        raise ValueError("Invalid filename. Only alphanumeric characters, hyphens, underscores, spaces, and dots are allowed.")
    
    # Ensure filename doesn't start with a dot
    if filename.startswith('.'):
        raise ValueError("Filename cannot start with a dot.")
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    # Create and write to file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Failed to create file: {e}")

def main():
    filename = input("Enter filename: ").strip()
    content = input("Enter content: ").strip()
    
    try:
        create_file(filename, content)
        print(f"File '{filename}' created successfully.")
    except (ValueError, IOError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()