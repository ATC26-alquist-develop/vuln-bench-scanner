```python
import os
import pickle
import hashlib
from typing import Any
from pathlib import Path
import tempfile
import logging
from functools import wraps

class SecureCache:
    def __init__(self, cache_dir: str = None):
        """Initialize secure cache with optional cache directory."""
        # Use system temp directory if no path provided
        self.cache_dir = cache_dir or tempfile.gettempdir()
        
        # Ensure cache directory exists with proper permissions
        self._secure_path(self.cache_dir)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _secure_path(self, path: str) -> None:
        """Create path securely with proper permissions."""
        try:
            # Convert to absolute path and validate
            cache_path = Path(path).resolve()
            
            # Ensure path is not outside allowed directory
            if not str(cache_path).startswith(str(Path.home())):
                raise ValueError("Cache path must be within user's home directory")
            
            # Create directory with secure permissions
            cache_path.mkdir(mode=0o700, parents=True, exist_ok=True)
        except Exception as e:
            self.logger.error(f"Error creating cache path: {e}")
            raise

    def _generate_key(self, obj: Any) -> str:
        """Generate secure hash key for object."""
        try:
            # Use SHA-256 for secure hashing
            return hashlib.sha256(
                pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
            ).hexdigest()
        except Exception as e:
            self.logger.error(f"Error generating cache key: {e}")
            raise

    def _validate_object(self, obj: Any) -> None:
        """Validate object for security."""
        # Implement object validation logic here
        # For example, check object type, size, etc.
        if not obj:
            raise ValueError("Invalid object")

    def set(self, key: str, obj: Any) -> None:
        """Securely store object in cache."""
        try:
            # Validate object
            self._validate_object(obj)

            # Generate secure key
            cache_key = self._generate_key(obj)

            # Create secure filename
            filename = f"{cache_key}.cache"
            file_path = (self.cache_dir / filename).resolve()

            # Ensure filename is safe
            if not file_path.name.startswith("cache_"):
                raise ValueError("Invalid cache filename")

            # Validate file path
            if not str(file_path).startswith(str(self.cache_dir)):
                raise ValueError("Invalid cache path")

            # Serialize and encrypt object
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tmp_file:
                try:
                    # Use highest pickle protocol for compatibility
                    pickle.dump(obj, tmp_file, protocol=pickle.HIGHEST_PROTOCOL)
                    tmp_file.flush()
                    os.fsync(tmp_file.fileno())

                    # Read encrypted data
                    encrypted_data = tmp_file.read()

                    # In a real implementation, add encryption here
                    # For this example, we'll just copy
                    with open(file_path, 'wb') as cache_file:
                        cache_file.write(encrypted_data)
                        cache_file.flush()
                        os.fsync(cache_file.fileno())

            self.logger.info(f"Object cached with key: {cache_key}")
        except Exception as e:
            self.logger.error(f"Error caching object: {e}")
            raise

    def get(self, key: str) -> Any:
        """Securely retrieve object from cache."""
        try:
            # Validate key
            if not key or not isinstance(key, str):
                raise ValueError("Invalid cache key")

            # Generate cache key
            cache_key = self._generate_key(key)

            # Construct file path
            filename = f"{cache_key}.cache"
            file_path = (self.cache_dir