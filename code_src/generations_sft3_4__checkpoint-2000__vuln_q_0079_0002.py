import os
import fnmatch
import re
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
            ValueError: If pattern is invalid or directory traversal attempt detected
        """
        # Validate pattern
        if not pattern or len(pattern) > 100:
            raise ValueError("Invalid pattern")
            
        # Sanitize pattern to prevent command injection
        pattern = re.sub(r'[^a-zA-Z0-9_\-.*?]', '', pattern)
        
        # Prevent directory traversal
        if self.base_directory in self.base_directory.match(pattern):
            matching_files = []
            for root, _, files in os.walk(self.base_directory):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        matching_files.append(Path(root) / name)
            return matching_files
        else:
            raise ValueError("Directory traversal attempt detected")

    def read_file(self, file_path):
        """
        Read contents of a file safely.
        
        Args:
            file_path (str): Path to the file to read
            
        Returns:
            str: File contents
            
        Raises:
            ValueError: If file path is invalid or file cannot be read
        """
        try:
            file_path = Path(file_path).resolve()
            if not file_path.is_file():
                raise ValueError("Invalid file path")
                
            # Ensure file is within base directory
            if self.base_directory not in file_path.parents:
                raise ValueError("Access denied: File is outside base directory")
                
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")