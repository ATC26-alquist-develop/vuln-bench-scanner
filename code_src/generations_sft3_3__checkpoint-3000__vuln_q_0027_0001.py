import os
from pathlib import Path
import logging
from typing import Optional

class SecureFileHandler:
    def __init__(self, base_directory: str):
        """
        Initialize secure file handler with a base directory.
        
        Args:
            base_directory: The base directory where files can be accessed
        """
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.exists():
            raise ValueError("Base directory does not exist")
        if not self.base_directory.is_dir():
            raise ValueError("Base directory is not a directory")
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_path(self, file_path: str) -> Path:
        """Validate and sanitize file path."""
        try:
            full_path = (self.base_directory / file_path).resolve()
            if not str(full_path).startswith(str(self.base_directory)):
                raise ValueError("Access denied: Path outside base directory")
            return full_path
        except Exception as e:
            self.logger.error(f"Path validation error: {e}")
            raise ValueError("Invalid file path")

    def read_file(self, file_path: str) -> Optional[str]:
        """Securely read file contents."""
        try:
            path = self._validate_path(file_path)
            if not path.is_file():
                self.logger.error(f"File not found: {file_path}")
                return None
            
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return None

    def write_file(self, file_path: str, content: str) -> bool:
        """Securely write content to file."""
        try:
            path = self._validate_path(file_path)
            
            # Create parent directories if they don't exist
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content with proper encoding
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Error writing to file {file_path}: {e}")
            return False