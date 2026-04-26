import os
import fnmatch
from pathlib import Path

class SecureFileManager:
    def __init__(self, base_directory):
        # Validate and resolve base directory
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.is_dir():
            raise ValueError("Base directory does not exist or is not a directory")

    def search_files(self, pattern):
        """
        Search for files matching the given pattern in the base directory.
        
        Args:
            pattern (str): Wildcard pattern to match file names against
            
        Returns:
            list: List of matching file paths
            
        Raises:
            ValueError: If the pattern is invalid
        """
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Pattern must be a non-empty string")

        # Sanitize the pattern to prevent directory traversal
        sanitized_pattern = os.path.basename(pattern)
        if not sanitized_pattern:
            raise ValueError("Invalid pattern")

        matches = []
        for root, _, files in os.walk(self.base_directory):
            for filename in fnmatch.filter(files, sanitized_pattern):
                full_path = Path(root) / filename
                if full_path.resolve().is_relative_to(self.base_directory):
                    matches.append(str(full_path))
        return matches