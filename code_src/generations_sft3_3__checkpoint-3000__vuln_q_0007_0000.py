```python
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
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SecureFileManager')

    def _validate_path(self, file_path: str) -> Path:
        """Validate and sanitize file path."""
        try:
            # Resolve path and check if it's within base directory
            full_path = (self.base_dir / file_path).resolve()
            if not str(full_path).startswith(str(self.base_dir)):
                raise ValueError("Access denied: Path outside base directory")
            return full_path
        except Exception as e:
            self.logger.error(f"Path validation error: {str(e)}")
            raise ValueError("Invalid path")

    def create_file(self, file_path: str, content: str) -> None:
        """Securely create a file with content."""
        try:
            full_path = self._validate_path(file_path)
            
            # Create directory if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file with secure permissions
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Set secure permissions (owner read/write only)
            os.chmod(full_path, stat.S_IRUSR | stat.S_IWUSR)
            
            self.logger.info(f"File created: {file_path}")
        except Exception as e:
            self.logger.error(f"File creation error: {str(e)}")
            raise

    def read_file(self, file_path: str) -> Optional[str]:
        """Securely read a file's contents."""
        try:
            full_path = self._validate_path(file_path)
            
            if not full_path.is_file():
                raise ValueError("Not a valid file")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.logger.info(f"File read: {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"File read error: {str(e)}")
            raise

    def delete_file(self, file_path: str) -> None:
        """Securely delete a file."""
        try:
            full_path = self._validate_path(file_path)
            
            if not full_path.is_file():
                raise ValueError("Not a valid file")
            
            os.remove(full_path)
            self.logger.info(f"File deleted: {file_path}")
        except Exception as e:
            self.logger.error(f"File deletion error: {str(e)}")
            raise

    def list_files(self) -> list[str]:
        """Securely list files in the base directory."""
        try:
            files = []
            for item in self.base_dir.iterdir():
                if item.is_file():
                    files.append(str(item.relative_to(self.base_dir)))
            return files
        except Exception as e:
            self.logger.error(f"File listing error: {str(e)}")
            raise

    def copy_file(self, source: str, destination: str) -> None:
        """Securely copy a file."""
        try:
            src_path = self._validate_path(source)
            dst_path = self._validate_path(destination)
            
            if not src_path.is_file():
                raise ValueError("Source is not a valid file")
            
            shutil.copy2(src_path, dst_path)
            os