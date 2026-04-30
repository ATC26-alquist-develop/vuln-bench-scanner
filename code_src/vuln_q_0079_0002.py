import os
import fnmatch
from typing import List, Optional

class SecureFileManager:
    def __init__(self, base_directory: str):
        """Initialize with a base directory, ensuring it's absolute and exists."""
        self.base_directory = os.path.abspath(base_directory)
        if not os.path.exists(self.base_directory):
            raise ValueError("Base directory does not exist")

    def _validate_path(self, path: str) -> str:
        """Validate and return an absolute path, preventing directory traversal."""
        full_path = os.path.abspath(os.path.join(self.base_directory, path))
        if not full_path.startswith(self.base_directory):
            raise ValueError("Access denied: Attempted directory traversal")
        return full_path

    def search_files(self, pattern: str) -> List[str]:
        """Search for files matching the given pattern, using wildcards."""
        if not pattern:
            raise ValueError("Pattern cannot be empty")
        
        try:
            matches = []
            for root, _, files in os.walk(self.base_directory):
                for filename in files:
                    if fnmatch.fnmatch(filename, pattern):
                        matches.append(os.path.join(root, filename))
            return matches
        except Exception as e:
            raise RuntimeError(f"Error searching files: {str(e)}")

    def list_files(self) -> List[str]:
        """List all files in the base directory."""
        try:
            return [f for f in os.listdir(self.base_directory) if os.path.isfile(os.path.join(self.base_directory, f))]
        except Exception as e:
            raise RuntimeError(f"Error listing files: {str(e)}")

    def read_file(self, filename: str) -> Optional[str]:
        """Read the contents of a file."""
        try:
            file_path = self._validate_path(filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise RuntimeError(f"Error reading file: {str(e)}")