import os

def read_file_contents(filename):
    """
    Securely read the contents of a file.
    
    Args:
        filename (str): The name of the file to read
        
    Returns:
        str: The contents of the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If there's no permission to read the file
        ValueError: If the filename is empty or contains invalid characters
    """
    # Validate filename
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    
    # Check if file exists
    if not os.path.exists(safe_filename):
        raise FileNotFoundError(f"File {safe_filename} not found")
    
    # Check if we have permission to read the file
    if not os.access(safe_filename, os.R_OK):
        raise PermissionError(f"No permission to read file {safe_filename}")
    
    try:
        with open(safe_filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

def main():
    try:
        filename = input("Enter the filename to read: ")
        contents = read_file_contents(filename)
        print(f"File contents:\n{contents}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()