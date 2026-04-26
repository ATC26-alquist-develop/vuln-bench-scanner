import os
import pathlib
import logging
from typing import Optional

def secure_delete_file(file_path: str) -> bool:
    """
    Securely delete a file by overwriting its contents before deletion.
    
    Args:
        file_path: Path to the file to be deleted
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # Convert to absolute path and resolve any symlinks
        abs_path = pathlib.Path(file_path).resolve()
        
        # Check if the path is within allowed directories
        allowed_dirs = ['/path/to/allowed/dir1', '/path/to/allowed/dir2']
        if not any(str(abs_path).startswith(allowed_dir) for allowed_dir in allowed_dirs):
            logging.error(f"Attempted to delete file outside allowed directories: {abs_path}")
            return False
            
        # Check if file exists and is a regular file
        if not abs_path.is_file():
            logging.error(f"Attempted to delete non-existent file: {abs_path}")
            return False
            
        # Overwrite file contents with random data
        with open(abs_path, 'wb') as f:
            f.write(os.urandom(abs_path.stat().st_size))
            
        # Delete the file
        os.remove(abs_path)
        return True
        
    except Exception as e:
        logging.error(f"Error deleting file {file_path}: {str(e)}")
        return False