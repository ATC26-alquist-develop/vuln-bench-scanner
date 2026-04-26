import os
import re
import sys
from pathlib import Path

def secure_delete_file(file_path):
    """Securely delete a file by overwriting its contents before removal."""
    try:
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Overwrite file with random data
        with open(file_path, 'wb') as f:
            f.write(os.urandom(file_size))
        
        # Remove file
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")

def find_and_delete_files(directory, pattern):
    """Find and securely delete files matching the pattern in the given directory."""
    try:
        # Validate directory path
        dir_path = Path(directory).resolve()
        if not dir_path.is_dir():
            raise ValueError("Invalid directory path")

        # Validate pattern
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Invalid pattern")

        # Compile regex pattern
        regex = re.compile(pattern)

        # Walk through directory
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = Path(root) / file
                if regex.search(file):
                    secure_delete_file(file_path)

        print("Files matching the pattern have been securely deleted.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <pattern>")
        sys.exit(1)

    directory = sys.argv[1]
    pattern = sys.argv[2]

    find_and_delete_files(directory, pattern)