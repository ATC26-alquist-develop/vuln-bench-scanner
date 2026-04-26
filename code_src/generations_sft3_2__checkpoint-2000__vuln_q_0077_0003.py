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
    
    def _check_size(self) -> bool:
        """Check if cache size exceeds limit."""
        total_size = sum(f.stat().st_size 
                        for f in self._cache_dir.glob("*.cache"))
        return total_size > self._max_size_bytes
    
    def set(self, key: str, value: Any) -> None:
        """Securely store object in cache."""
        if self._check_size():
            raise ValueError("Cache size limit exceeded")
            
        cache_path = self._get_cache_path(key)
        
        try:
            # Use secure temporary file for writing
            with tempfile.NamedTemporaryFile(mode='wb', 
                                            dir=str(self._cache_dir),
                                            delete=False) as temp_file:
                pickle.dump(value, temp_file)
                temp_file.flush()
                os.fsync(temp_file.fileno())
                
            # Rename temporary file to final cache file
            os.replace(temp_file.name, str(cache_path))
            
            # Set secure file permissions
            os.chmod(cache_path, 0o600)
            
        except Exception as e:
            # Clean up temporary file if anything fails
            if cache_path.exists():
                os.unlink(cache_path)
            raise RuntimeError(f"Cache write failed: {str(e)}")
    
    def get(self, key: str) -> Optional[Any]:
        """Securely retrieve object from cache."""
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
            
        try:
            # Check cache age
            if time.time() - cache_path.stat().st_mtime > self._max_age_seconds:
                os.unlink(cache_path)
                return None
                
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
                
        except (pickle.UnpicklingError, EOFError, AttributeError) as e:
            # Clean up corrupted file
            if cache_path.exists():
                os.unlink(cache_path)
            raise ValueError(f"Cache corruption: {str(e)}")