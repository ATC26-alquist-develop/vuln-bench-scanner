import os
import re
import sys

def sanitize_path(path):
    """Sanitize and validate the provided path."""
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    
    # Convert to absolute path and resolve any symlinks
    path = os.path.abspath(os.path.realpath(path))
    
    # Check if path exists and is a directory
    if not os.path.isdir(path):
        raise ValueError(f"Path does not exist or is not a directory: {path}")
    
    return path

def sanitize_pattern(pattern):
    """Sanitize the search pattern."""
    if not isinstance(pattern, str):
        raise ValueError("Pattern must be a string")
    
    # Remove any potentially dangerous characters
    pattern = re.sub(r'[^a-zA-Z0-9_\-.*?]', '', pattern)
    
    # Ensure pattern starts with a valid regex character
    if not pattern or not re.match(r'^[a-zA-Z0-9_\-.*?]', pattern):
        raise ValueError("Invalid pattern")
    
    return pattern

def find_and_delete_files(directory, pattern):
    """Find and delete files matching the pattern in the given directory."""
    try:
        sanitized_dir = sanitize_path(directory)
        sanitized_pattern = sanitize_pattern(pattern)
        
        for root, _, files in os.walk(sanitized_dir):
            for filename in files:
                if re.match(sanitized_pattern, filename):
                    file_path = os.path.join(root, filename)
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except OSError as e:
                        print(f"Error deleting {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <pattern>")
        sys.exit(1)
    
    try:
        find_and_delete_files(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)