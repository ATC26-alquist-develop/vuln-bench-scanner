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
    """Find and securely delete files matching the given pattern in the specified directory."""
    try:
        # Convert to absolute path and validate
        dir_path = Path(directory).resolve()
        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError("Invalid directory path")

        # Validate pattern
        if not isinstance(pattern, str) or not pattern:
            raise ValueError("Invalid pattern")

        # Compile regex pattern
        try:
            regex = re.compile(pattern)
        except re.error:
            raise ValueError("Invalid regex pattern")

        # Find and delete matching files
        for root, _, files in os.walk(str(dir_path)):
            for file in files:
                if regex.search(file):
                    file_path = Path(root) / file
                    secure_delete_file(file_path)
                    print(f"Deleted: {file_path}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <pattern>", file=sys.stderr)
        sys.exit(1)
    
    directory = sys.argv[1]
    pattern = sys.argv[2]
    find_and_delete_files(directory, pattern)