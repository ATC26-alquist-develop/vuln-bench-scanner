import os

def read_file_contents(file_path: str) -> str:
    """
    Securely read contents of a file at the given path.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        str: Contents of the file
        
    Raises:
        ValueError: If path is invalid or file cannot be read
        FileNotFoundError: If file does not exist
    """
    if not isinstance(file_path, str):
        raise ValueError("File path must be a string")
        
    # Convert to absolute path and resolve any symlinks
    abs_path = os.path.abspath(os.path.realpath(file_path))
    
    # Check if file exists and is a regular file
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"File not found or is not a regular file: {abs_path}")
        
    try:
        with open(abs_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise ValueError(f"Error reading file: {e}")