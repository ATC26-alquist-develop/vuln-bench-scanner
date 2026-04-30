import os
import fnmatch
import re
from pathlib import Path

def secure_delete_files(directory: str, pattern: str) -> None:
    """
    Securely delete files matching a pattern in a given directory.
    
    Args:
        directory: The directory to search in
        pattern: The pattern to match files against
        
    Raises:
        ValueError: If directory or pattern is invalid
        OSError: If file operations fail
    """
    # Validate inputs
    if not directory or not pattern:
        raise ValueError("Both directory and pattern must be provided")
        
    # Convert to absolute path and validate directory
    try:
        directory = os.path.abspath(directory)
        if not os.path.isdir(directory):
            raise ValueError("Invalid directory")
    except Exception as e:
        raise ValueError(f"Invalid directory: {str(e)}")
        
    # Validate pattern (only allow alphanumeric chars, dots, underscores, hyphens, and slashes)
    if not re.match(r'^[a-zA-Z0-9._-]+$', pattern):
        raise ValueError("Invalid pattern. Only alphanumeric chars, dots, underscores, hyphens, and slashes are allowed")
        
    try:
        # Walk through directory
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    file_path = os.path.join(root, filename)
                    try:
                        # Securely delete file
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except OSError as e:
                        print(f"Error deleting {file_path}: {str(e)}")
    except Exception as e:
        raise OSError(f"Error processing directory: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Securely delete files matching a pattern")
    parser.add_argument("directory", help="Directory to search in")
    parser.add_argument("pattern", help="Pattern to match files against")
    
    args = parser.parse_args()
    
    try:
        secure_delete_files(args.directory, args.pattern)
    except Exception as e:
        print(f"Error: {str(e)}")