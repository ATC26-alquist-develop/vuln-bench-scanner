import os
import fnmatch
from pathlib import Path

class SecureFileManager:
    def __init__(self, base_directory):
        # Validate and resolve base directory
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.is_dir():
            raise ValueError("Base directory must be a valid directory")

    def search_files(self, pattern):
        """
        Search for files matching the given pattern in the base directory.
        
        Args:
            pattern (str): Wildcard pattern to match file names against
            
        Returns:
            list: List of matching file paths
            
        Raises:
            ValueError: If pattern is invalid
        """
        if not pattern or len(pattern) > 100:  # Limit pattern length
            raise ValueError("Invalid pattern length")
            
        try:
            # Convert to absolute path and resolve any symlinks
            base_path = self.base_directory.absolute().resolve()
            
            # Validate pattern
            if not pattern or pattern.startswith('/'):
                raise ValueError("Pattern cannot start with /")
            
            # Perform search using pathlib
            matching_files = []
            for file_path in base_path.rglob(pattern):
                if file_path.is_file():
                    matching_files.append(str(file_path))
                    
            return matching_files
            
        except Exception as e:
            # Log error here if needed
            raise ValueError(f"Error searching files: {str(e)}")

# Example usage:
if __name__ == "__main__":
    try:
        manager = SecureFileManager("/path/to/search/directory")
        results = manager.search_files("*.txt")
        print(results)
    except ValueError as e:
        print(f"Error: {e}")