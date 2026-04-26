```python
import os
import stat
import logging
from pathlib import Path
from typing import List, Optional
import secrets
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureFileManager:
    def __init__(self, base_directory: str):
        """Initialize with a base directory for all operations."""
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.exists():
            raise ValueError("Base directory does not exist")
        
        # Ensure directory is absolute and normalized
        self.base_directory = self.base_directory.absolute()
        
        # Verify directory permissions
        if not os.access(self.base_directory, os.W_OK):
            raise PermissionError("Insufficient permissions for base directory")

    def _validate_path(self, file_path: str) -> Path:
        """Validate and normalize file path."""
        try:
            full_path = (self.base_directory / file_path).resolve()
            if not str(full_path).startswith(str(self.base_directory)):
                raise ValueError("Access denied: Path outside base directory")
            return full_path
        except Exception as e:
            logger.error(f"Path validation error: {str(e)}")
            raise ValueError("Invalid path")

    def create_file(self, file_path: str, content: str) -> None:
        """Securely create a file with proper permissions."""
        try:
            full_path = self._validate_path(file_path)
            if full_path.exists():
                raise FileExistsError("File already exists")
            
            # Create file with secure permissions (read/write for owner only)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Set secure permissions (0600)
            os.chmod(full_path, stat.S_IRUSR | stat.S_IWUSR)
            
            logger.info(f"File created: {file_path}")
        except Exception as e:
            logger.error(f"File creation error: {str(e)}")
            raise

    def read_file(self, file_path: str) -> Optional[str]:
        """Securely read a file's contents."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.exists():
                raise FileNotFoundError("File not found")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"File read: {file_path}")
            return content
        except Exception as e:
            logger.error(f"File reading error: {str(e)}")
            raise

    def list_files(self) -> List[str]:
        """Securely list files in the directory."""
        try:
            files = [f.name for f in self.base_directory.iterdir() 
                    if f.is_file() and f.resolve().parent == self.base_directory]
            logger.info("Files listed")
            return files
        except Exception as e:
            logger.error(f"File listing error: {str(e)}")
            raise

    def delete_file(self, file_path: str) -> None:
        """Securely delete a file."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.exists():
                raise FileNotFoundError("File not found")
            
            os.remove(full_path)
            logger.info(f"File deleted: {file_path}")
        except Exception as e:
            logger.error(f"File deletion error: {str(e)}")
            raise

    def set_file_permissions(self, file_path: str, owner: str, group: str) -> None:
        """Set secure file permissions."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.exists():
                raise FileNotFoundError("File not found")
            
            # Set secure permissions (read/write for owner only)
            os.chmod(full_path, stat.S_IRUSR | stat