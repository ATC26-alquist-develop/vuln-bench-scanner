import os
import tempfile
import uuid
import cloudpickle
import hashlib
from typing import Any, Dict

class SecureCache:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, Any] = {}
        self.temp_dir = tempfile.mkdtemp(prefix='secure_cache_')

    def _generate_key(self, obj: Any) -> str:
        """Generate a secure key for the object using SHA-256 hashing."""
        return hashlib.sha256(cloudpickle.dumps(obj)).hexdigest()

    def _get_temp_file_path(self) -> str:
        """Generate a secure temporary file path."""
        return os.path.join(self.temp_dir, f"{uuid.uuid4().hex}.pkl")

    def set(self, obj: Any) -> None:
        """Securely store an object in the cache."""
        if not isinstance(obj, (int, float, str, bool, type(None))):
            raise ValueError("Only basic data types are allowed for security reasons")
        
        key = self._generate_key(obj)
        file_path = self._get_temp_file_path()
        
        try:
            with open(file_path, 'wb') as f:
                cloudpickle.dump(obj, f)
            self.cache[key] = file_path
        except Exception as e:
            raise RuntimeError(f"Failed to store object: {str(e)}")

    def get(self, key: str) -> Any:
        """Securely retrieve an object from the cache."""
        if key not in self.cache:
            raise KeyError(f"Key not found: {key}")
        
        file_path = self.cache[key]
        try:
            with open(file_path, 'rb') as f:
                return cloudpickle.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve object: {str(e)}")

    def clear(self) -> None:
        """Securely clear the entire cache."""
        for file_path in self.cache.values():
            try:
                os.remove(file_path)
            except Exception as e:
                raise RuntimeError(f"Failed to clear cache: {str(e)}")
        self.cache.clear()
        os.rmdir(self.temp_dir)

    def __del__(self):
        """Ensure cache is cleared when object is destroyed."""
        self.clear()