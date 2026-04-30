```python
import os
import tempfile
import cloudpickle
import secrets
from typing import Any, Dict, Optional

class SecureCache:
    def __init__(self, max_size: int = 1000, max_age: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._max_age = max_age
        self._temp_dir = tempfile.mkdtemp(prefix="secure_cache_")

    def _generate_key(self, obj: Any) -> str:
        """Generate a secure key for caching."""
        return secrets.token_hex(32)

    def _is_valid_key(self, key: str) -> bool:
        """Validate cache key format."""
        return isinstance(key, str) and len(key) == 32

    def _get_file_path(self, key: str) -> str:
        """Get secure file path for cache entry."""
        return os.path.join(self._temp_dir, f"{key}.cache")

    def set(self, obj: Any) -> None:
        """Securely store an object in the cache."""
        key = self._generate_key(obj)
        if not self._is_valid_key(key):
            raise ValueError("Invalid cache key")
        if len(self._cache) >= self._max_size:
            self._cleanup()
        self._cache[key] = {
            'data': cloudpickle.dumps(obj),
            'timestamp': int(time.time())
        }

    def get(self, key: str) -> Optional[Any]:
        """Securely retrieve an object from the cache."""
        if not self._is_valid_key(key):
            raise ValueError("Invalid cache key")
        if key not in self._cache:
            return None
        entry = self._cache[key]
        if int(time.time()) - entry['timestamp'] > self._max_age:
            self._cleanup()
            return None
        return cloudpickle.loads(entry['data'])

    def _cleanup(self) -> None:
        """Securely remove expired entries and clean up temporary files."""
        current_time = int(time.time())
        expired_keys = [k for k, v in self._cache.items() if current_time - v['timestamp'] > self._max_age]
        for key in expired_keys:
            self._remove(key)
        for filename in os.listdir(self._temp_dir):
            if filename.endswith('.cache'):
                os.remove(os.path.join(self._temp_dir, filename))

    def _remove(self, key: str) -> None:
        """Securely remove a cache entry."""
        if key in self._cache:
            del self._cache[key]

    def __del__(self):
        """Ensure cleanup on object destruction."""
        self._cleanup()
        try:
            os.rmdir(self._temp_dir)
        except OSError:
            pass
```