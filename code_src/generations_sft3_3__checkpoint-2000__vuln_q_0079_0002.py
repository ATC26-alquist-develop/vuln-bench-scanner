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
            ValueError: If pattern contains invalid characters
        """
        # Validate pattern
        if not pattern or len(pattern) > 100:
            raise ValueError("Invalid pattern")
            
        # Sanitize pattern to prevent command injection
        pattern = re.sub(r'[^a-zA-Z0-9_\-.*?]', '', pattern)
        
        # Perform search
        matching_files = []
        for root, _, files in os.walk(self.base_directory):
            for filename in fnmatch.filter(files, pattern):
                matching_files.append(os.path.join(root, filename))
                
        return matching_files

    def get_file_contents(self, filename):
        """
        Read contents of a file safely.
        
        Args:
            filename (str): Name of the file to read
            
        Returns:
            str: File contents
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file is not readable
            ValueError: If filename is invalid
        """
        # Validate filename
        if not filename or len(filename) > 100:
            raise ValueError("Invalid filename")
            
        # Sanitize filename
        filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '', filename)
        
        file_path = os.path.join(self.base_directory, filename)
        
        # Validate file path
        if not file_path.startswith(str(self.base_directory)):
            raise ValueError("Access denied: File is outside base directory")
            
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {filename}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except PermissionError:
            raise PermissionError(f"Permission denied: Unable to read {filename}")
        except IOError as e:
            raise IOError(f"Error reading file {filename}: {str(e)}")