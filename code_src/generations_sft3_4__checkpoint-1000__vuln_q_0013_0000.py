import os

def read_file_contents(filename):
    """
    Securely read the contents of a file.
    
    Args:
        filename (str): The name of the file to read
        
    Returns:
        str: The contents of the file
        
    Raises:
        ValueError: If the file doesn't exist or is not readable
        IOError: If there's an error reading the file
    """
    # Validate filename
    if not isinstance(filename, str):
        raise ValueError("Filename must be a string")
    
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    
    # Check if file exists and is readable
    if not os.path.isfile(safe_filename):
        raise ValueError("File does not exist")
    
    try:
        with open(safe_filename, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading file: {e}")

# Example usage
if __name__ == "__main__":
    try:
        user_input = input("Enter the filename: ")
        contents = read_file_contents(user_input)
        print("File contents:")
        print(contents)
    except (ValueError, IOError) as e:
        print(f"Error: {e}")