import cloudpickle
import os
import tempfile
import threading
from typing import Any, Dict

class SecureCache:
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, bytes] = {}
        self._lock = threading.Lock()
        self._max_size = max_size

    def set(self, key: str, value: Any) -> None:
        """Securely store an object in the cache."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        with self._lock:
            # Serialize the object
            serialized = cloudpickle.dumps(value)
            
            # Check size before storing
            if len(serialized) > self._max_size:
                raise ValueError("Object too large for cache")
                
            # Store in temporary file first
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                temp_file.write(serialized)
                temp_path = temp_file.name
                
            # Update cache
            self._cache[key] = temp_path

    def get(self, key: str) -> Any:
        """Securely retrieve an object from the cache."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        with self._lock:
            if key not in self._cache:
                return None
                
            # Load from file
            with open(self._cache[key], 'rb') as f:
                serialized = f.read()
                
            # Deserialize
            return cloudpickle.loads(serialized)

    def clear(self) -> None:
        """Clear all cached objects."""
        with self._lock:
            self._cache.clear()
            for file_path in self._cache.values():
                if os.path.exists(file_path):
                    os.unlink(file_path)