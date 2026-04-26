```python
import os
import pathlib
import logging
from typing import Optional
import stat
import shutil
from datetime import datetime
import secrets

class SecureFileManager:
    def __init__(self, base_directory: str, max_file_size: int = 100_000_000):
        """Initialize with base directory and maximum file size."""
        self.base_directory = pathlib.Path(base_directory).resolve()
        self.max_file_size = max_file_size
        
        # Setup logging
        logging.basicConfig(
            filename='file_manager.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Ensure base directory exists and is secure
        if not self.base_directory.exists():
            raise ValueError("Base directory does not exist")
        if not self.base_directory.is_dir():
            raise ValueError("Base path is not a directory")
            
    def _validate_path(self, file_path: str) -> pathlib.Path:
        """Validate and sanitize file path."""
        try:
            path = pathlib.Path(file_path).resolve()
            if not str(path).startswith(str(self.base_directory)):
                raise ValueError("Access denied: Path outside base directory")
            return path
        except Exception as e:
            logging.error(f"Path validation error: {str(e)}")
            raise ValueError("Invalid file path")

    def _check_permissions(self, path: pathlib.Path) -> bool:
        """Check if user has required permissions."""
        try:
            return os.access(path, os.R_OK | os.W_OK)
        except Exception:
            logging.error(f"Permission check failed for {path}")
            return False

    def create_file(self, filename: str, content: str) -> None:
        """Securely create a new file with content."""
        try:
            path = self._validate_path(filename)
            if not self._check_permissions(path):
                raise PermissionError("Insufficient permissions")
            
            # Create file with secure permissions
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Set secure permissions (read/write for owner only)
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
            
            logging.info(f"File created: {path}")
        except Exception as e:
            logging.error(f"File creation failed: {str(e)}")
            raise

    def read_file(self, filename: str) -> Optional[str]:
        """Securely read a file's contents."""
        try:
            path = self._validate_path(filename)
            if not self._check_permissions(path):
                raise PermissionError("Insufficient permissions")
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            logging.info(f"File read: {path}")
            return content
        except Exception as e:
            logging.error(f"File read failed: {str(e)}")
            return None

    def delete_file(self, filename: str) -> None:
        """Securely delete a file."""
        try:
            path = self._validate_path(filename)
            if not self._check_permissions(path):
                raise PermissionError("Insufficient permissions")
            
            if path.exists():
                os.remove(path)
                logging.info(f"File deleted: {path}")
            else:
                logging.warning(f"File not found: {path}")
        except Exception as e:
            logging.error(f"File deletion failed: {str(e)}")
            raise

    def list_files(self) -> list[str]:
        """Securely list files in the directory."""
        try:
            files = []
            for item in self.base_directory.iterdir():
                if item.is_file():
                    files.append(str(item.name))
            return files
        except Exception as e:
            logging.error(f"File listing failed: {str(e)}")
            return []