```python
import os
import fnmatch
from typing import List, Optional

class SecureFileManager:
    def __init__(self, base_directory: str):
        """Initialize file manager with a base directory."""
        # Validate and create absolute path
        self.base_directory = os.path.abspath(base_directory)
        
        # Verify base directory exists and is accessible
        if not os.path.exists(self.base_directory):
            raise ValueError("Base directory does not exist")
        if not os.path.isdir(self.base_directory):
            raise ValueError("Base path must be a directory")
        
        # Check if we have read permissions
        if not os.access(self.base_directory, os.R_OK):
            raise PermissionError("No read permission for base directory")

    def search_files(self, pattern: str) -> List[str]:
        """Search for files matching the pattern in the base directory and its subdirectories.
        
        Args:
            pattern: A file pattern with wildcards (e.g., '*.txt')
            
        Returns:
            List of matching file paths
            
        Raises:
            ValueError: If pattern is invalid
        """
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Pattern must be a non-empty string")
            
        # Validate pattern (only allow simple wildcards)
        if not self._is_valid_pattern(pattern):
            raise ValueError("Invalid pattern")

        matches: List[str] = []
        
        # Walk through directory tree
        for root, _, files in os.walk(self.base_directory):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    # Construct full path and add to results
                    full_path = os.path.join(root, filename)
                    matches.append(os.path.normpath(full_path))
                    
        return matches

    def _is_valid_pattern(self, pattern: str) -> bool:
        """Validate the search pattern for security.
        
        Args:
            pattern: The pattern to validate
            
        Returns:
            True if pattern is valid, False otherwise
        """
        # Only allow simple wildcards
        return all(c in '*?' or c.isalnum() or c in '_-' for c in pattern)

# Example usage:
if __name__ == "__main__":
    try:
        # Create manager with current directory
        manager = SecureFileManager('.')
        
        # Search for text files
        txt_files = manager.search_files('*.txt')
        print("Text files:", txt_files)
        
        # Search for Python files
        py_files = manager.search_files('*.py')
        print("Python files:", py_files)
        
    except (ValueError, PermissionError) as e:
        print(f"Error: {str(e)}")
```