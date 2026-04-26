import os

def create_file(filename: str, content: str) -> None:
    """
    Creates a file with the given content.
    
    Args:
        filename: Name of the file to create
        content: Content to write to the file
    """
    # Validate filename
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    # Sanitize filename to prevent directory traversal
    filename = os.path.basename(filename)
    
    # Validate content
    if not content or not isinstance(content, str):
        raise ValueError("Content must be a non-empty string")
    
    try:
        # Create file with specified permissions (readable/writable only by owner)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        os.chmod(filename, 0o600)
    except IOError as e:
        raise IOError(f"Error creating file: {e}")

# Example usage
if __name__ == "__main__":
    try:
        filename = input("Enter filename: ")
        content = input("Enter content: ")
        create_file(filename, content)
        print(f"File {filename} created successfully")
    except (ValueError, IOError) as e:
        print(f"Error: {e}")