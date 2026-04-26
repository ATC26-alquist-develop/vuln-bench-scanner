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
        self._cache_dir = Path(tempfile.gettempdir()) / "secure_cache"
        self._max_size_bytes = max_size_bytes
        self._max_age_seconds = max_age_seconds
        
        # Ensure cache directory exists with secure permissions
        self._cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
    def _get_cache_path(self, key: str) -> Path:
        """Generate secure cache file path."""
        # Use SHA256 for key hashing
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self._cache_dir / f"{hashed_key}.cache"
    
    def set(self, key: str, value: Any) -> None:
        """Securely store an object in the cache."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        cache_path = self._get_cache_path(key)
        
        try:
            # Create temporary file for atomic write
            with tempfile.NamedTemporaryFile(mode='wb', 
                                            dir=str(self._cache_dir),
                                            delete=False) as temp_file:
                # Serialize with protocol 4 for better compatibility
                pickle.dump(value, temp_file, protocol=4)
                
            # Atomic rename for data integrity
            os.replace(temp_file.name, str(cache_path))
            
            # Set secure file permissions
            os.chmod(cache_path, 0o600)
            
        except Exception as e:
            # Log error securely (implement proper logging)
            print(f"Error caching {key}: {str(e)}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """Securely retrieve an object from the cache."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
            
        cache_path = self._get_cache_path(key)
        
        try:
            if not cache_path.exists():
                return None
                
            # Check cache age
            if time.time() - cache_path.stat().st_mtime > self._max_age_seconds:
                cache_path.unlink()
                return None
                
            with open(cache_path, 'rb') as f:
                # Deserialize with restricted protocol
                value = pickle.load(f)
                
            return value
            
        except Exception as e:
            # Log error securely (implement proper logging)
            print(f"Error retrieving {key}: {str(e)}")
            return None
    
    def clear(self) -> None:
        """Securely clear all cache entries."""
        try:
            for file in self._cache_dir.glob("*.cache"):
                file.unlink()
        except Exception as e:
            # Log error securely (implement proper logging)
            print(f"Error clearing cache: {str(e)}")
            raise