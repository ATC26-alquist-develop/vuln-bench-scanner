import os
import fnmatch
from pathlib import Path
import re

class SecureFileManager:
    def __init__(self, base_directory):
        # Validate and sanitize base directory path
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.exists() or not self.base_directory.is_dir():
            raise ValueError("Invalid base directory")

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
            
        # Sanitize pattern to prevent regex injection
        pattern = re.sub(r'[^a-zA-Z0-9_.*?]', '', pattern)
        
        matches = []
        try:
            for root, _, files in os.walk(self.base_directory):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        full_path = Path(root) / name
                        # Prevent path traversal
                        if self.base_directory in full_path.resolve().parents:
                            matches.append(str(full_path))
        except PermissionError:
            raise PermissionError("Insufficient permissions to access files")
            
        return matches