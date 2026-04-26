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
    def __init__(self, base_directory: str):
        """Initialize with a base directory for all operations."""
        # Validate and resolve base directory
        self.base_dir = pathlib.Path(base_directory).resolve()
        if not self.base_dir.exists():
            raise ValueError("Base directory does not exist")
        
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
            os.chmod(self.base_dir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        except OSError as e:
            logging.error(f"Failed to set directory permissions: {e}")
            raise

    def _validate_path(self, file_path: str) -> pathlib.Path:
        """Validate and resolve file path to prevent path traversal."""
        try:
            path = pathlib.Path(file_path).resolve()
            if not str(path).startswith(str(self.base_dir)):
                raise ValueError("Access denied: Path outside base directory")
            return path
        except Exception as e:
            logging.error(f"Path validation failed: {e}")
            raise ValueError("Invalid path")

    def create_file(self, filename: str, content: str) -> None:
        """Securely create a file with optional encryption."""
        try:
            path = self._validate_path(filename)
            
            # Create file with secure permissions
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Set secure permissions
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
            
            logging.info(f"File created: {path}")
        except Exception as e:
            logging.error(f"Failed to create file: {e}")
            raise

    def read_file(self, filename: str) -> Optional[str]:
        """Securely read a file with size limits."""
        try:
            path = self._validate_path(filename)
            
            # Check file size
            if path.stat().st_size > 10_000_000:  # 10MB limit
                raise ValueError("File too large")
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logging.info(f"File read: {path}")
            return content
        except Exception as e:
            logging.error(f"Failed to read file: {e}")
            raise

    def delete_file(self, filename: str) -> None:
        """Securely delete a file."""
        try:
            path = self._validate_path(filename)
            
            # Secure deletion
            if path.is_file():
                with open(path, 'wb') as f:
                    f.write(secrets.token_bytes(path.stat().st_size))
                os.remove(path)
            
            logging.info(f"File deleted: {path}")
        except Exception as e:
            logging.error(f"Failed to delete file: {e}")
            raise

    def list_files(self) -> list[str]:
        """Securely list files in directory."""
        try:
            files = []
            for item in self.base_dir.iterdir():
                if item.is_file():
                    files.append(str(item.relative_to(self.base_dir)))
            return files
        except Exception as e:
            logging.error(f"Failed to list files: {e}")
            raise

    def copy_file(self, source: str, destination: str) -> None:
        """Securely copy a file."""
        try: