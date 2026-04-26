```python
import os
import pickle
import hashlib
import tempfile
import time
from typing import Any, Optional
from pathlib import Path

class SecureDiskCache:
    def __init__(self, max_size_bytes: int = 100_000_000, 
                 max_age_seconds: int = 3600):
        """
        Initialize secure disk cache with size and age limits
        
        Args:
            max_size_bytes: Maximum total size of cached data
            max_age_seconds: Maximum age of cached data in seconds
        """
        self.max_size_bytes = max_size_bytes
        self.max_age_seconds = max_age_seconds
        self._cache_dir = None
        self._cache_size = 0
        self._cache_items = {}
        
    def __del__(self):
        """Secure cleanup on object destruction"""
        self._cleanup()

    def _get_cache_dir(self) -> Path:
        """Secure path generation for cache files"""
        if self._cache_dir is None:
            # Use secure temporary directory
            self._cache_dir = Path(tempfile.gettempdir()) / 'secure_cache'
            self._cache_dir.mkdir(mode=0o700, exist_ok=True)
        return self._cache_dir

    def _get_cache_path(self, key: str) -> Path:
        """Generate secure file path with hash"""
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self._get_cache_dir() / hashed_key

    def _secure_write(self, key: str, value: Any) -> None:
        """Securely write data to disk"""
        cache_path = self._get_cache_path(key)
        
        # Create parent directories securely
        cache_path.parent.mkdir(mode=0o700, exist_ok=True)
        
        # Use temporary file for atomic write
        with tempfile.NamedTemporaryFile(mode='wb', 
                                       dir=str(cache_path.parent),
                                       delete=False) as temp_file:
            pickle.dump(value, temp_file)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            
        # Atomic rename
        os.replace(temp_file.name, str(cache_path))
        os.chmod(cache_path, 0o600)

    def _secure_read(self, key: str) -> Optional[Any]:
        """Securely read data from disk"""
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
            
        # Check file permissions
        if not os.access(cache_path, os.R_OK):
            raise PermissionError(f"Cache file {cache_path} is not readable")
            
        # Check file modification time
        if time.time() - cache_path.stat().st_mtime > self.max_age_seconds:
            os.remove(cache_path)
            return None
            
        # Read data securely
        with open(cache_path, 'rb') as f:
            value = pickle.load(f)
            
        return value

    def set(self, key: str, value: Any) -> None:
        """Securely store data in cache"""
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")
            
        # Check size limits
        if self._cache_size + len(pickle.dumps(value)) > self.max_size_bytes:
            raise ValueError("Cache size limit exceeded")
            
        self._secure_write(key, value)
        self._cache_items[key] = time.time()
        self._cache_size += len(pickle.dumps(value))

    def get(self, key: str) -> Optional[Any]:
        """Securely retrieve data from cache"""
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")
            
        value = self._secure_read(key)
        if value is not None: