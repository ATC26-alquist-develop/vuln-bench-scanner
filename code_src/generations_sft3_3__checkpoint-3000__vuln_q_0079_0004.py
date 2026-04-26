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
    if not directory or not pattern:
        raise ValueError("Directory and pattern cannot be empty")
    
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist")
    
    try:
        for filename in os.listdir(directory):
            if re.match(pattern, filename):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                elif os.path.isdir(file_path):
                    print(f"Skipped directory: {file_path}")
    except PermissionError:
        print(f"Permission denied: Unable to access {directory}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <pattern>")
        sys.exit(1)
    
    try:
        directory = sys.argv[1]
        pattern = sys.argv[2]
        find_and_delete_files(directory, pattern)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)