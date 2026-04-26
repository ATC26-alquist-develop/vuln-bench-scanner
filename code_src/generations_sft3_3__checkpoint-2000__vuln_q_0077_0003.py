import os
import pickle
import hashlib
import tempfile
import time
from typing import Any, Optional
from pathlib import Path

class SecureDiskCache:
    def __init__(self, max_size_bytes: int = 1024 * 1024, 
                 max_age_seconds: int = 3600):
        """Initialize secure disk cache with size and age limits."""
        self._max_size = max_size_bytes
        self._max_age = max_age_seconds
        self._cache_dir = Path(tempfile.gettempdir()) / "secure_cache"
        self._cache: dict[str, tuple[bytes, float]] = {}
        
        # Ensure cache directory exists with secure permissions
        self._cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Generate secure path for cache file."""
        # Use SHA256 for key hashing
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self._cache_dir / f"{hashed_key}.cache"

    def set(self, key: str, value: Any) -> None:
        """Securely store an object in cache."""
        try:
            # Serialize object safely
            serialized_value = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
            
            # Check size before storing
            if sum(len(v) for v in self._cache.values()) + len(serialized_value) > self._max_size:
                raise ValueError("Cache size limit exceeded")
            
            # Store with timestamp
            self._cache[key] = (serialized_value, time.time())
            
            # Create cache file with secure permissions
            cache_path = self._get_cache_path(key)
            cache_path.write_bytes(serialized_value)
            cache_path.chmod(0o600)
            
        except (pickle.PickleError, OSError) as e:
            raise ValueError(f"Failed to cache data: {str(e)}")

    def get(self, key: str) -> Optional[Any]:
        """Securely retrieve an object from cache."""
        try:
            if key not in self._cache:
                return None

            value, timestamp = self._cache[key]
            
            # Check if cache is expired
            if time.time() - timestamp > self._max_age:
                del self._cache[key]
                return None

            # Deserialize safely
            return pickle.loads(value)
            
        except (pickle.UnpicklingError, OSError, ValueError) as e:
            raise ValueError(f"Failed to retrieve data: {str(e)}")

    def clear(self) -> None:
        """Securely clear all cache data."""
        for file in self._cache_dir.glob("*.cache"):
            file.unlink()
        self._cache.clear()