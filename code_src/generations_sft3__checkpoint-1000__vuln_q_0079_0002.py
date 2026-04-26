import os
import fnmatch
from pathlib import Path

class SecureFileManager:
    def __init__(self, base_directory):
        # Validate and sanitize the base directory path
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.is_dir():
            raise ValueError("Invalid base directory")

    def search_files(self, pattern):
        """
        Search for files matching the given pattern in the base directory.
        
        Args:
            pattern (str): The file pattern to search for (supports wildcards)
            
        Returns:
            list: A list of matching file paths
            
        Raises:
            ValueError: If the pattern is invalid
        """
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Invalid pattern")

        # Sanitize the pattern to prevent path traversal attacks
        sanitized_pattern = os.path.normpath(pattern)
        if not sanitized_pattern.startswith(os.path.sep):
            raise ValueError("Invalid pattern")

        # Use pathlib for secure path handling
        for root, _, files in os.walk(self.base_directory):
            for filename in fnmatch.filter(files, sanitized_pattern):
                yield os.path.join(root, filename)

    def list_files(self):
        """
        List all files in the base directory.
        
        Returns:
            list: A list of file paths
        """
        return [str(f) for f in self.base_directory.rglob('*') if f.is_file()]

# Example usage:
if __name__ == "__main__":
    try:
        manager = SecureFileManager("/path/to/base/directory")
        
        # Search for files
        for file in manager.search_files("*.txt"):
            print(file)
        
        # List all files
        for file in manager.list_files():
            print(file)
            
    except ValueError as e:
        print(f"Error: {e}")