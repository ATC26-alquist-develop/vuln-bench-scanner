```python
import os
import pathlib
import logging
from typing import Optional
from functools import wraps
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='file_manager.log'
)

class SecureFileManager:
    def __init__(self, base_path: str):
        """Initialize with base path and generate encryption key."""
        # Validate and create absolute path
        self.base_path = pathlib.Path(base_path).resolve()
        
        # Ensure base path exists and is a directory
        if not self.base_path.exists():
            raise ValueError("Base path does not exist")
        if not self.base_path.is_dir():
            raise ValueError("Base path is not a directory")
            
        # Generate encryption key from environment variable
        salt = os.environ.get('SECURE_FILE_MANAGER_SALT')
        if not salt:
            raise EnvironmentError("Encryption salt not set in environment")
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(os.environ['SECURE_FILE_MANAGER_KEY'].encode()))
        self.fernet = Fernet(key)

    def _validate_path(self, file_path: str) -> pathlib.Path:
        """Validate and sanitize file path."""
        try:
            # Resolve to absolute path and ensure it's within base path
            full_path = (self.base_path / file_path).resolve()
            if not str(full_path).startswith(str(self.base_path)):
                raise ValueError("Access denied: Path outside base directory")
            return full_path
        except Exception as e:
            logging.error(f"Path validation error: {str(e)}")
            raise ValueError(f"Invalid file path: {file_path}")

    def _encrypt_file(self, file_path: pathlib.Path) -> None:
        """Encrypt file contents."""
        try:
            with file_path.open('rb') as file:
                data = file.read()
            encrypted_data = self.fernet.encrypt(data)
            with file_path.open('wb') as file:
                file.write(encrypted_data)
        except Exception as e:
            logging.error(f"Encryption error: {str(e)}")
            raise

    def _decrypt_file(self, file_path: pathlib.Path) -> None:
        """Decrypt file contents."""
        try:
            with file_path.open('rb') as file:
                data = file.read()
            decrypted_data = self.fernet.decrypt(data)
            with file_path.open('wb') as file:
                file.write(decrypted_data)
        except Exception as e:
            logging.error(f"Decryption error: {str(e)}")
            raise

    def create_file(self, file_path: str, content: str) -> None:
        """Create a new file with content."""
        try:
            path = self._validate_path(file_path)
            if path.exists():
                raise FileExistsError(f"File already exists: {file_path}")
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Encrypt and write content
            with path.open('w') as file:
                file.write(content)
            self._encrypt_file(path)
            logging.info(f"Created and encrypted file: {file_path}")
        except Exception as e:
            logging.error(f"File creation error: {str(e)}")
            raise

    def read_file(self, file_path: str) -> str:
        """Read and decrypt file contents."""