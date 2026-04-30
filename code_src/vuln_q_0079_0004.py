```python
import os
import fnmatch
import stat
from pathlib import Path

def secure_delete_files(directory: str, pattern: str) -> None:
    """
    Securely delete files matching the specified pattern in the given directory.
    
    Args:
        directory: The directory to search in
        pattern: The file pattern to match (e.g., '*.tmp')
    """
    try:
        # Convert to absolute path and resolve any symlinks
        directory = os.path.abspath(os.path.realpath(directory))
        
        # Ensure directory exists and is a directory
        if not os.path.isdir(directory):
            raise ValueError("Invalid directory path")
            
        # Iterate through files in directory
        for root, _, files in os.walk(directory):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    file_path = os.path.join(root, filename)
                    
                    # Verify file exists and is a regular file
                    if os.path.isfile(file_path):
                        try:
                            # Securely delete the file
                            os.chmod(file_path, stat.S_IWRITE)  # Ensure write permission
                            os.remove(file_path)
                            os.chmod(file_path, stat.S_IWRITE)  # Revert permissions
                        except OSError as e:
                            print(f"Error deleting {file_path}: {e}")
                            
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
# secure_delete_files('/path/to/directory', '*.tmp')
```