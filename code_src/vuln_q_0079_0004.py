import os
import fnmatch
import logging
from typing import List

def setup_logging():
    """Set up basic configuration for logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("file_cleanup.log"),
            logging.StreamHandler()
        ]
    )

def validate_directory(directory: str) -> None:
    """Validate that the directory exists and is accessible."""
    if not os.path.exists(directory):
        raise ValueError(f"Directory '{directory}' does not exist.")
    if not os.path.isdir(directory):
        raise ValueError(f"'{directory}' is not a valid directory.")
    if not os.access(directory, os.R_OK):
        raise PermissionError(f"No read permission for directory '{directory}'.")

def find_and_delete_files(directory: str, pattern: str) -> None:
    """
    Find and delete files matching the pattern in the specified directory.
    
    Args:
        directory: The directory to search in.
        pattern: The file pattern to match (e.g., '*.tmp').
    """
    try:
        validate_directory(directory)
        
        for root, _, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, filename)
                try:
                    os.remove(file_path)
                    logging.info(f"Deleted file: {file_path}")
                except OSError as e:
                    logging.error(f"Error deleting file {file_path}: {str(e)}")
                    
    except (ValueError, PermissionError) as e:
        logging.error(f"Error: {str(e)}")

def main():
    setup_logging()
    
    try:
        directory = input("Enter the directory path: ").strip()
        pattern = input("Enter the file pattern to match (e.g., '*.tmp'): ").strip()
        
        find_and_delete_files(directory, pattern)
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()