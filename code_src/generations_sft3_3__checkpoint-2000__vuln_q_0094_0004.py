import cloudpickle
import os
import time
from typing import Any, Dict, Optional

class SecureCache:
    def __init__(self, max_size: int = 1000, expiration_time: int = 3600):
        """
        Initialize the cache with maximum size and expiration time.
        
        Args:
            max_size: Maximum number of items in the cache
            expiration_time: Time in seconds after which items expire
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._expiration_time = expiration_time

    def set(self, key: str, value: Any) -> None:
        """
        Store an object in the cache with an expiration time.
        
        Args:
            key: Unique identifier for the cached object
            value: Object to be cached
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        if not isinstance(value, (str, bytes, int, float, bool, list, dict, tuple)):
            raise TypeError("Only basic Python types are supported")

        if len(self._cache) >= self._max_size:
            self._evict_oldest()

        expiration = time.time() + self._expiration_time
        self._cache[key] = {
            'value': value,
            'expiration': expiration
        }

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve an object from the cache.
        
        Args:
            key: Unique identifier for the cached object
            
        Returns:
            Cached object if found and not expired, None otherwise
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        if key not in self._cache:
            return None

        item = self._cache[key]
        if time.time() > item['expiration']:
            del self._cache[key]
            return None

        return item['value']

    def _evict_oldest(self) -> None:
        """
        Remove the oldest item from the cache.
        """
        oldest_key = min(self._cache, key=lambda k: self._cache[k]['expiration'])
        del self._cache[oldest_key]

    def clear(self) -> None:
        """
        Clear all items from the cache.
        """
        self._cache.clear()