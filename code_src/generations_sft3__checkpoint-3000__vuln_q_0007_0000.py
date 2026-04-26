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
        if not self.base_dir.is_dir():
            raise ValueError("Base path must be a directory")
            
        # Setup logging
        logging.basicConfig(
            filename='file_manager.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Ensure proper permissions on base directory
        os.chmod(self.base_dir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    def _validate_path(self, file_path: str) -> pathlib.Path:
        """Validate and resolve file path to prevent path traversal."""
        try:
            full_path = (self.base_dir / file_path).resolve()
            if not str(full_path).startswith(str(self.base_dir)):
                raise ValueError("Access denied: Path outside base directory")
            return full_path
        except Exception as e:
            logging.error(f"Path validation error: {str(e)}")
            raise ValueError("Invalid file path")

    def create_file(self, file_path: str, content: str) -> None:
        """Securely create a file with random name and content."""
        try:
            # Generate secure random filename
            filename = secrets.token_hex(16)
            full_path = self._validate_path(file_path)
            file_path = full_path / filename
            
            # Create file with secure permissions
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
            
            logging.info(f"File created: {file_path}")
        except Exception as e:
            logging.error(f"File creation error: {str(e)}")
            raise

    def read_file(self, file_path: str) -> Optional[str]:
        """Securely read file contents."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.is_file():
                raise ValueError("File does not exist")
                
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            logging.info(f"File read: {file_path}")
            return content
        except Exception as e:
            logging.error(f"File read error: {str(e)}")
            raise

    def delete_file(self, file_path: str) -> None:
        """Securely delete a file."""
        try:
            full_path = self._validate_path(file_path)
            if not full_path.is_file():
                raise ValueError("File does not exist")
                
            os.remove(full_path)
            logging.info(f"File deleted: {file_path}")
        except Exception as e:
            logging.error(f"File deletion error: {str(e)}")
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
            logging.error(f"File listing error: {str(e)}")
            raise