import os
import re
import sys

def find_and_delete_files(directory, pattern):
    """
    Find and delete files matching the given pattern in the specified directory.
    
    Args:
        directory (str): The directory to search for files
        pattern (str): The file pattern to match (supports wildcards)
    
    Raises:
        ValueError: If directory or pattern is empty
        FileNotFoundError: If directory doesn't exist
    """
    # Input validation
    if not directory or not pattern:
        raise ValueError("Directory and pattern cannot be empty")
    
    # Validate directory exists
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist")
    
    # Compile regex pattern
    try:
        regex = re.compile(pattern)
    except re.error:
        raise ValueError("Invalid regex pattern")
    
    # Find and delete matching files
    for root, _, files in os.walk(directory):
        for filename in files:
            if regex.search(filename):
                file_path = os.path.join(root, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <pattern>")
        sys.exit(1)
    
    try:
        find_and_delete_files(sys.argv[1], sys.argv[2])
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)