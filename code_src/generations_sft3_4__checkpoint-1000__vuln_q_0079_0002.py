import os
import fnmatch
import re
from typing import List, Optional

class SecureFileManager:
    def __init__(self, base_directory: str):
        self.base_directory = os.path.abspath(base_directory)
        if not os.path.exists(self.base_directory):
            raise ValueError("Base directory does not exist")

    def search_files(self, pattern: str) -> List[str]:
        """
        Search for files matching the given pattern in the base directory.
        
        Args:
            pattern (str): The search pattern (supports wildcards)
            
        Returns:
            List[str]: List of matching file paths
            
        Raises:
            ValueError: If the pattern is invalid
        """
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Invalid pattern")

        # Validate pattern to prevent injection attacks
        if not re.match(r'^[a-zA-Z0-9_\-./]*$', pattern):
            raise ValueError("Invalid characters in pattern")

        results = []
        for root, _, files in os.walk(self.base_directory):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    full_path = os.path.join(root, filename)
                    # Resolve to absolute path to prevent directory traversal
                    results.append(os.path.abspath(full_path))
        return results

    def get_file_contents(self, file_path: str) -> Optional[str]:
        """
        Read the contents of a file securely.
        
        Args:
            file_path (str): The path to the file
            
        Returns:
            Optional[str]: File contents or None if file doesn't exist
            
        Raises:
            ValueError: If the file path is invalid
        """
        if not file_path or not isinstance(file_path, str):
            raise ValueError("Invalid file path")

        # Validate file path
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.base_directory, file_path)
        
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            # Log the error but don't expose details to the user
            print(f"Error reading file: {str(e)}")
            return None