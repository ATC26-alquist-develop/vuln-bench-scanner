import os
from pathlib import Path
from typing import Optional

class SecureFileHandler:
    def __init__(self, file_path: str):
        """Initialize with file path and validate it exists."""
        self.file_path = Path(file_path).resolve()
        if not self.file_path.exists():
            raise ValueError("File does not exist")
        if not self.file_path.is_file():
            raise ValueError("Path is not a file")

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
            # Create parent directory if it doesn't exist
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write with explicit encoding
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except IOError as e:
            print(f"Error writing to file: {e}")
            return False

    def delete_file(self) -> bool:
        """Securely delete the file."""
        try:
            os.remove(self.file_path)
            return True
        except OSError as e:
            print(f"Error deleting file: {e}")
            return False