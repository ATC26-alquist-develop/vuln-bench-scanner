```python
import os
import pickle
import hashlib
import tempfile
from typing import Any, Optional
from pathlib import Path
from threading import Lock

class SecureDiskCache:
    def __init__(self, cache_dir: str = "secure_cache", max_size_mb: int = 100):
        """
        Initialize secure disk cache with size limits and encryption
        
        Args:
            cache_dir: Base directory for cache files
            max_size_mb: Maximum allowed cache size in MB
        """
        # Create secure temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix="secure_cache_")
        self.cache_dir = Path(self.temp_dir)
        
        # Set maximum cache size
        self.max_size = max_size_mb * 1024 * 1024
        
        # Ensure cache directory exists and has proper permissions
        self.cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Initialize lock for thread safety
        self._lock = Lock()
        
        # Encryption key (in production, use proper key management)
        self._encryption_key = os.urandom(32)

    def _get_cache_path(self, key: str) -> Path:
        """Generate secure file path with hash"""
        # Create hash of key for safe filename
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed_key}.cache"

    def _encrypt_data(self, data: bytes) -> bytes:
        """Simple encryption for added security"""
        return bytes([b ^ 0xAA for b in data])

    def _decrypt_data(self, data: bytes) -> bytes:
        """Simple decryption (for demonstration only)"""
        return self._encrypt_data(data)

    def set(self, key: str, value: Any) -> None:
        """Securely store object in cache"""
        try:
            with self._lock:
                cache_path = self._get_cache_path(key)
                
                # Check size before writing
                with self._lock:
                    if self._get_cache_size() + len(cache_path) > self.max_size:
                        raise ValueError("Cache size limit exceeded")
                
                # Serialize and encrypt data
                serialized = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
                encrypted = self._encrypt_data(serialized)
                
                # Write to temporary file first
                with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                    temp_file.write(encrypted)
                    temp_path = temp_file.name
                
                # Atomic rename
                os.replace(temp_path, cache_path)
                
        except Exception as e:
            raise RuntimeError(f"Failed to cache data: {str(e)}")

    def get(self, key: str) -> Optional[Any]:
        """Securely retrieve object from cache"""
        try:
            with self._lock:
                cache_path = self._get_cache_path(key)
                
                if not cache_path.exists():
                    return None
                
                # Read encrypted data
                with open(cache_path, 'rb') as f:
                    encrypted = f.read()
                
                # Decrypt and deserialize
                serialized = self._decrypt_data(encrypted)
                return pickle.loads(serialized)
                
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve data: {str(e)}")

    def delete(self, key: str) -> None:
        """Securely delete cache entry"""
        try:
            with self._lock:
                cache_path = self._get_cache_path(key)
                if cache_path.exists():
                    cache_path.unlink()
        except Exception as e:
            raise RuntimeError(f"Failed to delete cache entry: {str(e)}")

    def _get_cache_size(self) -> int:
        """Securely get current cache size"""
        try:
            return sum(f.stat().st_size for f in self.cache_dir.glob('