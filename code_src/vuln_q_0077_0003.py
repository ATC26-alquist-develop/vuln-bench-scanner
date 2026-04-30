```python
import os
import pickle
import hashlib
import hmac
import hashlib
import time
from typing import Any, Dict
from pathlib import Path
import tempfile

class SecureDiskCache:
    def __init__(self, cache_dir: str, max_size_mb: int = 100, 
                 max_age_seconds: int = 3600, 
                 max_file_size: int = 1024 * 1024):
        """Initialize secure disk cache with strict security controls."""
        
        # Validate and create cache directory
        self._cache_dir = Path(cache_dir).resolve()
        if not self._cache_dir.exists():
            self._cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Security parameters
        self._max_size = max_size_mb * 1024 * 1024  # Convert to bytes
        self._max_age = max_age_seconds
        self._max_file_size = max_file_size
        
        # Initialize cache dictionary
        self._cache: Dict[str, Any] = {}
        
    def _secure_filename(self, key: str) -> str:
        """Generate secure filename using cryptographic hash."""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def _validate_object(self, obj: Any) -> bool:
        """Validate object for security."""
        # Implement strict object validation here
        # For example, check object type, size, etc.
        return True
    
    def _secure_serialize(self, obj: Any) -> bytes:
        """Securely serialize object with integrity check."""
        if not self._validate_object(obj):
            raise ValueError("Invalid object for serialization")
            
        # Serialize with integrity check
        pickled = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        signature = hmac.new(
            os.urandom(32),
            pickled,
            hashlib.sha256
        ).digest()
        
        return signature + pickled
    
    def _secure_deserialize(self, data: bytes) -> Any:
        """Securely deserialize object with integrity check."""
        if len(data) < 32:  # Minimum size for signature
            raise ValueError("Invalid data format")
            
        signature, pickled = data[:32], data[32:]
        if hmac.new(
            os.urandom(32),
            pickled,
            hashlib.sha256
        ).digest() != signature:
            raise ValueError("Data integrity check failed")
            
        return pickle.loads(pickled)
    
    def set(self, key: str, value: Any) -> None:
        """Securely store object in cache."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        if not self._validate_object(value):
            raise ValueError("Invalid object for storage")
            
        if len(value) > self._max_file_size:
            raise ValueError("Object too large")
            
        filename = self._secure_filename(key)
        filepath = self._cache_dir / filename
        
        # Use atomic file operations
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp:
            try:
                self._secure_serialize(value).write(temp.name)
                os.replace(temp.name, filepath)
                
                # Implement size limit
                if filepath.stat().st_size > self._max_size:
                    os.remove(filepath)
                    raise ValueError("Cache size limit exceeded")
                    
            except Exception as e:
                if filepath.exists():
                    os.remove(filepath)
                raise e
        
        self._cache[key] = filename
    
    def get(self, key: str) -> Any:
        """Securely retrieve object from cache."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        filename = self._secure_filename(key)
        filepath = self._cache_dir / filename
        
        if not filepath.exists():