import os
import sys
import urllib.parse
from pathlib import Path

def is_safe_path(base_path, path):
    """Check if the given path is safe to access."""
    try:
        base_path = Path(base_path).resolve()
        path = Path(base_path, path).resolve()
        return base_path in path.parents
    except (TypeError, ValueError):
        return False

def download_file(file_path):
    """Download file from given path."""
    try:
        parsed_path = urllib.parse.urlparse(file_path)
        if parsed_path.scheme:
            print("Error: URL schemes are not allowed")
            return

        if not parsed_path.netloc:
            print("Error: Missing host in URL")
            return

        if not is_safe_path(os.getcwd(), parsed_path.path):
            print("Error: Access to path outside current directory is not allowed")
            return

        file_path = Path(parsed_path.path).resolve()
        if not file_path.is_file():
            print("Error: File does not exist")
            return

        if not os.access(file_path, os.R_OK):
            print("Error: No read permission for file")
            return

        print(f"Downloading file: {file_path}")
        with open(file_path, 'rb') as file:
            content = file.read()
        
        print("File downloaded successfully")
        return content

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    content = download_file(file_path)
    if content:
        print("Content length:", len(content))