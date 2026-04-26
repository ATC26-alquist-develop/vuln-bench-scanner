```python
import os
import pickle
import hashlib
import tempfile
import time
from typing import Any, Optional
from pathlib import Path

class SecureDiskCache:
    def __init__(self, max_size_bytes: int = 10_000_000, 
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
        """Generate secure file path for cache item"""
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")
        return self._get_cache_dir() / hashlib.sha256(key.encode()).hexdigest()

    def _secure_pickle(self, obj: Any) -> bytes:
        """Securely serialize object"""
        try:
            return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        except pickle.PicklingError:
            raise ValueError("Unable to serialize object")

    def _secure_unpickle(self, data: bytes) -> Any:
        """Securely deserialize object"""
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError:
            raise ValueError("Invalid or malicious object data")

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Securely store object in cache with TTL"""
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")
            
        cache_path = self._get_cache_path(key)
        data = self._secure_pickle(value)
        
        # Check size limits
        if self._cache_size + len(data) > self.max_size_bytes:
            raise ValueError("Cache size limit exceeded")
            
        # Check age limits
        if ttl is not None:
            if not isinstance(ttl, int) or ttl <= 0:
                raise ValueError("Invalid TTL")
            if (time.time() - self._cache_items.get(key, 0)) > ttl:
                raise ValueError("Cache item expired")
                
        # Write to temporary file first
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            temp_file.write(data)
            temp_path = temp_file.name
            
        # Atomic rename
        os.replace(temp_path, cache_path)
        self._cache_size += len(data)
        self._cache_items[key] = time.time()

    def get(self, key: str) -> Any:
        """Securely retrieve object from cache"""
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")
            
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None
            
        # Check age limits
        if (time.time() - self._cache_items.get(key, 0)) > self.max_age_seconds:
            os.remove(cache_path)
            del self._cache_items[key]
            return None
            
        try:
            with open(cache_path, 'rb') as f:
                data