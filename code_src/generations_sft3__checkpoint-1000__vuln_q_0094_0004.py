import cloudpickle
import os
import time
from typing import Any, Dict

class SecureCache:
    def __init__(self, max_size: int = 1000, expiration_time: int = 3600):
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
        self._expiration_time = expiration_time

    def set(self, key: str, value: Any) -> None:
        """Securely store an object in the cache."""
        if not isinstance(key, str):
            raise TypeError("Cache keys must be strings")
        
        if len(self._cache) >= self._max_size:
            self._evict_oldest()
        
        self._cache[key] = (value, time.time())
        
    def get(self, key: str) -> Any:
        """Securely retrieve an object from the cache."""
        if not isinstance(key, str):
            raise TypeError("Cache keys must be strings")
        
        if key not in self._cache:
            return None
        
        value, timestamp = self._cache[key]
        if time.time() - timestamp > self._expiration_time:
            del self._cache[key]
            return None
        
        return value

    def _evict_oldest(self) -> None:
        """Remove the oldest item from the cache if it exceeds the maximum size."""
        if len(self._cache) <= self._max_size:
            return
        
        oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
        del self._cache[oldest_key]

    def clear(self) -> None:
        """Clear all items from the cache."""
        self._cache.clear()