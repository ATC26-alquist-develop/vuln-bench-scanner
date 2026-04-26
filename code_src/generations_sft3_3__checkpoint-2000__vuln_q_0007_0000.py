```python
import os
import pathlib
import logging
import stat
from typing import Optional
import shutil
from datetime import datetime
import secrets

class SecureFileManager:
    def __init__(self, base_directory: str, max_file_size: int = 100_000_000):
        """Initialize with strict security controls"""
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
            raise ValueError("Base path must be a directory")
        
        # Verify permissions
        if not os.access(self.base_directory, os.W_OK):
            raise ValueError("Insufficient permissions for base directory")

    def _validate_path(self, file_path: str) -> pathlib.Path:
        """Validate and sanitize file path"""
        try:
            path = pathlib.Path(file_path).resolve()
            if not str(path).startswith(str(self.base_directory)):
                raise ValueError("Access denied: Path outside base directory")
            return path
        except Exception as e:
            logging.error(f"Path validation error: {str(e)}")
            raise ValueError("Invalid path")

    def _check_file_size(self, file_path: pathlib.Path) -> None:
        """Check file size before operations"""
        if file_path.stat().st_size > self.max_file_size:
            raise ValueError("File exceeds maximum allowed size")

    def create_file(self, filename: str, content: str) -> None:
        """Securely create a new file"""
        try:
            path = self._validate_path(filename)
            if path.exists():
                raise ValueError("File already exists")
            
            # Create file with secure permissions
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Set secure permissions (read/write for owner only)
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
            
            logging.info(f"File created: {path}")
        except Exception as e:
            logging.error(f"File creation error: {str(e)}")
            raise

    def read_file(self, filename: str) -> Optional[str]:
        """Securely read a file"""
        try:
            path = self._validate_path(filename)
            if not path.exists():
                raise FileNotFoundError("File not found")
            
            self._check_file_size(path)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logging.info(f"File read: {path}")
            return content
        except Exception as e:
            logging.error(f"File read error: {str(e)}")
            raise

    def delete_file(self, filename: str) -> None:
        """Securely delete a file"""
        try:
            path = self._validate_path(filename)
            if not path.exists():
                raise FileNotFoundError("File not found")
            
            os.remove(path)
            logging.info(f"File deleted: {path}")
        except Exception as e:
            logging.error(f"File deletion error: {str(e)}")
            raise

    def list_files(self) -> list[str]:
        """Securely list files in directory"""
        try:
            files = []
            for item in self.base_directory.iterdir():
                if item.is_file():
                    files.append(str(item.name))
            return files
        except Exception as e:
            logging.error(f"File listing error: {str(e)}")
            raise

    def copy_file(self, source: str, destination: str) -> None: