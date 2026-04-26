import os
from pathlib import Path
from typing import Optional

class SecureFileHandler:
    def __init__(self, file_path: str):
        """Initialize with file path and validate it exists."""
        self.file_path = Path(file_path).resolve()
        if not self.file_path.exists():
            raise ValueError("File does not exist")
        
        # Ensure the file is not a symlink
        if self.file_path.is_symlink():
            raise ValueError("Symlinks are not allowed")
            
        # Check if we have read/write permissions
        if not os.access(self.file_path, os.R_OK | os.W_OK):
            raise PermissionError("Insufficient permissions")

    def read_file(self) -> Optional[str]:
        """Securely read file contents."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading file: {e}")
            return None

    def write_file(self, content: str) -> bool:
        """Securely write content to file."""
        try:
            # Create a temporary file
            temp_path = self.file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            # Rename temp file to target file
            os.replace(temp_path, self.file_path)
            return True
        except IOError as e:
            print(f"Error writing file: {e}")
            return False

    def delete_file(self) -> bool:
        """Securely delete the file."""
        try:
            os.remove(self.file_path)
            return True
        except OSError as e:
            print(f"Error deleting file: {e}")
            return False