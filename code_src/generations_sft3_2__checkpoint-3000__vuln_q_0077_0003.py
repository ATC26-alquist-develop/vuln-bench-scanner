```python
import os
import json
import hashlib
import tempfile
from typing import Any, Optional
from pathlib import Path
from threading import Lock
from functools import wraps

class SecureDiskCache:
    def __init__(self, cache_dir: str = "secure_cache", max_size_mb: int = 100):
        """
        Initialize secure disk cache with size limits and encryption
        
        Args:
            cache_dir: Base directory for cache files
            max_size_mb: Maximum allowed cache size in MB
        """
        # Create secure cache directory with restricted permissions
        self.cache_dir = Path(cache_dir).resolve()
        self.max_size = max_size_mb * 1024 * 1024  # Convert to bytes
        
        # Ensure cache directory exists and has restricted permissions
        self.cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Initialize lock for thread safety
        self._lock = Lock()
        
        # Initialize cache size tracking
        self._cache_size = 0
        
    def _get_cache_path(self, key: str) -> Path:
        """Generate secure cache file path"""
        # Use SHA256 for key hashing
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed_key}.json"
    
    def _check_size_limit(self) -> None:
        """Check if cache size exceeds limit"""
        while self._cache_size > self.max_size:
            # Remove oldest file if limit exceeded
            with self._lock:
                if not self.cache_dir.iterdir():
                    break
                oldest = min(self.cache_dir.glob("*.json"), 
                            key=os.path.getctime)
                oldest.unlink()
                self._cache_size -= os.path.getsize(oldest)
    
    def _secure_load(self, path: Path) -> Any:
        """Securely load JSON data"""
        if not path.exists():
            return None
        
        # Check file size
        if path.stat().st_size > 10 * 1024 * 1024:  # 10MB limit
            raise ValueError("Cache file too large")
            
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError:
            return None
    
    def _secure_save(self, key: str, data: Any) -> None:
        """Securely save data to file"""
        # Create temporary file for atomic write
        with tempfile.NamedTemporaryFile(mode='w', 
                                      dir=self.cache_dir,
                                      delete=False) as temp_file:
            json.dump(data, temp_file)
            
        # Rename file securely
        temp_path = Path(temp_file.name)
        new_path = self._get_cache_path(key)
        temp_path.rename(new_path)
        
        # Update cache size
        self._cache_size += new_path.stat().st_size
        
    def set(self, key: str, value: Any) -> None:
        """Securely store data in cache"""
        with self._lock:
            self._check_size_limit()
            
            # Create cache path
            cache_path = self._get_cache_path(key)
            
            # Store data
            self._secure_save(key, value)
    
    def get(self, key: str) -> Optional[Any]:
        """Securely retrieve data from cache"""
        with self._lock:
            cache_path = self._get_cache_path(key)
            
            # Check if file exists
            if not cache_path.exists():
                return None
                
            # Load data
            data = self._secure_load(cache_path)
            return data
    
    def clear(self) -> None:
        """Securely clear all cache data"""
        with self._lock:
            # Remove all files in cache directory