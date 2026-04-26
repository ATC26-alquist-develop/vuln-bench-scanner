```python
import os
import json
import hashlib
import tempfile
import time
from typing import Any, Dict
from pathlib import Path
from threading import Lock

class SecureDiskCache:
    def __init__(self, max_size_bytes: int = 100_000_000, 
                 max_age_seconds: int = 3600):
        """
        Initialize secure disk cache with size and age limits
        
        Args:
            max_size_bytes: Maximum total size of cached data
            max_age_seconds: Maximum age of cached data in seconds
        """
        self._max_size_bytes = max_size_bytes
        self._max_age_seconds = max_age_seconds
        self._cache_dir = Path(tempfile.gettempdir()) / "secure_cache"
        self._lock = Lock()
        
        # Ensure cache directory exists with secure permissions
        self._cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Generate secure file path for cache entry"""
        # Use SHA256 for key hashing
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self._cache_dir / f"{hashed_key}.json"

    def _check_size_limit(self) -> bool:
        """Check if cache size limit has been exceeded"""
        with self._lock:
            cache_size = sum(f.stat().st_size 
                            for f in self._cache_dir.glob("**/*") 
                            if f.is_file())
            return cache_size <= self._max_size_bytes

    def _check_age_limit(self, file_path: Path) -> bool:
        """Check if cache entry is within age limit"""
        try:
            mtime = file_path.stat().st_mtime
            return time.time() - mtime <= self._max_age_seconds
        except (OSError, FileNotFoundError):
            return False

    def set(self, key: str, value: Any) -> None:
        """Securely store an object in the cache"""
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")

        with self._lock:
            if not self._check_size_limit():
                raise RuntimeError("Cache size limit exceeded")

            cache_path = self._get_cache_path(key)
            
            try:
                # Create directory if it doesn't exist
                cache_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                
                # Serialize and write data
                data = json.dumps(value).encode('utf-8')
                with open(cache_path, 'wb') as f:
                    f.write(data)
                
                # Set secure file permissions
                cache_path.chmod(0o600)
                
            except (OSError, json.JSONDecodeError) as e:
                raise RuntimeError(f"Failed to cache data: {str(e)}")

    def get(self, key: str) -> Any:
        """Securely retrieve an object from the cache"""
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")

        cache_path = self._get_cache_path(key)
        
        try:
            if not cache_path.exists():
                return None
            
            if not self._check_age_limit(cache_path):
                cache_path.unlink()
                return None

            with open(cache_path, 'rb') as f:
                data = f.read()
            
            # Deserialize data
            return json.loads(data.decode('utf-8'))
            
        except (OSError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to retrieve data: {str(e)}")

    def clear(self) -> None:
        """Securely clear all cache entries"""
        with self._lock:
            for file_path in self._cache_dir.glob("**/*"):
                if file_path.is