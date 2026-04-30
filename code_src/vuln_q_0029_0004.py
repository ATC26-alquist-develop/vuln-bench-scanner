import os
import pathlib

def secure_delete_file(file_path: str) -> None:
    """
    Securely delete a file using user input.
    
    Args:
        file_path: The path to the file to be deleted
        
    Raises:
        ValueError: If the file path is invalid or the file doesn't exist
        PermissionError: If the user doesn't have permission to delete the file
    """
    try:
        # Convert to absolute path and resolve any symlinks
        abs_path = pathlib.Path(file_path).resolve()
        
        # Validate path is within allowed directory
        allowed_dir = pathlib.Path.home() / "secure_files"
        if not abs_path.is_relative_to(allowed_dir):
            raise ValueError("Access denied: File must be within allowed directory")
            
        # Check if file exists
        if not abs_path.is_file():
            raise ValueError("File does not exist")
            
        # Securely delete the file
        os.remove(abs_path)
        print(f"File {abs_path} has been securely deleted.")
        
    except (OSError, ValueError) as e:
        raise ValueError(f"Error deleting file: {str(e)}")