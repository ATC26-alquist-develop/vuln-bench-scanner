import os
import fnmatch
from pathlib import Path

class SecureFileManager:
    def __init__(self, base_directory):
        # Validate and resolve base directory
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
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Invalid pattern")

        # Convert to absolute path and resolve any symlinks
        search_path = str(self.base_directory.absolute().resolve())
        
        # Validate pattern
        if not pattern.startswith('*') and not pattern.endswith('*'):
            pattern = '*' + pattern + '*'
            
        matches = []
        
        try:
            for root, _, files in os.walk(search_path):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        full_path = os.path.join(root, name)
                        # Resolve to absolute path to avoid symlink attacks
                        matches.append(os.path.abspath(os.path.realpath(full_path)))
        except PermissionError:
            raise PermissionError("Permission denied accessing some directories")
            
        return matches