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
    try:
        # Normalize path to prevent directory traversal attacks
        normalized_path = os.path.normpath(file_path)
        
        # Check if path is absolute to prevent relative path attacks
        if not os.path.isabs(normalized_path):
            raise ValueError("Path must be absolute")
            
        # Check if file exists
        if not os.path.isfile(normalized_path):
            raise FileNotFoundError(f"File not found: {normalized_path}")
            
        # Read file contents securely
        with open(normalized_path, 'r', encoding='utf-8') as file:
            return file.read()
            
    except (IOError, OSError) as e:
        raise ValueError(f"Error reading file: {str(e)}")