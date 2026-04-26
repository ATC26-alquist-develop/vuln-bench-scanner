import os

def create_file(filename: str, content: str) -> None:
    """
    Creates a file with the given content.
    
    Args:
        filename (str): The name of the file to create
        content (str): The content to write to the file
        
    Raises:
        ValueError: If filename or content is empty
        OSError: If there's an error creating the file
    """
    if not filename or not content:
        raise ValueError("Filename and content cannot be empty")
        
    # Sanitize filename to prevent directory traversal
    safe_filename = os.path.basename(filename)
    
    try:
        with open(safe_filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except OSError as e:
        raise OSError(f"Failed to create file {safe_filename}: {str(e)}")

def main():
    try:
        filename = input("Enter filename: ").strip()
        content = input("Enter content: ").strip()
        create_file(filename, content)
        print(f"File {filename} created successfully")
    except (ValueError, OSError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()