import os
import shutil
from pathlib import Path
import logging
from typing import List, Optional

class SecureFileManager:
    def __init__(self, base_path: str):
        """Initialize the file manager with a base path."""
        self.base_path = Path(base_path).resolve()
        if not self.base_path.exists():
            raise ValueError("Base path does not exist")
        self.logger = logging.getLogger(__name__)

    def _sanitize_path(self, path: str) -> Path:
        """Sanitize and resolve the given path."""
        full_path = (self.base_path / path).resolve()
        if not str(full_path).startswith(str(self.base_path)):
            raise ValueError("Access denied: Path outside base directory")
        return full_path

    def list_files(self, user_path: str) -> List[str]:
        """List files in a directory based on user access."""
        try:
            path = self._sanitize_path(user_path)
            if not path.is_dir():
                raise ValueError("Invalid directory")
            return [f.name for f in path.iterdir() if f.is_file()]
        except Exception as e:
            self.logger.error(f"Error listing files: {str(e)}")
            raise

    def create_file(self, user_path: str, filename: str, content: str) -> None:
        """Create a new file with given content."""
        try:
            path = self._sanitize_path(user_path)
            if not path.is_dir():
                raise ValueError("Invalid directory")
            file_path = path / filename
            with open(file_path, 'w') as f:
                f.write(content)
            self.logger.info(f"File created: {file_path}")
        except Exception as e:
            self.logger.error(f"Error creating file: {str(e)}")
            raise

    def delete_file(self, user_path: str, filename: str) -> None:
        """Delete a file based on user access."""
        try:
            path = self._sanitize_path(user_path)
            if not path.is_dir():
                raise ValueError("Invalid directory")
            file_path = path / filename
            if not file_path.is_file():
                raise ValueError("File does not exist")
            os.remove(file_path)
            self.logger.info(f"File deleted: {file_path}")
        except Exception as e:
            self.logger.error(f"Error deleting file: {str(e)}")
            raise

    def read_file(self, user_path: str, filename: str) -> str:
        """Read content of a file based on user access."""
        try:
            path = self._sanitize_path(user_path)
            if not path.is_dir():
                raise ValueError("Invalid directory")
            file_path = path / filename
            if not file_path.is_file():
                raise ValueError("File does not exist")
            with open(file_path, 'r') as f:
                content = f.read()
            self.logger.info(f"File read: {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"Error reading file: {str(e)}")
            raise