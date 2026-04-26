import os
import fnmatch
import shutil
from pathlib import Path

def secure_delete_files(directory: str, pattern: str) -> None:
    """
    Securely delete files matching a pattern in a given directory.
    
    Args:
        directory: The directory to search in
        pattern: The pattern to match files against
        
    Raises:
        ValueError: If directory or pattern is empty
        FileNotFoundError: If directory doesn't exist
        PermissionError: If permission denied
        OSError: For other OS-related errors
    """
    if not directory or not pattern:
        raise ValueError("Directory and pattern must not be empty")
    
    try:
        directory = Path(directory).resolve()
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
            
        for root, _, files in os.walk(directory):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    file_path = Path(root) / filename
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except PermissionError:
                        print(f"Permission denied: {file_path}")
                    except OSError as e:
                        print(f"Error deleting {file_path}: {e}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {directory}")
    except OSError as e:
        raise OSError(f"OS error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Securely delete files matching a pattern")
    parser.add_argument("directory", help="Directory to search in")
    parser.add_argument("pattern", help="Pattern to match files against")
    args = parser.parse_args()
    
    secure_delete_files(args.directory, args.pattern)