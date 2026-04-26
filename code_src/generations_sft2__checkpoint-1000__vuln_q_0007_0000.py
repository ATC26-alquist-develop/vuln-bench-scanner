```python
import os
import pathlib
import shutil
import logging
from typing import List, Optional
from pathlib import Path
import secrets
import hashlib

class SecureFileManager:
    def __init__(self, base_dir: str):
        """Initialize secure file manager with base directory."""
        self.base_dir = Path(base_dir).resolve()
        if not self.base_dir.exists():
            raise ValueError("Base directory must exist")
        if not self.base_dir.is_dir():
            raise ValueError("Base directory must be a directory")
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _sanitize_path(self, path: str) -> Path:
        """Sanitize and resolve path to prevent directory traversal."""
        try:
            full_path = (self.base_dir / path).resolve()
            if not str(full_path).startswith(str(self.base_dir)):
                raise ValueError("Access denied: Path outside base directory")
            return full_path
        except Exception as e:
            self.logger.error(f"Path validation error: {e}")
            raise ValueError("Invalid path")

    def create_file(self, filename: str, content: str) -> None:
        """Create a new file with secure permissions."""
        try:
            file_path = self._sanitize_path(filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Set secure permissions (read/write for owner only)
            os.chmod(file_path, 0o600)
            
            self.logger.info(f"File created: {file_path}")
        except Exception as e:
            self.logger.error(f"File creation error: {e}")
            raise

    def read_file(self, filename: str) -> Optional[str]:
        """Securely read file content."""
        try:
            file_path = self._sanitize_path(filename)
            if not file_path.is_file():
                raise ValueError("File does not exist")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.logger.info(f"File read: {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"File read error: {e}")
            raise

    def delete_file(self, filename: str) -> None:
        """Securely delete a file."""
        try:
            file_path = self._sanitize_path(filename)
            if not file_path.is_file():
                raise ValueError("File does not exist")
            
            # Secure delete by overwriting content
            with open(file_path, 'wb') as f:
                f.write(os.urandom(file_path.stat().st_size))
            
            os.remove(file_path)
            
            self.logger.info(f"File deleted: {file_path}")
        except Exception as e:
            self.logger.error(f"File deletion error: {e}")
            raise

    def list_files(self) -> List[str]:
        """List files in base directory."""
        try:
            files = [f.name for f in self.base_dir.iterdir() if f.is_file()]
            self.logger.info("File listing completed")
            return files
        except Exception as e:
            self.logger.error(f"File listing error: {e}")
            raise

    def generate_secure_filename(self, original_name: str) -> str:
        """Generate a secure filename using cryptographic hash."""
        try:
            # Generate secure random salt
            salt = secrets.token_bytes(16)
            # Create secure hash of original filename
            secure_hash = hashlib.sha256(salt + original_name.encode()).hexdigest()
            return f"{secure_hash[:16]}_{original_name}"
        except Exception as e:
            self.logger.error(f"Secure filename generation error: {e}")
            raise

# Usage example
if __name__ ==