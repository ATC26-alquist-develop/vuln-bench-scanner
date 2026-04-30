```python
import os
import cloudpickle
import hashlib
from typing import Any, Optional
from pathlib import Path

class SecureCache:
    def __init__(self, cache_dir: str = "secure_cache"):
        """
        Initialize the cache with a secure storage directory.
        
        Args:
            cache_dir: The directory to store cache files. Must be an absolute path.
        """
        self.cache_dir = Path(cache_dir).resolve()
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Get a secure cache file path from the key."""
        # Create a hash of the key to use as filename
        filename = hashlib.sha256(key.encode('utf-8')).hexdigest()
        return self.cache_dir / f"{filename}.cache"

    def set(self, key: str, value: Any) -> None:
        """Store an object in the cache."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        
        try:
            cache_path = self._get_cache_path(key)
            # Serialize and write data with integrity check
            data = cloudpickle.dumps(value)
            integrity = hashlib.sha256(data).digest()
            
            with open(cache_path, 'wb') as f:
                f.write(integrity)
                f.write(data)
        except (OSError, cloudpickle.PicklingError) as e:
            raise RuntimeError(f"Failed to cache data: {str(e)}")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve an object from the cache.
        
        Returns:
            The cached object if found, None otherwise.
        """
        if not isinstance(key, str):
            return None

        try:
            cache_path = self._get_cache_path(key)
            if not cache_path.exists():
                return None

            with open(cache_path, 'rb') as f:
                # Read integrity and data
                integrity = f.read(32)  # SHA-256 hash is 32 bytes
                data = f.read()

            if not integrity or not data:
                return None

            # Verify integrity
            if hashlib.sha256(data).digest() != integrity:
                raise ValueError("Cache data integrity check failed")

            # Deserialize and return the object
            return cloudpickle.loads(data)
        except (OSError, cloudpickle.UnpicklingError, ValueError) as e:
            raise RuntimeError(f"Failed to retrieve cache: {str(e)}")
```