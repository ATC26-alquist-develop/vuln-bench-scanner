import os
import fnmatch
from typing import List, Optional

class FileManager:
    def __init__(self, base_path: str):
        """Initialize FileManager with a base directory path."""
        self.base_path = os.path.abspath(base_path)
        if not os.path.exists(self.base_path):
            raise ValueError("Base path does not exist")

    def _is_safe_path(self, path: str) -> bool:
        """Check if the given path is safe (within base directory)."""
        return os.path.abspath(path).startswith(self.base_path)

    def search_files(self, pattern: str) -> List[str]:
        """Search for files matching the given pattern within the base directory."""
        if not pattern:
            raise ValueError("Pattern cannot be empty")
        
        matched_files = []
        for root, _, files in os.walk(self.base_path):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    full_path = os.path.join(root, filename)
                    if self._is_safe_path(full_path):
                        matched_files.append(full_path)
        return matched_files

    def list_files(self) -> List[str]:
        """List all files in the base directory."""
        return [f for f in os.listdir(self.base_path) 
                if os.path.isfile(os.path.join(self.base_path, f))]

    def read_file(self, filename: str) -> Optional[str]:
        """Read the contents of a file."""
        if not self._is_safe_path(filename):
            raise ValueError("Access denied: File outside base directory")
        
        try:
            with open(filename, 'r') as file:
                return file.read()
        except IOError as e:
            raise IOError(f"Error reading file: {e}")