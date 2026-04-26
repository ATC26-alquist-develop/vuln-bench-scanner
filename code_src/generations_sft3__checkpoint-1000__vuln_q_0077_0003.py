import os
import json
import hashlib
import tempfile
from typing import Any, Dict
from pathlib import Path
from datetime import datetime, timedelta

class SecureDiskCache:
    def __init__(self, 
                 max_size_mb: int = 100, 
                 expiration_hours: int = 24,
                 cache_dir: str = "secure_cache"):
        """
        Initialize secure disk cache with safety controls
        
        Args:
            max_size_mb: Maximum cache size in MB
            expiration_hours: Cache expiration time in hours
            cache_dir: Base directory for cache files
        """
        self.max_size_mb = max_size_mb
        self.expiration_hours = expiration_hours
        self.cache_dir = Path(cache_dir)
        
        # Ensure cache directory exists and has proper permissions
        self.cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
    def _get_cache_path(self, key: str) -> Path:
        """Generate secure cache file path"""
        # Use SHA-256 for key hashing
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed_key}.json"

    def _check_cache_size(self) -> bool:
        """Check if cache size exceeds limit"""
        cache_size = sum(f.stat().st_size for f in self.cache_dir.glob('*'))
        return cache_size <= self.max_size_mb * 1024 * 1024

    def _check_expiration(self, file_path: Path) -> bool:
        """Check if file has expired"""
        if not file_path.exists():
            return True
        file_age = datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)
        return file_age > timedelta(hours=self.expiration_hours)

    def set(self, key: str, value: Any) -> None:
        """Securely store an object in cache"""
        if not isinstance(key, str):
            raise TypeError("Cache keys must be strings")
            
        if not self._check_cache_size():
            raise RuntimeError("Cache size limit reached")
            
        cache_path = self._get_cache_path(key)
        
        try:
            # Use temporary file for atomic write
            with tempfile.NamedTemporaryFile(mode='w', 
                                             dir=str(self.cache_dir),
                                             delete=False) as temp_file:
                json.dump(value, temp_file)
                
            # Atomic rename to final location
            os.replace(temp_file.name, str(cache_path))
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'temp_file' in locals():
                os.unlink(temp_file.name)
            raise RuntimeError(f"Cache write failed: {str(e)}")

    def get(self, key: str) -> Any:
        """Securely retrieve an object from cache"""
        if not isinstance(key, str):
            raise TypeError("Cache keys must be strings")
            
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
            
        if self._check_expiration(cache_path):
            os.unlink(cache_path)
            return None
            
        try:
            with open(cache_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If JSON is corrupted, remove file
            os.unlink(cache_path)
            return None
        except Exception as e:
            # Clean up file if it's corrupted
            if 'cache_path' in locals():
                os.unlink(cache_path)
            raise RuntimeError(f"Cache read failed: {str(e)}")