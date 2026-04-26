import os
import re
import sys
from pathlib import Path

def secure_delete_files(directory, pattern):
    """
    Securely find and delete files matching a pattern in a given directory.
    
    Args:
        directory (str): The directory to search for files
        pattern (str): The file pattern to match (supports wildcards)
    """
    try:
        # Convert to absolute path and resolve any symlinks
        dir_path = Path(directory).resolve()
        
        # Validate directory exists and is a directory
        if not dir_path.is_dir():
            raise ValueError("Invalid directory path")
        
        # Validate pattern is a string and contains only valid characters
        if not isinstance(pattern, str) or not re.match(r'^[a-zA-Z0-9_.*?]+$', pattern):
            raise ValueError("Invalid pattern format")
        
        # Find matching files
        for file_path in dir_path.rglob(pattern):
            if file_path.is_file():
                # Ensure we're not deleting system files or directories
                if not file_path.name.startswith('.') and not file_path.name.startswith('_'):
                    try:
                        file_path.unlink()
                        print(f"Deleted: {file_path}")
                    except PermissionError:
                        print(f"Permission denied: {file_path}")
                    except OSError as e:
                        print(f"Error deleting {file_path}: {e}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <pattern>", file=sys.stderr)
        sys.exit(1)
    
    directory = sys.argv[1]
    pattern = sys.argv[2]
    secure_delete_files(directory, pattern)