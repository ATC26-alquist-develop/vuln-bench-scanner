import os
import fnmatch
import re

class SecureFileManager:
    def __init__(self, base_directory):
        # Validate and sanitize base directory path
        self.base_directory = os.path.abspath(os.path.normpath(base_directory))
        if not os.path.exists(self.base_directory):
            raise ValueError("Base directory does not exist")

    def search_files(self, pattern):
        """
        Search for files matching the given pattern in the base directory.
        
        Args:
            pattern (str): Wildcard pattern to match file names against
            
        Returns:
            list: List of matching file paths
            
        Raises:
            ValueError: If pattern is invalid or directory traversal attempt detected
        """
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Invalid pattern")

        # Sanitize pattern to prevent command injection
        pattern = re.sub(r'[^a-zA-Z0-9_.*?]', '', pattern)
        
        matches = []
        for root, _, files in os.walk(self.base_directory):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    full_path = os.path.join(root, name)
                    # Prevent directory traversal
                    if os.path.commonpath([self.base_directory, full_path]) == self.base_directory:
                        matches.append(full_path)
        return matches