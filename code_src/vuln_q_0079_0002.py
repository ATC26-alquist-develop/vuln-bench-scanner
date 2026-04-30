import os
import fnmatch
from pathlib import Path
import re

class SecureFileManager:
    def __init__(self, base_directory):
        """Initialize with a base directory, ensuring it's absolute and exists."""
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.is_dir():
            raise ValueError("Invalid base directory")

    def _sanitize_filename(self, filename):
        """Sanitize filename to prevent path traversal attacks."""
        return re.sub(r'[^\w\-_\. ]', '_', filename)

    def search_files(self, pattern, max_depth=5):
        """Securely search files with wildcards, limiting depth."""
        if not isinstance(pattern, str) or not pattern:
            raise ValueError("Invalid search pattern")
        
        sanitized_pattern = self._sanitize_filename(pattern)
        results = []
        current_dir = self.base_directory
        
        for _ in range(max_depth):
            try:
                for item in current_dir.iterdir():
                    if item.is_file() and fnmatch.fnmatch(item.name, sanitized_pattern):
                        results.append(str(item.relative_to(self.base_directory)))
                if not any(current_dir.iterdir()):  # No more files to search
                    break
                current_dir = current_dir / next(current_dir.iterdir())  # Move to next directory
            except PermissionError:
                break  # Stop if we don't have permission to access a directory
        
        return results