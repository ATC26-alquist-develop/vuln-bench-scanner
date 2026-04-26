```python
import os
import stat
import pathlib
import logging
from typing import List, Optional
from pathlib import Path
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureFileManager:
    def __init__(self, base_directory: str):
        """Initialize with a base directory for all operations."""
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.exists():
            raise ValueError("Base directory does not exist")
        if not self.base_directory.is_dir():
            raise ValueError("Base directory must be a directory")

    def _validate_path(self, file_path: str) -> Path:
        """Validate and resolve file path to prevent path traversal."""
        try:
            full_path = (self.base_directory / file_path).resolve()
            if not str(full_path).startswith(str(self.base_directory)):
                raise ValueError("Access denied: Path outside base directory")
            return full_path
        except Exception as e:
            logger.error(f"Path validation error: {e}")
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
            logger.error(f"File creation error: {e}")
            raise

    def read_file(self, file_path: str) -> Optional[str]:
        """Securely read a file's contents."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.is_file():
                raise FileNotFoundError("File does not exist")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"File read: {file_path}")
            return content
        except Exception as e:
            logger.error(f"File reading error: {e}")
            raise

    def list_files(self) -> List[str]:
        """Securely list files in the base directory."""
        try:
            files = [f.name for f in self.base_directory.iterdir() 
                    if f.is_file() and f.is_relative_to(self.base_directory)]
            logger.info("Files listed")
            return files
        except Exception as e:
            logger.error(f"File listing error: {e}")
            raise

    def delete_file(self, file_path: str) -> None:
        """Securely delete a file."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.is_file():
                raise FileNotFoundError("File does not exist")
            
            os.remove(full_path)
            logger.info(f"File deleted: {file_path}")
        except Exception as e:
            logger.error(f"File deletion error: {e}")
            raise

    def copy_file(self, src_path: str, dst_path: str) -> None:
        """Securely copy a file."""
        try:
            src_full = self._validate_path(src_path)
            dst_full = self._validate_path(dst_path)
            
            if not src_full.is_file():
                raise FileNotFoundError("Source file does not exist")
            
            shutil.copy2(src_full, dst_full)
            os.chmod(dst_full, stat.S_IRUSR | stat.S_IWUSR)
            logger.info(f"File copied: {src_path} -> {dst_path}")
        except Exception