import cloudpickle
import os
import tempfile
import shutil
from typing import Any, Dict

class SecureCache:
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
        self._temp_dir = tempfile.mkdtemp(prefix='secure_cache_')

    def __del__(self):
        shutil.rmtree(self._temp_dir)

    def _serialize(self, obj: Any) -> bytes:
        """Securely serialize an object using cloudpickle."""
        return cloudpickle.dumps(obj)

    def _deserialize(self, data: bytes) -> Any:
        """Securely deserialize an object using cloudpickle."""
        return cloudpickle.loads(data)

    def set(self, key: str, value: Any) -> None:
        """Add an item to the cache."""
        if len(self._cache) >= self._max_size:
            self._evict()
        self._cache[key] = self._serialize(value)

    def get(self, key: str) -> Any:
        """Retrieve an item from the cache."""
        if key not in self._cache:
            return None
        return self._deserialize(self._cache[key])

    def _evict(self) -> None:
        """Evict an item from the cache."""
        if self._cache:
            oldest_key = min(self._cache, key=lambda k: os.path.getmtime(os.path.join(self._temp_dir, f"{k}.pkl")))
            del self._cache[oldest_key]

    def clear(self) -> None:
        """Clear all items from the cache."""
        self._cache.clear()
        shutil.rmtree(self._temp_dir)
        os.makedirs(self._temp_dir)

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return len(self._cache)