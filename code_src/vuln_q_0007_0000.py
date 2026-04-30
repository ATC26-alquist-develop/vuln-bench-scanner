```python
import os
import stat
import pathlib
import logging
from typing import Optional
from pathlib import Path
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureFileManager:
    def __init__(self, base_dir: str):
        """Initialize with base directory and set permissions"""
        self.base_dir = Path(base_dir).resolve()
        if not self.base_dir.is_dir():
            raise ValueError("Base directory must exist and be a directory")
        self._set_secure_permissions()

    def _set_secure_permissions(self):
        """Set secure permissions on base directory"""
        os.chmod(self.base_dir, stat.S_IRUSR | stat.S_IWUSR)
        logger.info(f"Secure permissions set on {self.base_dir}")

    def _is_safe_path(self, path: Path) -> bool:
        """Check if path is within base directory and safe"""
        try:
            resolved_path = path.resolve()
            return self.base_dir in resolved_path.parents and not resolved_path.is_relative_to(self.base_dir)
        except (RuntimeError, ValueError):
            return False

    def create_file(self, filename: str, content: Optional[str] = None) -> bool:
        """Create a new file with secure permissions"""
        file_path = (self.base_dir / filename).resolve()
        if not self._is_safe_path(file_path):
            logger.error(f"Attempted access outside base directory: {file_path}")
            return False
        try:
            with open(file_path, 'x', encoding='utf-8') as f:
                if content:
                    f.write(content)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
            logger.info(f"File created: {file_path}")
            return True
        except FileExistsError:
            logger.error(f"File already exists: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return False

    def read_file(self, filename: str) -> Optional[str]:
        """Securely read file contents"""
        file_path = (self.base_dir / filename).resolve()
        if not self._is_safe_path(file_path):
            logger.error(f"Attempted access outside base directory: {file_path}")
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"File read: {file_path}")
            return content
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None

    def delete_file(self, filename: str) -> bool:
        """Securely delete a file"""
        file_path = (self.base_dir / filename).resolve()
        if not self._is_safe_path(file_path):
            logger.error(f"Attempted access outside base directory: {file_path}")
            return False
        try:
            os.remove(file_path)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
            logger.info(f"File deleted: {file_path}")
            return True
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False

    def list_files(self) -> list:
        """Securely list files in base directory"""
        try:
            files = [f.name for f in self.base_dir.iterdir() if f.is_file()]
            logger.info(f"Files listed in base directory")
            return files
        except Exception as e:
            logger.error(f"Error listing files: