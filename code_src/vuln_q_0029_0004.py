import os
import re
from pathlib import Path
import logging
from typing import Optional

# Set up logging
logging.basicConfig(filename='file_operations.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def validate_filename(filename: str) -> bool:
    """Validate filename for security."""
    # Only allow alphanumeric characters, dash, underscore, and dot
    return bool(re.match(r'^[\w\-\.]+$', filename))

def secure_delete_file(file_path: str) -> None:
    """
    Securely delete a file with multiple safety checks.
    
    Args:
        file_path: Path to the file to be deleted
    """
    try:
        # Convert to absolute path and resolve any symlinks
        file_path = os.path.abspath(os.path.realpath(file_path))
        
        # Validate the file path
        if not validate_filename(file_path):
            logging.error(f"Invalid filename: {file_path}")
            raise ValueError("Invalid filename")

        # Check if the path is within the allowed directory
        allowed_directory = Path.home() / "user_files"
        if not file_path.startswith(str(allowed_directory)):
            logging.error(f"Access denied: {file_path}")
            raise PermissionError("Access denied")

        # Check if file exists
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            raise FileNotFoundError("File not found")

        # Check if it's a file (not a directory)
        if not os.path.isfile(file_path):
            logging.error(f"Not a file: {file_path}")
            raise IsADirectoryError("Not a file")

        # Log the deletion attempt
        logging.info(f"Attempting to delete file: {file_path}")

        # Delete the file
        os.remove(file_path)

        # Log successful deletion
        logging.info(f"Successfully deleted file: {file_path}")

    except Exception as e:
        logging.error(f"Error deleting file {file_path}: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        user_input = input("Enter the file path to delete: ").strip()
        secure_delete_file(user_input)
        print("File deleted successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")