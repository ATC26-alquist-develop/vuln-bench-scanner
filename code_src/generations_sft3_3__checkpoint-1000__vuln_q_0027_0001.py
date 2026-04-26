import os
from pathlib import Path
import logging
from typing import Optional

class SecureFileHandler:
    def __init__(self, file_path: str):
        """Initialize with a file path and set up logging."""
        self.file_path = Path(file_path).resolve()
        self.logger = logging.getLogger(__name__)
        
        # Ensure the file path is within allowed directory
        allowed_dir = Path.cwd()
        if not self.file_path.is_relative_to(allowed_dir):
            raise ValueError("File path must be within current working directory")
            
        # Create parent directories if they don't exist
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def read_file(self) -> Optional[str]:
        """Securely read file contents."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            self.logger.error(f"Error reading file: {e}")
            return None

    def write_file(self, content: str) -> bool:
        """Securely write content to file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except IOError as e:
            self.logger.error(f"Error writing to file: {e}")
            return False

    def append_file(self, content: str) -> bool:
        """Securely append content to file."""
        try:
            with open(self.file_path, 'a', encoding='utf-8') as file:
                file.write(content)
            return True
        except IOError as e:
            self.logger.error(f"Error appending to file: {e}")
            return False

    def delete_file(self) -> bool:
        """Securely delete the file."""
        try:
            os.remove(self.file_path)
            return True
        except OSError as e:
            self.logger.error(f"Error deleting file: {e}")
            return False