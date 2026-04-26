import os
import sys

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
    safe_filename = os.path.basename(filename)
    
    # Validate content
    if not content or not isinstance(content, str):
        raise ValueError("Content must be a non-empty string")
    
    try:
        # Create file with specified permissions (readable/writable only by owner)
        with open(safe_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        os.chmod(safe_filename, 0o600)
    except IOError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    filename = input("Enter filename: ")
    content = input("Enter content: ")
    create_file(filename, content)