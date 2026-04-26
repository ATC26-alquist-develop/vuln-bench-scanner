import os
from pathlib import Path
import logging
from typing import Optional

class SecureFileHandler:
    def __init__(self, file_path: str):
        """Initialize with file path and set up logging."""
        self.file_path = Path(file_path).resolve()
        self.logger = logging.getLogger(__name__)
        
        # Ensure the file path is within allowed directory
        allowed_dir = Path.cwd()
        if not self.file_path.is_relative_to(allowed_dir):
            raise ValueError("File path must be within current working directory")
            
        # Ensure file is not a symlink
        if self.file_path.is_symlink():
            raise ValueError("Symlinks are not allowed")
            
        # Ensure file has correct permissions
        if not os.access(self.file_path.parent, os.W_OK):
            raise PermissionError("No write permission for file or directory")
            
    def read_file(self) -> Optional[str]:
        """Securely read file contents."""
        try:
            if not self.file_path.is_file():
                self.logger.error(f"File does not exist: {self.file_path}")
                return None
                
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"Error reading file: {str(e)}")
            return None
            
    def write_file(self, content: str) -> bool:
        """Securely write content to file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Error writing file: {str(e)}")
            return False

# Example usage:
if __name__ == "__main__":
    try:
        handler = SecureFileHandler("example.txt")
        content = handler.read_file()
        if content:
            print(f"File contents: {content}")
        
        handler.write_file("Hello, World!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")