import os
import pathlib

def delete_file(file_path):
    """
    Securely delete a file from the system.
    
    Args:
        file_path (str): The path to the file to be deleted.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        # Convert to absolute path and resolve any symlinks
        abs_path = pathlib.Path(file_path).resolve()
        
        # Check if the path exists and is a file
        if not abs_path.is_file():
            print(f"Error: {abs_path} is not a valid file.")
            return False
            
        # Check if we have permission to delete the file
        if not os.access(abs_path, os.W_OK):
            print(f"Error: No permission to delete {abs_path}")
            return False
            
        # Delete the file
        os.remove(abs_path)
        print(f"File {abs_path} deleted successfully.")
        return True
        
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False