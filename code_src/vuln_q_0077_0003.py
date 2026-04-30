```python
import os
import json
import hashlib
import hmac
import secrets
from typing import Any, Dict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class SecureDiskCache:
    def __init__(self, cache_dir: str, secret_key: bytes):
        """Initialize secure disk cache with proper security measures."""
        self._cache_dir = os.path.abspath(cache_dir)
        self._secret_key = secret_key
        self._ensure_cache_dir_exists()
        self._max_cache_size = 1000  # Limit cache size
        
    def _ensure_cache_dir_exists(self) -> None:
        """Securely create cache directory if it doesn't exist."""
        try:
            os.makedirs(self._cache_dir, mode=0o700, exist_ok=True)
        except OSError as e:
            raise ValueError(f"Failed to create cache directory: {e}")

    def _generate_filename(self, key: str) -> str:
        """Generate secure filename using cryptographic hash."""
        return hashlib.sha256(key.encode()).hexdigest()

    def _encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data using secure key derivation."""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(self._secret_key)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return salt + iv + encryptor.update(data) + encryptor.finalize()

    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt data using secure key derivation."""
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        encrypted = encrypted_data[32:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(self._secret_key)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted) + decryptor.finalize()

    def set(self, key: str, value: Any) -> None:
        """Securely store object in cache."""
        if not isinstance(key, str) or not isinstance(value, (str, int, float, bool, type(None))):
            raise ValueError("Invalid key or value type")
        
        filename = self._generate_filename(key)
        encrypted_value = self._encrypt_data(json.dumps(value).encode())
        
        if len(os.listdir(self._cache_dir)) >= self._max_cache_size:
            self._cleanup_cache()
            
        with open(os.path.join(self._cache_dir, filename), 'wb') as f:
            f.write(encrypted_value)

    def get(self, key: str) -> Any:
        """Securely retrieve object from cache."""
        if not isinstance(key, str):
            raise ValueError("Invalid key type")
            
        filename = self._generate_filename(key)
        file_path = os.path.join(self._cache_dir, filename)
        
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'rb') as f:
            encrypted_value = f.read()
            
        decrypted_value = self._decrypt_data(encrypted_value)
        return json.loads(de