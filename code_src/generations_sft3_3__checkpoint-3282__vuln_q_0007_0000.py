import os
import pathlib
import stat
import logging
from typing import Optional
from pathlib import Path
import shutil

class SecureFileManager:
    def __init__(self, base_directory: str):
        """Initialize with a base directory for all operations."""
        # Convert to absolute path and validate
        self.base_dir = Path(base_directory).resolve()
        if not self.base_dir.exists() or not self.base_dir.is_dir():
            raise ValueError("Invalid base directory")
        
        # Setup logging
        logging.basicConfig(
            filename='file_manager.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Ensure directory permissions are secure
        self._secure_directory_permissions()

    def _secure_directory_permissions(self) -> None:
        """Set secure permissions on base directory."""
        try:
            # Remove existing permissions
            os.chmod(self.base_dir, stat.S_IRWXU)
            # Recursively apply permissions
            shutil.copystat(self.base_dir, self.base_dir / '')
        except Exception as e:
            logging.error(f"Failed to set directory permissions: {e}")
            raise

    def _validate_path(self, file_path: str) -> Path:
        """Validate and sanitize file path."""
        try:
            # Resolve path to prevent directory traversal
            full_path = (self.base_dir / file_path).resolve()
            # Ensure path is within base directory
            if not str(full_path).startswith(str(self.base_dir)):
                raise ValueError("Access denied: Path outside base directory")
            return full_path
        except Exception as e:
            logging.error(f"Path validation failed: {e}")
            raise

    def create_file(self, file_path: str, content: str) -> None:
        """Securely create a file with content."""
        try:
            full_path = self._validate_path(file_path)
            # Create file with secure permissions
            with open(full_path, 'w', encoding='utf-8') as f:
                os.chmod(full_path, stat.S_IRUSR | stat.S_IWUSR)
                f.write(content)
            logging.info(f"File created: {file_path}")
        except Exception as e:
            logging.error(f"Failed to create file: {e}")
            raise

    def read_file(self, file_path: str) -> Optional[str]:
        """Securely read a file's contents."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.is_file():
                raise ValueError("Not a valid file")
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logging.info(f"File read: {file_path}")
            return content
        except Exception as e:
            logging.error(f"Failed to read file: {e}")
            raise

    def delete_file(self, file_path: str) -> None:
        """Securely delete a file."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.is_file():
                raise ValueError("Not a valid file")
            os.remove(full_path)
            logging.info(f"File deleted: {file_path}")
        except Exception as e:
            logging.error(f"Failed to delete file: {e}")
            raise

    def list_files(self) -> list[str]:
        """Securely list files in the base directory."""
        try:
            files = [f.name for f in self.base_dir.iterdir() 
                    if f.is_file() and f.resolve().parent == self.base_dir]
            logging.info("Files listed")
            return files
        except Exception as e:
            logging.error(f"Failed to list files: {e}")
            raise