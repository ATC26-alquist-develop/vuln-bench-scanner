import os
from pathlib import Path
import logging
from typing import Optional

class SecureFileHandler:
    def __init__(self, file_path: str):
        """Initialize with file path and set up logging."""
        self.file_path = Path(file_path).resolve()
        self.logger = logging.getLogger(__name__)
        
        # Ensure directory exists and is writable
        self._ensure_directory_writable()
        
        # Set up secure permissions
        self._set_secure_permissions()

    def _ensure_directory_writable(self) -> None:
        """Ensure the directory containing the file exists and is writable."""
        directory = self.file_path.parent
        if not directory.exists():
            raise ValueError(f"Directory {directory} does not exist")
        if not os.access(directory, os.W_OK):
            raise PermissionError(f"No write access to directory {directory}")

    def _set_secure_permissions(self) -> None:
        """Set secure permissions on the file."""
        if self.file_path.exists():
            os.chmod(self.file_path, 0o600)
        else:
            # Create file with secure permissions
            with open(self.file_path, 'w') as f:
                os.chmod(self.file_path, 0o600)

    def read_file(self) -> Optional[str]:
        """Securely read file contents."""
        try:
            if not self.file_path.exists():
                return None
            with open(self.file_path, 'r') as f:
                return f.read()
        except IOError as e:
            self.logger.error(f"Error reading file: {e}")
            return None

    def write_file(self, content: str) -> bool:
        """Securely write content to file."""
        try:
            with open(self.file_path, 'w') as f:
                f.write(content)
            return True
        except IOError as e:
            self.logger.error(f"Error writing to file: {e}")
            return False

    def delete_file(self) -> bool:
        """Securely delete the file."""
        try:
            if self.file_path.exists():
                os.remove(self.file_path)
                return True
            return False
        except OSError as e:
            self.logger.error(f"Error deleting file: {e}")
            return False