import os
import sys
import urllib.request
from pathlib import Path

def secure_download_file(file_path):
    """
    Securely download a file from a given URL or local path.
    
    Args:
        file_path (str): The path to the file to be downloaded.
    """
    try:
        # Convert to Path object for secure path handling
        path = Path(file_path).resolve()
        
        # Check if path is within allowed directory
        if not str(path).startswith(str(Path.cwd())):
            print("Error: Access denied. File must be within current directory.")
            return

        # Check if file exists
        if not path.exists():
            print(f"Error: File '{file_path}' not found.")
            return

        # Check if it's a file (not a directory)
        if not path.is_file():
            print(f"Error: '{file_path}' is not a valid file.")
            return

        # Check if file is readable
        if not os.access(path, os.R_OK):
            print(f"Error: No read permission for '{file_path}'.")
            return

        # File is valid and accessible, proceed with download
        print(f"Downloading file: {path}")
        urllib.request.urlretrieve(str(path), str(path))
        print(f"File downloaded successfully to: {path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    secure_download_file(sys.argv[1])