import os
import fnmatch
from pathlib import Path
from typing import List, Optional

class FileManager:
    def __init__(self, base_directory: str):
        """Initialize file manager with a base directory."""
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.exists():
            raise ValueError("Base directory does not exist")

    def search_files(self, pattern: str) -> List[str]:
        """
        Search for files matching the given pattern in the base directory.
        
        Args:
            pattern: Wildcard pattern to match file names against
            
        Returns:
            List of matching file paths
            
        Raises:
            ValueError: If pattern is invalid
        """
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Invalid pattern")

        try:
            # Convert to absolute path and resolve any symlinks
            base_path = self.base_directory.absolute().resolve()
            
            # Validate pattern
            if not pattern.startswith('*') and not pattern.endswith('*'):
                pattern = '*' + pattern
            
            # Perform search
            matches = []
            for root, _, files in os.walk(base_path):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        full_path = Path(root) / name
                        # Resolve to absolute path to avoid symlink attacks
                        resolved_path = full_path.resolve()
                        if resolved_path.is_file() and resolved_path.is_relative_to(base_path):
                            matches.append(str(resolved_path))
            
            return matches
        except Exception as e:
            raise RuntimeError(f"Error searching files: {str(e)}")

    def get_file_size(self, file_path: str) -> Optional[int]:
        """
        Get the size of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes or None if file doesn't exist
            
        Raises:
            ValueError: If file_path is invalid
        """
        if not file_path or not isinstance(file_path, str):
            raise ValueError("Invalid file path")

        try:
            path = Path(file_path).resolve()
            if not path.is_file():
                return None
            
            # Resolve to absolute path to avoid symlink attacks
            resolved_path = path.resolve()
            if not resolved_path.is_relative_to(self.base_directory):
                return None
                
            return resolved_path.stat().st_size
        except Exception as e:
            raise RuntimeError(f"Error getting file size: {str(e)}")

    def list_directory(self, directory: str) -> List[str]:
        """
        List contents of a directory.
        
        Args:
            directory: Directory to list
            
        Returns:
            List of file/directory names
            
        Raises:
            ValueError: If directory is invalid
        """
        if not directory or not isinstance(directory, str):
            raise ValueError("Invalid directory")

        try:
            path = Path(directory).resolve()
            if not path.is_dir():
                raise ValueError("Not a directory")
            
            # Resolve to absolute path to avoid symlink attacks
            resolved_path = path.resolve()
            if not resolved_path.is_relative_to(self.base_directory):
                raise ValueError("Directory outside base path")
                
            return [str(f.relative_to(self.base_directory)) for f in resolved_path.iterdir() 
                    if f.is_file() or f.is_dir()]
        except Exception as e:
            raise RuntimeError(f"Error listing directory: {str(e)}")